"""Deep numeric tests for sections 9-16 of the note.

Sections 9-11 (granularity and contact configurations), 12 (the checks
behind figure 1, now drawn by section 44) and 13 (figure 2, with its
exact statements), 14-16 (gaps, state count, Koide).

The bodies of sections 12, 13 and 16 live here now (SPEC-002 §1): the
check block, the depth table, the figure sentinel and the two printed
lines this module used to read back from a section's stdout are asserted
on their values by the migrated code below.  No test of this file runs a
section any more.
"""

from __future__ import annotations

import itertools
import math
from typing import Any

import numpy as np
import pytest
from scipy.optimize import brentq
from scipy.special import j0, y0

from kkgt.constants import (
    EPS0,
    FIGURES,
    LN_PHI,
    M_KOIDE_MEV,
    M_PCF,
    M_TAU_MEV,
    PHI,
)
from kkgt.harness import verify_figure_artifact


# ═══════════════════════════════════════════════════════════ section 9 ══
class TestSection9GapRatios:
    """section 9 -- 'Gap ratios (Discussion 6.1)'"""

    @staticmethod
    def _disc(a, n):
        x = np.sort((np.arange(1, n + 1) * a) % 1)
        i = np.arange(1, n + 1)
        return max(np.max(i / n - x), np.max(x - (i - 1) / n))

    @staticmethod
    def _gaps(a, n):
        x = np.sort(np.r_[0, (np.arange(1, n + 1) * a) % 1, 1])
        g = np.round(np.diff(x), 10)
        g = np.unique(g[g > 0])
        return len(g), g.max() / g.min()

    @pytest.mark.parametrize(
        "name,a,d100,d1000,d10000",
        [
            ("phi", PHI, 1.418, 1.336, 2.568),
            ("sqrt2", 2 ** 0.5, 1.472, 1.694, 2.647),
            ("pi", math.pi, 1.767, 10.283, 65.800),
            ("e", math.e, 1.942, 1.100, 2.527),
            ("rational 13/8", 13 / 8, 12.500, 125.000, 1250.000),
        ],
    )
    def test_star_discrepancy(self, name, a, d100, d1000, d10000):
        """N*D_N for the five rotations; recomputed here from the definition."""
        assert round(100 * self._disc(a, 100), 3) == d100, name
        assert round(1000 * self._disc(a, 1000), 3) == d1000, name
        assert round(10000 * self._disc(a, 10000), 3) == d10000, name

    @pytest.mark.parametrize(
        "a,expected",
        [(PHI, (3, PHI**2)), (13 / 8, (1, 1.0))],
    )
    def test_gap_structure_at_n1000(self, a, expected):
        """phi has three gaps in the ratio phi^2; a rational step has one."""
        count, ratio = self._gaps(a, 1000)
        assert count == expected[0]
        assert ratio == pytest.approx(expected[1], abs=1e-6)


