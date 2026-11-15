"""An exact rational value represented by a small JSON message."""

import json
from fractions import Fraction

from .core import Expansion, fraction_from_digits


def encode_message(value: Expansion) -> bytes:
    """Encode the radix and digit fields as deterministic UTF-8 JSON."""
    return json.dumps({
        'base': value.base,
        'integer': value.integer,
        'prefix': value.prefix,
        'repetend': value.repetend,
    }, separators=(',', ':')).encode('utf-8')


def decode_message(payload: bytes) -> Fraction:
    """Recover the exact value from a message, without sender state."""
    def unique_fields(pairs: list[tuple[str, object]]) -> dict[str, object]:
        fields = dict(pairs)
        if len(fields) != len(pairs):
            raise ValueError('duplicate fraction message field')
        return fields

    fields = json.loads(payload.decode('utf-8'), object_pairs_hook=unique_fields)
    digit_fields = ('integer', 'prefix', 'repetend')
    if (not isinstance(fields, dict) or fields.keys() != {'base', *digit_fields}
            or type(fields['base']) is not int
            or any(not isinstance(fields[name], str) for name in digit_fields)):
        raise ValueError('invalid fraction message fields')
    return fraction_from_digits(
        fields['base'], fields['integer'], fields['prefix'], fields['repetend'],
    )
