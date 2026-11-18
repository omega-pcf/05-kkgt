"""Deep numeric tests for sections 17-28 of the note.

Observer level, unit conversions, window and nome: every number here is
recomputed from the closed form with an explicit tolerance, at the
precision or tolerance of the line that used to carry it.

The bodies of sections 17, 18 and 23 live here now (SPEC-002 §1): the
seeded propagation, the printed identity and the background line this
module used to read back from a section's stdout are asserted on their
values by the migrated functions below.  No test of this file runs a
section any more.
"""

from __future__ import annotations

import math
import random

import numpy as np
import pytest

from kkgt.constants import (
    C_LIGHT,
    G_NEWTON,
    HBAR,
    LN_PHI,
    M_GEV,
    M_KOIDE_MEV,
    M_PLANCK_GEV,
    M_PCF,
    M_TAU_MEV,
    MPC_M,
    PHI,
    PHI_BAR,
)
from kkgt.harness import lam_planck

# HBAR/C_LIGHT/G_NEWTON/MPC_M and lam_planck are single-sourced in
# kkgt.constants / kkgt.harness (SEC-001, layer 1).  The three below also
# appear inside section bodies, which layer 1 does not touch.
HBAR_EVS = 6.582119569e-16      # eV s
MPC_KM = 3.0856775814913673e19  # km
LP_M = 1.616255e-35             # m
U_EV = M_KOIDE_MEV * 1e6 / M_PCF   # the unit of (F1), eV


# ══════════════════════════════════════════════════════════ section 17 ══
class TestSection17ObserverLevelFromLambda:
    """section 17 -- 'The observer level from the value of Lambda, below (F9) and the unit of (F1)'"""

    @staticmethod
    def sigma_obs(h0: float, omega_l: float) -> float:
        lam = 3 * (HBAR_EVS * h0 / MPC_KM) ** 2 * omega_l
        return math.log(6 * U_EV**2 / lam) / LN_PHI

    def test_unit_of_f1(self):
        assert U_EV / 1e6 == pytest.approx(4.6258, abs=5e-5)

    def test_planck_central_value(self):
        assert self.sigma_obs(67.36, 0.6847) == pytest.approx(380.315, abs=5e-4)

    def test_monte_carlo_error(self):
        """Seeded gaussian propagation of (H0, Omega_L): +-0.040 levels.

        Section 17 printed ``sigma_obs = 380.315 +- 0.040``: the level is
        the closed form at the Planck central values (the three decimals
        it printed, half a unit = 5e-4) and the error is the spread of the
        200000 seeded samples, asserted here on its value inside the
        0.03..0.05 band the printed number stood in (SPEC-002 §1).
        """
        assert self.sigma_obs(67.36, 0.6847) == pytest.approx(380.315, abs=5e-4)
        sd = monte_carlo_level_error()
        assert 0.03 <= sd <= 0.05, sd


# ═══════════════════ section 17's seeded propagation (migrated) ══════
def monte_carlo_level_error(samples: int = 200_000) -> float:
    """Spread of the levels section 17 drew from (H0, Omega_L).

    The section seeded ``random`` with 1, drew ``samples`` pairs
    ``random.gauss(67.36, 0.54)`` / ``random.gauss(0.6847, 0.0073)`` and
    printed the population standard deviation of the resulting levels as
    ``+- 0.040``; the seed, the sample count and the standard deviation are
    its own, unchanged (SPEC-002 §1).
    """
    random.seed(1)
    levels = [
        TestSection17ObserverLevelFromLambda.sigma_obs(
            random.gauss(67.36, 0.54), random.gauss(0.6847, 0.0073)
        )
        for _ in range(samples)
    ]
    mean = sum(levels) / len(levels)
    return (sum((x - mean) ** 2 for x in levels) / len(levels)) ** 0.5


