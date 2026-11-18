"""Deep numeric tests for sections 29-38 of the note.

Lattice point of the observer, quintessence, entropy consistency and the
area law of section 38 (the one main.tex cites as
test_shannon_bit_against_the_area_law).

The bodies of sections 29, 30, 32, 34, 36, 37 and 38 live here now
(SPEC-002 §1): every number this module used to read back from a
section's stdout is asserted on its value, produced by the migrated
functions below.  No test of this file runs a section any more.
"""

from __future__ import annotations

import math
from decimal import Decimal, localcontext
from functools import lru_cache
from typing import Any

import numpy as np
import pytest
from scipy.integrate import solve_ivp
from scipy.linalg import eigh
from scipy.optimize import brentq
from scipy.special import j0, jn_zeros, y0

from kkgt.constants import (
    C_LIGHT,
    G_NEWTON,
    HBAR,
    LN_PHI,
    M_GEV,
    M_PLANCK_GEV,
    M_PCF,
    MPC_M,
    PHI,
)

LP2 = HBAR * G_NEWTON / C_LIGHT**3          # Planck length squared, m^2
H100 = 100e3 / MPC_M                        # h = 100 km/s/Mpc in s^-1


def omega_l_required(level: int) -> float:
    """Omega_L h^2 needed to place Lambda at the level `level` (section 29/32)."""
    lam = 3 * PHI ** -level / LP2
    return lam * C_LIGHT**2 / (3 * H100**2)


# ═══════════════════════ migrated bodies of sections 29-38 (SPEC-002 §1) ══
def planck_like(omega_m: float, d_omega_m: float, h0: float, d_h0: float,
                correlation: float) -> tuple[float, float]:
    """Omega_L h^2 and its 1-sigma error from one (Omega_m, H0) row.

    Section 32's ``det``: the flatness relation with the correlation of
    the two bounds of Planck 2018 or of DESI DR2 + CMB.
    """
    h, dh = h0 / 100, d_h0 / 100
    a = -h * h * d_omega_m
    b = 2 * (1 - omega_m) * h * dh
    return (1 - omega_m) * h * h, math.sqrt(a * a + b * b + 2 * a * b * correlation)


def level_read_from(omega_l: float, sigma_omega_l: float) -> tuple[float, float, int, float]:
    """The level a measured Omega_L h^2 reads off, and its distance to a lattice point.

    ``(level, 1-sigma of the level, nearest integer, distance to it in
    sigmas)`` -- sections 29 and 32 print exactly these four numbers.
    """
    level = 584 - math.log(omega_l / omega_l_required(584)) / LN_PHI
    sigma = sigma_omega_l / omega_l / LN_PHI
    nearest = round(level)
    return level, sigma, nearest, abs(level - nearest) / sigma


def half_last_digit(printed: str) -> float:
    """Half a unit of the last digit of a ``%.1e`` print, e.g. ``9.1e-05``."""
    return 0.5 * 10 ** (int(printed.split("e")[1]) - 1)


def planck_window_statements() -> None:
    """Section 29's own claims: H0 from flatness and the 1.4-1.8 sigma window.

    The section asserted ``1.3 < min(ten) < 1.5 and 1.7 < max(ten) < 1.9``
    on the two correlations of Omega_m and H_0 and printed the range as
    ``Planck and the combination agree (1.4-1.8 sigma)``; both now fail
    here, on their values (SPEC-002 §1).
    """
    omega_l = omega_l_required(584)
    # with omega_m = 0.143 +- 0.0011 and flatness: H0 = 66.01 +- 0.08
    root = math.sqrt(omega_l + 0.1430)
    assert round(100 * root, 2) == 66.01, root
    assert round(100 * 0.5 * 0.0011 / root, 2) == 0.08, root
    desi, desi_sigma = planck_like(0.3027, 0.0036, 68.17, 0.28, -0.975)
    tensions = []
    for correlation in (0.0, -1.0):
        planck, planck_sigma = planck_like(0.3153, 0.0073, 67.36, 0.54, correlation)
        tensions.append((desi - planck) / math.hypot(desi_sigma, planck_sigma))
    assert 1.3 < min(tensions) < 1.5, tensions
    assert 1.7 < max(tensions) < 1.9, tensions
    assert (round(min(tensions), 1), round(max(tensions), 1)) == (1.4, 1.8), tensions


