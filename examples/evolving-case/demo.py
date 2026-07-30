from datetime import date
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from policy_assistant import Actor, PolicyAssistant, PolicyDocument, PolicyRepository


documents = [
    PolicyDocument(
        policy_id="POL-REMOTO-BR",
        title="Política de trabalho remoto no Brasil",
        version="3.0",
        valid_from=date(2026, 1, 1),
        valid_until=None,
        jurisdiction="BR",
        access_level="employee",
        content=(
            "o trabalho temporário em outro estado exige registro prévio e aprovação da liderança."
        ),
        authority="Recursos Humanos",
    )
]

actor = Actor(
    actor_id="emp-123",
    access_level="employee",
    permissions=frozenset({"create_remote_work_request"}),
)
assistant = PolicyAssistant(PolicyRepository(documents))

answer = assistant.answer(
    question="Posso trabalhar temporariamente em outro estado?",
    actor=actor,
    jurisdiction="BR",
    when=date(2026, 7, 30),
)
print("RESPOSTA")
print(answer)

proposal = assistant.propose_action(
    action="create_remote_work_request",
    parameters={"destination_state": "MG", "days": 10},
    actor=actor,
)
print("\nPROPOSTA SEM EFEITO")
print(proposal)

result = assistant.execute(
    proposal_id=proposal.proposal_id,
    confirmation_token=proposal.confirmation_token,
    request_id="req-demo-001",
    actor=actor,
)
print("\nRESULTADO")
print(result)

repeated = assistant.execute(
    proposal_id=proposal.proposal_id,
    confirmation_token=proposal.confirmation_token,
    request_id="req-demo-001",
    actor=actor,
)
print("\nREPETIÇÃO SEGURA")
print(repeated)

print("\nTRACE MINIMIZADO")
print(next(iter(assistant.traces.values())).events)
