"""Deep numeric tests for sections 9-16 of kkgt.sections.

Sections 9-11 (granularity and contact configurations), 12 (the checks
behind figure 1, now drawn by section 44) and 13 (figure 2, with its
exact statements), 14-16 (gaps, state count, Koide).
"""

from __future__ import annotations

import itertools
import math

import numpy as np
import pytest

from kkgt.constants import LN_PHI, M_KOIDE_MEV, PHI


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
        """phi never leaves the phi^2 ratio; the phase step reaches 17.542."""
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

    def test_section12_runs_all_of_its_checks(self, run_section):
        run = run_section(12)
        run.has("all checks: ok")
        run.value(r"eps0\*M/pi = ([\d.]+)", want=1.0, tol=1e-12, label="eps0 M/pi")
        run.has("m2/m1 against the depth: {6: 2.093, 12: 2.171, 24: 2.228, "
                "30: 2.241, 81.74: 2.275} : ok")
        assert run.figures == (), run.figures


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
    def test_section13_draws_figure_two(self, run_section):
        run = run_section(13)
        assert run.stdout.strip() == "ok", run.stdout
        assert "fig_mobius_throat.pdf" in run.figures


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
        assert vals == pytest.approx(printed, abs=5e-4)
        assert vals[-1] < vals[0]


# ══════════════════════════════════════════════════════════ section 16 ══
class TestSection16KoideFromM:
    """section 16 -- 'The scale M of (F1): Koide-type reconstruction of the lepton masses'"""

    OBS = {"e": 0.51099895, "mu": 105.6583755, "tau": 1776.86}

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

    def test_printed_values(self, run_section):
        run = run_section(16)
        run.has("Koide from M:  1776.8761")
        assert "rel. 6.1e-05" in run.stdout
