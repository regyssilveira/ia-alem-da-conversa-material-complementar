from datetime import date
from pathlib import Path
import importlib.util
import json
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from policy_assistant import Actor, PolicyAssistant, PolicyDocument, PolicyRepository
from benchmark import run
from model_benchmark import evaluate as evaluate_model
from policy_assistant.models import ModelRequest, ReplayAdapter, TaskRouter
from release_gate import decide


TODAY = date(2026, 7, 30)


def policy(
    policy_id: str = "POL-1",
    *,
    content: str = "trabalho remoto exige aprovação prévia da liderança",
    access_level: str = "employee",
    valid_from: date = date(2026, 1, 1),
) -> PolicyDocument:
    return PolicyDocument(
        policy_id=policy_id,
        title="Política de trabalho remoto",
        version="1.0",
        valid_from=valid_from,
        valid_until=None,
        jurisdiction="BR",
        access_level=access_level,
        content=content,
        authority="Recursos Humanos",
    )


class PolicyAssistantTests(unittest.TestCase):
    def setUp(self) -> None:
        self.actor = Actor(
            actor_id="emp-1",
            access_level="employee",
            permissions=frozenset({"create_request"}),
        )

    def test_answer_contains_versioned_evidence(self) -> None:
        service = PolicyAssistant(PolicyRepository([policy()]))
        answer = service.answer("trabalho remoto", self.actor, "BR", TODAY)
        self.assertEqual("answered", answer.status)
        self.assertEqual("POL-1", answer.evidence[0].policy_id)
        self.assertEqual("1.0", answer.evidence[0].version)

    def test_abstains_without_sufficient_evidence(self) -> None:
        service = PolicyAssistant(PolicyRepository([policy()]))
        answer = service.answer("reembolso de viagem", self.actor, "BR", TODAY)
        self.assertEqual("abstained", answer.status)
        self.assertEqual("insufficient_evidence", answer.reason)

    def test_access_level_filters_restricted_policy(self) -> None:
        service = PolicyAssistant(
            PolicyRepository([policy(access_level="manager")])
        )
        answer = service.answer("trabalho remoto", self.actor, "BR", TODAY)
        self.assertEqual("abstained", answer.status)

    def test_confirmation_is_bound_to_exact_proposal(self) -> None:
        service = PolicyAssistant(PolicyRepository([]))
        proposal = service.propose_action("create_request", {"days": 2}, self.actor)
        result = service.execute(
            proposal.proposal_id,
            "token-alterado",
            "req-1",
            self.actor,
        )
        self.assertEqual("denied", result.status)

    def test_authorization_is_checked_at_execution(self) -> None:
        service = PolicyAssistant(PolicyRepository([]))
        proposal = service.propose_action("create_request", {"days": 2}, self.actor)
        revoked_actor = Actor("emp-1", "employee", frozenset())
        result = service.execute(
            proposal.proposal_id,
            proposal.confirmation_token,
            "req-2",
            revoked_actor,
        )
        self.assertEqual("denied", result.status)

    def test_idempotency_prevents_duplicate_effect(self) -> None:
        service = PolicyAssistant(PolicyRepository([]))
        proposal = service.propose_action("create_request", {"days": 2}, self.actor)
        first = service.execute(
            proposal.proposal_id,
            proposal.confirmation_token,
            "req-3",
            self.actor,
        )
        second = service.execute(
            proposal.proposal_id,
            proposal.confirmation_token,
            "req-3",
            self.actor,
        )
        self.assertEqual("executed", first.status)
        self.assertEqual("already_executed", second.status)

    def test_conflicting_applicable_policies_cause_abstention(self) -> None:
        service = PolicyAssistant(
            PolicyRepository(
                [
                    policy("POL-A"),
                    policy("POL-B", content="trabalho remoto exige análise de segurança"),
                ]
            )
        )
        answer = service.answer("trabalho remoto", self.actor, "BR", TODAY)
        self.assertEqual("abstained", answer.status)
        self.assertEqual("conflicting_evidence", answer.reason)

    def test_trace_rejects_raw_content(self) -> None:
        service = PolicyAssistant(PolicyRepository([policy()]))
        service.answer("trabalho remoto", self.actor, "BR", TODAY)
        trace = next(iter(service.traces.values()))
        with self.assertRaises(ValueError):
            trace.record("unsafe", content="dado sensível")

    def test_governed_benchmark_preserves_invariants(self) -> None:
        report = run()
        governed = report["configurations"]["lexical_governed"]
        baseline = report["configurations"]["lexical_ungoverned"]
        self.assertEqual(1.0, governed["task_success_rate"])
        self.assertEqual(0, governed["unauthorized_exposures"])
        self.assertLess(baseline["task_success_rate"], governed["task_success_rate"])

    def test_replay_adapter_and_router_are_provider_independent(self) -> None:
        default = ReplayAdapter({"general": "resposta geral"}, name="small")
        specialist = ReplayAdapter({"risk": "resposta especializada"}, name="large")
        router = TaskRouter(default, {"risk": specialist})
        self.assertEqual("small", router.generate(ModelRequest("general", "x")).model)
        self.assertEqual("large", router.generate(ModelRequest("risk", "x")).model)

    def test_model_benchmark_replay_passes_versioned_cases(self) -> None:
        dataset = json.loads(
            (ROOT / "evaluation" / "model-cases.json").read_text(encoding="utf-8")
        )
        report = evaluate_model(
            ReplayAdapter(dataset["replay_responses"]),
            dataset,
        )
        self.assertEqual(1.0, report["pass_rate"])

    def test_release_gate_blocks_unsafe_candidate(self) -> None:
        safe = run()["configurations"]["lexical_governed"]
        self.assertEqual("promote", decide(safe)["decision"])
        unsafe = dict(safe, unauthorized_exposures=1)
        self.assertEqual("block", decide(unsafe)["decision"])

    def test_fine_tuning_dataset_has_no_split_leakage(self) -> None:
        script = ROOT.parent / "fine-tuning-lab" / "validate_dataset.py"
        spec = importlib.util.spec_from_file_location("validate_dataset", script)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(module)
        self.assertEqual("valid", module.validate()["status"])

    def test_serving_simulator_reports_cost_per_success(self) -> None:
        script = ROOT.parent / "serving-lab" / "simulate.py"
        spec = importlib.util.spec_from_file_location("serving_simulator", script)
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        report = module.simulate(module.SimulationConfig(requests=20))
        self.assertEqual(20, report["accepted"])
        self.assertGreater(report["throughput_requests_s"], 0)
        self.assertGreater(report["cost_per_success"], 0)


if __name__ == "__main__":
    unittest.main()
