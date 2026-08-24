import sys
import unittest
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB))

from retrieve import evaluate, retrieve  # noqa: E402


class RetrievalLabTests(unittest.TestCase):
    def test_revoked_version_is_filtered_before_ranking(self):
        results = retrieve("prazo reembolso 45 dias", "brasil", "2026-07-01")
        ids = [item["chunk_id"] for item in results]
        self.assertIn("POL-REEMBOLSO:v7:4.2", ids)
        self.assertNotIn("POL-REEMBOLSO:v6:4.2", ids)

    def test_local_exception_and_global_rule_are_both_available(self):
        results = retrieve("prazo viagem internacional", "brasil-sul", "2026-07-01")
        ids = [item["chunk_id"] for item in results]
        self.assertIn("POL-EXCECAO:v2:2.1", ids)
        self.assertIn("POL-REEMBOLSO:v7:4.2", ids)

    def test_out_of_scope_query_abstains(self):
        self.assertEqual(retrieve("férias coletivas", "brasil", "2026-07-01"), [])

    def test_hybrid_resolves_synonym_case(self):
        results = retrieve(
            "Até quando posso pedir ressarcimento depois de voltar da viagem?",
            "brasil",
            "2026-07-01",
            "hybrid",
        )
        self.assertEqual(results[0]["chunk_id"], "POL-REEMBOLSO:v7:4.2")

    def test_report_exposes_layer_metrics(self):
        report = evaluate("hybrid")
        self.assertIn("recall_at_3", report)
        self.assertIn("mrr", report)
        self.assertIn("abstention_accuracy", report)


if __name__ == "__main__":
    unittest.main()
