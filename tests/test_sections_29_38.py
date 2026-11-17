"""Deep numeric tests for sections 29-38 of kkgt.sections.

Lattice point of the observer, quintessence, entropy consistency and the
area law of section 38 (the one main.tex cites as
test_shannon_bit_against_the_area_law).
"""

from __future__ import annotations

import math
import re

import numpy as np
import pytest
from scipy.special import jn_zeros

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

    def test_the_planck_level_is_2_2_to_3_1_sigma_from_584(self, run_section):
        """main.tex L2024-2025: Planck's level 583.877 sits 2.2 (r = -1) to
        3.1 (r = 0) standard deviations from 584 as the correlation of
        Omega_m and H_0 runs from -1 to 0 (section 29 prints both).

        One node rather than a parametrised pair: the manuscript cites this
        test by name, and a parametrised id carries its parameters."""
        ol = omega_l_required(584)
        out = run_section(29)
        for r, printed in [(-1.0, 2.2), (0.0, 3.1)]:
            p, dp = self.planck(r)
            level = 584 + math.log(ol / p) / LN_PHI
            dist = (584 - level) * p * LN_PHI / dp     # in units of the level sigma
            assert round(level, 3) == 583.877, (r, level)
            assert round(dist, 1) == printed, (r, dist)
            r_tag = re.escape(f"{r:+.0f}")            # the sign is a regex metachar
            m = out.match(
                rf"Planck only, r = {r_tag}: level ([\d.]+), ([\d.]+) sigma from 584"
            )
            assert round(float(m.group(1)), 3) == 583.877
            assert round(float(m.group(2)), 1) == printed

    @pytest.mark.parametrize("r,ten", [(0.0, 1.81), (-1.0, 1.43)])
    def test_desi_against_planck(self, r, ten):
        """DESI DR2 + CMB (0.3240 +- 0.0043) agrees with Planck at 1.4-1.8 sigma."""
        p, sigma = self.planck(r)
        p_d, dp_d = 0.3240, 0.0043
        got = (p_d - p) / math.hypot(dp_d, sigma)
        assert round(got, 2) == ten, (r, got)

    def test_the_script_asserts_the_window_it_quotes(self, run_section):
        run = run_section(29)
        run.has("Planck and the combination agree (1.4-1.8 sigma)")
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

    def test_vector_ratio_range(self, run_section):
        """2.228 (symmetric) against 2.275 (Planck top): inside the observed band.

        The band is the gluon candidates of section 1, 8600/(4000..3600);
        2.275 is the quotient of the two vector zeros that
        test_vector_zeros_against_the_lyr_table pins at four decimals, and
        2.228 is the same quotient at the depth phi^24, as section 37
        prints it for the symmetric window.
        """
        low, high = 8600 / 4000, 8600 / 3600
        assert (low, high) == pytest.approx((2.15, 2.39), abs=5e-3)
        vec = [2.4448, 5.5615, 8.6958]   # from test_vector_zeros_against_the_lyr_table
        planck_top = vec[1] / vec[0]
        assert planck_top == pytest.approx(2.275, abs=5e-4)
        symmetric = run_section(37).value(
            r"\[-12,12\]: m2/m1 = ([\d.]+)", tol=5e-4, label="[-12,12]"
        )
        assert low <= symmetric <= high, symmetric
        assert low <= planck_top <= high, planck_top

    def test_the_top_of_the_clock_is_the_printed_39_33(self, run_section):
        """main.tex L2108: the depth-24 clock tops out at 39.33 (AUD-001).

        Class b, cited to test_depth_of_the_clock, test_scales and
        test_vector_ratio_depends_only_on_the_depth; the figure lives in
        the label section 30 prints (section 1 computes the same 39.33).
        """
        run_section(30).has("(top at Planck: 39.33)")


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

    def test_the_worst_case_is_deci(self, run_section):
        """DESI r = -1 reads the level at 7.6 sigma from every integer."""
        run = run_section(32)
        run.has("DESI DR2 + CMB, LCDM, r = -1 (worst case)")
        assert run.has("integer 584 at 7.6 sigma")
        assert run.has("integer 584 at 3.1 sigma")
        assert run.has("integer 583 at 5.0 sigma")

    def test_the_criterion(self, run_section):
        run_section(32).has(
            "criterion: a level read 3 sigma or more from every integer rules out the lattice shape"
        )

    def test_the_worst_case_level_is_583_789_plus_or_minus_0_028(self, run_section):
        """main.tex L2028/L2330: 583.789 +- 0.028 at 7.6 sigma from 584.

        AUD-001 L2028: the two figures lived in the tests' code without an
        assertion; section 32 prints them on the DESI worst-case row, with
        the ``.3f`` width (half a unit, 5e-4) each.
        """
        run = run_section(32)
        m = run.match(
            r"DESI DR2 \+ CMB, LCDM, r = -1 \(worst case\)[^\n]*"
            r"level ([-\d.]+) \+- ([\d.]+); integer 584 at 7\.6 sigma"
        )
        level, err = float(m.group(1)), float(m.group(2))
        assert level == pytest.approx(583.789, abs=5e-4), level
        assert err == pytest.approx(0.028, abs=5e-4), err


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
    def test_cpl_projection(self, run_section, omega_m, w_at_0, w0, wa):
        """The background solution projected on w0+wa(1-a) over z < 2."""
        run = run_section(34)
        m = run.match(
            rf"Omega_m = {omega_m}: w\(0\) = ([-\d.]+); CPL projection \(z < 2\): "
            r"w0 = ([-\d.]+), wa = ([-\d.]+)"
        )
        got = [float(g) for g in m.groups()]
        assert got == pytest.approx([w_at_0, w0, wa], abs=5e-4), (omega_m, got)


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

    def test_correlation_converges_only_for_the_irrational_step(self, run_section):
        """The tower step log(phi)/2pi equidistributes; 13/8 stalls at 1e-3."""
        run = run_section(36)
        run.has("tower phase, log(phi)/2pi: N=10000: connected-part error 9.1e-05")
        run.has("rational 13/8: N=10000: connected-part error 6.8e-03")


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
    def test_vector_ratio_depends_only_on_the_depth(self, window, printed, run_section):
        run = run_section(37)
        lo, hi = window
        got = run.value(
            rf"\[{lo},{hi}\]: m2/m1 = ([\d.]+)", tol=5e-4, label=str(window)
        )
        assert got == pytest.approx(printed, abs=5e-4)

    @pytest.mark.parametrize("mass,printed", [(3600, 17.60), (4000, 17.82)])
    def test_gluon_background_level(self, mass, printed):
        """sigma = log_phi(m/(j_{0,1} M)) with M = 0.31384 GeV."""
        got = math.log(mass / (jn_zeros(0, 1)[0] * M_GEV)) / LN_PHI
        assert round(got, 2) == printed, (mass, got)

    def test_ratio_700_over_380_is_the_bessel_ratio(self):
        r = 700 / 380
        t = jn_zeros(1, 2)[1] / jn_zeros(1, 2)[0]
        e = r * math.hypot(20 / 700, 20 / 380)
        assert round(r, 4) == 1.8421
        assert round(t, 4) == 1.8309
        assert round(100 * (r / t - 1), 2) == 0.61
        assert round((r - t) / e, 2) == 0.10

    @pytest.mark.parametrize("d,printed", [(24, 257), (81.74, 247)])
    def test_first_gluon_at_the_background(self, d, printed, run_section):
        run = run_section(37)
        run.has(f"background 12, depth {d}: first gluon {printed} GeV")

    def test_w2_integer_dimension(self, run_section):
        """W2 of main.tex: dim H = 1654, 3436182, 820599769985 at sigma = 3,4,5."""
        run = run_section(37)
        run.has("sigma=3,4,5 -> 1654, 3436182, 820599769985")
        assert run.value(
            r"fit lnD = a S \+ b ln L \+ c \(sigma=3\.\.9\): a = ([\d.]+)",
            want=0.9972, tol=5e-5, label="W2 slope",
        )

    def test_cardy_slope_of_the_count(self, run_section):
        """ln W + (3/2) ln L0 = a S + b with a = 1.0010 (nats)."""
        run = run_section(37)
        run.value(
            r"ln W \+ \(3/2\) ln L0 = a S \+ b: a = ([\d.]+)",
            want=1.0010, tol=5e-5, label="Cardy slope",
        )

    def test_e_to_the_s_is_never_an_integer(self, run_section):
        """Gelfond-Schneider: e^(S/n) is at least 6.76e-5 away from an integer."""
        run = run_section(37)
        run.has("no integer (minimum distance 6.76e-05)")

    @pytest.mark.parametrize(
        "measure,printed",
        [("e^{4A}", [1.0, 1.8308, 2.6545, 3.4757, 4.2954]),
         ("e^{6A}", [1.0, 1.9993, 2.9970, 3.9925, 4.9850])],
    )
    def test_the_measure_that_gives_the_spectrum(self, run_section, measure, printed):
        run = run_section(37)
        pattern = "measure " + re.escape(measure) + r": \[([^\]]+)\]"
        got = [float(v) for v in run.match(pattern).group(1).split()]
        assert got == pytest.approx(printed, abs=5e-5), measure


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

    def test_section38_stdout(self, run_section):
        run = run_section(38)
        run.has("area law: 0.5 per ell^2 = 0.25 per ell_P^2 (Bekenstein-Hawking 1/4)")
        run.has("one Shannon bit per Planck area against the area law: ratio 2.773")