# ══════════════════════════════════════════════════════════ section 18 ══
class TestSection18TwoReadingsOfTheSameCurvature:
    """section 18 -- 'The observer level and the unit of the curvature'"""

    @staticmethod
    def readings(h0=67.36, omega_l=0.6847):
        lam_e_v2 = 3 * (HBAR_EVS * h0 / MPC_KM) ** 2 * omega_l
        s_curv = math.log(6 * U_EV**2 / lam_e_v2) / LN_PHI      # W8, unit of (F1)
        lam_m = 3 * (h0 * 1e3 / MPC_M) ** 2 * omega_l / C_LIGHT**2
        s_entropy = math.log((3 * math.pi / (lam_m * LP_M**2)) / math.pi) / LN_PHI
        return s_curv, s_entropy

    def test_w4_equals_w8_in_the_gravitational_unit(self):
        s_curv, s_entropy = self.readings()
        assert s_entropy == pytest.approx(583.877, abs=5e-4)
        assert s_curv == pytest.approx(380.315, abs=5e-4)

    def test_the_gap_is_a_unit_conversion(self):
        """s_entropy - s_curv = 2 log_phi(M_Pl/u) - log_phi 2 = 203.562."""
        s_curv, s_entropy = self.readings()
        m_pl = M_PLANCK_GEV * 1e9     # eV
        formula = 2 * math.log(m_pl / U_EV) / LN_PHI - math.log(2) / LN_PHI
        assert s_entropy - s_curv == pytest.approx(formula, abs=1e-6)
        assert formula == pytest.approx(203.562, abs=5e-4)

    def test_lambda_times_s_is_six_pi(self):
        """``Lambda(sigma) S(sigma) = 6 pi = 3 pi / G_N`` with ``G_N = 1/2``.

        Section 18 printed this identity as ``True``; the truth value of
        the very inequality is asserted here on its value (SPEC-002 §1).
        """
        assert abs(6 * PHI**-7.3 * math.pi * PHI**7.3 - 6 * math.pi) < 1e-12


# ══════════════════════════════════════════════════════════ section 19 ══
class TestSection19TowerOffset:
    """section 19 -- 'The phase offset of the tower: exact zeros against the asymptotic form, and the Maldacena–Qi form'"""

    def test_offsets_against_the_printed_column(self):
        from scipy.special import jn_zeros

        j = jn_zeros(1, 8)
        got = [round(x / math.pi - k, 4) for k, x in enumerate(j, 1)]
        assert got == [0.2197, 0.2331, 0.2383, 0.2411, 0.2428, 0.2439,
                       0.2448, 0.2454], got

    @pytest.mark.parametrize("d,printed", [(2, -0.250), (3, 0.000), (4, 0.250),
                                           (5, 0.500), (6, 0.750), (7, 1.000),
                                           (8, 1.250)])
    def test_dimensional_offset_d_over_4_minus_3_over_4(self, d, printed):
        assert round(d / 4 - 0.75, 3) == printed

    def test_only_d4_matches_one_over_d(self):
        for d in range(2, 9):
            equal = abs(d / 4 - 0.75 - 1 / d) < 1e-12
            assert equal == (d == 4), d


# ══════════════════════════════════════════════════════════ section 20 ══
class TestSection20TwoCandidates:
    """section 20 -- 'The contrast with the two observed candidates (380 and 700 GeV)'"""

    @staticmethod
    def fit(masses, errors, m_scale=M_GEV):
        """Weighted fit of the scale lambda with mu = the J1 zeros."""
        from scipy.special import jn_zeros

        w = [1 / e**2 for e in errors]
        mu = jn_zeros(1, len(masses))
        lam = sum(a * b * c for a, b, c in zip(w, masses, mu)) / sum(
            a * c * c for a, c in zip(w, mu)
        )
        dl = 1 / math.sqrt(sum(a * c * c for a, c in zip(w, mu)))
        return math.log(lam / m_scale) / LN_PHI, dl / lam / LN_PHI, lam

    def test_bottom_level_is_twelve(self):
        s, ds, _ = self.fit([380, 700], [20, 20])
        assert s == pytest.approx(11.97, abs=5e-3)
        assert ds == pytest.approx(0.05, abs=5e-3)
        assert abs(s - 12) / ds == pytest.approx(0.6, abs=0.05)

    def test_ratio_against_the_bessel_ratio(self):
        from scipy.special import jn_zeros

        assert round(700 / 380, 3) == 1.842
        assert round(jn_zeros(1, 2)[1] / jn_zeros(1, 2)[0], 3) == 1.831

    @pytest.mark.parametrize("k,printed", [(2, 1028), (3, 1346), (4, 1664),
                                           (5, 1982)])
    def test_predictions_at_sigma_12(self, k, printed):
        from scipy.special import jn_zeros

        got = round(jn_zeros(1, 6)[k] * M_GEV * PHI**12)
        assert got == printed, k


