from __future__ import annotations

import argparse
import json
from pathlib import Path

from policy_assistant.models import (
    ModelRequest,
    OpenAICompatibleAdapter,
    ReplayAdapter,
)


ROOT = Path(__file__).resolve().parent
DEFAULT_DATASET = ROOT / "evaluation" / "model-cases.json"


def evaluate(adapter, dataset: dict, max_cost: float | None = None) -> dict:
    results = []
    total_input = total_output = 0
    for case in dataset["cases"]:
        response = adapter.generate(ModelRequest(case["id"], case["prompt"]))
        normalized = response.text.lower()
        passed = all(term.lower() in normalized for term in case["required_terms"])
        passed &= not any(term.lower() in normalized for term in case["forbidden_terms"])
        total_input += response.input_tokens or 0
        total_output += response.output_tokens or 0
        results.append(
            {
                "id": case["id"],
                "passed": passed,
                "model": response.model,
                "latency_ms": response.latency_ms,
            }
        )

    return {
        "dataset": dataset["dataset"],
        "adapter": adapter.name,
        "pass_rate": sum(item["passed"] for item in results) / len(results),
        "input_tokens": total_input,
        "output_tokens": total_output,
        "cost_limit_declared": max_cost,
        "results": results,
        "limitations": [
            "Verificação lexical não substitui rubrica humana ou checagem factual.",
            "Custos dependem da tabela datada do provedor e não são inferidos automaticamente.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument(
        "--adapter",
        choices=("replay", "openai-compatible"),
        default="replay",
    )
    parser.add_argument("--max-cost", type=float)
    args = parser.parse_args()
    dataset = json.loads(args.dataset.read_text(encoding="utf-8"))
    adapter = (
        ReplayAdapter(dataset["replay_responses"])
        if args.adapter == "replay"
        else OpenAICompatibleAdapter.from_environment()
    )
    print(
        json.dumps(
            evaluate(adapter, dataset, args.max_cost),
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
