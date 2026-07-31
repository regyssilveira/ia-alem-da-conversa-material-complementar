from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SPLITS = ("train", "validation", "test")
REQUIRED = {"scenario_id", "input", "output"}


def load_split(name: str) -> list[dict]:
    path = ROOT / "data" / f"{name}.jsonl"
    records = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        record = json.loads(line)
        missing = REQUIRED - record.keys()
        if missing:
            raise ValueError(f"{path.name}:{number}: campos ausentes {sorted(missing)}")
        if any(not str(record[field]).strip() for field in REQUIRED):
            raise ValueError(f"{path.name}:{number}: campo vazio")
        records.append(record)
    return records


def validate() -> dict:
    loaded = {name: load_split(name) for name in SPLITS}
    ids = {name: {row["scenario_id"] for row in rows} for name, rows in loaded.items()}
    for index, left in enumerate(SPLITS):
        for right in SPLITS[index + 1 :]:
            overlap = ids[left].intersection(ids[right])
            if overlap:
                raise ValueError(f"Vazamento entre {left} e {right}: {sorted(overlap)}")

    all_inputs = [
        row["input"].strip().lower()
        for rows in loaded.values()
        for row in rows
    ]
    if len(all_inputs) != len(set(all_inputs)):
        raise ValueError("Entradas duplicadas entre os conjuntos.")

    return {
        "splits": {name: len(rows) for name, rows in loaded.items()},
        "total": sum(len(rows) for rows in loaded.values()),
        "overlap": 0,
        "status": "valid",
    }


if __name__ == "__main__":
    print(json.dumps(validate(), ensure_ascii=False, indent=2))