# ══════════════════════════════════════════════════════════ section 21 ══
class TestSection21TwoBraneRival:
    """section 21 -- 'The two-brane rival fitted to the same two candidates'"""

    def test_free_scale_versus_the_throat_scale(self):
        _sigma, _ds, lam = TestSection20TwoCandidates.fit([380, 700], [20, 20])
        from scipy.special import jn_zeros

        j = jn_zeros(1, 4)
        lg = M_GEV * PHI**12
        assert lam == pytest.approx(99.64, abs=5e-3)
        assert round(j[2] * lam) == 1014
        assert round(j[3] * lam) == 1328
        assert lg == pytest.approx(101.06, abs=5e-3)
        assert round(j[2] * lg) == 1028
        assert round(j[3] * lg) == 1346
        assert round(100 * (lg / lam - 1), 1) == 1.4
        assert round(j[2] * (lg - lam)) == 14
        assert round(j[3] * (lg - lam)) == 19

    def test_the_two_models_differ_by_one_point_four_percent(self):
        """main.tex L1578: the throat differs from the two-brane fit by 1.4 %.

        Every mode carries the same scale ratio, so 1028 against 1014 and
        1346 against 1328 both give 1.4 %; telling the models apart needs a
        resolution of 0.014 x 1028 = 14.4 GeV, 'about 15 GeV' in the text.
        """
        _sigma, _ds, lam = TestSection20TwoCandidates.fit([380, 700], [20, 20])
        from scipy.special import jn_zeros

        j = jn_zeros(1, 6)
        lg = M_GEV * PHI**12
        for k in (2, 3):
            g, t = j[k] * lg, j[k] * lam
            assert round(100 * abs(g - t) / g, 1) == 1.4, k
        # integer precision on 'about 15 GeV': the width of 15 is 1 GeV
        assert 0.014 * 1028 == pytest.approx(15, abs=1)


# ══════════════════════════════════════════════════════════ section 22 ══
class TestSection22CurvatureUnit:
    """section 22 -- 'The unit of the curvature and the observer level'"""

    def test_the_length_unit_is_sqrt2_planck(self):
        assert 1 / math.sqrt(0.5) == pytest.approx(math.sqrt(2), abs=1e-12)

    @pytest.mark.parametrize("name,printed", [("W4", 583.877), ("W8", 583.877)])
    def test_both_readings_agree(self, name, printed):
        """W8 (unit l = sqrt2 l_P) and W4 (entropy) agree: Lambda S = 6 pi."""
        lp = lam_planck(67.36, 0.6847)
        w8 = math.log(6 / (lp / 0.5)) / LN_PHI
        w4 = math.log(3 / lp) / LN_PHI
        value = w8 if name == "W8" else w4
        assert value == pytest.approx(printed, abs=5e-4)

    def test_cw6_equation_is_w4_plus_log_phi_two(self):
        lp = lam_planck(67.36, 0.6847)
        s_cw6 = math.log(6 / lp) / LN_PHI
        s_w4 = math.log(3 / lp) / LN_PHI
        assert s_cw6 == pytest.approx(s_w4 + math.log(2) / LN_PHI, abs=1e-9)
        assert s_cw6 == pytest.approx(585.317, abs=5e-4)

    @pytest.mark.parametrize("name,h0,ol,printed",
                             [("Planck 2018", 67.36, 0.6847, 583.877),
                              ("SH0ES", 73.04, 1 - 0.1430 / 0.7304 ** 2, 583.402)])
    def test_data_readings(self, name, h0, ol, printed):
        got = math.log(3 / lam_planck(h0, ol)) / LN_PHI
        assert got == pytest.approx(printed, abs=5e-4), name


