import unittest
from neumann.periods import (multiplicative_order, periods_for_parameter,
                             normalized_family, middle_candidates, BoundedRotor, RotorState)

class PeriodTests(unittest.TestCase):
    def test_families(self):
        self.assertEqual(periods_for_parameter(11), (11,22,11))
        self.assertEqual(periods_for_parameter(23), (23,46,23))
        self.assertEqual(periods_for_parameter(29), (58,58,29))
        self.assertEqual(normalized_family(periods_for_parameter(41)), (2,1,1))
    def test_hex_identity(self):
        for p in range(1,101):
            t = multiplicative_order(2,2*p+1)
            self.assertEqual(multiplicative_order(16,2*p+1), t // __import__('math').gcd(t,4))
    def test_candidates(self):
        self.assertIn(10, middle_candidates(11))
        self.assertNotIn(8, middle_candidates(11))
    def test_bounded_repeat(self):
        r = BoundedRotor(11, (10,8,6), 64)
        self.assertEqual(r.base(RotorState(0,0)), 2)
        self.assertEqual(r.base(RotorState(1,0)), 10)
        self.assertEqual(r.base(RotorState(2,0)), 16)
        self.assertIsNotNone(r.find_repeat())
    def test_invalid(self):
        with self.assertRaises(ValueError):
            periods_for_parameter(11, 23)

if __name__ == '__main__': unittest.main()
