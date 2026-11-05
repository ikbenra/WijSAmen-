# Neumann Bin–Dec–Hex prototype v0.2

**Experimental branch; not mission-ready.** Bases remain 2, 10, 16. Decimal is never replaced by octal.

This independent prototype provides exact rational representations, finite/repeating fractional expansions, reconstruction, modular multiplicative order and remainder-phase cursor switching. It is not integrated with the earlier Neumann mission-core v0.2/v0.3 packages.

Run `python -m unittest discover -s projects/neumann-bin-dec-hex -p 'test_*.py' -v` from the repository root. Python standard library only.

**Limitations:** Cursor accepts [0,1) only; phase equality is not time equality; switch picks the first matching target remainder; finite search caps can reject; no multi-probe scheduler, persistence, concurrency, physical device control or flight safety validation.

**Provenance:** adapted from the local independently tested `neumann_bin_dec_hex_core_v02.zip` prototype, 2026-11-05. The original package is preserved separately. No private corpus or identifying data included.

**Next:** review differences against original mission-core APIs before integration. Keep the exponent backloop exploration in a separate research fork.
