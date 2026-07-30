from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Any, Literal


AccessLevel = Literal["public", "employee", "manager"]
ACCESS_ORDER: dict[AccessLevel, int] = {
    "public": 0,
    "employee": 1,
    "manager": 2,
}


@dataclass(frozen=True)
class Actor:
    actor_id: str
    access_level: AccessLevel
    permissions: frozenset[str] = frozenset()


@dataclass(frozen=True)
class PolicyDocument:
    policy_id: str
    title: str
    version: str
    valid_from: date
    valid_until: date | None
    jurisdiction: str
    access_level: AccessLevel
    content: str
    authority: str

    def is_valid_on(self, when: date) -> bool:
        return self.valid_from <= when and (
            self.valid_until is None or when <= self.valid_until
        )


@dataclass(frozen=True)
class Evidence:
    policy_id: str
    title: str
    version: str
    excerpt: str
    authority: str


@dataclass(frozen=True)
class Answer:
    status: Literal["answered", "abstained"]
    text: str
    evidence: tuple[Evidence, ...] = ()
    reason: str | None = None


@dataclass(frozen=True)
class ActionProposal:
    proposal_id: str
    action: str
    parameters: dict[str, Any]
    actor_id: str
    confirmation_token: str


@dataclass(frozen=True)
class ActionResult:
    status: Literal["executed", "already_executed", "denied"]
    request_id: str
    detail: str


@dataclass
class Trace:
    trace_id: str
    events: list[dict[str, Any]] = field(default_factory=list)

    def record(self, event: str, **attributes: Any) -> None:
        forbidden = {"question", "content", "excerpt", "raw_document"}
        if forbidden.intersection(attributes):
            raise ValueError("O trace recebeu conteúdo que deveria ser minimizado.")
        self.events.append({"event": event, **attributes})
