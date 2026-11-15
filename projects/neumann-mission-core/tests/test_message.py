import subprocess
import sys
import unittest
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory

from neumann.core import expansion
from neumann.message import decode_message, encode_message


class FractionMessageTests(unittest.TestCase):
    def test_two_readers_recover_the_same_saved_fraction(self):
        value = Fraction(11, 46)
        payload = encode_message(expansion(value, 16))
        self.assertEqual(
            payload, b'{"base":16,"integer":"0","prefix":"3","repetend":"D37A6F4DE9B"}',
        )
        reader = (
            'from pathlib import Path; from sys import argv; '
            'from neumann.message import decode_message; '
            'print(decode_message(Path(argv[1]).read_bytes()))'
        )
        with TemporaryDirectory() as directory:
            path = Path(directory) / 'fraction.json'
            path.write_bytes(payload)
            outcomes = [
                subprocess.check_output([sys.executable, '-c', reader, str(path)], text=True).strip()
                for _ in range(2)
            ]
        self.assertEqual(outcomes, ['11/46', '11/46'])

    def test_rejects_ambiguous_or_invalid_fields(self):
        for payload in (
            b'{"base":2,"base":10,"integer":"0","prefix":"","repetend":"01"}',
            b'{"base":2.0,"integer":"0","prefix":"","repetend":"01"}',
            b'{"base":2,"integer":"0","repetend":"01"}',
        ):
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                decode_message(payload)
