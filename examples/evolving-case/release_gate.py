from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_RULES = {
    "task_success_rate": {"min": 0.95},
    "evidence_accuracy": {"min": 0.95},
    "abstention_accuracy": {"min": 0.95},
    "unauthorized_exposures": {"max": 0},
    "conflict_detection_rate": {"min": 1.0},
}


def decide(metrics: dict, rules: dict = DEFAULT_RULES) -> dict:
    checks = []
    for metric, rule in rules.items():
        value = metrics[metric]
        if "min" in rule:
            passed = value >= rule["min"]
            expected = f">= {rule['min']}"
        else:
            passed = value <= rule["max"]
            expected = f"<= {rule['max']}"
        checks.append(
            {
                "metric": metric,
                "value": value,
                "expected": expected,
                "passed": passed,
            }
        )
    return {
        "decision": "promote" if all(item["passed"] for item in checks) else "block",
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--configuration", default="lexical_governed")
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding="utf-8"))
    metrics = report["configurations"][args.configuration]
    decision = decide(metrics)
    print(json.dumps(decision, ensure_ascii=False, indent=2))
    raise SystemExit(0 if decision["decision"] == "promote" else 2)


if __name__ == "__main__":
    main()