# ══════════════════════════════════════════════════════════ section 10 ══
class TestSection10Granularity:
    """section 10 -- 'Figure 3: granularity, with its numbers'"""

    @staticmethod
    def _gaps(x):
        x = np.sort(np.r_[0, np.mod(x, 1), 1])
        g = np.diff(x)
        return g[g > 1e-12]

    @pytest.mark.parametrize(
        "n,max_gap", [(5, 0.23607), (8, 0.1459), (13, 0.09017), (21, 0.05573),
                      (34, 0.03444), (55, 0.02129)]
    )
    def test_three_golds_with_ratio_phi_squared(self, n, max_gap):
        """N points {k phi}: exactly three gaps, ratio phi^2, for N Fibonacci."""
        g = self._gaps(np.arange(1, n + 1) * PHI)
        assert len(np.unique(np.round(g, 9))) == 3, n
        assert round(g.max() / g.min(), 4) == 2.6180, n
        assert round(g.max(), 5) == max_gap, n

    @pytest.mark.parametrize("k", [1, 5, 10])
    def test_dyadic_resolution_costs_k_bits(self, k):
        """2^-k resolution needs k binary digits (k registers)."""
        assert 2.0 ** -k == pytest.approx(1 / 2 ** k, abs=0)
        assert round(1 / 2.0 ** -k) == 2 ** k

    def test_worst_gap_ratio_over_the_first_5000_levels(self):
        """phi never leaves the phi^2 ratio; the phase step reaches 17.542.

        main.tex L1823-1824: the same worst-case scan for the three comparison
        steps -- 3.414 for sqrt(2), 9.52 for e, 293.6 for pi, each at the
        printed precision over N = 10..5000.
        """
        worst_phi = max(
            (lambda g: g.max() / g.min())(self._gaps(np.arange(1, N + 1) * PHI))
            for N in range(10, 5001)
        )
        assert round(worst_phi, 3) == 2.618, worst_phi

        step = LN_PHI / (2 * np.pi)
        worst_phase = max(
            (lambda g: g.max() / g.min())(self._gaps(np.arange(1, N + 1) * step))
            for N in range(10, 5001)
        )
        assert round(worst_phase, 3) == 17.542, worst_phase

        for name, a, printed, nd in (
            ("sqrt2", 2**0.5, 3.414, 3),
            ("e", math.e, 9.52, 2),
            ("pi", math.pi, 293.6, 1),
        ):
            worst = max(
                (lambda g: g.max() / g.min())(self._gaps(np.arange(1, N + 1) * a))
                for N in range(10, 5001)
            )
            assert round(worst, nd) == printed, (name, worst)

    def test_the_levels_that_break_the_phi_squared_ratio(self):
        """N+1 = Fibonacci: only there the origin joins the marks."""
        exc = [
            N for N in range(3, 5001)
            if abs(
                (lambda g: g.max() / g.min())(self._gaps(np.arange(1, N + 1) * PHI))
                - PHI**2
            ) > 1e-6
        ]
        assert exc == [4, 7, 12, 20, 33, 54, 88, 143, 232, 376, 609, 986,
                       1596, 2583, 4180], exc

    def test_phase_rotation_is_a_fraction_of_a_turn(self):
        assert LN_PHI / (2 * np.pi) == pytest.approx(0.07658724063250828, abs=1e-12)


# ══════════════════════════════════════════════════════════ section 11 ══
class TestSection11ContactConfigurations:
    """section 11 -- 'Contact configurations in 1D, 2D and 3D (6.1)'"""

    def test_sixth_roots_of_unity_are_a_2d_contact_set(self):
        u = np.exp(1j * np.pi * np.arange(6) / 3)
        d = [abs(a - b) for a, b in itertools.combinations(u, 2)]
        assert np.allclose(abs(u), 1)
        assert min(d) == pytest.approx(1.0, abs=1e-12)

    @staticmethod
    def _icosahedron():
        V = []
        for s1 in (1, -1):
            for s2 in (1, -1):
                p = (0, s1, s2 * PHI)
                V += [p, (p[1], p[2], p[0]), (p[2], p[0], p[1])]
        return np.array(V, float)

    def test_the_twelve_vertices_have_squared_norm_phi_plus_two(self):
        V = self._icosahedron()
        assert len(V) == 12
        assert np.allclose((V**2).sum(1), PHI + 2)

    def test_icosaedral_contact_spheres_do_not_touch(self):
        """The 12 unit spheres around the centre keep 2.1029 > 2 apart."""
        V = self._icosahedron()
        W = 2 * V / np.sqrt(PHI + 2)
        m = min(np.linalg.norm(a - b)
                for a, b in itertools.combinations(W, 2))
        assert m == pytest.approx(2.1029, abs=5e-5)
        assert m >= 2

    def test_fcc_and_hcp_reach_the_twelve_without_phi(self):
        fcc = [v for v in itertools.product([-1, 0, 1], repeat=3)
               if sorted(map(abs, v)) == [0, 1, 1]]
        Wf = [2 * np.array(v) / np.sqrt(2) for v in fcc]
        mf = min(np.linalg.norm(a - b) for a, b in itertools.combinations(Wf, 2))
        assert len(fcc) == 12
        assert abs(mf - 2) < 1e-12

        hc = [(2 * math.cos(k * math.pi / 3), 2 * math.sin(k * math.pi / 3), 0)
              for k in range(6)]
        for s in (1, -1):
            for k in range(3):
                t = k * 2 * math.pi / 3 + math.pi / 6
                hc.append((2 * math.cos(t) / math.sqrt(3),
                           2 * math.sin(t) / math.sqrt(3),
                           2 * s * math.sqrt(2 / 3)))
        hc = np.array(hc)
        mh = min(np.linalg.norm(a - b) for a, b in itertools.combinations(hc, 2))
        assert len(hc) == 12
        assert np.allclose(np.linalg.norm(hc, axis=1), 2)
        assert abs(mh - 2) < 1e-12

    def test_the_chain_of_twelves(self):
        """|A5|/5 = pi(10)/5 = lcm(4,6) = -1/zeta(-1) = 12."""
        import mpmath as mp

        assert 60 // 5 == 12
        assert np.lcm(4, 6) == 12
        assert float(-1 / mp.zeta(-1)) == pytest.approx(12.0, abs=1e-9)


