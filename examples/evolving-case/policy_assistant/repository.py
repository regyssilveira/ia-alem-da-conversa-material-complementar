from __future__ import annotations

import re
from datetime import date

from .domain import ACCESS_ORDER, Actor, PolicyDocument


def _terms(text: str) -> set[str]:
    stopwords = {
        "a",
        "as",
        "com",
        "como",
        "da",
        "de",
        "do",
        "e",
        "em",
        "o",
        "os",
        "para",
        "por",
        "que",
        "um",
        "uma",
    }
    return {
        term
        for term in re.findall(r"[a-zá-ú0-9]+", text.lower())
        if len(term) > 2 and term not in stopwords
    }


class PolicyRepository:
    def __init__(self, documents: list[PolicyDocument]) -> None:
        self._documents = tuple(documents)

    def search(
        self,
        question: str,
        actor: Actor,
        jurisdiction: str,
        when: date,
        limit: int = 3,
    ) -> list[PolicyDocument]:
        query_terms = _terms(question)
        candidates: list[tuple[int, PolicyDocument]] = []

        for document in self._documents:
            if document.jurisdiction != jurisdiction:
                continue
            if not document.is_valid_on(when):
                continue
            if ACCESS_ORDER[actor.access_level] < ACCESS_ORDER[document.access_level]:
                continue

            score = len(query_terms.intersection(_terms(document.content + " " + document.title)))
            if score:
                candidates.append((score, document))

        candidates.sort(
            key=lambda item: (item[0], item[1].valid_from, item[1].version),
            reverse=True,
        )
        return [document for _, document in candidates[:limit]]
