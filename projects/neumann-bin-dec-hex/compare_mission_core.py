"""Compare 11/46 with the pinned mission-core checkout on PYTHONPATH."""

import unittest
from fractions import Fraction

from core import represent
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


if __name__ == "__main__":
    unittest.main()