# ═══════════════════ section 12's own checks (migrated) ═══════════════
def one_structure_checks() -> None:
    """Every statement section 12 checked, and the two numbers it printed.

    Migrated from the section (SPEC-002 §1): the check block used to end
    in ``print("all checks: ok")``, the ratio of the two units printed as
    ``eps0*M/pi`` and the vector-ratio table as ``m2/m1 against the
    depth: {6: 2.093, ...} : ok``, and this module read the three back
    from stdout.  Each statement now fails here, on its value, with
    pytest's assertion rewriting: every tolerance is the section's own,
    unchanged, and the two units come from ``kkgt.constants``.
    """

    def vector_ratio(depth_value: float) -> float:
        """m2/m1 of the vector tower at ``depth_value`` = ``phi**d``.

        The section solved ``j0(x/D) y0(x) - y0(x/D) j0(x) = 0`` on
        ``np.linspace(0.3, 12, 3000)`` and divided its second root by
        its first; this is that computation, unchanged.
        """
        epsilon = 1.0 / depth_value

        def equation(x: Any) -> Any:
            return j0(epsilon * x) * y0(x) - y0(epsilon * x) * j0(x)

        grid = np.linspace(0.3, 12, 3000)
        values = equation(grid)
        roots = [
            brentq(equation, float(grid[i]), float(grid[i + 1]))
            for i in range(len(grid) - 1)
            if values[i] * values[i + 1] < 0
        ]
        return roots[1] / roots[0]

    # ── the check block, one assert per Lean theorem the section names ──
    assert abs(EPS0 * M_PCF - np.pi) < 1e-12                   # certainty_principle
    for s in np.linspace(-3, 20, 47):
        assert abs((EPS0 * PHI**s) * (M_PCF * PHI**-s) - np.pi) < 1e-9  # closure_each_level
        assert abs((EPS0 * PHI**s) * (M_PCF * PHI**s)
                   - np.pi * PHI ** (2 * s)) < 1e-6 * PHI ** (2 * s)     # phase_on_cell
        assert abs(PHI ** (s + 1) / PHI**s - PHI) < 1e-12                 # ring_ratio
        z = complex(PHI**s * M_PCF, 0)
        assert abs((z * 1j) / z - 1j) < 1e-12                             # lattice_tower_tau
    assert abs(np.exp(1j * np.pi) + 1) < 1e-15                # fibre_half_turn
    theta = np.linspace(0, 7, 50)
    assert np.allclose(abs(0.5 * np.exp(1j * theta)), 0.5)    # worldline_modulus
    y = np.linspace(-8, 0, 400)
    assert np.allclose(np.exp(y) ** 2 + (1 - np.exp(y) ** 2), 1)  # pseudosphere_unit_speed
    # Clifford torus: stereographic projection from (0,0,0,1) -> surface
    # of revolution R = sqrt2, r = 1
    a, b = np.meshgrid(np.linspace(0, 2 * np.pi, 60), np.linspace(0, 2 * np.pi, 60))
    X = np.stack([np.cos(a), np.sin(a), np.cos(b), np.sin(b)]) / np.sqrt(2)
    P = X[:3] / (1 - X[3])
    rho = np.hypot(P[0], P[1])
    assert np.allclose((rho - np.sqrt(2)) ** 2 + P[2] ** 2, 1,
                       atol=1e-9)                             # clifford_square + stereographic

    # ── the value the section printed with its checks ──────────────────
    assert abs(EPS0 * M_PCF / np.pi - 1.0) <= 1e-12           # "eps0*M/pi = 1.0"

    # ── the five rows of m2/m1 against the depth, at three decimals ───
    for depth, printed in ((6, 2.093), (12, 2.171), (24, 2.228),
                           (30, 2.241), (81.74, 2.275)):
        assert round(vector_ratio(PHI**depth), 3) == printed, depth


