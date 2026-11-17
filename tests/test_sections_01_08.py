"""Deep numeric tests for sections 1-8 of kkgt.sections.

Section identity: the manuscript cites the tests that check a number
(``\testref{...}``), and every test docstring here names the section of
``kkgt.sections`` it checks.

Two kinds of check:
  * independent -- the quantity is recomputed here from the closed form,
    with an explicit tolerance (this is the real regression net);
  * contract    -- the number is read from the section's stdout with an
    explicit tolerance, for quantities whose computation lives only inside
    the section (fits, discretisations).
"""

from __future__ import annotations

import math
import re

import numpy as np
import pytest
from scipy.special import jn_zeros

from kkgt.constants import LN_PHI, M_GEV, OBS_G, PHI

# Half the last digit of the figure each constant guards (decision (ii) of
# AUD-001): .3f -> 5e-4, .4f -> 5e-5.  R2 guards two-decimal figures, whose
# width would be 5e-3, but every one of them is read from the section's
# stdout, where the figure is already exact, so it keeps the .3f width:
# tighter than the rule asks, never looser.
R2 = 5e-4
R3 = 5e-4   # .3f
R4 = 5e-5   # .4f


# ═══════════════════════════════════════════════════════════ section 1 ══
class TestSection1Numbers:
    """section 1 -- 'Every number in order of appearance; alternatives for m0 (§9)'"""

    def test_observed_ratios(self):
        obs = np.array(OBS_G)
        got = obs / obs[0]
        assert got == pytest.approx([1.0, 1.842, 2.632, 3.479], abs=R3)

    def test_j1_ratios(self):
        j = jn_zeros(1, 4)
        got = j / j[0]
        assert got == pytest.approx([1.0, 1.8309, 2.6551, 3.4772], abs=R4)

    def test_residual_of_the_j1_fit_is_half_a_percent(self):
        """lam = (obs.mu)/(mu.mu) with mu = the J1 zeros; rms in percent."""
        mu = jn_zeros(1, 4)
        obs = np.array(OBS_G)
        lam = (obs @ mu) / (mu @ mu)
        rms = 100 * np.sqrt(np.mean(((obs - lam * mu) / obs) ** 2))
        assert rms == pytest.approx(0.54, abs=5e-3), rms

    def test_offset_of_j1_zeros_tends_to_one_quarter(self):
        """j_{1,k}/pi - k -> 1/4 (the printed column of section 1)."""
        j = jn_zeros(1, 8)
        off = j / math.pi - np.arange(1, 9)
        assert off == pytest.approx(
            [0.2197, 0.2331, 0.2383, 0.2411, 0.2428, 0.2439, 0.2448, 0.2454],
            abs=R4,
        )
        assert np.all(np.diff(off) > 0), "the offset must increase to 1/4"
        assert 0 < 0.25 - off[-1] < 5e-3

    def test_ring_constant_mode_equals_the_bf_bound_scale(self):
        """m^2 = -1/(log phi)^2 = -4.3184 for the constant mode of the ring.

        main.tex quotes the same figure at three decimals, -4.318 (AUD-001
        L877); section 1 prints both, ``(-4.318)`` and ``round(..., 4)``.
        """
        assert -1 / LN_PHI**2 == pytest.approx(-4.3184, abs=5e-5)
        assert round(-1 / LN_PHI**2, 3) == -4.318

    def test_masses_at_the_bottom_of_the_throat(self):
        """m_k = j_{1,k} M phi^12 with M = 0.31384 GeV -> 387, 709, 1028, 1346."""
        M = M_GEV
        got = [round(x * M * PHI**12) for x in jn_zeros(1, 4)]
        assert got == [387, 709, 1028, 1346]

    @pytest.mark.parametrize("matrix,order", [("S", 4), ("ST", 6)])
    def test_sl2z_orders(self, matrix, order):
        """v5 of section 1: order(S) = 4, order(ST) = 6, half power = -1."""
        S = np.array([[0, -1], [1, 0]])
        T = np.array([[1, 1], [0, 1]])
        A = S if matrix == "S" else S @ T
        assert np.array_equal(np.linalg.matrix_power(A, order), np.eye(2, dtype=int))
        assert np.array_equal(
            np.linalg.matrix_power(A, order // 2), -np.eye(2, dtype=int)
        )

    def test_st_mod_2_is_the_fibonacci_matrix(self):
        S = np.array([[0, -1], [1, 0]])
        T = np.array([[1, 1], [0, 1]])
        assert np.array_equal((S @ T) % 2, np.array([[0, 1], [1, 1]]))

    @pytest.mark.parametrize(
        "block",
        [
            "eta K symmetric",
            "eta == e^{4A}, A=-sigma log phi",
            "Q = 16, 32, 64, 128",
            "[3.832, 3.832, 3.832, 3.832]",
            "sigma_IR with m0 = M",
            "M_PCF log phi = 6 sqrt3 pi (framework units): M_PCF",
        ],
    )
    def test_section1_stdout_blocks(self, run_section, block):
        """Contract: the summary lines section 1 must keep printing."""
        run_section(1).has(block)

    def test_alternatives_for_the_bottom_level(self, run_section):
        """v2 of section 1: the level read from the scale depends on m0.

        One node rather than a parametrised triple: the manuscript cites
        this test by name, and a parametrised id carries its parameters.
        """
        run = run_section(1)
        for label, printed in [("M", 11.96), ("m_p/3", 11.97), ("m_e", 25.3)]:
            got = run.value(
                rf"sigma_IR with m0 = {label}\s+([-\d.]+)", label=f"sigma_IR m0={label}"
            )
            assert got == pytest.approx(printed, abs=5e-3), (label, got)

    def test_mpcf_framework_unit(self, run_section):
        """M_PCF log phi = 6 sqrt(3) pi -> 67.846 (same value as section 12).

        The stdout value carries the printed .3f width (half a unit, 5e-4).
        """
        got = run_section(1).value(r"framework units\): M_PCF\s+([-\d.]+)",
                                   label="M_PCF")
        assert got == pytest.approx(6 * math.sqrt(3) * math.pi / LN_PHI, abs=5e-4)

    def test_dirichlet_lowest_eigenvalue_is_positive(self, run_section):
        """Boundary conditions: Neumann has the zero mode, Dirichlet starts at 26.4.

        main.tex: "with them the lowest eigenvalue is 0, the massless
        four-dimensional graviton; with Dirichlet ... there is no zero mode".
        """
        run = run_section(1)
        m = run.match(
            r"lowest m\^2: Neumann \(~0\) ; Dirichlet \(26\.4\)\s+"
            r"\('([-\d.e+]+)',\s*(?:np\.float64\()?([\d.]+)"
        )
        neumann, dirichlet = float(m.group(1)), float(m.group(2))
        assert abs(neumann) < 1e-6, neumann
        assert dirichlet == pytest.approx(26.4, abs=0.05), dirichlet

    def test_second_order_convergence_on_the_golden_grid(self, run_section):
        """Relative error of m1 on [0,12] at Q = 16,32,64,128: 1.2e-4 ... 1.8e-6."""
        run = run_section(1)
        m = run.match(
            r"relative error of m1 on \[0,12\], Q=16,32,64,128 vs 3\.83182\s+"
            r"(\[[^\]]+\])"
        )
        errs = [float(v) for v in re.findall(r"'([\d.e+-]+)'", m.group(1))]
        # every entry is printed as ``.1e``, so each carries its own half
        # unit: 5e-6 on 1.2e-4 and 5e-7 on the three smaller ones
        for got_, want_, half in zip(
            errs, [1.2e-4, 2.9e-5, 7.3e-6, 1.8e-6], [5e-6, 5e-7, 5e-7, 5e-7]
        ):
            assert abs(got_ - want_) <= half, (got_, want_)
        # second order: every refinement divides the error by ~4
        for a, b in zip(errs, errs[1:]):
            assert a / b == pytest.approx(4.0, rel=0.3), (a, b)

    def test_one_node_per_level_degrades_the_residual(self, run_section):
        """One node per golden level: the residual rounds to 11-12 %.

        The section prints 12.4 for sigma[0,6] and 10.8 for sigma[-6,6];
        both round to the integers the sentence quotes.
        """
        run = run_section(1)
        vals = [float(v) for v in re.findall(
            r"one node per level, sigma\[-?\d+,6\] residual \(11-12%\)\s+([\d.]+)",
            run.stdout,
        )]
        assert len(vals) == 2, vals
        assert sorted(round(v) for v in vals) == [11, 12], vals

    def test_m_phi_11_is_62_5_gev(self, run_section):
        """The level 11 of M-theory read as a scale: M phi^11 = 62.5 GeV."""
        got = run_section(1).value(
            r"M phi\^11 \(GeV\), CW6 M-theory level read as a scale\s+([\d.]+)",
            label="M phi^11",
        )
        assert got == pytest.approx(62.5, abs=0.05), got

    def test_cw6_sine_band_matches_the_eigenvalues(self, run_section):
        """m_k = 2 sin(k pi/16)/log phi is the spectrum of (K), to 1e-10."""
        run = run_section(1)
        closed = run.value(
            r"eig\(K\) = \(2-2cos\(pi k/8\)\)/\(log phi\)\^2 \(max diff\)\s+([\d.e+-]+)",
            label="eig(K) closed form",
        )
        band = run.value(
            r"CW6 \(160\): m_k = 2 sin\(k pi/16\)/log phi vs eig\(K\)\s+([\d.e+-]+)",
            label="CW6 (160)",
        )
        assert closed < 1e-10, closed
        assert band < 1e-10, band

    def test_the_three_spacings_have_the_variance_of_the_ensemble(self, run_section):
        """main.tex L1366: the three spacings of eq:data /mean have variance 0.001.

        The GUE reference for that variance is 3pi/8 - 1 = 0.178; section 1
        prints both ('Additions A-C', B5 rigidity).
        """
        obs = np.array(OBS_G)
        sp = np.diff(obs)
        sp = sp / sp.mean()
        assert round(float(np.var(sp)), 3) == 0.001
        assert round(3 * math.pi / 8 - 1, 3) == 0.178
        run = run_section(1)
        run.value(
            r"data unfolded spacing variance \(~0\)\s+([\d.]+)",
            want=0.001, tol=R3, label="spacing variance",
        )
        run.value(
            r"GUE \(beta=2\) spacing variance 3pi/8 - 1 \(0\.178\)\s+([\d.]+)",
            want=0.178, tol=R3, label="GUE variance",
        )

    def test_the_residues_of_phi_to_the_twelve(self):
        """main.tex L1508-1512: phi^12 = 89 + 144 phi on the 24-clock.

        Modulo 16, 9, 12, 24, 48, 72 the coefficient 144 vanishes, so the
        half-turn phi^12 is an integer residue which squares to 1; modulo 9
        it is 8, i.e. -1. Modulo 5 the clock is 20 and phi^12 is not an
        involution. Section 1 prints these tuples ('Proposition: phi^12 is
        the half-turn of the 24-clock' / 'Clock of phi mod N (Pisano period)').
        """
        a, b = 89, 144        # phi^12 = F_11 + F_12 phi
        for n in (16, 9, 12, 24, 48, 72):
            assert b % n == 0, n          # integer residue: 144 = 0 (mod n)
            r = a % n
            assert r * r % n == 1, n      # the half-turn: the residue squares to 1
        assert a % 9 == 8                 # modulo 9 it is -1
        # modulo 5: 144 = 4 (mod 5), and (4 + 4 phi)^2 = 32 + 48 phi = 2 + 3 phi,
        # not 1 -> phi^12 is neither an integer residue nor an involution
        assert b % 5 == 4
        aa, bb = a % 5, b % 5
        sq = ((aa * aa + bb * bb) % 5, (2 * aa * bb + bb * bb) % 5)
        assert sq != (1, 0), sq
        # the order of phi mod 5 is 20: phi^k = F_{k-1} + F_k phi
        u, v, k = 1 % 5, 0, 0
        while True:
            u, v, k = v, (u + v) % 5, k + 1
            if (u, v) == (1 % 5, 0):
                break
            assert k < 100, k
        assert k == 20, k

    @pytest.mark.parametrize(
        "n,printed", [(16, 24), (9, 24), (12, 24), (24, 24),
                      (48, 24), (72, 24), (5, 20), (10, 60)]
    )
    def test_the_orders_of_phi_are_pisano_periods(self, n, printed):
        """main.tex L939-943: the orders of phi are Pisano periods of N.

        24 for N = 16, 9, 12, 24, 48, 72; 20 for N = 5; 60 for N = 10 --
        both as the order of phi in (Z[phi]/N)^x and as the Fibonacci
        period mod N. Section 1 prints 'Clock of phi mod N (Pisano period)'.
        """
        # Pisano period: smallest k > 0 with (F_k, F_{k+1}) = (0, 1) (mod n)
        a, b, k = 0, 1, 0
        while True:
            a, b, k = b, (a + b) % n, k + 1
            if (a, b) == (0, 1 % n):
                break
            assert k < 10000, n
        assert k == printed, (n, k)
        # order of phi: phi^k = F_{k-1} + F_k phi = 1 (mod n)
        u, v, k = 1, 0, 0
        while True:
            u, v, k = v, (u + v) % n, k + 1
            if (u % n, v % n) == (1 % n, 0):
                break
            assert k < 10000, n
        assert k == printed, (n, k)

    # ── AUD-001 policy (i): the figures section 1 prints that no test
    # asserted.  Each docstring names the manuscript line and the test the
    # manuscript cites for it; the tolerance is half the last digit of the
    # value the section prints (decision (ii)).

    def test_the_printed_koide_scale_is_313_84(self, run_section):
        """main.tex L805 and L1464: M = 313.84 MeV (AUD-001, class b).

        Cited to test_reconstruction_is_below_one_part_in_ten_thousand and
        test_alternatives_for_the_bottom_level; section 1 prints the figure
        with ``round(M_lep, 2)``.
        """
        run_section(1).value(
            r"M \(Koide\) MeV \(313\.84\)\s+([-\d.]+)",
            want=313.84, tol=5e-3, label="Koide M (.2f)",
        )

    def test_the_ir_level_in_phi_units_is_the_printed_3_8319(self, run_section):
        """main.tex L1454: m1/phi^sigma_IR = 3.8319 (AUD-001, class b).

        Cited to test_second_order_convergence_on_the_golden_grid; the value
        is printed with ``round(..., 4)``.
        """
        run_section(1).value(
            r"\[0,12\] m1/phi\^sigma_IR \(3\.8319\); ratios\s+"
            r"\((?:np\.float64\()?([-\d.]+)",
            want=3.8319, tol=5e-5, label="m1/phi^sigma_IR (.4f)",
        )

    def test_the_scale_in_powers_of_two_is_the_printed_8_30(self, run_section):
        """main.tex L1475: the same scale in powers of 2 = 8.30.

        Section 1 prints 8.3 (``round(..., 2)``); 8.30 is the manuscript's
        two-decimal reading of it (AUD-001, class b, cited to
        test_alternatives_for_the_bottom_level).
        """
        got = run_section(1).value(
            r"same number in powers of 2 \(8\.30\)\s+([-\d.]+)",
            want=8.30, tol=5e-3, label="scale in powers of 2 (.2f)",
        )
        assert round(got, 2) == 8.30, got

    def test_the_log_pi_of_the_scale_is_the_printed_5_03(self, run_section):
        """main.tex L1557: log_pi(scale/M) = 5.03 (AUD-001, class b).

        Section 1 prints the value with ``round(..., 3)`` as 5.028 and the
        label carries the manuscript's two-decimal 5.03.
        """
        got = run_section(1).value(
            r"log_pi\(scale/M\) \(5\.03\); pi\^5 deviation \(-1\.9 sd\)\s+"
            r"\((?:np\.float64\()?([-\d.]+)",
            want=5.028, tol=5e-4, label="log_pi(scale/M) (.3f)",
        )
        assert round(got, 2) == 5.03, got

    def test_the_j0_limit_is_the_printed_2_295(self, run_section):
        """main.tex L1594 and L1601: m2/m1 -> 2.295 at the J0 limit.

        AUD-001, class b, cited to test_vector_ratio_range; the value is
        printed with ``round(..., 3)``.
        """
        run_section(1).value(
            r"J0 limit \(2\.295\)\s+([-\d.]+)",
            want=2.295, tol=5e-4, label="J0 limit (.3f)",
        )

    def test_the_two_uv_tops_in_levels_are_the_printed_two(self, run_section):
        """main.tex L1610: the UV top at the two Planck masses.

        k pi r = 39.33 at M_Pl and 37.72 at the reduced M_Pl, with
        sigma_UV = 93.74 and 90.39 (AUD-001, class b, cited to
        test_vector_ratio_range); both pairs are printed with
        ``round(..., 2)``.
        """
        run = run_section(1)
        m_pl = run.match(
            r"^M_Pl: k pi r \(39\.33/37\.72\); sigma_UV \(93\.74/90\.39\)\s+"
            r"\((?:np\.float64\()?([-\d.]+)\),\s*(?:np\.float64\()?([-\d.]+)\)"
        )
        reduced = run.match(
            r"^reduced M_Pl: k pi r \(39\.33/37\.72\); sigma_UV \(93\.74/90\.39\)\s+"
            r"\((?:np\.float64\()?([-\d.]+)\),\s*(?:np\.float64\()?([-\d.]+)\)"
        )
        for m, want, tol, label in (
            (m_pl, (39.33, 93.74), 5e-3, "M_Pl"),
            (reduced, (37.72, 90.39), 5e-3, "reduced M_Pl"),
        ):
            got = (float(m.group(1)), float(m.group(2)))
            assert got == pytest.approx(want, abs=tol), (label, got)

    def test_the_four_graviton_zeros_are_the_printed_four(self, run_section):
        """main.tex L1612 and L1613: 3.8317, 7.0156, 10.1735, 13.3237.

        AUD-001, class b, cited to test_vector_ratio_range; section 1
        prints them with ``np.round(g_, 4)`` at both Planck masses.
        """
        run = run_section(1)
        m = run.match(
            r"graviton zeros \(3\.8317, 7\.0156, 10\.1735, 13\.3237\)\s+"
            r"\[([^\]]+)\]"
        )
        got = [float(v) for v in m.group(1).split()]
        assert got == pytest.approx(
            [3.8317, 7.0156, 10.1735, 13.3237], abs=5e-5
        ), got

    def test_the_lyr_vector_table_is_the_printed_four(self, run_section):
        """main.tex L1617 and L1618: the LYR vector zeros 2.45, 5.57, 8.7, 11.84.

        AUD-001, class b, cited to test_vector_ratio_range: the four LYR
        figures live in the label section 1 prints, and the section's own
        four-decimal zeros are asserted beside them.
        """
        run = run_section(1)
        run.has("vs LYR 2.45 5.57 8.7 11.84")
        m = run.match(
            r"vector zeros \(2\.4448, 5\.5615, 8\.6958, 11\.835\) vs LYR"
            r"[^\[]*\[([^\]]+)\]"
        )
        got = [float(v) for v in m.group(1).split()]
        assert got == pytest.approx([2.4448, 5.5615, 8.6958, 11.834], abs=5e-5), got

    def test_the_rounding_tolerance_of_a_four_decimal_figure_is_5e_5(self):
        """main.tex L2506: 5e-5 is the rounding width of a .4f figure.

        AUD-001 L2472: the figure lived only in the tests' code (``R4``);
        this pins the rule the manuscript states and the property that
        makes half a unit the right width.
        """
        assert R4 == 5e-5 == 0.5 * 10 ** -4
        figure = 3.8317     # a four-decimal figure section 1 prints
        assert round(figure + 4.9e-5, 4) == 3.8317   # still the same print
        assert round(figure + 6e-5, 4) == 3.8318     # and beyond it is not


# ═══════════════════════════════════════════════════════════ section 2 ══
class TestSection2Casimir:
    """section 2 -- 'Vacuum energy of the tower, exact zeros of J1 (§9)'"""

    def test_a_converges_with_the_number_of_exact_zeros(self, run_section):
        """A(K=20) and A(K=60) agree to 5e-5 (McMahon tail + Hurwitz zeta)."""
        run = run_section(2)
        a20 = run.value(r"K=20: A=([\d.]+)", label="A K=20")
        a60 = run.value(r"K=60: A=([\d.]+)", label="A K=60")
        assert a20 == pytest.approx(0.22327442, abs=5e-9), a20
        assert abs(a60 - a20) < 5e-5, (a20, a60)

    def test_b_is_positive(self, run_section):
        run = run_section(2)
        b = run.value(r"K=60: A=[\d.]+\s+B=([\d.]+)", label="B K=60")
        assert b > 0
        assert run.has("sign B: +")

    def test_depth_is_minus_log_s_over_log_phi(self, run_section):
        """log_phi(1/s*) = -log s* / log phi, checked against the printed depth."""
        run = run_section(2)
        line = run.match(r"K=60:[^\n]*")
        ls = float(re.search(r"log s\*=([-\d.]+)", line.group(0)).group(1))
        depth = float(re.search(
            r"depth log_phi\(1/s\*\) = ([\d.]+)", line.group(0)
        ).group(1))
        assert -ls / LN_PHI == pytest.approx(depth, abs=5e-8)
        assert depth == pytest.approx(1.0694864, abs=5e-8)


# ═══════════════════════════════════════════════════════════ section 3 ══
class TestSection3TwoBraneSpectra:
    """section 3 -- 'Two-brane spectra (Proposition of the two-brane model)'"""

    @pytest.mark.parametrize("depth,printed", [(6, 2.093), (12, 2.171), (30, 2.241)])
    def test_vector_ratio_grows_with_the_depth(self, run_section, depth, printed):
        """Exact two-brane condition: m2/m1 -> 2.295 as the throat deepens."""
        got = run_section(3).value(
            rf"depth phi\^{depth}: vector m2/m1 = ([\d.]+)",
            label=f"vector m2/m1 at phi^{depth}",
        )
        assert got == pytest.approx(printed, abs=R3)

    def test_graviton_zeros_are_the_j1_zeros(self, run_section):
        run = run_section(3)
        m = run.match(r"graviton x_n = \[\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\]")
        got = [float(g) for g in m.groups()]
        assert got == pytest.approx(list(jn_zeros(1, 3)), abs=5e-5)

    def test_vector_zeros_against_the_lyr_table(self, run_section):
        """x_1^vec/x_1^grav = 0.6381; the vector zeros track LYR 2.45, 5.57, 8.7."""
        run = run_section(3)
        m = run.match(r"vector   x_n = \[([\d.]+)\s+([\d.]+)\s+([\d.]+)\]")
        vec = [float(g) for g in m.groups()]
        assert vec == pytest.approx([2.4448, 5.5615, 8.6958], abs=5e-5)
        # both factors are printed at 4 decimals, so the quotient of the
        # printed values carries up to 1e-4 of rounding propagation
        assert vec[0] / jn_zeros(1, 1)[0] == pytest.approx(0.6381, abs=1e-4)
        run.value(r"x1_vec/x1_grav = ([\d.]+)", want=0.6381, tol=5e-5,
                  label="section 3 quotient")
        # the LYR gluon band in units of the graviton, as section 3 prints it
        run.has("9.47 - 10.53")

    def test_uv_depth_in_levels(self, run_section):
        """k pi r = 39.33 = 81.74 levels, sigma_UV = 12 + 81.74 = 93.74."""
        run = run_section(3)
        m = run.match(r"k pi r = ([\d.]+) = ([\d.]+) levels; sigma_UV = ([\d.]+)")
        kpr, levels, sigma_uv = (float(g) for g in m.groups())
        assert levels * LN_PHI == pytest.approx(kpr, abs=5e-3)
        assert 12 + levels == pytest.approx(sigma_uv, abs=5e-3)
        assert sigma_uv == pytest.approx(93.74, abs=5e-3)

    def test_lyr_gluon_over_graviton(self):
        assert round(3600 / 380, 2) == 9.47
        assert round(4000 / 380, 2) == 10.53


# ═══════════════════════════════════════════════════════════ section 4 ══
class TestSection4MetricPositivity:
    """section 4 -- 'Metric and reflection positivity (Proposition of the metric, §4)'"""

    def test_standard_product_is_not_positive(self, run_section):
        """In the standard product sym(T) has a negative eigenvalue for a >= 0.2."""
        run = run_section(4)
        vals = [float(v) for v in re.findall(
            r"min eigenvalue of sym\(T\)=([-\d.e+]+)", run.stdout
        )]
        assert len(vals) == 3, vals
        assert vals[0] > 0 and vals[1] < 0 and vals[2] < 0, vals

    def test_sym_t_eigenvalues_are_the_printed_three(self, run_section):
        """The three magnitudes: +0.35 at a=0.05, -0.06 at a=0.2, -2.83 at a=1."""
        run = run_section(4)
        vals = [float(v) for v in re.findall(
            r"min eigenvalue of sym\(T\)=([-\d.e+]+)", run.stdout
        )]
        assert len(vals) == 3, vals
        assert vals == pytest.approx([0.35, -0.06, -2.83], abs=5e-3), vals

    def test_eta_weighted_product_is_positive(self, run_section):
        """<f,Tf>_eta > 0 for a = 0.05, 0.2, 1.0: the metric restores positivity."""
        run = run_section(4)
        vals = [float(v) for v in re.findall(
            r"<f,Tf>_eta min = ([\d.e+-]+)", run.stdout
        )]
        assert len(vals) == 3, vals
        assert all(v > 0 for v in vals), vals

    def test_eta_is_the_sqrt_minus_g_of_the_metric(self, run_section):
        run = run_section(4)
        assert re.search(r"eta_sigma == e\^\{4A\(sigma\)\}.*:\s*True", run.stdout)

    def test_K_is_self_adjoint_in_the_eta_product_only(self, run_section):
        run = run_section(4)
        assert re.search(r"K self-adjoint in the standard product:\s*False", run.stdout)
        assert re.search(r"K self-adjoint in <u,v>_eta = u.eta.v :\s*True", run.stdout)


# ═══════════════════════════════════════════════════════════ section 5 ══
class TestSection5QuarterPhase:
    """section 5 -- 'Phase 1/4 (Corollary of the phase)'"""

    def test_measured_phase_in_d4_is_a_quarter(self, run_section):
        """d=4: measured phase 0.233 against the asymptotic (d-3)/4 = 0.25."""
        run = run_section(5)
        m = run.match(
            r"d=4: nu=1.0\s+asympt\. phase \(d-3\)/4=([\d.]+)\s+measured phase=([\d.]+)"
            r"\s+rms=([\d.]+)%"
        )
        asym, measured, rms = (float(g) for g in m.groups())
        assert asym == pytest.approx(0.25, abs=1e-9)
        assert abs(measured - asym) <= 0.02, (measured, asym)
        assert rms <= 0.6, rms

    def test_free_phase_fit_is_not_better(self, run_section):
        """Two parameters (theta free) give rms 0.57%, no better than the 1/4."""
        run = run_section(5)
        m = run.match(r"optimal theta = ([\d.]+)\s+rms=([\d.]+)%")
        theta, rms = float(m.group(1)), float(m.group(2))
        assert theta == pytest.approx(0.217, abs=R3)
        assert rms <= 0.6, rms


# ═══════════════════════════════════════════════════════════ section 6 ══
class TestSection6BesselChain:
    """section 6 -- 'Bessel chain (Bessel theorem, Observation of levels)'"""

    @pytest.mark.parametrize(
        "window,printed_rms", [("0,6", 1.00), ("-6,6", 0.54), ("-20,6", 0.54)]
    )
    def test_rms_against_the_lyr_table(self, run_section, window, printed_rms):
        run = run_section(6)
        m = run.match(
            rf"sigma\[{re.escape(window)}\] M=32: m/m1=\[([^\]]+)\]\s+rms LYR=([\d.]+)%"
        )
        ratios = [float(v) for v in m.group(1).split()]
        rms = float(m.group(2))
        assert rms == pytest.approx(printed_rms, abs=R2)
        assert len(ratios) == 4

    def test_deep_chain_yields_the_j1_zeros(self, run_section):
        """sigma[-6,6], M=32 -> 1.8308, 2.6545, 3.4757: within 0.05% of J1.

        The residual 1.5e-3 on the fourth ratio is the discretisation error
        of the M=32 chain (the section itself reports rms 0.54% against data).
        main.tex L1296: the shallow window's m2/m1 (1.8421) differs from the
        deep value (1.8308) by 0.011, i.e. 0.6%.
        """
        run = run_section(6)
        m = run.match(r"sigma\[-6,6\] M=32: m/m1=\[([^\]]+)\]")
        got = [float(v) for v in m.group(1).split()]
        j = jn_zeros(1, 4)
        want = list(j / j[0])
        assert got[0] == pytest.approx(1.0, abs=1e-12)
        assert got[1:] == pytest.approx(want[1:], rel=2e-3)
        m2 = run.match(r"sigma\[0,6\] M=32: m/m1=\[([^\]]+)\]")
        shallow = [float(v) for v in m2.group(1).split()]
        diff = shallow[1] - got[1]
        assert round(diff, 3) == 0.011, diff
        assert round(100 * diff / got[1], 1) == 0.6, diff

    def test_without_the_weight_the_chain_degrades(self, run_section):
        run = run_section(6)
        m = run.match(
            r"without the e\^\{2A\} weight \(as in A.7\), sigma\[-6,6\], M=32: \[([^\]]+)\]"
        )
        ratios = [float(v) for v in m.group(1).split()]
        assert ratios == pytest.approx([1.0, 2.227, 3.458, 4.687], abs=5e-4)


# ═══════════════════════════════════════════════════════════ section 7 ══
class TestSection7Prediction:
    """section 7 -- 'Prediction and what is not claimed (§10, §11)'"""

    @pytest.mark.parametrize(
        "m,dm,printed", [(700, 20, 0.110), (1000, 30, 0.159), (1322, 40, 0.211)]
    )
    def test_error_on_the_ratios(self, run_section, m, dm, printed):
        """sigma(m/380) = (m/380) hypot(dm/m, 20/380) -- recomputed here."""
        ratio = m / 380.0
        err = ratio * math.hypot(dm / m, 20 / 380)
        assert round(err, 3) == printed, (m, err)
        run_section(7).has(f"{m}/380: {ratio:.3f} +- {err:.3f}")

    def test_gluon_scale_needs_three_levels(self, run_section):
        run = run_section(7)
        got = run.value(
            r"gluon\s+scale=[^\n]*log_phi\(scale/graviton\)=([\d.]+)",
            want=5.39, tol=R2, label="gluon delta sigma",
        )
        assert got == pytest.approx(5.39, abs=R2)
        run.has("gluon/graviton would require Delta sigma = 3")


# ═══════════════════════════════════════════════════════════ section 8 ══
class TestSection8LookElsewhere:
    """section 8 -- 'Look-elsewhere (§6, §9)'"""

    @pytest.mark.parametrize(
        "tol,printed", [(0.01, 0.08), (0.03, 0.25), (0.05, 0.43), (0.10, 0.84)]
    )
    def test_probability_of_a_phi_coincidence(self, tol, printed):
        """Recomputed with the script's seed: 200k log-uniform ratios."""
        rng = np.random.default_rng(1)
        r = np.exp(rng.uniform(np.log(1.3), np.log(4.5), 200000))
        grid = PHI ** (np.arange(1, 9) / 2)
        d = np.min(np.abs(r[:, None] / grid[None, :] - 1), axis=1)
        assert round(float(np.mean(d < tol)), 2) == printed

    def test_a_random_scale_lands_within_point_zero_four_of_an_integer_level(self):
        """main.tex L1557-1558: the seed-2 twin of the look-elsewhere test.

        200k values of log_phi(scale) uniform in [0, 30]: the chance of
        landing within 0.04 of an integer level is 0.08 (section 1 prints
        the same draw rounded to .3f, 0.082).
        """
        rng = np.random.default_rng(2)
        u = rng.uniform(0, 30, 200000)
        p = float(np.mean(np.abs(u - np.round(u)) < 0.04))
        assert round(p, 2) == 0.08, p

    def test_rs_fit_beats_the_golden_fit(self, run_section):
        """rms RS = 0.5% against rms phi^k = 12.1% (one parameter each)."""
        obs = np.array(OBS_G)
        xi = jn_zeros(1, 4)
        m_rs = (obs @ xi) / (xi @ xi)
        rms_rs = 100 * np.sqrt(np.mean(((obs - m_rs * xi) / obs) ** 2))
        assert round(rms_rs, 1) == 0.5, rms_rs
        run_section(8).has("rms RS=0.5%   rms phi^k=12.1%")

    def test_lyr_table_follows_the_bessel_zeros(self):
        """The LYR prediction table is the RS (J1) tower.

        The table is quoted at 2-4 significant figures, so the entry "10."
        (J1 zero 10.1735) is only good to 2%; every entry with at least three
        significant figures sits within 1% of its zero.
        """
        table = np.array([380, 700, 1000, 1322, 1640, 1945, 2260, 2590, 2905],
                         dtype=float) / 100.0
        zeros = jn_zeros(1, 9)
        rel = np.abs(table / zeros - 1)
        assert rel[2] < 0.02, rel          # the two-significant-figure entry
        assert np.delete(rel, 2).max() < 0.01, rel

    @pytest.mark.parametrize(
        "num,den,nearest,printed_dev",
        [
            (1000, 380, 2.618, 0.5),
            (8600, 3600, 2.618, -8.8),
            (2150, 1040, 2.058, 0.4),
            (3600, 1000, 3.330, 8.1),
        ],
    )
    def test_observed_ratio_against_the_nearest_phi_power(
        self, num, den, nearest, printed_dev
    ):
        ratio = num / den
        grid = PHI ** (np.arange(1, 9) / 2)
        j = int(np.argmin(np.abs(ratio / grid - 1)))
        assert grid[j] == pytest.approx(nearest, abs=5e-4)
        assert round(100 * (ratio / grid[j] - 1), 1) == printed_dev

    def test_discrete_kk_operator_matches_its_closed_form(self, run_section):
        """eig(L) = (-2 + 2 cos(k pi/8)) / ln^2 phi for the 7-level operator."""
        n = 7
        L = np.diag(np.full(n, -2.0))
        for s in range(1, n):
            L[s, s - 1] = PHI**2
            L[s - 1, s] = PHI**-2
        L /= LN_PHI**2
        ev = np.sort(np.linalg.eigvals(L).real)[::-1]
        ana = np.sort(
            (-2 + 2 * np.cos(np.arange(1, n + 1) * np.pi / (n + 1))) / LN_PHI**2
        )[::-1]
        assert ev == pytest.approx(ana, abs=1e-10)
        run_section(8).has("hopping symmetrized sqrt(phi^2*phi^-2) = 1.0")
