from __future__ import annotations

import argparse
import json
import statistics
import time
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path

from policy_assistant import Actor, PolicyAssistant, PolicyDocument, PolicyRepository
from policy_assistant.repository import _terms


ROOT = Path(__file__).resolve().parent
DEFAULT_DATASET = ROOT / "evaluation" / "cases.json"
TODAY = date(2026, 7, 30)


def documents() -> list[PolicyDocument]:
    def doc(
        policy_id: str,
        title: str,
        content: str,
        *,
        access: str = "employee",
        jurisdiction: str = "BR",
        valid_from: date = date(2026, 1, 1),
        valid_until: date | None = None,
    ) -> PolicyDocument:
        return PolicyDocument(
            policy_id=policy_id,
            title=title,
            version="1.0",
            valid_from=valid_from,
            valid_until=valid_until,
            jurisdiction=jurisdiction,
            access_level=access,
            content=content,
            authority="Domínio responsável",
        )

    return [
        doc("POL-REMOTE-1", "Trabalho remoto revogado", "trabalho remoto sem aprovação", valid_until=date(2025, 12, 31)),
        doc("POL-REMOTE-2", "Trabalho remoto vigente", "trabalho remoto exige aprovação da liderança", valid_from=date(2026, 2, 1)),
        doc("POL-SUPPORT-1", "Suporte público", "canal público suporte portal ajuda", access="public", valid_from=date(2026, 3, 1)),
        doc("POL-TRAVEL-OLD", "Viagens revogada", "adiantamento internacional viagens", valid_until=date(2025, 6, 30)),
        doc("POL-SALARY-M", "Remuneração gerencial", "faixa salarial executiva", access="manager", valid_from=date(2026, 3, 15)),
        doc("POL-PT-1", "Benefício Portugal", "benefício alimentação portugal", jurisdiction="PT", valid_from=date(2026, 3, 20)),
        doc("POL-BYOD-A", "Equipamento pessoal A", "equipamento pessoal trabalho permitido com cadastro", valid_from=date(2026, 4, 1)),
        doc("POL-BYOD-B", "Equipamento pessoal B", "equipamento pessoal trabalho proibido sem exceção", valid_from=date(2026, 4, 1)),
    ]


class UngovernedRepository(PolicyRepository):
    """Baseline didática: ranqueia termos sem vigência, jurisdição ou autorização."""

    def search(self, question, actor, jurisdiction, when, limit=3):
        query_terms = _terms(question)
        ranked = []
        for document in self._documents:
            score = len(query_terms.intersection(_terms(document.content + " " + document.title)))
            if score:
                ranked.append((score, document))
        ranked.sort(key=lambda item: (item[0], item[1].valid_from), reverse=True)
        return [document for _, document in ranked[:limit]]


@dataclass(frozen=True)
class Metrics:
    cases: int
    task_success_rate: float
    evidence_accuracy: float
    abstention_accuracy: float
    unauthorized_exposures: int
    conflict_detection_rate: float
    latency_p50_ms: float
    latency_p95_ms: float


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, int((len(ordered) - 1) * fraction)))
    return ordered[index]


def evaluate(repository_type, cases: list[dict]) -> Metrics:
    service = PolicyAssistant(repository_type(documents()))
    successes = evidence_checks = correct_evidence = 0
    abstention_checks = correct_abstentions = 0
    conflict_checks = correct_conflicts = 0
    exposures = 0
    latencies = []

    for case in cases:
        actor = Actor(f"actor-{case['id']}", case["actor_level"])
        started = time.perf_counter()
        answer = service.answer(case["question"], actor, "BR", TODAY)
        latencies.append((time.perf_counter() - started) * 1000)

        policy_ids = {item.policy_id for item in answer.evidence}
        expected_policy = case.get("expected_policy")
        expected_reason = case.get("expected_reason")
        forbidden_policy = case.get("forbidden_policy")

        if expected_policy:
            evidence_checks += 1
            correct_evidence += expected_policy in policy_ids
        if case["expected_status"] == "abstained":
            abstention_checks += 1
            correct_abstentions += answer.status == "abstained" and answer.reason == expected_reason
        if expected_reason == "conflicting_evidence":
            conflict_checks += 1
            correct_conflicts += answer.reason == "conflicting_evidence"
        if forbidden_policy and forbidden_policy in policy_ids:
            exposures += 1

        successes += (
            answer.status == case["expected_status"]
            and (expected_policy is None or expected_policy in policy_ids)
            and (expected_reason is None or answer.reason == expected_reason)
        )

    return Metrics(
        cases=len(cases),
        task_success_rate=successes / len(cases),
        evidence_accuracy=correct_evidence / evidence_checks if evidence_checks else 1.0,
        abstention_accuracy=correct_abstentions / abstention_checks if abstention_checks else 1.0,
        unauthorized_exposures=exposures,
        conflict_detection_rate=correct_conflicts / conflict_checks if conflict_checks else 1.0,
        latency_p50_ms=statistics.median(latencies),
        latency_p95_ms=percentile(latencies, 0.95),
    )


def run(dataset_path: Path = DEFAULT_DATASET) -> dict:
    payload = json.loads(dataset_path.read_text(encoding="utf-8"))
    cases = payload["cases"]
    return {
        "dataset": payload["dataset"],
        "configurations": {
            "lexical_ungoverned": asdict(evaluate(UngovernedRepository, cases)),
            "lexical_governed": asdict(evaluate(PolicyRepository, cases)),
        },
        "notes": [
            "Latência mede somente este laboratório local e não representa serving de LLM.",
            "Casos são sintéticos; resultados demonstram o método, não desempenho de mercado.",
        ],
    }


def markdown(report: dict) -> str:
    lines = [
        "# Benchmark reproduzível do assistente de políticas",
        "",
        f"Dataset: `{report['dataset']['name']}` versão `{report['dataset']['version']}`.",
        "",
        "| Configuração | Sucesso | Evidência | Abstenção | Exposições | Conflito | p50 ms | p95 ms |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, result in report["configurations"].items():
        lines.append(
            f"| {name} | {result['task_success_rate']:.1%} | "
            f"{result['evidence_accuracy']:.1%} | {result['abstention_accuracy']:.1%} | "
            f"{result['unauthorized_exposures']} | {result['conflict_detection_rate']:.1%} | "
            f"{result['latency_p50_ms']:.3f} | {result['latency_p95_ms']:.3f} |"
        )
    lines.extend(["", "## Limites", ""])
    lines.extend(f"- {note}" for note in report["notes"])
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--json", action="store_true", help="Emite JSON em vez de Markdown.")
    args = parser.parse_args()
    report = run(args.dataset)
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json else markdown(report), end="")


if __name__ == "__main__":
    main()
