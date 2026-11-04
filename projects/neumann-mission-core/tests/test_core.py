import unittest
from fractions import Fraction
from neumann import expansion, carry_sum

class CoreTests(unittest.TestCase):
    def test_periods(self):
        self.assertEqual({b: len(expansion(Fraction(11,46), b).repetend) for b in (2,10,16)}, {2:11,10:22,16:11})
    def test_exact_decimal(self):
        x = expansion(Fraction(11,46), 10)
        self.assertEqual(x.prefix, '2')
        self.assertEqual(x.repetend, '3913043478260869565217')
    def test_carry(self):
        self.assertEqual(carry_sum([15, 1], 16, 1), (1,0))
        self.assertEqual(carry_sum([255, 1], 16, 2), (1,0))
    def test_terminating(self):
        x = expansion(Fraction(1,2), 2)
        self.assertEqual((x.prefix,x.repetend), ('1',''))

if __name__ == '__main__': unittest.main()
