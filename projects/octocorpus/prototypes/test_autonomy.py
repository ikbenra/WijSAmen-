import copy, unittest
from autonomy import initial,evolve,score,examples
class AutonomyTests(unittest.TestCase):
    def test_determinism(self): self.assertEqual(evolve(initial()),evolve(initial()))
    def test_resume(self):
        a=evolve(initial(),1); b=evolve(copy.deepcopy(a),12)
        self.assertGreaterEqual(b["generation"],a["generation"])
    def test_holdout(self):
        a=initial(); b=evolve(initial()); hold=[examples()[i] for i in (3,7)]
        for kind in a["policies"]:
            self.assertGreaterEqual(score(b["policies"][kind],hold),score(a["policies"][kind],hold))
    def test_budget(self): self.assertLessEqual(evolve(initial(),2)["generation"],2)
    def test_claims(self): self.assertFalse(evolve(initial())["consciousness_proven"])
    def test_immutable_input(self):
        a=initial(); evolve(copy.deepcopy(a)); self.assertEqual(a,initial())
if __name__=="__main__": unittest.main()
