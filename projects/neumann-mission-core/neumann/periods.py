"""Exact period families and bounded deterministic experimental base scheduler."""
from dataclasses import dataclass
from math import gcd


def multiplicative_order(base: int, modulus: int) -> int:
    """Smallest positive k with base**k == 1 (mod modulus)."""
    if modulus < 2 or gcd(base, modulus) != 1:
        raise ValueError('base and modulus must be coprime; modulus >= 2')
    residue, k = base % modulus, 1
    while residue != 1:
        residue = (residue * base) % modulus
        k += 1
    return k


def periods_for_parameter(p: int, middle: int = 10) -> tuple[int, int, int]:
    """Period lengths of p/(2*(2*p+1)) for bases 2,middle,16.

    Only middle bases coprime to the odd modulus 2*p+1 are supported.
    A factor of 2 in the denominator contributes a finite prefix, not a period.
    """
    if p < 1 or middle < 2 or gcd(middle, 2*p + 1) != 1:
        raise ValueError('p must be positive and middle coprime to denominator')
    modulus = 2*p + 1
    return tuple(multiplicative_order(b, modulus) for b in (2, middle, 16))


def normalized_family(periods: tuple[int, int, int]) -> tuple[int, int, int]:
    divisor = gcd(gcd(periods[0], periods[1]), periods[2])
    return tuple(v // divisor for v in periods)


def middle_candidates(p: int, bases=range(3, 17), target=(1, 2, 1)) -> list[int]:
    return [b for b in bases if gcd(b, 2*p+1) == 1
            and normalized_family(periods_for_parameter(p, b)) == target]

@dataclass(frozen=True)
class RotorState:
    cycle: int
    phase: int

class BoundedRotor:
    """Finite deterministic *experimental* schedule, not the carry algorithm.

    One cycle comprises exactly three stages: 2 -> middle -> 16.
    The phase is a bounded integer. Every transition is deterministic;
    consequently a state must eventually recur. This is a baseline for
    comparing a future carry-driven rotor, not a substitute for it.
    """
    def __init__(self, p: int, middle_sequence=(10, 8, 6), phase_modulus=256):
        if p < 1 or phase_modulus < 1 or not middle_sequence:
            raise ValueError('invalid rotor configuration')
        if any(gcd(b, 2*p+1) != 1 for b in middle_sequence):
            raise ValueError('middle bases must be coprime to denominator')
        self.p = p
        self.middle_sequence = tuple(middle_sequence)
        self.phase_modulus = phase_modulus

    def base(self, state: RotorState) -> int:
        slot = state.cycle % (3*len(self.middle_sequence))
        stage, index = slot % 3, slot // 3
        return (2, self.middle_sequence[index], 16)[stage]

    def step(self, state: RotorState) -> RotorState:
        base = self.base(state)
        # Explicit bounded toy transition; no claimed carry equivalence.
        return RotorState((state.cycle + 1) % (3*len(self.middle_sequence)),
                          (state.phase * base + 1) % self.phase_modulus)

    def find_repeat(self, max_steps=None):
        state = RotorState(0, 0)
        seen = {}
        limit = max_steps or (3*len(self.middle_sequence)*self.phase_modulus + 1)
        for step in range(limit):
            if state in seen:
                return seen[state], step - seen[state]
            seen[state] = step
            state = self.step(state)
        return None
