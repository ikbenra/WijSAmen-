import unittest
from simulate import run, evaluate, CANDIDATES

class SimulationTests(unittest.TestCase):
    def test_no_candidate_deployed(self):
        self.assertTrue(all(not r["deployed"] for r in run()["results"]))
    def test_unsafe_candidate_blocked(self):
        self.assertFalse(evaluate(CANDIDATES[2])["eligible_for_review"])
    def test_unknown_impact_blocked(self):
        self.assertFalse(evaluate(CANDIDATES[3])["eligible_for_review"])
    def test_safe_candidate_review_only(self):
        self.assertTrue(evaluate(CANDIDATES[1])["eligible_for_review"])
        self.assertTrue(run()["requires_human_review"])

if __name__ == "__main__":
    unittest.main()