def level_lattice_shape_statements() -> None:
    """Every row section 32 printed: Omega_L h^2, level, sigma, integer, distance.

    Six rows (five cases of the table plus the local H0 reading), each
    asserted with the half unit of the digit the section printed it with.
    """
    rows = [
        ((0.3153, 0.0073, 67.36, 0.54, 0.0), (0.3107, 0.0060, 583.877, 0.040, 584, 3.1)),
        ((0.3153, 0.0073, 67.36, 0.54, -1.0), (0.3107, 0.0083, 583.877, 0.055, 584, 2.2)),
        ((0.3027, 0.0036, 68.17, 0.28, -1.0), (0.3240, 0.0043, 583.789, 0.028, 584, 7.6)),
        ((0.3027, 0.0036, 68.17, 0.28, -0.975), (0.3240, 0.0043, 583.789, 0.028, 584, 7.6)),
        ((0.3027, 0.0036, 68.17, 0.28, 0.0), (0.3240, 0.0031, 583.789, 0.020, 584, 10.5)),
    ]
    for case, printed in rows:
        omega_l, sigma_omega_l = planck_like(*case)
        level, sigma, nearest, distance = level_read_from(omega_l, sigma_omega_l)
        want_omega, want_sigma, want_level, want_sigma_level, want_nearest, want_distance = printed
        assert round(omega_l, 4) == want_omega, case
        assert round(sigma_omega_l, 4) == want_sigma, case
        assert round(level, 3) == want_level, case
        assert round(sigma, 3) == want_sigma_level, case
        assert nearest == want_nearest, case
        assert round(distance, 1) == want_distance, case
    # the row the local value of H0 reads
    omega_l = 0.7304 ** 2 - 0.1430
    sigma_omega_l = math.hypot(2 * 0.7304 * 0.0104, 0.0011)
    level, sigma, nearest, distance = level_read_from(omega_l, sigma_omega_l)
    assert (round(omega_l, 4), round(sigma_omega_l, 4)) == (0.3905, 0.0152)
    assert (round(level, 3), round(sigma, 3)) == (583.402, 0.081)
    assert (nearest, round(distance, 1)) == (583, 5.0)


def vector_roots(depth: float) -> list[float]:
    """Zeros of ``J0(eps x) Y0(x) - Y0(eps x) J0(x)`` at the depth ``depth``.

    The two-brane vector equation of sections 30 and 37, with
    ``eps = phi^-depth`` (the depth is all it depends on).
    """
    epsilon = PHI ** -depth

    def equation(x: Any) -> Any:
        return j0(epsilon * x) * y0(x) - y0(epsilon * x) * j0(x)

    grid = np.linspace(0.5, 15, 6000)
    values = equation(grid)
    return [brentq(equation, float(grid[i]), float(grid[i + 1]))
            for i in range(len(grid) - 1) if values[i] * values[i + 1] < 0]


def vector_ratio(depth: float) -> float:
    """m2/m1 of the vector tower at the depth ``depth`` (section 37)."""
    roots = vector_roots(depth)
    return roots[1] / roots[0]


def cpl_projection(omega_m: float) -> tuple[float, float, float]:
    """``(w(0), w0, wa)`` of the ring quintessence fitted over z < 2 (section 34)."""
    lam = 1 / math.sqrt(2)

    def evolution(y_initial: float, n0: float = -8.0) -> Any:
        def equations(n: float, state: np.ndarray) -> list[float]:
            x, y = state
            total = 2 * x * x + (1 - x * x - y * y)
            return [-3 * x + lam * np.sqrt(6) / 2 * y * y + 1.5 * x * total,
                    -lam * np.sqrt(6) / 2 * x * y + 1.5 * y * total]

        return solve_ivp(equations, [n0, 0.0], [0.0, y_initial],
                         dense_output=True, rtol=1e-10, atol=1e-13)

    initial = brentq(
        lambda y: sum(v * v for v in evolution(y).y[:, -1]) - (1 - omega_m),
        1e-8, 1e-1,
    )
    solution = evolution(initial)
    z = np.linspace(0, 2, 400)
    n = -np.log(1 + z)
    x, y = solution.sol(n)
    w = (x * x - y * y) / (x * x + y * y)
    a = 1 / (1 + z)
    weight = x * x + y * y
    design = np.vstack([np.ones_like(a), 1 - a]).T * weight[:, None]
    w0, wa = np.linalg.lstsq(design, w * weight, rcond=None)[0]
    return float(w[0]), float(w0), float(wa)


def orbit_errors(step: float, samples: int) -> tuple[float, float]:
    """``(connected-part error, mean of the rest over its rms)`` of the tower orbit.

    Section 36 compares the phase ``log(phi)/2pi`` against the rational
    ``13/8`` on ``f(t) = e^{cos 2pi t}`` and ``g(t) = e^{2 cos 2pi t + 0.5 sin 4pi t}``.
    """

    def f(t: np.ndarray) -> np.ndarray:
        return np.exp(np.cos(2 * np.pi * t))

    def g(t: np.ndarray) -> np.ndarray:
        return np.exp(2 * np.cos(2 * np.pi * t) + 0.5 * np.sin(4 * np.pi * t))

    grid = np.arange(1 << 16) / (1 << 16)
    ff, gg = f(grid), g(grid)
    population = (ff * gg).mean()
    connected = population - ff.mean() * gg.mean()
    t = (np.arange(samples) * step) % 1
    x, y = f(t), g(t)
    residual = x * y - population
    error = abs((x * y).mean() - x.mean() * y.mean() - connected) / connected
    return float(error), float(abs(residual.mean()) / np.sqrt((residual * residual).mean()))


@lru_cache(maxsize=1)
def w2_partition_counts() -> tuple[int, ...]:
    """``pp[n]`` of section 37: the counting that grows as e^S (up to n = 3000)."""
    limit = 3000
    divisor_sum = [0] * (limit + 1)
    for d in range(1, limit + 1):
        for k in range(d, limit + 1, d):
            divisor_sum[k] += d
    counts = [0] * (limit + 1)
    counts[0] = 1
    for n in range(1, limit + 1):
        counts[n] = 3 * sum(divisor_sum[k] * counts[n - k] for k in range(1, n + 1)) // n
    return tuple(counts)


