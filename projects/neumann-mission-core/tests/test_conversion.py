import unittest
from fractions import Fraction

from neumann.core import convert, expansion, fraction_from_digits


class ConversionTests(unittest.TestCase):
    def test_exact_round_trip_through_three_radices(self):
        for value in (Fraction(11, 46), Fraction(1, 7), Fraction(5, 8), Fraction(17, 6)):
            with self.subTest(value=value):
                start = current = expansion(value, 2)
                for base in (10, 16, 2):
                    current = convert(current, base)
                    self.assertEqual(current, expansion(value, base))
                    self.assertEqual(
                        fraction_from_digits(base, current.integer, current.prefix, current.repetend),
                        value,
                    )
                self.assertEqual(current, start)

    def test_decode_known_notation(self):
        self.assertEqual(fraction_from_digits(2, '0', '', '01'), Fraction(1, 3))
        self.assertEqual(fraction_from_digits(10, '0', '1', '6'), Fraction(1, 6))
        self.assertEqual(fraction_from_digits(16, '1', 'A', 'B'), Fraction(401, 240))

    def test_reject_digit_outside_radix(self):
        with self.assertRaises(ValueError):
            fraction_from_digits(2, '0', '', '2')
