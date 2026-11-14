import json
import unittest
from pathlib import Path
from check import validate

class ContinuityTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads((Path(__file__).parent / "manifest.json").read_text())

    def test_valid(self):
        self.assertTrue(validate(self.data))

    def test_duplicate_agent_rejected(self):
        self.data["agents"].append(self.data["agents"][0])
        with self.assertRaises(AssertionError):
            validate(self.data)

    def test_unverified_consciousness_claim_rejected(self):
        self.data["claims"]["consciousness_continuity"] = "proven"
        with self.assertRaises(AssertionError):
            validate(self.data)

if __name__ == "__main__":
    unittest.main()
