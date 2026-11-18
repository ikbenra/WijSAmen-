import unittest
from fractions import Fraction
from bridge import BASES, Mission, expansion, decode, run

class BridgeTests(unittest.TestCase):
    def test_exact_11_over_46_all_bases(self):
        for base in BASES:
            with self.subTest(base=base):
                self.assertEqual(decode(expansion(11, 46, base)), Fraction(11, 46))

    def test_deterministic_mission(self):
        mission = Mission("neumann-11-46", 11, 46)
        self.assertEqual(run(mission), run(mission))
        self.assertTrue(run(mission)["passed"])
        self.assertEqual(run(mission)["integration_status"], "UNVERIFIED_EXTERNAL_CORE")

    def test_terminating_and_repeating(self):
        self.assertEqual(decode(expansion(1, 2, 2)), Fraction(1, 2))
        self.assertEqual(decode(expansion(1, 3, 10)), Fraction(1, 3))

    def test_invalid_inputs(self):
        for args in [(11, 0, 10), (-1, 46, 10), (46, 46, 10), (11, 46, 8)]:
            with self.subTest(args=args):
                with self.assertRaises(ValueError):
                    expansion(*args)

    def test_mission_identifier_required(self):
        with self.assertRaises(ValueError):
            run(Mission("", 11, 46))

if __name__ == "__main__":
    unittest.main()