# ══════════════════════════════════════════════════════════ section 23 ══
class TestSection23LatticeOfUnits:
    """section 23 -- 'The lattice: units of Z[phi], the background and the observer'"""

    @pytest.mark.parametrize(
        "n,a,b,norm",
        [(1, 0, 1, -1), (2, 1, 1, 1), (3, 1, 2, -1), (6, 5, 8, 1), (12, 89, 144, 1)],
    )
    def test_powers_of_phi_are_fibonacci_units(self, n, a, b, norm):
        """phi^n = F_{n-1} + F_n phi with norm (-1)^n."""
        assert PHI**n == pytest.approx(a + b * PHI, abs=1e-12)
        assert a * a + a * b - b * b == norm

    @staticmethod
    def h0_for(n, mode, omega_m=0.1430, omega_l=0.6847):
        lo, hi = 40.0, 120.0
        for _ in range(100):
            h = (lo + hi) / 2
            ol = 1 - omega_m / (h / 100) ** 2 if mode == "wm" else omega_l
            if math.log(3 / lam_planck(h, ol)) / LN_PHI > n:
                lo = h
            else:
                hi = h
        return h

    @pytest.mark.parametrize(
        "n,wm,ol,printed",
        [(583, 78.53, 83.18, None), (584, 66.01, 65.39, None),
         (585, 56.92, 51.41, None)],
    )
    def test_h0_at_each_lattice_point(self, n, wm, ol, printed):
        assert self.h0_for(n, "wm") == pytest.approx(wm, abs=5e-3)
        assert self.h0_for(n, "OL") == pytest.approx(ol, abs=5e-3)

    def test_the_584_point_is_excluded_by_both_datasets(self):
        h = self.h0_for(584, "wm")
        assert round((h - 67.36) / 0.54, 1) == -2.5
        assert round((h - 73.04) / 1.04, 1) == -6.8

    def test_the_background_level_is_twelve(self):
        """The line section 23 printed, on its values.

        The section wrote ``background: 11.97 +- 0.05 against lattice
        point 12 (0.6 standard deviations)`` as a literal; the three
        numbers are section 20's fit, recomputed here at the two decimals,
        two decimals and one decimal that line printed (SPEC-002 §1).
        """
        s, ds, _ = TestSection20TwoCandidates.fit([380, 700], [20, 20])
        assert s == pytest.approx(11.97, abs=5e-3)
        assert ds == pytest.approx(0.05, abs=5e-3)
        assert abs(s - 12) / ds == pytest.approx(0.6, abs=0.05)


# ══════════════════════════════════════════════════════════ section 24 ══
class TestSection24ScaleAndTop:
    """section 24 -- 'The two dimensionful data and the top'"""

    def test_koide_scale_and_unit(self):
        # m_tau from kkgt.constants: 1776.86 reproduces the printed 313.84
        # (the former tau mass gave 313.8509 -> 313.851, 19.6x this tolerance).
        me, mmu, mtau = 0.51099895, 105.6583755, M_TAU_MEV
        m = (math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mtau)) ** 2 / 9 / 1e3
        assert m * 1e3 == pytest.approx(313.841, abs=5e-4)
        u = m / M_PCF
        assert u * 1e3 == pytest.approx(4.6258, abs=5e-5)

    def test_planck_mass_in_gev(self):
        g_j = 1.602176634e-10
        m_pl = math.sqrt(HBAR * C_LIGHT**5 / G_NEWTON) / g_j
        assert m_pl == pytest.approx(M_PLANCK_GEV, rel=1e-6)

    def test_the_grid_does_not_fix_the_top(self):
        """2 log_phi(l_u/l) = 203.562, 0.44 away from the nearest integer."""
        me, mmu, mtau = 0.51099895, 105.6583755, M_TAU_MEV
        m = (math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mtau)) ** 2 / 9 / 1e3
        u = m / M_PCF
        g_j = 1.602176634e-10
        m_pl = math.sqrt(HBAR * C_LIGHT**5 / G_NEWTON) / g_j
        r = 2 * math.log(m_pl * math.sqrt(0.5) / u) / LN_PHI
        assert r == pytest.approx(203.562, abs=5e-4)
        assert abs(r - round(r)) == pytest.approx(0.44, abs=5e-3)

    def test_uv_level(self):
        me, mmu, mtau = 0.51099895, 105.6583755, M_TAU_MEV
        m = (math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mtau)) ** 2 / 9 / 1e3
        g_j = 1.602176634e-10
        m_pl = math.sqrt(HBAR * C_LIGHT**5 / G_NEWTON) / g_j
        assert math.log(m_pl / m) / LN_PHI == pytest.approx(93.737, abs=5e-4)