@lru_cache(maxsize=1)
def w2_cumulative_counts() -> tuple[int, ...]:
    """Prefix sums of ``w2_partition_counts`` (the states with L0 <= N/2)."""
    total = 0
    out = [0]
    for value in w2_partition_counts():
        total += value
        out.append(total)
    return tuple(out)


def w2_integer_dimension(sigma: int) -> int:
    """Integer dimension of level ``sigma``: states with L0 <= N/2 (section 37)."""
    return w2_cumulative_counts()[math.floor(PHI ** (2 * sigma) / 2) + 1]


def w2_log_slope() -> float:
    """``a`` of the fit ``lnD = a S + b ln L + c`` over sigma = 3..9 (section 37)."""
    cumulative = w2_cumulative_counts()
    x, y, z = [], [], []
    for sigma in range(1, 10):
        largest = math.floor(PHI ** (2 * sigma) / 2)
        x.append(math.pi * PHI ** sigma)
        y.append(math.log(cumulative[largest + 1]))
        z.append(math.log(largest))
    design = np.vstack([x, z, np.ones(len(x))]).T[2:]
    return float(np.linalg.lstsq(design, np.array(y[2:]), rcond=None)[0][0])


def cardy_log_slope() -> float:
    """``a`` of ``ln W + (3/2) ln L0 = a S + b`` in nats, over sigma = 3..9 (section 37)."""
    counts = w2_partition_counts()
    x, y = [], []
    for sigma in range(3, 10):
        largest = round(PHI ** (2 * sigma) / 2)
        x.append(math.pi * math.sqrt(2 * largest))
        y.append(math.log(counts[largest]) + 1.5 * math.log(largest))
    return float(np.polyfit(x, y, 1)[0])


def minimum_distance_to_an_integer() -> tuple[Decimal, int]:
    """Closest approach of ``e^{S/n}`` to an integer, in 60 digits (section 37).

    Returns the distance and the number of the ``sigma = 0..12, n = 1..40``
    cases below ``10^40``, where 60 digits still resolve the fraction.
    """
    with localcontext() as ctx:
        ctx.prec = 60
        pi = Decimal("3.14159265358979323846264338327950288419716939937510582097494459")
        phi = (1 + Decimal(5).sqrt()) / 2
        values = [(pi * phi ** sigma / n).exp()
                  for sigma in range(13) for n in range(1, 41)]
        values = [v for v in values if v < Decimal(10) ** 40]
        return min(abs(v - v.to_integral_value()) for v in values), len(values)


def measure_spectrum(power: float) -> list[float]:
    """``m_k/m_1`` of the chain with the measure ``e^{power A}`` (section 37)."""
    q, lo, hi, n = 32, -6, 6, 5
    h = LN_PHI / q
    w = np.arange(lo * q, hi * q + 1) / q * LN_PHI
    weight = np.exp(-power * (w[:-1] + w[1:]) / 2)
    size = len(w)
    stiffness = np.zeros((size, size))
    for i in range(size - 1):
        coupling = weight[i] / h ** 2
        stiffness[i, i] += coupling
        stiffness[i + 1, i + 1] += coupling
        stiffness[i, i + 1] -= coupling
        stiffness[i + 1, i] -= coupling
    r = np.exp(-2 * w)
    r[0] /= 2
    r[-1] /= 2
    masses = np.sqrt(np.clip(eigh(stiffness, np.diag(r), eigvals_only=True), 0, None))
    return list(masses[1:n + 1] / masses[1])


