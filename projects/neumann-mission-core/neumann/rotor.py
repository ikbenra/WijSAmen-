"""Bounded experimental carry rotor. Not mission-control software."""
from dataclasses import dataclass
from math import gcd, lcm
from .periods import multiplicative_order as order

@dataclass(frozen=True)
class State:
    stage: int = 0
    position: int = 0
    width: int = 1
    middle: int = 10

def digit(p, base, position):
    denominator = 2*(2*p+1)
    remainder = p * pow(base, position, denominator) % denominator
    return (remainder * base) // denominator

def step(p, state, max_width=3, candidates=(6,8,10)):
    """Carry from two adjacent groups switches base and overlaps one digit.

    Position is a per-base phase, NOT an invariant cross-base digit coordinate.
    On hex->binary carry, group width increases, wrapping at max_width.
    """
    q = 2*p+1
    valid = tuple(b for b in candidates if gcd(b,q)==1)
    if not valid or max_width < 1:
        raise ValueError("invalid configuration")
    base = (2,state.middle,16)[state.stage]
    horizon = lcm(*(order(b,q) for b in (2,16,*valid)))
    def group(start):
        v = 0
        for j in range(state.width):
            v = v*base + digit(p,base,start+j)
        return v
    carry = group(state.position)+group(state.position+state.width) >= base**state.width
    if not carry:
        return State(state.stage,(state.position+1)%horizon,state.width,state.middle),False
    next_stage = (state.stage+1)%3
    width = 1+state.width%max_width if state.stage==2 else state.width
    middle = state.middle
    if state.stage==0:
        def score(b):
            periods=(order(2,q),order(b,q),order(16,q))
            return (max(periods)-min(periods),periods[1])
        ranked=sorted(valid,key=lambda b:(score(b),b))
        tied=[b for b in ranked if score(b)==score(ranked[0])]
        middle=tied[state.position%len(tied)]
    return State(next_stage,(state.position-1)%horizon,width,middle),True

def simulate(p, limit=100000, max_width=3):
    state=State()
    seen={}
    carries=0
    visited=set()
    for t in range(limit+1):
        if state in seen:
            return {"p":p,"transient":seen[state],"cycle":t-seen[state],
                    "steps":t,"carries":carries,"visited_stages":sorted(visited)}
        seen[state]=t
        visited.add(state.stage)
        state,carry=step(p,state,max_width)
        carries+=int(carry)
    return {"p":p,"cycle":None,"steps":limit,"carries":carries,
            "visited_stages":sorted(visited)}