# ══════════════════════════════════════════════════════════ section 12 ══
class TestSection12FigureOneStatements:
    """section 12 -- 'One structure seen at once: the checks, the points of Z[i] per level and the vector ratio'

    Figure 1 left this section with the v134 and is drawn by section 44 now;
    what stayed is everything the section checks.
    """

    def test_certainty_principle_eps0_times_m_is_pi(self):
        """eps0 = log phi/(6 sqrt3), M = 6 sqrt(3) pi/log phi -> eps0 M = pi."""
        eps0 = LN_PHI / (6 * math.sqrt(3))
        M = 6 * math.sqrt(3) * math.pi / LN_PHI
        assert abs(eps0 * M - math.pi) < 1e-12

    @pytest.mark.parametrize("s", [-3.0, 0.0, 12.0, 20.0])
    def test_closure_each_level(self, s):
        """(eps0 phi^s)(M phi^-s) = pi at every level."""
        eps0 = LN_PHI / (6 * math.sqrt(3))
        M = 6 * math.sqrt(3) * math.pi / LN_PHI
        assert abs((eps0 * PHI**s) * (M * PHI**-s) - math.pi) < 1e-9

    @pytest.mark.parametrize(
        "s,count,floor_s",
        [(0, 5, 3), (1, 5, 5), (2, 9, 8), (3, 13, 13), (4, 21, 21),
         (5, 37, 34), (6, 57, 56)],
    )
    def test_lattice_points_and_mode_count(self, s, count, floor_s):
        """Points of Z[i] in the disc of area S = pi phi^s, and floor(S)."""
        r2 = PHI**s
        c = sum(1 for a in range(-20, 21) for b in range(-20, 21)
                if a * a + b * b <= r2)
        assert c == count, s
        assert math.floor(math.pi * PHI**s) == floor_s, s

    def test_lattice_points_follow_the_area_on_average(self):
        """count/S = 1.59, 0.98, 1.09, 0.98, 0.98, 1.06, 1.01 (printed to 2 dp)."""
        got = []
        for s in range(7):
            r2 = PHI**s
            c = sum(1 for a in range(-20, 21) for b in range(-20, 21)
                    if a * a + b * b <= r2)
            got.append(round(c / (math.pi * PHI**s), 2))
        assert got == [1.59, 0.98, 1.09, 0.98, 0.98, 1.06, 1.01], got

    def test_ratio_at_sigma_22_is_unity_to_four_decimals(self):
        r2 = PHI**22
        c = sum(1 for a in range(-200, 201) for b in range(-200, 201)
                if a * a + b * b <= r2)
        assert round(c / (math.pi * PHI**22), 4) == 0.9998

    def test_bottom_of_the_throat(self):
        """sigma = 12: 1005 lattice points against floor(S) = 1011."""
        r2 = PHI**12
        c = sum(1 for a in range(-40, 41) for b in range(-40, 41)
                if a * a + b * b <= r2)
        assert c == 1005
        assert math.floor(math.pi * PHI**12) == 1011

    @pytest.mark.parametrize("side,points,projected",
                             [(2, 8, 7), (3, 27, 19), (5, 125, 61),
                              (7, 343, 127), (9, 729, 217)])
    def test_cube_projection_counts(self, side, points, projected):
        """The window {0..side-1}^3 projects onto 3 side^2 - 3 side + 1 points.

        main.tex:1354 asserts the five pairs, so the projection is really
        computed here: the points of the window are projected along
        (1,1,1) onto the plane spanned by (1,-1,0)/sqrt2 and (1,1,-1)/sqrt6
        and the shadows are counted, which is what the section does in 3D.
        """
        n3 = np.array([1, 1, 1]) / 3 ** 0.5
        e1 = np.array([1, -1, 0]) / 2 ** 0.5
        e2 = np.cross(n3, e1)
        pts = np.array(list(itertools.product(range(side), repeat=3)), float)
        assert len(pts) == points
        shadows = {tuple(np.round([p @ e1, p @ e2], 9)) for p in pts}
        assert len(shadows) == projected
        assert len(shadows) == 3 * side * side - 3 * side + 1

    def test_section12_runs_all_of_its_checks(self):
        """The section's checks and the two numbers it printed, on values.

        This test used to run section 12 and read ``all checks: ok``, the
        ``eps0*M/pi`` value (want 1.0, tol 1e-12) and the ``m2/m1 against
        the depth`` table back from its stdout (SPEC-002 §1); the three
        now live in ``one_structure_checks``, which fails on its values.
        The section writes no file, which is what ``run.figures == ()``
        observed: figure 1 belongs to section 44 and section 12 carries
        no figure in ``FIGURES``.
        """
        one_structure_checks()
        assert 12 not in FIGURES, FIGURES


