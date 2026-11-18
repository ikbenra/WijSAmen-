"""Exact rational representations and phase transitions in bases 2, 10 and 16."""
from dataclasses import dataclass
from fractions import Fraction
from math import gcd

BASES = (2, 10, 16)
DIGITS = "0123456789ABCDEF"

def require_base(base):
    if type(base) is not int or base not in BASES:
        raise ValueError("Only bases 2, 10 and 16 are supported")

def encode_integer(number, base):
    require_base(base)
    if number < 0:
        raise ValueError("Unsigned integer required")
    if number == 0:
        return "0"
    result = ""
    while number:
        number, digit = divmod(number, base)
        result = DIGITS[digit] + result
    return result

def decode_integer(text, base):
    require_base(base)
    if not text or any(ch not in DIGITS[:base] for ch in text):
        raise ValueError("Invalid digits")
    number = 0
    for ch in text:
        number = number * base + DIGITS.index(ch)
    return number

@dataclass(frozen=True)
class Representation:
    base: int
    sign: int
    integer: str
    prefix: str
    cycle: str

    def display(self):
        return ("-" if self.sign < 0 else "") + self.integer + "." + self.prefix + (f"({self.cycle})" if self.cycle else "")

    def exact_value(self):
        require_base(self.base)
        integer = decode_integer(self.integer, self.base)
        prefix = decode_integer(self.prefix, self.base) if self.prefix else 0
        result = Fraction(integer) + Fraction(prefix, self.base ** len(self.prefix))
        if self.cycle:
            cycle = decode_integer(self.cycle, self.base)
            result += Fraction(cycle, self.base ** len(self.prefix) * (self.base ** len(self.cycle) - 1))
        return self.sign * result

def represent(value, base, max_digits=10000):
    require_base(base)
    value = Fraction(value)
    if max_digits < 1:
        raise ValueError("Invalid digit limit")
    sign = -1 if value < 0 else 1
    value = abs(value)
    integer, remainder = divmod(value.numerator, value.denominator)
    seen, digits = {}, []
    while remainder and remainder not in seen:
        if len(digits) >= max_digits:
            raise ValueError("Expansion exceeds max_digits")
        seen[remainder] = len(digits)
        digit, remainder = divmod(remainder * base, value.denominator)
        digits.append(DIGITS[digit])
    boundary = seen[remainder] if remainder else len(digits)
    return Representation(base, sign, encode_integer(integer, base), "".join(digits[:boundary]), "".join(digits[boundary:]))

def multiplicative_order(base, modulus):
    require_base(base)
    if modulus < 1 or gcd(base, modulus) != 1:
        raise ValueError("Modulus must be positive and coprime to base")
    if modulus == 1:
        return 1
    residue, count = base % modulus, 1
    while residue != 1:
        residue = residue * base % modulus
        count += 1
    return count

@dataclass(frozen=True)
class Cursor:
    value: Fraction
    base: int
    index: int
    remainder: int

def start_cursor(value, base):
    require_base(base)
    value = Fraction(value)
    if not 0 <= value < 1:
        raise ValueError("Cursor requires [0,1)")
    return Cursor(value, base, 0, value.numerator)

def advance(cursor, steps=1):
    require_base(cursor.base)
    if type(steps) is not int or steps < 0:
        raise ValueError("Nonnegative integral steps required")
    if cursor.index < 0 or not 0 <= cursor.remainder < cursor.value.denominator:
        raise ValueError("Corrupted cursor")
    expected = cursor.value.numerator * pow(cursor.base, cursor.index, cursor.value.denominator) % cursor.value.denominator
    if expected != cursor.remainder:
        raise ValueError("Corrupted cursor")
    remainder = cursor.remainder * pow(cursor.base, steps, cursor.value.denominator) % cursor.value.denominator
    return Cursor(cursor.value, cursor.base, cursor.index + steps, remainder)

def switch(cursor, target_base, max_search=10000):
    require_base(target_base)
    if type(max_search) is not int or max_search < 1:
        raise ValueError("Invalid search limit")
    cursor = advance(cursor, 0)
    if cursor.base == target_base:
        return cursor
    denominator = cursor.value.denominator
    remainder = cursor.value.numerator
    visited = set()
    index = 0
    while remainder not in visited:
        if remainder == cursor.remainder:
            return Cursor(cursor.value, target_base, index, remainder)
        if index >= max_search:
            raise ValueError("SEARCH_LIMIT")
        visited.add(remainder)
        remainder = remainder * target_base % denominator
        index += 1
    raise ValueError("UNREACHABLE_PHASE")
