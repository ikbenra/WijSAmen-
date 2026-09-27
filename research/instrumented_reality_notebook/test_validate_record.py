#!/usr/bin/env python3
import copy
import json
import unittest
from pathlib import Path

from validate_record import canonical_bytes, validate


EXAMPLE = json.loads((Path(__file__).parent / "record.example.json").read_text(encoding="utf-8"))


class NotebookValidatorTests(unittest.TestCase):
    def test_example_is_complete_for_review_but_not_authorized(self):
        receipt = validate(copy.deepcopy(EXAMPLE))
        self.assertEqual(receipt["documentation_status"], "COMPLETE_FOR_REVIEW")
        self.assertEqual(receipt["action_gate"], "NOT_AUTHORIZED_BY_THIS_TOOL")
        self.assertIn("apparatus identity is not exact and verified", receipt["physical_action_blockers"])

    def test_literal_observation_is_required(self):
        record = copy.deepcopy(EXAMPLE)
        record["observation"]["literal"] = ""
        receipt = validate(record)
        self.assertEqual(receipt["documentation_status"], "INCOMPLETE")
        self.assertIn("observation.literal is required", receipt["errors"])

    def test_physical_action_remains_blocked_even_with_verified_hardware(self):
        record = copy.deepcopy(EXAMPLE)
        record["apparatus_identity"]["status"] = "EXACT_VERIFIED"
        record["energy_inventory"] = {"state": "DEENERGIZED_VERIFIED", "sources": [], "stored_energy_checked": True}
        record["authority"] = {
            "physical_action_requested": True,
            "owner_permission": "VERIFIED",
            "competent_safety_review": "VERIFIED"
        }
        receipt = validate(record)
        self.assertIn("physical action requires separate human authority and competent safety review", receipt["physical_action_blockers"])
        self.assertEqual(receipt["action_gate"], "NOT_AUTHORIZED_BY_THIS_TOOL")

    def test_receipt_hash_is_deterministic(self):
        a = validate(copy.deepcopy(EXAMPLE))
        b = validate(json.loads(canonical_bytes(EXAMPLE)))
        self.assertEqual(a["record_sha256"], b["record_sha256"])
        self.assertEqual(a["receipt_sha256"], b["receipt_sha256"])


if __name__ == "__main__":
    unittest.main()
