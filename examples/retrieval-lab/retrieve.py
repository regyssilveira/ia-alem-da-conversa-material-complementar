"""Laboratório determinístico de recuperação lexical, conceitual e híbrida."""

from __future__ import annotations

import argparse
import json
import math
import re
import unicodedata
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"

CONCEPTS = {
    "reembolso": {"reembolso", "ressarcimento", "despesa", "prestacao", "contas"},
    "prazo": {"prazo", "quando", "ate", "dias", "depois"},
    "viagem": {"viagem", "retorno", "voltar", "internacional"},
    "comprovante": {"comprovante", "recibo", "nota", "fiscal"},
    "hospedagem": {"hospedagem", "hotel", "estabelecimento", "periodo"},
    "pagamento": {"pagamento", "credito", "folha", "aprovado"},
}


def normalize(text: str) -> list[str]:
    folded = unicodedata.normalize("NFKD", text.lower())
    ascii_text = "".join(char for char in folded if not unicodedata.combining(char))
    return re.findall(r"[a-z0-9]+", ascii_text)


def conceptual(tokens: list[str]) -> Counter[str]:
    features: Counter[str] = Counter(tokens)
    token_set = set(tokens)
    for concept, members in CONCEPTS.items():
        if token_set & members:
            features[f"concept:{concept}"] += 2
    return features


def cosine(left: Counter[str], right: Counter[str]) -> float:
    dot = sum(value * right.get(key, 0) for key, value in left.items())
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    return dot / (left_norm * right_norm) if left_norm and right_norm else 0.0


def is_valid(document: dict, unit: str, as_of: str) -> bool:
    instant = date.fromisoformat(as_of)
    starts = date.fromisoformat(document["valid_from"])
    ends = date.fromisoformat(document["valid_until"]) if document["valid_until"] else None
    unit_allowed = document["unit"] in {"brasil", unit}
    return unit_allowed and starts <= instant and (ends is None or instant <= ends)


def score(query: str, document: dict, mode: str) -> float:
    query_tokens = normalize(query)
    document_tokens = normalize(document["text"])
    lexical = len(set(query_tokens) & set(document_tokens)) / max(len(set(query_tokens)), 1)
    semantic = cosine(conceptual(query_tokens), conceptual(document_tokens))
    if mode == "lexical":
        return lexical
    if mode == "semantic":
        return semantic
    return (0.45 * lexical) + (0.55 * semantic)


def retrieve(query: str, unit: str, as_of: str, mode: str = "hybrid", limit: int = 3) -> list[dict]:
    documents = json.loads((DATA / "documents.json").read_text(encoding="utf-8"))
    candidates = [document for document in documents if is_valid(document, unit, as_of)]
    scored = []
    for document in candidates:
        relevance = score(query, document, mode)
        if relevance < 0.16:
            continue
        rank_score = relevance + (document["authority"] / 250)
        scored.append({**document, "score": round(relevance, 4), "rank_score": round(rank_score, 4)})
    ranked = sorted(scored, key=lambda item: (item["rank_score"], item["authority"]), reverse=True)
    return ranked[:limit]


def evaluate(mode: str) -> dict:
    cases = json.loads((DATA / "cases.json").read_text(encoding="utf-8"))
    reciprocal_ranks: list[float] = []
    recall_hits = 0
    abstention_hits = 0
    details = []
    for case in cases:
        results = retrieve(case["query"], case["unit"], case["as_of"], mode)
        result_ids = [item["chunk_id"] for item in results]
        ranks = [result_ids.index(expected) + 1 for expected in case["expected"] if expected in result_ids]
        reciprocal_ranks.append(1 / min(ranks) if ranks else 0.0)
        recall_hits += int(bool(ranks) or case["must_abstain"])
        abstained = not results
        abstention_hits += int(abstained == case["must_abstain"])
        details.append({"case_id": case["case_id"], "results": result_ids, "abstained": abstained})
    total = len(cases)
    return {
        "mode": mode,
        "recall_at_3": round(recall_hits / total, 3),
        "mrr": round(sum(reciprocal_ranks) / total, 3),
        "abstention_accuracy": round(abstention_hits / total, 3),
        "details": details,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("lexical", "semantic", "hybrid"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    reports = [evaluate(args.mode)] if args.mode else [evaluate(mode) for mode in ("lexical", "semantic", "hybrid")]
    if args.json:
        print(json.dumps(reports, ensure_ascii=False, indent=2))
        return
    print("modo      recall@3  MRR    abstenção")
    for report in reports:
        print(f"{report['mode']:<10}{report['recall_at_3']:<10.3f}{report['mrr']:<7.3f}{report['abstention_accuracy']:.3f}")


if __name__ == "__main__":
    main()