# ══════════════════════════════════════════════════════════ section 29 ══
class TestSection29LatticePointFromOmegaLambda:
    """section 29 -- 'What fixes the lattice point: Omega_Lambda h^2'"""

    @staticmethod
    def planck(r: float, h=0.6736, dh=0.0054, om=0.3153, dom=0.0073):
        a, b = -h * h * dom, 2 * (1 - om) * h * dh
        return (1 - om) * h * h, math.sqrt(a * a + b * b + 2 * a * b * r)

    def test_required_omega_at_level_584(self):
        # half the last digit of the six-significant-figure print
        assert 3 * PHI**-584 == pytest.approx(2.68126e-122, abs=5e-128)
        assert round(omega_l_required(584), 4) == 0.2928

    @pytest.mark.parametrize("r,dp,tension", [(0.0, 0.0060, -3.0),
                                              (-1.0, 0.0083, -2.2)])
    def test_planck_tension(self, r, dp, tension):
        """Omega_L h^2 = 0.3107 +- dp; level 584 sits `tension` sigma away."""
        p, sigma = self.planck(r)
        assert round(p, 4) == 0.3107
        assert round(sigma, 4) == dp
        ol = omega_l_required(584)
        assert round((ol - p) / sigma, 1) == tension

    def test_the_planck_level_is_2_2_to_3_1_sigma_from_584(self):
        """main.tex L2024-2025: Planck's level 583.877 sits 2.2 (r = -1) to
        3.1 (r = 0) standard deviations from 584 as the correlation of
        Omega_m and H_0 runs from -1 to 0 (section 29 prints both).

        One node rather than a parametrised pair: the manuscript cites this
        test by name, and a parametrised id carries its parameters.

        The two numbers used to be read back from the stdout of section 29
        (``Planck only, r = ...: level ..., ... sigma from 584``); they are
        asserted on their values here (SPEC-002 §1), with the section's own
        print precision -- three decimals for the level, one for the sigma.
        """
        ol = omega_l_required(584)
        for r, printed in [(-1.0, 2.2), (0.0, 3.1)]:
            p, dp = self.planck(r)
            level = 584 + math.log(ol / p) / LN_PHI
            dist = (584 - level) * p * LN_PHI / dp     # in units of the level sigma
            assert round(level, 3) == 583.877, (r, level)
            assert round(dist, 1) == printed, (r, dist)

    @pytest.mark.parametrize("r,ten", [(0.0, 1.81), (-1.0, 1.43)])
    def test_desi_against_planck(self, r, ten):
        """DESI DR2 + CMB (0.3240 +- 0.0043) agrees with Planck at 1.4-1.8 sigma."""
        p, sigma = self.planck(r)
        p_d, dp_d = 0.3240, 0.0043
        got = (p_d - p) / math.hypot(dp_d, sigma)
        assert round(got, 2) == ten, (r, got)

    def test_the_script_asserts_the_window_it_quotes(self):
        """Section 29 asserted its own window and printed it; both live here.

        ``planck_window_statements`` carries the section's claim -- the two
        tensions must sit in 1.4-1.8 sigma -- recomputed from the Planck and
        DESI rows instead of read back from stdout (SPEC-002 §1).
        """
        planck_window_statements()
        assert 1.3 < 1.43 < 1.5 and 1.7 < 1.81 < 1.9

    def test_sensitivity_and_arithmetic(self):
        assert round(-2 / LN_PHI, 3) == -4.156
        assert round(0.02 / LN_PHI, 3) == 0.042
        assert 584 % 24 == 8
        assert 584 == 2**3 * 73


# ══════════════════════════════════════════════════════════ section 30 ══
class TestSection30SymmetricThroat:
    """section 30 -- 'The symmetric throat [-12, 12] and the UV scale'"""

    def test_depth_of_the_clock(self):
        assert round(24 * LN_PHI, 2) == 11.55

    @pytest.mark.parametrize("level,printed",
                             [(12, 101.06), (36, 1.048e7)])
    def test_scales(self, level, printed):
        m = M_GEV
        got = m * PHI**level
        if printed > 1e5:
            # 1.048e+07 is printed to four significant figures: half a unit
            # of its last digit is 5e3
            assert got == pytest.approx(printed, abs=5e3)
        else:
            assert got == pytest.approx(printed, abs=5e-3)

    def test_vector_ratio_range(self):
        """2.228 (symmetric) against 2.275 (Planck top): inside the observed band.

        The band is the gluon candidates of section 1, 8600/(4000..3600);
        2.275 is the quotient of the two vector zeros that
        test_vector_zeros_against_the_lyr_table pins at four decimals, and
        2.228 is the same quotient at the depth phi^24, as section 37
        prints it for the symmetric window.  The quotient used to be read
        from the stdout of section 37; ``vector_ratio`` computes it here
        (SPEC-002 §1), at the three decimals the section printed.
        """
        low, high = 8600 / 4000, 8600 / 3600
        assert (low, high) == pytest.approx((2.15, 2.39), abs=5e-3)
        vec = [2.4448, 5.5615, 8.6958]   # from test_vector_zeros_against_the_lyr_table
        planck_top = vec[1] / vec[0]
        assert planck_top == pytest.approx(2.275, abs=5e-4)
        symmetric = vector_ratio(24)
        assert round(symmetric, 3) == 2.228, symmetric
        assert low <= symmetric <= high, symmetric
        assert low <= planck_top <= high, planck_top

    def test_the_top_of_the_clock_is_the_printed_39_33(self):
        """main.tex L2108: the depth-24 clock tops out at 39.33 (AUD-001).

        Class b, cited to test_depth_of_the_clock, test_scales and
        test_vector_ratio_depends_only_on_the_depth; the figure lives in
        the label section 30 prints (section 1 computes the same 39.33).
        Section 30 printed the number as a label; it is the reading
        ``k pi r = log(M_Pl / M phi^12)`` of the two-brane top, so the
        test computes it instead of asking the section for its stdout
        (SPEC-002 §1), at the two decimals the section printed.
        """
        top = math.log(M_PLANCK_GEV / (M_GEV * PHI**12))
        assert round(top, 2) == 39.33, top


