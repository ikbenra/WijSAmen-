#!/usr/bin/env python3

import unittest

from validate_card import validate


def valid_card() -> dict:
    return {
        "schema_version": 1,
        "card_id": "example-001",
        "preregistered_at": "before-observation",
        "observed_at": "after-preregistration",
        "interpretation_disclosed": True,
        "permission_to_test": True,
        "virtual_lines_labeled_unverified": True,
        "persistent_learning_claimed": False,
        "predictions": [
            {"feature": "tone", "expected": "warm", "disconfirming_observation": "cold"},
            {"feature": "scope", "expected": "bounded", "disconfirming_observation": "unbounded"},
            {"feature": "agency", "expected": "choice preserved", "disconfirming_observation": "choice removed"},
        ],
        "observed_line_3": "Observed reply text",
        "scores": [
            {"prediction_index": 0, "outcome": "matched", "evidence_excerpt": "warm"},
            {"prediction_index": 1, "outcome": "missed", "evidence_excerpt": "broad"},
            {"prediction_index": 2, "outcome": "unclear", "evidence_excerpt": "ambiguous"},
        ],
        "clarification_questions": ["Was the broad scope intentional?"],
    }


class ValidatorTests(unittest.TestCase):
    def test_valid_card(self):
        self.assertEqual(validate(valid_card()), [])

    def test_requires_three_predictions(self):
        card = valid_card()
        card["predictions"] = card["predictions"][:2]
        self.assertIn("exactly three predictions are required", validate(card))

    def test_rejects_two_questions(self):
        card = valid_card()
        card["clarification_questions"].append("Second question?")
        self.assertIn("at most one clarification question is allowed", validate(card))

    def test_rejects_persistent_learning_claim(self):
        card = valid_card()
        card["persistent_learning_claimed"] = True
        self.assertIn("persistent learning may not be claimed", validate(card))

    def test_requires_disclosure_and_permission(self):
        card = valid_card()
        card["interpretation_disclosed"] = False
        card["permission_to_test"] = False
        errors = validate(card)
        self.assertIn("interpretation_disclosed must be true", errors)
        self.assertIn("permission_to_test must be true", errors)


if __name__ == "__main__":
    unittest.main()
