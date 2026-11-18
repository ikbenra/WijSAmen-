"""Check shared value contracts against the pinned mission-core on PYTHONPATH."""

import unittest
from fractions import Fraction

from core import Representation, represent
from neumann.core import expansion, fraction_from_digits


class MissionCoreComparison(unittest.TestCase):
    def test_exact_value_and_digits_of_11_over_46(self):
        expected = Fraction(11, 46)
        for base in (2, 10, 16):
            with self.subTest(base=base):
                candidate = represent(expected, base)
                reference = expansion(expected, base)

                candidate_value = candidate.exact_value()
                reference_value = fraction_from_digits(
                    reference.base, reference.integer, reference.prefix, reference.repetend,
                )
                self.assertEqual(candidate_value, expected)
                self.assertEqual(reference_value, expected)

                self.assertEqual(candidate.sign, 1)
                self.assertEqual(
                    (candidate.base, candidate.integer, candidate.prefix, candidate.cycle),
                    (reference.base, reference.integer, reference.prefix, reference.repetend),
                )
                self.assertEqual(fraction_from_digits(
                    base=candidate.base,
                    integer=candidate.integer,
                    prefix=candidate.prefix,
                    repetend=candidate.cycle,
                ), expected)
                print(f"base {base}: {candidate.display()} -> {candidate_value} = {reference_value}")


    def test_shared_nonnegative_domain(self):
        checked = 0
        for denominator in range(1, 32):
            for numerator in range(2 * denominator + 1):
                expected = Fraction(numerator, denominator)
                for base in (2, 10, 16):
                    with self.subTest(numerator=numerator, denominator=denominator, base=base):
                        candidate = represent(expected, base)
                        reference = expansion(expected, base)
                        self.assertEqual(candidate.sign, 1)
                        self.assertEqual(
                            (candidate.integer, candidate.prefix, candidate.cycle),
                            (reference.integer, reference.prefix, reference.repetend),
                        )
                        self.assertEqual(candidate.exact_value(), expected)
                        self.assertEqual(fraction_from_digits(
                            reference.base, reference.integer, reference.prefix, reference.repetend,
                        ), expected)
                        self.assertEqual(fraction_from_digits(
                            candidate.base, candidate.integer, candidate.prefix, candidate.cycle,
                        ), expected)
                        mapped_reference = Representation(
                            reference.base, 1, reference.integer, reference.prefix, reference.repetend,
                        )
                        self.assertEqual(mapped_reference.exact_value(), expected)
                        checked += 1
        print(f"Shared domain: {checked} numerator/denominator/base cases checked")

    def test_negative_values_have_different_contracts(self):
        for value in (Fraction(-5, 6), Fraction(-2)):
            for base in (2, 10, 16):
                with self.subTest(value=value, base=base):
                    candidate = represent(value, base)
                    self.assertEqual(candidate.sign, -1)
                    self.assertEqual(candidate.exact_value(), value)
                    with self.assertRaisesRegex(ValueError, 'nonnegative'):
                        expansion(value, base)


if __name__ == "__main__":
    unittest.main()