# ══════════════════════════════════════════════════════════ section 31 ══
class TestSection31ModuliMetric:
    """section 31 -- 'The moduli metric of the ring and the conjectures'"""

    def test_canonical_slope(self):
        d = math.sqrt(2) * LN_PHI
        assert d == pytest.approx(0.6805, abs=5e-5)
        assert LN_PHI / d == pytest.approx(0.7071, abs=5e-5)   # = 1/sqrt2

    def test_tcc_bound_is_not_met(self):
        """slope 0.7071 < sqrt(2/3) = 0.8165: the contrast fails here."""
        slope = LN_PHI / (math.sqrt(2) * LN_PHI)
        bound = math.sqrt(2 / 3)
        assert bound == pytest.approx(0.8165, abs=5e-5)
        assert slope < bound

    @pytest.mark.parametrize("k,holds", [(0.5, True), (0.75, True), (1.0, False)])
    def test_condition_on_the_moduli_kinetic_term(self, k, holds):
        """With K = -k ln Im tau the slope is 1/sqrt(2k); the bound holds iff k <= 3/4."""
        slope = 1 / math.sqrt(2 * k)
        assert (slope >= math.sqrt(2 / 3)) == holds, k

    @pytest.mark.parametrize("n,printed", [(2, 1.4), (12, 8.2), (584, 397.4)])
    def test_canonical_distance_along_the_tower(self, n, printed):
        got = math.sqrt(2) * n * LN_PHI
        assert round(got, 1) == printed, (n, got)

    @pytest.mark.parametrize("s", [2, 12, 100])
    def test_the_two_scales_have_unit_norm(self, s):
        assert PHI**s * PHI**-s == pytest.approx(1.0, abs=1e-12)


# ══════════════════════════════════════════════════════════ section 32 ══
class TestSection32LevelVersusGridShape:
    """section 32 -- 'The level read off the observer against the lattice shape'"""

    @pytest.mark.parametrize("level,printed",
                             [(583, 0.4737), (584, 0.2928), (585, 0.1809)])
    def test_required_omega_per_level(self, level, printed):
        assert round(omega_l_required(level), 4) == printed

    def test_levels_are_one_phi_apart(self):
        """Consecutive levels differ by the factor phi in Omega_L h^2."""
        r584 = omega_l_required(584)
        assert omega_l_required(583) / r584 == pytest.approx(PHI, rel=1e-9)
        assert r584 / omega_l_required(585) == pytest.approx(PHI, rel=1e-9)

    def test_the_worst_case_is_deci(self):
        """DESI r = -1 reads the level at 7.6 sigma from every integer.

        The three rows section 32 printed its decision on -- the DESI worst
        case, Planck at r = 0 and the local H0 reading -- are asserted on
        their values now instead of on their printed labels (SPEC-002 §1);
        ``level_lattice_shape_statements`` carries the whole table.
        """
        # "DESI DR2 + CMB, LCDM, r = -1 (worst case)": integer 584 at 7.6 sigma
        _level, _sigma, nearest, distance = level_read_from(
            *planck_like(0.3027, 0.0036, 68.17, 0.28, -1.0)
        )
        assert (nearest, round(distance, 1)) == (584, 7.6), distance
        # "Planck 2018, LCDM, r = 0": integer 584 at 3.1 sigma
        _level, _sigma, nearest, distance = level_read_from(
            *planck_like(0.3153, 0.0073, 67.36, 0.54, 0.0)
        )
        assert (nearest, round(distance, 1)) == (584, 3.1), distance
        # "H0 local with omega_m from Planck": integer 583 at 5.0 sigma
        local = 0.7304 ** 2 - 0.1430, math.hypot(2 * 0.7304 * 0.0104, 0.0011)
        _level, _sigma, nearest, distance = level_read_from(*local)
        assert (nearest, round(distance, 1)) == (583, 5.0), distance

    def test_the_criterion(self):
        """A level read 3 sigma or more from every integer rules out the lattice shape.

        Section 32 printed that criterion under its table; the table is
        asserted here row by row (SPEC-002 §1) and the deciding row is the
        one that has to clear the 3-sigma bar.
        """
        level_lattice_shape_statements()
        # the nearest integer is the closest one, so 3 sigma from it is
        # 3 sigma or more from every integer of the lattice
        _level, _sigma, _nearest, worst = level_read_from(
            *planck_like(0.3027, 0.0036, 68.17, 0.28, -1.0)
        )
        assert worst >= 3, worst
        assert round(worst, 1) == 7.6, worst

    def test_the_worst_case_level_is_583_789_plus_or_minus_0_028(self):
        """main.tex L2028/L2330: 583.789 +- 0.028 at 7.6 sigma from 584.

        AUD-001 L2028: the two figures lived in the tests' code without an
        assertion; section 32 prints them on the DESI worst-case row, with
        the ``.3f`` width (half a unit, 5e-4) each.  They come out of the
        row's own computation now, not out of a regex on its stdout
        (SPEC-002 §1).
        """
        level, sigma, nearest, distance = level_read_from(
            *planck_like(0.3027, 0.0036, 68.17, 0.28, -1.0)
        )
        assert level == pytest.approx(583.789, abs=5e-4), level
        assert sigma == pytest.approx(0.028, abs=5e-4), sigma
        assert (nearest, round(distance, 1)) == (584, 7.6), distance


