import unittest
from fractions import Fraction
from core import represent, multiplicative_order, start_cursor, advance, switch

class BinDecHexTests(unittest.TestCase):
    def test_roundtrip(self):
        for value in (Fraction(1,23), Fraction(1,8), Fraction(7,20), Fraction(-5,6), Fraction(13,4), Fraction(0)):
            for base in (2,10,16):
                with self.subTest(value=value,base=base):
                    self.assertEqual(represent(value,base).exact_value(),value)

    def test_periods(self):
        self.assertEqual([multiplicative_order(b,23) for b in (2,10,16)],[11,22,11])
        self.assertEqual([multiplicative_order(b,47) for b in (2,10,16)],[23,46,23])

    def test_phase(self):
        c=advance(start_cursor(Fraction(1,23),2),11)
        d=switch(c,10)
        self.assertEqual(d.remainder,c.remainder)
        self.assertEqual(d.value,c.value)

    def test_reject(self):
        c=advance(start_cursor(Fraction(2,5),2),1)
        with self.assertRaisesRegex(ValueError,"UNREACHABLE_PHASE"):
            switch(c,16)
        self.assertEqual(c.index,1)

    def test_finite(self):
        self.assertEqual(represent(Fraction(1,8),2).cycle,"")
        self.assertEqual(represent(Fraction(1,3),10).cycle,"3")

if __name__=="__main__":
    unittest.main()
