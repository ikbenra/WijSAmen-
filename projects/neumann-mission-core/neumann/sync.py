"""Exact period synchronization; no claim of cross-radix digit alignment."""
from dataclasses import dataclass
from math import gcd, lcm
from .periods import periods_for_parameter

@dataclass(frozen=True)
class SyncPlan:
    p: int
    middle: int
    periods: tuple[int, int, int]
    horizon: int
    repetitions: tuple[int, int, int]
    imbalance: int

def plan(p: int, middle: int) -> SyncPlan:
    a, b, c = periods_for_parameter(p, middle)
    h = lcm(a, b, c)
    return SyncPlan(p, middle, (a,b,c), h, (h//a,h//b,h//c),
                    max(a,b,c)-min(a,b,c))

def select(p: int, candidates=(6,8,10), criterion='balanced') -> list[SyncPlan]:
    """Rank coprime bases; ties favor shorter periods and lower base."""
    plans = [plan(p,b) for b in candidates if gcd(b,2*p+1)==1]
    if not plans:
        raise ValueError('no middle base coprime with 2p+1')
    if criterion == 'balanced':
        return sorted(plans,key=lambda x:(x.imbalance,x.horizon,sum(x.periods),x.middle))
    if criterion == 'horizon':
        return sorted(plans,key=lambda x:(x.horizon,x.imbalance,sum(x.periods),x.middle))
    raise ValueError('criterion must be balanced or horizon')

def digit_remainder(p: int, base: int, index: int) -> int:
    """Exact remainder after index digits of p/(2(2p+1)) in base."""
    if p < 1 or index < 0 or base < 2:
        raise ValueError('invalid parameter/base/index')
    denominator = 2*(2*p+1)
    return (p * pow(base,index,denominator)) % denominator