# ══════════════════════════════════════════════════════════ section 33 ══
class TestSection33ColourHole:
    """section 33 -- 'The colour hole: the welded tension, Higuchi and the Regge scale'"""

    @pytest.mark.parametrize("q2,printed",
                             [(2 * math.pi, 0.9140), (1.0, 5.7429)])
    def test_welded_tension_is_level_independent(self, q2, printed):
        """sigma_t S = 4 pi^4/(q^2 M_PCF), the same at every level."""
        got = 4 * math.pi**4 / (q2 * M_PCF)
        assert round(got, 4) == printed, (q2, got)
        for s in (0, 5, 12):
            value = ((2 * math.pi) ** 2 / q2) * (math.pi / M_PCF) \
                * PHI**-s * math.pi * PHI**s
            assert value == pytest.approx(got, rel=1e-9), (q2, s)

    @pytest.mark.parametrize("q2,ratio,kappa",
                             [(2 * math.pi, 0.0727, 3.71), (1.0, 0.4570, 1.48)])
    def test_higuchi_bound(self, q2, ratio, kappa):
        got = math.pi**3 / (q2 * M_PCF)
        assert round(got, 4) == ratio
        assert round(1 / math.sqrt(got), 2) == kappa

    def test_higuchi_threshold_q(self):
        assert round(math.pi**3 / M_PCF, 4) == 0.4570

    def test_regge_masses_in_both_units(self):
        m = M_GEV
        u = m / M_PCF
        m_pl = M_PLANCK_GEV
        assert u / math.sqrt(M_PCF) == pytest.approx(5.616e-4, rel=5e-5)
        # 1.048e+18 to four significant figures: half a unit of the last
        # digit is 5e14
        assert (m_pl / math.sqrt(2)) / math.sqrt(M_PCF) == pytest.approx(
            1.048e18, abs=5e14
        )
        conv = 2 * math.log(m_pl / u) / LN_PHI - math.log(2) / LN_PHI
        assert round(conv, 2) == 203.56

    def test_graviton_modes_below_1000_tev(self):
        m = M_GEV
        mk = jn_zeros(1, 5000) * m * PHI**12
        count = int((mk < 1e6).sum())
        estimate = 1e6 / (math.pi * m * PHI**12)
        assert count == 3149
        assert round(estimate, 1) == 3149.9
        assert abs(count - estimate) < 1.0

    def test_first_mode(self):
        assert round(jn_zeros(1, 1)[0] * M_GEV * PHI**12, 1) == 387.2


# ══════════════════════════════════════════════════════════ section 34 ══
class TestSection34Quintessence:
    """section 34 -- 'The quintessence of the ring: lambda = 1/sqrt2 against the data'"""

    LAM = 1 / math.sqrt(2)

    def test_distance_to_the_measured_lambda(self):
        """DESI DR2 + CMB + DESY5: lambda = 0.698 +0.173/-0.202 (AAN 2024)."""
        c, up = 0.698, 0.173
        assert round((self.LAM - c) / up, 2) == 0.05
        assert round((math.sqrt(2 / 3) - c) / up, 2) == 0.68
        assert round((math.sqrt(2) - c) / up, 2) == 4.14

    @pytest.mark.parametrize("omega_m,w_at_0,w0,wa",
                             [(0.3, -0.923, -0.922, -0.114),
                              (0.31, -0.924, -0.924, -0.112),
                              (0.32, -0.926, -0.926, -0.110)])
    def test_cpl_projection(self, omega_m, w_at_0, w0, wa):
        """The background solution projected on w0+wa(1-a) over z < 2.

        ``cpl_projection`` integrates the ring quintessence and fits it
        here; the three numbers used to be matched against the stdout of
        section 34 (SPEC-002 §1).  They are compared at the three decimals
        the section printed them with.
        """
        got = cpl_projection(omega_m)
        assert tuple(round(v, 3) for v in got) == (w_at_0, w0, wa), (omega_m, got)


# ══════════════════════════════════════════════════════════ section 35 ══
class TestSection35HalfThreshold:
    """section 35 -- 'The 1/2 threshold: Fisher time, binary entropy, one bit per eigenvalue'"""

    @pytest.mark.parametrize(
        "f,ratio,entropy",
        [(0.25, 1.4142, 0.8113), (0.5, 1.0000, 1.0000), (1.0, 0.7071, 0.0000)],
    )
    def test_fisher_time_and_binary_entropy(self, f, ratio, entropy):
        got_ratio = 1 / math.sqrt(2 * f)
        got_entropy = -(f * math.log2(f) + (1 - f) * math.log2(1 - f)) \
            if 0 < f < 1 else 0.0
        assert round(got_ratio, 4) == ratio, f
        assert round(got_entropy, 4) == entropy, f

    @pytest.mark.parametrize("f", [0.1, 0.3, 0.5, 0.7, 0.9])
    def test_half_is_the_maximum(self, f):
        h = -(f * math.log2(f) + (1 - f) * math.log2(1 - f)) if 0 < f < 1 else 0.0
        assert h <= 1.0 + 1e-12
        if f != 0.5:
            assert h < 1.0