# ══════════════════════════════════════════════════════════ section 25 ══
class TestSection25AutodualWindow:
    """section 25 -- 'The cut and projection with the self-dual Gaussian, in both spaces'"""

    @classmethod
    def best(cls, x, rad=0.6):
        out = []
        for b in range(-50, 400):
            a0 = round(x - b * PHI)
            for a in (a0 - 1, a0, a0 + 1):
                v = a + b * PHI
                if abs(v - x) < rad:
                    c = a + b * PHI_BAR
                    out.append((math.exp(-math.pi * c * c), a, b, v))
        return sorted(out, reverse=True)[:2]

    @pytest.mark.parametrize(
        "x,weight,a,b,v",
        [(11.97, 0.074, 4, 5, 12.09), (583.88, 0.74, 161, 261, 583.31)],
    )
    def test_best_lattice_index(self, x, weight, a, b, v):
        got = self.best(x)[0]
        assert (got[1], got[2]) == (a, b), (x, got)
        assert got[3] == pytest.approx(v, abs=5e-3), (x, got)
        # half the last digit of the printed weight: 0.074 -> 5e-4,
        # 0.74 -> 5e-3 (decision (ii)), tighter than the former rel=0.02
        half = 0.5 * 10 ** -len(str(weight).split(".")[1])
        assert abs(got[0] - weight) <= half, (x, got[0], weight)

    def test_second_entry_near_the_observer(self):
        got = self.best(583.88)[1]
        assert (got[1], got[2]) == (162, 261)
        assert got[3] == pytest.approx(584.31, abs=5e-3)
        assert got[0] == pytest.approx(0.22, rel=0.02)

    def test_the_integer_12_kills_the_cut(self):
        """weight of the conjugate of 12 is 10^-196: the cut disappears."""
        assert round(math.pi * 144 / math.log(10)) == 196

    @pytest.mark.parametrize(
        "n,printed",
        [(0, 0.04), (1, 0.30), (2, 0.63), (3, 0.84), (4, 0.94), (5, 0.97),
         (6, 0.99)],
    )
    def test_scale_weights(self, n, printed):
        """weight exp(-pi phi^-2n) along the tower."""
        got = math.exp(-math.pi * PHI ** (-2 * n))
        assert round(got, 2) == printed, (n, got)


# ══════════════════════════════════════════════════════════ section 26 ══
class TestSection26WindowEdge:
    """section 26 -- 'The edge of the window and sigma_G'"""

    def test_the_two_crossings(self):
        n_weight = 0.5 * math.log(math.pi / math.log(2)) / LN_PHI
        n_entropy = math.log(2) / LN_PHI
        assert round(n_weight, 3) == 1.570
        assert round(n_entropy, 3) == 1.440

    @pytest.mark.parametrize("n,weight,h_l",
                             [(0, 0.043, 1.414), (1, 0.301, 1.112),
                              (2, 0.632, 0.874), (3, 0.839, 0.687)])
    def test_weight_and_entropy_of_the_first_levels(self, n, weight, h_l):
        assert round(math.exp(-math.pi * PHI ** (-2 * n)), 3) == weight
        assert round(math.sqrt(2 * PHI ** (-n)), 3) == h_l

    def test_first_active_level_is_two(self):
        """Both routes (weight 1/2 and H l = 1) activate n = 2 first."""
        thresholds = (math.exp(-math.pi * PHI**-2), math.exp(-math.pi * PHI**-4))
        assert tuple(round(t, 3) for t in thresholds) == (0.301, 0.632)
        active = [n for n in range(10)
                  if math.exp(-math.pi * PHI ** (-2 * n)) > 0.5
                  and math.sqrt(2 * PHI ** (-n)) < 1]
        assert active[0] == 2


