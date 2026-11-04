# Neumann Mission Core

Open-source experimental mathematics kernel for the **Neumann missie software uitwerking** project.

## Run (Python 3.10+, no dependencies)

```sh
python -m neumann
python -m unittest discover -s tests -v
```

## Status

The rational-expansion engine is exact and tested. It tracks long-division remainders to preserve the distinction between positional phase and digit index. `carry_sum` provides an explicit carry primitive for bounded digit groups.

**Not yet implemented:** the project's proposed base-rotation scheduler (binary → decimal → hexadecimal → binary), overlap/backtracking, adaptive group widths, probe communications, consensus, safety logic or hardware control. The switching algorithm's cross-base alignment and width-update rules must be specified and tested before implementation. No performance or mission-readiness claims are made.

## Proposed next milestones

1. Formalize a base-independent phase identifier using rational remainder states.
2. Implement configurable carry-triggered rotation and one-position overlap, logging all transitions.
3. Compare rotation against fixed-base controls, testing determinism, periodicity and failure recovery.
4. Prototype a deterministic, auditable *simulation-only* probe-task scheduler.

## License

MIT. See LICENSE.

## Period-family research (new)

`neumann/periods.py` implements exact multiplicative orders for `p/(2*(2*p+1))`, normalized ratio families, candidate middle-base selection and a **bounded demonstration rotor**. The rotor is explicitly **not** the proposed carry/backtracking algorithm: its phase transition is a deterministic toy baseline for repeat-detection tests. Bases 2 and 16 are fixed anchors. The candidate selector permits 6, 8 and 10, as well as other valid bases; a matching period family does not establish correct carry behavior.

Run the full test suite with `python -m unittest discover -s tests -v`.

## Exact synchronization experiments (v0.3)

`neumann/sync.py` adds `plan(p, middle)`, `select(p, candidates=(6,8,10), criterion='balanced')`, and `digit_remainder(p,base,index)`. The selection minimizes period imbalance (or common LCM horizon), using only exact integer arithmetic. For `p=11`, base 6 and 8 produce equal periods `(11,11,11)`; for `p=29`, base 8 yields `(58,58,29)` with LCM 58. An LCM of digit-index periods is **not** proof that positions in different bases represent the same fractional location, nor that the carry/backtracking rotor has returned to the same state. Full carry-transition rules remain to be implemented.

## Weekproef 01 · exacte retourconversie

Een gesimuleerde sonde moet een rationale waarde kunnen lezen die een andere
sonde in een andere basis schrijft. De eerste proef test de rekenkern die
zo'n uitwisseling nodig heeft. Haakjes markeren het herhalende deel.

| Basis | Exacte weergave van 11/46 |
| --- | --- |
| 2 | `0.0(01111010011)` |
| 10 | `0.2(3913043478260869565217)` |
| 16 | `0.3(D37A6F4DE9B)` |

```sh
python -m unittest discover -s tests -p 'test_conversion.py' -v
```

`fraction_from_digits(base, integer, prefix, repetend)` leest losse velden
met hoofdletters. `convert(expansion, target_base)` rekent via een exacte
`Fraction` en geeft de canonieke doelrepresentatie terug. De retourproef
gebruikt vier rationale waarden, waaronder een eindige breuk en een getal
groter dan één. Elke tussenrepresentatie moet exact de invoerwaarde opleveren.
De laatste binaire representatie moet identiek zijn aan de eerste.

De proef controleert waarde-identiteit. Een protocol voor berichten,
uitlijning van rotorfasen en carry/overlap blijven open ontwerpvragen.

**Hervatpunt** — voeg bij `tests/test_conversion.py` één proef toe waarin twee
gesimuleerde lezers hetzelfde opgeslagen breukbericht onafhankelijk afspelen
en exact dezelfde rationale waarde terugvinden. Leg eerst het minimale
berichtformaat vast met velden voor basis, geheel deel, prefix en repetend.

Bijdragen kan met een tegenvoorbeeld en de verwachte breuk, of met een
kleine patch en een herhaalbare test. Python 3.10+ volstaat.