# ══════════════════════════════════════════════════════════ section 36 ══
class TestSection36BlackHoleWhereNeeded:
    """section 36 -- 'The black hole where needed: the orbit of the tower, the horizon of S(12), the threshold'"""

    def test_four_readings_of_s_of_12_agree(self):
        """Gibbons-Hawking, area/4G and Cardy all give pi phi^12 = 1011.58."""
        s = 12
        s_entropy = math.pi * PHI**s
        h = math.sqrt(2) * PHI ** (-s / 2)
        gh = math.pi / (0.5 * h * h)
        area = 2 * math.pi * PHI**s / 2
        cardy = 2 * math.pi * math.sqrt(3 * PHI ** (2 * s) / 12)
        assert round(s_entropy, 2) == 1011.58
        for other in (gh, area, cardy):
            assert other == pytest.approx(s_entropy, rel=1e-9), other

    def test_entropy_over_the_gh_temperature_grows_as_phi_to_the_three_sigma_over_two(self):
        """main.tex L2045-2046: S times the inverse Gibbons-Hawking temperature.

        S = pi phi^sigma (section 36) and T_GH ~ H = sqrt2 phi^{-sigma/2}
        (also section 36), so the ratio steps by phi^{3/2} per level; the
        claim is checked at s = 0, 12, 24.
        """
        def ratio(s):
            return math.pi * PHI**s / PHI ** (-s / 2)

        for s in (0, 12, 24):
            assert ratio(s + 1) / ratio(s) == pytest.approx(PHI**1.5, rel=1e-12), s

    def test_lambda_is_positive(self):
        assert 6 * PHI**-12 == pytest.approx(0.0186, abs=5e-5)

    @pytest.mark.parametrize("k,printed", [(0.1, 26), (0.05, 104), (0.01, 2610)])
    def test_black_hole_threshold(self, k, printed):
        """k/M_Pl in units of the first mode: the threshold in KK masses."""
        x1 = jn_zeros(1, 1)[0]
        assert round(1 / (x1 * k * k)) == printed, k

    def test_correlation_converges_only_for_the_irrational_step(self):
        """The tower step log(phi)/2pi equidistributes; 13/8 stalls at 1e-3.

        ``orbit_errors`` computes both columns section 36 printed -- the
        connected-part error and the mean of the rest over its rms -- for
        the three sample sizes, at the two significant figures the section
        used (SPEC-002 §1).
        """
        tower, rational = LN_PHI / (2 * math.pi), 13 / 8
        table = (
            (tower, (("2.9e-02", "1.1e-02"), ("3.0e-03", "1.8e-03"),
                     ("9.1e-05", "4.8e-05"))),
            (rational, (("2.9e-03", "5.6e-03"), ("6.8e-03", "2.4e-03"),
                        ("6.8e-03", "2.4e-03"))),
        )
        for step, rows in table:
            for samples, (want_connected, want_rest) in zip((100, 1000, 10000), rows):
                connected, rest = orbit_errors(step, samples)
                assert connected == pytest.approx(
                    float(want_connected), abs=half_last_digit(want_connected)
                ), (step, samples, connected)
                assert rest == pytest.approx(
                    float(want_rest), abs=half_last_digit(want_rest)
                ), (step, samples, rest)