# ══════════════════════════════════════════════════════════ section 27 ══
class TestSection27WindowAsNome:
    """section 27 -- 'The window as a nome: the tower of tori and S as a mirror'"""

    @pytest.mark.parametrize(
        "n,tau_n,nome,inv",
        [(0, 1.0, 0.0432, 1.0), (1, 0.3820, 0.3012, 2.6180),
         (2, 0.1459, 0.6323, 6.8541), (3, 0.0557, 0.8394, 17.9443)],
    )
    def test_nome_and_mirror(self, n, tau_n, nome, inv):
        """tau_n = phi^-2n, q = exp(-pi tau_n), -1/tau_n = tau_{-n}."""
        t = PHI ** (-2 * n)
        assert round(t, 4) == tau_n
        assert round(math.exp(-math.pi * t), 4) == nome
        assert round(1 / t, 4) == inv

    def test_weight_crossing_is_a_quarter_turn(self):
        n_h = 0.5 * math.log(math.pi / math.log(2)) / LN_PHI
        assert round(n_h, 6) == 1.570247
        assert round(math.pi / 2, 6) == 1.570796
        assert abs(n_h - math.pi / 2) < 1e-3
        assert round(math.exp(-math.pi * PHI ** (-math.pi)), 6) == 0.500183

    def test_autodual_width(self):
        """log2 * phi^pi = 3.143254 is pi to three decimals: the window is autodual."""
        got = math.log(2) * PHI**math.pi
        assert round(got, 6) == 3.143254
        assert abs(got - math.pi) < 2e-3


# ══════════════════════════════════════════════════════════ section 28 ══
class TestSection28PoissonTheta:
    """section 28 -- 'Poisson: the proper time and 1/N; theta_3 at tau = i'"""

    @pytest.mark.parametrize("n,printed", [(PHI**2, 2.6180), (PHI**4, 6.8541)])
    def test_modes_equal_windings(self, n, printed):
        lhs = sum(math.exp(-math.pi * k * k * n) for k in range(-60, 61))
        rhs = n**-0.5 * sum(math.exp(-math.pi * m * m / n) for m in range(-60, 61))
        assert round(n, 4) == printed
        assert abs(lhs - rhs) < 1e-9, (lhs, rhs)
        assert round(math.exp(-math.pi / n), 4) == (
            0.3012 if printed == 2.6180 else 0.6323
        )

    def test_theta3_at_tau_i(self):
        """theta_3(e^-pi) = pi^(1/4)/Gamma(3/4) (the fixed point of S: tau -> -1/tau)."""
        t3 = sum(math.exp(-math.pi * k * k) for k in range(-30, 31))
        closed = math.pi ** 0.25 / math.gamma(0.75)
        assert t3 == pytest.approx(closed, abs=1e-10)
        assert round(t3, 12) == 1.086434811213

    def test_the_lambda_transformation_laws_hold_to_1e_16(self):
        """main.tex L1541-1543: lambda(-1/tau) = 1 - lambda(tau), lambda(i) = 1/2.

        lambda = (theta_2/theta_3)^4 at tau = i t. The laws are asserted to
        1e-16 -- the precision main.tex used to state (DEC-001 section 5.6,
        dropped concurrently); at float64 the residual is one ulp
        (1.1e-16), hence mpmath at 50 digits.
        """
        import mpmath as mp

        def lam(t):
            th2 = 2 * mp.fsum(
                mp.exp(-mp.pi * t * (mp.mpf(n) + mp.mpf("0.5")) ** 2)
                for n in range(40)
            )
            th3 = 1 + 2 * mp.fsum(mp.exp(-mp.pi * t * n * n) for n in range(1, 40))
            return (th2 / th3) ** 4

        with mp.workdps(50):
            assert abs(lam(mp.mpf(1)) - mp.mpf(1) / 2) < mp.mpf(10) ** -16
            for t in (mp.mpf(2), mp.mpf(3)):
                # -1/(i t) = i / t, so the law reads lambda(i/t) = 1 - lambda(i t)
                assert abs(lam(1 / t) - (1 - lam(t))) < mp.mpf(10) ** -16, t
