"""Exact rational radix exploration for a prospective Neumann mission scheduler."""
from dataclasses import dataclass
from fractions import Fraction

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

@dataclass(frozen=True)
class Expansion:
    base: int
    integer: str
    prefix: str
    repetend: str
    remainders: tuple[int, ...]

def expansion(value: Fraction, base: int) -> Expansion:
    if not 2 <= base <= 36:
        raise ValueError("base must be 2..36")
    if value < 0:
        raise ValueError("nonnegative fractions only")
    integer, remainder = divmod(value.numerator, value.denominator)
    def encode(n: int) -> str:
        if n == 0:
            return "0"
        chars = []
        while n:
            n, digit = divmod(n, base)
            chars.append(DIGITS[digit])
        return "".join(reversed(chars))
    seen: dict[int, int] = {}
    digits: list[str] = []
    remainders: list[int] = []
    while remainder and remainder not in seen:
        seen[remainder] = len(digits)
        remainders.append(remainder)
        digit, remainder = divmod(remainder * base, value.denominator)
        digits.append(DIGITS[digit])
    split = seen[remainder] if remainder else len(digits)
    return Expansion(base, encode(integer), "".join(digits[:split]),
                     "".join(digits[split:]) if remainder else "", tuple(remainders))

def carry_sum(groups: list[int], base: int, width: int) -> tuple[int, int]:
    """Return (carry, remainder) for addition of width-digit groups."""
    if width < 1 or not 2 <= base <= 36:
        raise ValueError("invalid base or width")
    limit = base ** width
    if any(not 0 <= x < limit for x in groups):
        raise ValueError("group exceeds width")
    return divmod(sum(groups), limit)

def sample() -> dict[int, Expansion]:
    return {b: expansion(Fraction(11, 46), b) for b in (2, 8, 10, 16)}
