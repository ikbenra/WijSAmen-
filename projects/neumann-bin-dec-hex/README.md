# Neumann Bin–Dec–Hex prototype v0.2

**Experimental branch; not mission-ready.** Bases remain 2, 10, 16. Decimal is never replaced by octal.

This independent prototype provides exact rational representations, finite/repeating fractional expansions, reconstruction, modular multiplicative order and remainder-phase cursor switching. It is not integrated with the earlier Neumann mission-core v0.2/v0.3 packages.

Run `python -m unittest discover -s projects/neumann-bin-dec-hex -p 'test_*.py' -v` from the repository root. Python standard library only.

**Limitations:** Cursor accepts [0,1) only; phase equality is not time equality; switch picks the first matching target remainder; finite search caps can reject; no multi-probe scheduler, persistence, concurrency, physical device control or flight safety validation.

**Provenance:** adapted from the local independently tested `neumann_bin_dec_hex_core_v02.zip` prototype, 2026-11-05. The original package is preserved separately. No private corpus or identifying data included.

**Next:** review differences against original mission-core APIs before integration. Keep the exponent backloop exploration in a separate research fork.

## Bounded API contract check · 15 November 2026

`compare_mission_core.py` also checks every numerator from 0 through twice the
denominator, for denominators 1 through 31, in each of bases 2, 10 and 16.
This is 3,069 input triples, including repeated equivalent fractions. Both
APIs must reconstruct the input exactly and emit identical integer, prefix
and repeating digits. The test also decodes each API's digit fields through
the other API, mapping `cycle` to `repetend` and requiring a positive sign.
The existing 11/46 case remains as a separate regression.

The same script checks the explicit negative-value boundary with -5/6 and
-2. Candidate representations preserve the sign and exact value. The
mission-core expansion API rejects those values. This defines a boundary for
a future adapter. Cursor phase, timing, carry and overlap compatibility remain
open questions. Mission-core retains its nonnegative value contract.

Run from the repository root with the fixed reference available locally.

```sh
git fetch origin 41a2926962c3fb9f99d614db0d06efbd47d830f5
git worktree add --detach ../neumann-mission-reference 41a2926962c3fb9f99d614db0d06efbd47d830f5
PYTHONPATH=../neumann-mission-reference/projects/neumann-mission-core \
  python3 projects/neumann-bin-dec-hex/compare_mission_core.py -v
```

The shared-domain claim is limited to the tested input range.