# ══════════════════════════════════════════════════════════ section 37 ══
class TestSection37Consistency:
    """section 37 -- 'Consistency: entropy, modes and bits; depth; gluons; unit; 700/380'"""

    def test_entropy_modes_and_bits(self):
        s12 = math.pi * PHI**12
        assert round(s12, 2) == 1011.58
        assert int(s12) == 1011
        assert round(int(s12) * math.log(2), 1) == 700.8
        assert round(math.log(2), 4) == 0.6931

    @pytest.mark.parametrize("window,printed", [((-12, 12), 2.228), ((12, 36), 2.228)])
    def test_vector_ratio_depends_only_on_the_depth(self, window, printed):
        """m2/m1 of the vector tower at the depth of the window (section 37).

        ``vector_ratio`` solves the two-brane equation here; the quotient
        used to be read from the section's stdout (SPEC-002 §1), at the
        three decimals it printed.
        """
        lo, hi = window
        got = vector_ratio(hi - lo)
        assert round(got, 3) == printed, (window, got)

    @pytest.mark.parametrize("mass,printed", [(3600, 17.60), (4000, 17.82)])
    def test_gluon_background_level(self, mass, printed):
        """sigma = log_phi(m/(j_{0,1} M)) with M = 0.31384 GeV."""
        got = math.log(mass / (jn_zeros(0, 1)[0] * M_GEV)) / LN_PHI
        assert round(got, 2) == printed, (mass, got)
        # section 37 reads the same ladder from the proton third: it
        # printed "m_p/3 = 0.3128 GeV: sigma_IR = 11.98", a number no
        # stdout is left to carry (SPEC-002 §1)
        assert round(math.log(99.6 / 0.3128) / LN_PHI, 2) == 11.98

    def test_ratio_700_over_380_is_the_bessel_ratio(self):
        r = 700 / 380
        t = jn_zeros(1, 2)[1] / jn_zeros(1, 2)[0]
        e = r * math.hypot(20 / 700, 20 / 380)
        assert round(r, 4) == 1.8421
        assert round(t, 4) == 1.8309
        assert round(100 * (r / t - 1), 2) == 0.61
        assert round((r - t) / e, 2) == 0.10

    @pytest.mark.parametrize("d,printed", [(24, 257), (81.74, 247)])
    def test_first_gluon_at_the_background(self, d, printed):
        """The first vector zero at the background, in GeV (section 37).

        The section printed ``background 12, depth {d}: first gluon {n} GeV``
        with ``{:.0f}``; ``vector_roots`` produces the number here
        (SPEC-002 §1), rounded the same way.
        """
        first = vector_roots(d)[0]
        assert round(first * M_GEV * PHI**12) == printed, (d, first)

    def test_w2_integer_dimension(self):
        """W2 of main.tex: dim H = 1654, 3436182, 820599769985 at sigma = 3,4,5.

        The counting and the fit behind the printed row live in
        ``w2_integer_dimension`` and ``w2_log_slope`` now, instead of in
        the stdout of section 37 (SPEC-002 §1); the slope keeps the
        section's own 5e-5 window.
        """
        assert w2_integer_dimension(3) == 1654
        assert w2_integer_dimension(4) == 3436182
        assert w2_integer_dimension(5) == 820599769985
        assert w2_log_slope() == pytest.approx(0.9972, abs=5e-5)

    def test_cardy_slope_of_the_count(self):
        """ln W + (3/2) ln L0 = a S + b with a = 1.0010 (nats)."""
        assert cardy_log_slope() == pytest.approx(1.0010, abs=5e-5)

    def test_e_to_the_s_is_never_an_integer(self):
        """Gelfond-Schneider: e^(S/n) is at least 6.76e-05 away from an integer.

        ``minimum_distance_to_an_integer`` runs the 60-digit search of
        section 37 here; the section also asserted the distance stays
        above 1e-9 and counted the 497 cases below 10^40, and both are
        asserted with it (SPEC-002 §1).
        """
        distance, cases = minimum_distance_to_an_integer()
        assert cases == 497, cases
        assert distance > Decimal("1e-9"), distance
        # "minimum distance 6.76e-05": half a unit of the last digit
        assert float(distance) == pytest.approx(6.76e-05, abs=5e-08), distance

    @pytest.mark.parametrize(
        "measure,printed",
        [("e^{4A}", [1.0, 1.8308, 2.6545, 3.4757, 4.2954]),
         ("e^{6A}", [1.0, 1.9993, 2.9970, 3.9925, 4.9850])],
    )
    def test_the_measure_that_gives_the_spectrum(self, measure, printed):
        """The measure that gives the spectrum of J1 (and the one with no offset).

        ``measure_spectrum`` diagonalises the chain with the measure
        ``e^{power A}``; the ratios used to be parsed out of the stdout of
        section 37 (SPEC-002 §1), at the four decimals it rounded them to.
        """
        power = {"e^{4A}": 4.0, "e^{6A}": 6.0}[measure]
        got = [round(v, 4) for v in measure_spectrum(power)]
        assert got == printed, measure


# ══════════════════════════════════════════════════════════ section 38 ══
class TestSection38AreaLawHalf:
    """section 38 -- 'The 1/2 of (B1): area quantum, Fisher unit and Shannon bit'

    main.tex: "that would be $\\log2$ per area (test
    test_shannon_bit_against_the_area_law)".
    """

    G_N = 0.5
    A = 1 / (4 * 0.5)          # 1/(4 G_N) = 1/2 per ell^2

    def test_area_law(self):
        """0.5 per ell^2 = 0.25 per ell_P^2 (Bekenstein-Hawking 1/4)."""
        assert self.A == 0.5
        assert self.A / 2 == 0.25

    def test_shannon_bit_against_the_area_law(self):
        ln2 = math.log(2)
        assert round(ln2, 4) == 0.6931
        assert round(ln2 / (self.A / 2), 3) == 2.773      # per Planck area
        assert round(ln2 / self.A, 3) == 1.386            # per ell^2

    def test_area_per_unit_of_s(self):
        """One mode (one unit of S) is 2 ell^2 = 4 ell_P^2."""
        assert 1 / self.A == 2.0
        assert 2 / self.A == 4.0

    def test_section38_stdout(self):
        """The three lines section 38 printed, asserted on their values.

        Section 38 had no assert of its own: it printed the area law, the
        Shannon ratio and the area per unit of S, and this test read the
        first two back from its stdout.  The body of the section lives
        here now (SPEC-002 §1), at the print precision of each line; the
        name is the one tests/README records for it.
        """
        ln2 = math.log(2)
        # "area law: 0.5 per ell^2 = 0.25 per ell_P^2 ...; Shannon bit ln2 = 0.6931"
        assert (self.A, self.A / 2) == (0.5, 0.25)
        assert round(ln2, 4) == 0.6931
        # "one Shannon bit per Planck area ...: ratio 2.773; per ell^2: 1.386"
        assert round(ln2 / (self.A / 2), 3) == 2.773
        assert round(ln2 / self.A, 3) == 1.386
        # "area per unit of S (one mode): 2.0 ell^2 = 4.0 ell_P^2"
        assert (1 / self.A, 2 / self.A) == (2.0, 4.0)
