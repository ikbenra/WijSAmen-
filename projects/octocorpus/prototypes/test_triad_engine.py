import unittest
from triad_engine import run, compare

class TriadEngineTests(unittest.TestCase):
    def test_six_and_eight(self):
        self.assertEqual(len(run(6)["traces"][0]["local"]), 6)
        self.assertEqual(len(run(8)["traces"][0]["local"]), 8)
    def test_deterministic(self):
        self.assertEqual(compare(), compare())
    def test_head_off(self):
        self.assertEqual(run(head=False)["memory"], {})
    def test_rollback(self):
        self.assertFalse(run()["base_policy_modified"])
        self.assertEqual(run(overlay=False), run(overlay=False))
    def test_no_consciousness_claim(self):
        self.assertTrue(all(not r["subjective_consciousness_proven"] for r in compare()))
    def test_invalid_mode(self):
        with self.assertRaises(ValueError):
            run(7)

if __name__ == "__main__":
    unittest.main()