# ══════════════════════════════════════════════════════════ section 13 ══
class TestSection13FigureTwoReciprocity:
    """section 13 -- 'Figure 2: the two reciprocal families'"""

    @pytest.mark.parametrize("s", range(12, 19))
    def test_radius_times_period_is_constant(self, s):
        """z(s) tau(s) = phi^-6 for every level: the two families are reciprocal."""
        rz = PHI ** (s - 18)
        rt = PHI ** -(s - 12)
        assert rz * rt == pytest.approx(PHI**-6, abs=1e-12)

    @pytest.mark.parametrize("s", [12, 15, 18])
    def test_half_turn_per_level_eps_tau_is_pi(self, s):
        eps0 = LN_PHI / (6 * math.sqrt(3))
        M = 6 * math.sqrt(3) * math.pi / LN_PHI
        assert abs((eps0 * PHI**s) * (M * PHI**-s) - math.pi) < 1e-12

    @pytest.mark.figure
    def test_section13_draws_figure_two(self):
        """Figure 2: the section's statement holds and the artifact is pinned.

        Section 13 used to run here through the section-run fixture and
        this test read its ``ok`` sentinel back from stdout; the sentinel
        only certified the section's own loop -- z(s) tau(s) = phi^-6 at
        every level 12..18 -- which is asserted here on its value with
        the section's own 1e-12 (SPEC-002 §1).  The drawing belongs to
        ``pnpm run figures`` (SPEC-002 §1.1), so only the committed bytes
        are verified here.
        """
        for s in range(12, 19):
            z, tau = PHI ** (s - 18), PHI ** -(s - 12)
            assert abs(z * tau - PHI**-6) < 1e-12, s
        # section 13 checks figure 2 but no longer draws it (SPEC-002 §1.1)
        verify_figure_artifact("fig_mobius_throat.pdf")


# ══════════════════════════════════════════════════════════ section 14 ══
class TestSection14RingGaps:
    """section 14 -- 'Three gaps of the marks on the ring (6.1)'"""

    @staticmethod
    def _gap_count(a, k):
        x = sorted((n * a) % 1 for n in range(k))
        g = [x[i + 1] - x[i] for i in range(k - 1)] + [1 - x[-1] + x[0]]
        return len(set(round(v, 9) for v in g))

    @pytest.mark.parametrize(
        "s,n_printed,counts",
        [
            (1, 2.618, [3, 3, 3]),
            (2, 6.854, [3, 3, 3]),
            (3, 17.944, [3, 3, 3]),
            (4, 46.979, [3, 3, 3]),
            (5, 122.992, [2, 3, 3]),
            (6, 321.997, [2, 3, 3]),
        ],
    )
    def test_three_gaps_of_the_marks(self, s, n_printed, counts):
        """Marks at step phi^-2s on the ring: three gaps (two at large s)."""
        a = PHI ** (-2 * s)
        assert round(PHI ** (2 * s), 3) == n_printed
        got = [self._gap_count(a, k) for k in (100, 1000, 10000)]
        assert got == counts, (s, got)

    @pytest.mark.parametrize("s", range(1, 7))
    def test_discrepancy_stays_below_half_a_percent(self, s):
        a = PHI ** (-2 * s)
        k = 10000
        x = [(n * a) % 1 for n in range(k)]
        d = max(abs(sum(1 for v in x if v < t) / k - t)
                for t in [i / 50 for i in range(51)])
        assert d < 0.005, (s, d)


