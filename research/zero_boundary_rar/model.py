"""Zero-boundary RAR candidate model.

This module implements the candidate law derived in
ideas/zero-boundary-rar-derivation-v02.md.

It is a research hypothesis, not established physics.
"""

from __future__ import annotations

import math

C = 299_792_458.0  # m/s
MPC_M = 3.085677581491367e22


def boundary_coordinate(g_bar: float, a0: float) -> float:
    """x = sqrt(g_bar/a0)."""
    if g_bar < 0 or a0 <= 0:
        raise ValueError("Require g_bar >= 0 and a0 > 0")
    return math.sqrt(g_bar / a0)


def partition_factor(x: float) -> float:
    """Z_+(x) = 1/(1-exp(-x)), evaluated stably."""
    if x < 0:
        raise ValueError("Require x >= 0")
    if x == 0:
        return math.inf
    return -1.0 / math.expm1(-x)


def g_effective(g_bar: float, a0: float) -> float:
    """Candidate effective acceleration in m/s^2.

    For exactly g_bar=0 the continuous limiting value is 0.
    """
    if g_bar < 0 or a0 <= 0:
        raise ValueError("Require g_bar >= 0 and a0 > 0")
    if g_bar == 0:
        return 0.0
    x = boundary_coordinate(g_bar, a0)
    return g_bar * partition_factor(x)


def deep_limit(g_bar: float, a0: float) -> float:
    """Leading deep-boundary/MOND asymptote sqrt(a0*g_bar)."""
    if g_bar < 0 or a0 <= 0:
        raise ValueError("Require g_bar >= 0 and a0 > 0")
    return math.sqrt(a0 * g_bar)


def deep_series_through_3half(g_bar: float, a0: float) -> float:
    """Small-g expansion through O(g_bar^(3/2))."""
    if g_bar < 0 or a0 <= 0:
        raise ValueError("Require g_bar >= 0 and a0 > 0")
    if g_bar == 0:
        return 0.0
    return (
        math.sqrt(a0 * g_bar)
        + 0.5 * g_bar
        + (g_bar ** 1.5) / (12.0 * math.sqrt(a0))
    )


def high_limit_ratio(g_bar: float, a0: float) -> float:
    """g_eff/g_bar; tends to 1 at high acceleration."""
    if g_bar <= 0:
        raise ValueError("Require g_bar > 0")
    return g_effective(g_bar, a0) / g_bar


def hubble_si(H_km_s_Mpc: float) -> float:
    """Convert km/s/Mpc to s^-1."""
    if H_km_s_Mpc <= 0:
        raise ValueError("Require H > 0")
    return H_km_s_Mpc * 1000.0 / MPC_M


def a0_hubble(H_km_s_Mpc: float) -> float:
    """Candidate H-branch a0 = c H / (2*pi). Not established physics."""
    return C * hubble_si(H_km_s_Mpc) / (2.0 * math.pi)


def E_flat_lcdm(z: float, omega_m: float = 0.315, omega_lambda: float = 0.685) -> float:
    """H(z)/H0 for a flat matter+Lambda background, neglecting radiation."""
    if z < 0:
        raise ValueError("Require z >= 0")
    if omega_m < 0 or omega_lambda < 0:
        raise ValueError("Density parameters must be non-negative")
    return math.sqrt(omega_m * (1.0 + z) ** 3 + omega_lambda)


def a0_evolving_from_local(
    z: float,
    a0_local: float,
    omega_m: float = 0.315,
    omega_lambda: float = 0.685,
) -> float:
    """H-branch prediction a0(z)=a0(0)*H(z)/H0.

    This is a falsifiable candidate branch, not a derived cosmological law.
    """
    if a0_local <= 0:
        raise ValueError("Require a0_local > 0")
    return a0_local * E_flat_lcdm(z, omega_m, omega_lambda)


if __name__ == "__main__":
    a0 = 1.2e-10
    samples = [1e-8, 1e-10, 1e-12, 1e-14]
    print("g_bar [m/s^2]      g_eff             deep-limit         ratio")
    for g in samples:
        ge = g_effective(g, a0)
        gd = deep_limit(g, a0)
        print(f"{g: .3e}        {ge: .3e}        {gd: .3e}        {ge/g: .6g}")

    print("\nH-branch illustrative a0(z), normalized to local a0=1.2e-10:")
    for z in (0.0, 0.5, 1.0, 1.5):
        print(f"z={z:3.1f}: {a0_evolving_from_local(z, a0):.3e} m/s^2")
