"""Multiplicative orders for the reduced denominator of p/[2(2p+1)]."""
from math import gcd

def multiplicative_order(base: int, modulus: int) -> int:
    if modulus < 2 or gcd(base, modulus) != 1:
        raise ValueError("base and modulus must be coprime; modulus >= 2")
    residue, count = base % modulus, 1
    while residue != 1:
        residue = residue * base % modulus
        count += 1
    return count

def periods_for_parameter(p: int, middle: int) -> tuple[int,int,int]:
    if p < 1 or middle < 2:
        raise ValueError("invalid p or middle")
    # gcd(p,2(2p+1)) = 1; the factor 2 contributes only a preperiod
    modulus = 2*p+1
    return tuple(multiplicative_order(b,modulus) for b in (2,middle,16))