# ══════════════════════════════════════════════════════════ section 15 ══
class TestSection15StateCount:
    """section 15 -- 'Exact count of states with c=3 at the level N/2 against S (6.1)'"""

    @staticmethod
    def _partition(max_n=3000):
        """prod (1-q^n)^-3:  n p(n) = 3 sum_k sigma(k) p(n-k)."""
        sig = [0] * (max_n + 1)
        for d in range(1, max_n + 1):
            for k in range(d, max_n + 1, d):
                sig[k] += d
        p = [0] * (max_n + 1)
        p[0] = 1
        for n in range(1, max_n + 1):
            p[n] = 3 * sum(sig[k] * p[n - k] for k in range(1, n + 1)) // n
        return p

    @pytest.mark.parametrize(
        "s,l0,lnw,s_entropy,ratio",
        [
            (1, 1, 1.099, 4.443, 0.2473),
            (3, 9, 7.299, 13.329, 0.5476),
            (5, 61, 25.987, 34.700, 0.7489),
            (7, 421, 79.624, 91.160, 0.8735),
            (9, 2889, 224.406, 238.802, 0.9397),
        ],
    )
    def test_count_against_the_entropy(self, s, l0, lnw, s_entropy, ratio):
        """L0 = round(N/2), ln W from the c=3 partition function, S = pi sqrt(N)."""
        p = self._partition()
        n = PHI ** (2 * s)
        assert round(n / 2) == l0, s
        ln_w = math.log(p[l0])
        s_ent = math.pi * math.sqrt(2 * l0)
        assert ln_w == pytest.approx(lnw, abs=5e-4), s
        assert s_ent == pytest.approx(s_entropy, abs=5e-4), s
        assert round(ln_w / s_ent, 4) == ratio, s

    def test_cardy_correction_settles(self):
        """S - ln W - (3/2) ln L0 tends to a constant of order 2.44."""
        p = self._partition()
        vals = []
        for s in range(3, 10):
            l0 = round(PHI ** (2 * s) / 2)
            s_ent = math.pi * math.sqrt(2 * l0)
            vals.append(s_ent - math.log(p[l0]) - 1.5 * math.log(l0))
        printed = [2.7337, 2.6203, 2.5463, 2.5004, 2.4722, 2.4546, 2.4437]
        assert vals == pytest.approx(printed, abs=5e-5)
        assert vals[-1] < vals[0]


# ══════════════════════════════════════════════════════════ section 16 ══
class TestSection16KoideFromM:
    """section 16 -- 'The scale M of (F1): Koide-type reconstruction of the lepton masses'"""

    OBS = {"e": 0.51099895, "mu": 105.6583755, "tau": M_TAU_MEV}

    @staticmethod
    def _koide(m_scale=M_KOIDE_MEV, delta=2 / 9):
        """m_k = M (1 + sqrt2 cos(delta + 2 pi k/3))^2, sorted."""
        return sorted(
            m_scale * (1 + math.sqrt(2) * math.cos(delta + 2 * math.pi * k / 3)) ** 2
            for k in range(3)
        )

    @pytest.mark.parametrize("name", ["e", "mu", "tau"])
    def test_reconstruction_is_below_one_part_in_ten_thousand(self, name):
        got = self._koide()
        for (n, obs), x in zip(self.OBS.items(), got):
            if n == name:
                rel = abs(x - obs) / obs
                assert rel < 1e-4, (name, x, obs, rel)

    def test_printed_values(self):
        """The two lines section 16 printed, on their values.

        ``Koide from M:  1776.8761`` is the tau row, asserted to half a
        unit of the four decimals it printed; ``rel. 6.1e-05`` is the
        electron's relative error, printed to two significant figures
        (half a unit of its last digit).  The section used to print both
        and this test read them back from stdout (SPEC-002 §1).
        """
        got = self._koide()          # sorted: e, mu, tau
        assert got[2] == pytest.approx(1776.8761, abs=5e-5)
        rel_e = abs(got[0] - self.OBS["e"]) / self.OBS["e"]
        assert rel_e == pytest.approx(6.1e-05, abs=5e-7)
