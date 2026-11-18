"""Deterministic, side-effect-free Neumann/Octo mission bridge prototype."""
from dataclasses import dataclass, asdict
from fractions import Fraction
from hashlib import sha256
import json

BASES = (2, 10, 16)
DIGITS = "0123456789abcdef"

def expansion(numerator: int, denominator: int, base: int, limit: int = 1000) -> dict:
    if base not in BASES or denominator <= 0 or numerator < 0 or numerator >= denominator:
        raise ValueError("Expected 0 <= numerator < denominator, positive denominator and base 2/10/16")
    if limit <= 0:
        raise ValueError("limit must be positive")
    remainder = numerator
    seen = {}
    digits = []
    while remainder and remainder not in seen:
        if len(digits) >= limit:
            raise ValueError("period limit exceeded")
        seen[remainder] = len(digits)
        remainder *= base
        digit, remainder = divmod(remainder, denominator)
        digits.append(DIGITS[digit])
    start = seen[remainder] if remainder else len(digits)
    return {"base": base, "prefix": "".join(digits[:start]),
            "cycle": "".join(digits[start:]), "terminating": remainder == 0}

def decode(result: dict) -> Fraction:
    base = result["base"]
    prefix = result["prefix"]
    cycle = result["cycle"]
    p = sum(int(c, base) * base ** (len(prefix)-i-1) for i,c in enumerate(prefix))
    value = Fraction(p, base ** len(prefix))
    if cycle:
        c = sum(int(ch, base) * base ** (len(cycle)-i-1) for i,ch in enumerate(cycle))
        value += Fraction(c, base ** len(prefix) * (base ** len(cycle) - 1))
    return value

@dataclass(frozen=True)
class Mission:
    mission_id: str
    numerator: int
    denominator: int

def run(mission: Mission) -> dict:
    if not mission.mission_id.strip():
        raise ValueError("mission_id required")
    expected = Fraction(mission.numerator, mission.denominator)
    records = [expansion(mission.numerator, mission.denominator, b) for b in BASES]
    passed = all(decode(r) == expected for r in records)
    payload = {"mission": asdict(mission), "expected": str(expected),
               "records": records, "passed": passed,
               "integration_status": "UNVERIFIED_EXTERNAL_CORE"}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return {**payload, "sha256": sha256(canonical.encode()).hexdigest()}

if __name__ == "__main__":
    print(json.dumps(run(Mission("neumann-11-46", 11, 46)), indent=2))
