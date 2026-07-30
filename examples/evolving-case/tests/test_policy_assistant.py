from datetime import date
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from policy_assistant import Actor, PolicyAssistant, PolicyDocument, PolicyRepository


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


if __name__ == "__main__":
    unittest.main()
