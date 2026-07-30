from __future__ import annotations

import hashlib
import json
import uuid
from datetime import date
from typing import Any

from .domain import (
    ActionProposal,
    ActionResult,
    Actor,
    Answer,
    Evidence,
    Trace,
)
from .repository import PolicyRepository


def _stable_hash(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


class PolicyAssistant:
    def __init__(self, repository: PolicyRepository) -> None:
        self._repository = repository
        self._proposals: dict[str, ActionProposal] = {}
        self._results: dict[str, ActionResult] = {}
        self.traces: dict[str, Trace] = {}

    def answer(
        self,
        question: str,
        actor: Actor,
        jurisdiction: str,
        when: date,
    ) -> Answer:
        trace = self._new_trace()
        documents = self._repository.search(
            question=question,
            actor=actor,
            jurisdiction=jurisdiction,
            when=when,
        )
        trace.record(
            "retrieval_completed",
            actor_id=actor.actor_id,
            jurisdiction=jurisdiction,
            result_count=len(documents),
        )

        if not documents:
            trace.record("answer_abstained", reason="insufficient_evidence")
            return Answer(
                status="abstained",
                text="Não encontrei uma política vigente e autorizada para sustentar a resposta.",
                reason="insufficient_evidence",
            )

        top = documents[0]
        same_priority = [
            document
            for document in documents[1:]
            if document.valid_from == top.valid_from
            and document.policy_id != top.policy_id
        ]
        if same_priority:
            trace.record("answer_abstained", reason="conflicting_evidence")
            return Answer(
                status="abstained",
                text="Encontrei políticas aplicáveis em conflito. O caso precisa de revisão.",
                reason="conflicting_evidence",
            )

        evidence = Evidence(
            policy_id=top.policy_id,
            title=top.title,
            version=top.version,
            excerpt=top.content,
            authority=top.authority,
        )
        trace.record(
            "answer_created",
            policy_id=top.policy_id,
            policy_version=top.version,
        )
        return Answer(
            status="answered",
            text=f"Segundo {top.title}, {top.content}",
            evidence=(evidence,),
        )

    def propose_action(
        self,
        action: str,
        parameters: dict[str, Any],
        actor: Actor,
    ) -> ActionProposal:
        proposal_id = str(uuid.uuid4())
        confirmation_payload = {
            "proposal_id": proposal_id,
            "action": action,
            "parameters": parameters,
            "actor_id": actor.actor_id,
        }
        proposal = ActionProposal(
            proposal_id=proposal_id,
            action=action,
            parameters=dict(parameters),
            actor_id=actor.actor_id,
            confirmation_token=_stable_hash(confirmation_payload),
        )
        self._proposals[proposal_id] = proposal
        return proposal

    def execute(
        self,
        proposal_id: str,
        confirmation_token: str,
        request_id: str,
        actor: Actor,
    ) -> ActionResult:
        if request_id in self._results:
            previous = self._results[request_id]
            return ActionResult(
                status="already_executed",
                request_id=request_id,
                detail=previous.detail,
            )

        proposal = self._proposals[proposal_id]
        if proposal.actor_id != actor.actor_id:
            return ActionResult("denied", request_id, "A proposta pertence a outro ator.")
        if confirmation_token != proposal.confirmation_token:
            return ActionResult("denied", request_id, "A confirmação não corresponde à proposta.")
        if proposal.action not in actor.permissions:
            return ActionResult("denied", request_id, "O ator não possui autorização para a ação.")

        result = ActionResult(
            status="executed",
            request_id=request_id,
            detail=f"{proposal.action} executada com parâmetros validados.",
        )
        self._results[request_id] = result
        return result

    def _new_trace(self) -> Trace:
        trace = Trace(trace_id=str(uuid.uuid4()))
        self.traces[trace.trace_id] = trace
        return trace
