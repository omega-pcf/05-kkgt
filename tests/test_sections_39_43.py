"""Deep numeric tests for sections 39-43 of reproduce_v108.py.

The tilings (figures 4 and 5), the dictionary of section 40 and the three
columns of section 43 -- the last section main.tex cites (``section~43``).
"""

from __future__ import annotations

import itertools
import math
import re

import numpy as np
import pytest

from kkgt.constants import LN_PHI, M_PCF, PHI


# ══════════════════════════════════════════════════════════ section 39 ══
class TestSection39FibonacciTiling:
    """section 39 -- 'El throat con el teselado de Fibonacci de sus anillos (Figura 4)'"""

    @staticmethod
    def words(n=7):
        w = ["AAB"]
        for _ in range(n - 1):
            w.append("".join({"A": "AB", "B": "A"}[c] for c in w[-1]))
        return w

    @staticmethod
    def bounds(w):
        width = [1 if c == "A" else 1 / PHI for c in w]
        c = np.cumsum([0] + width)
        return c / c[-1]

    @pytest.mark.parametrize(
        "s,a,b",
        [(0, 2, 1), (1, 3, 2), (2, 5, 3), (3, 8, 5), (4, 13, 8), (5, 21, 13),
         (6, 34, 21)],
    )
    def test_tile_counts_are_fibonacci(self, s, a, b):
        """A_sigma long and B_sigma short tiles: F_{s+3} and F_{s+2}."""
        w = self.words()[s]
        assert (w.count("A"), w.count("B")) == (a, b), s

    @pytest.mark.parametrize("s", range(7))
    def test_weighted_sum_is_the_entropy(self, s):
        """S = pi (A/phi^2 + B/phi^3) = pi phi^s exactly (rel. 1e-12)."""
        w = self.words()[s]
        a, b = w.count("A"), w.count("B")
        weighted = math.pi * (a / PHI**2 + b / PHI**3)
        assert weighted == pytest.approx(math.pi * PHI**s, rel=1e-12), s

    @pytest.mark.parametrize("s", range(6))
    def test_boundaries_nest(self, s):
        """Every boundary of ring s is a boundary of ring s+1 (they nest)."""
        b0, b1 = self.bounds(self.words()[s]), self.bounds(self.words()[s + 1])
        assert all(np.min(np.abs(b1 - x)) < 1e-12 for x in b0), s

    @pytest.mark.parametrize("s,printed",
                             [(0, 3), (1, 5), (2, 8), (3, 13), (4, 21), (5, 34),
                              (6, 56)])
    def test_mode_count_is_floor_of_s(self, s, printed):
        assert math.floor(math.pi * PHI**s) == printed, s

    @pytest.mark.figure
    def test_section39_draws_figure_four(self, run_section):
        run = run_section(39)
        assert "fig_throat_tiling.pdf" in run.figures
        run.has("S = pi(A/phi^2+B/phi^3) exacto; fronteras anidadas")


# ══════════════════════════════════════════════════════════ section 40 ══
class TestSection40DictionaryAgainstTheCusp:
    """section 40 -- 'El diccionario sobre un teselado regular frente a la cuspide'"""

    @pytest.mark.parametrize(
        "s,legs",
        [(0, 7), (1, 14), (2, 28), (3, 35), (4, 56), (5, 84), (6, 133),
         (7, 217), (8, 350), (9, 567), (10, 938), (11, 1484), (12, 2443)],
    )
    def test_open_legs_of_73(self, s, legs, run_section):
        """Open legs the {7,3} boundary cuts at each level (Crofton)."""
        run = run_section(40)
        m = run.match(r"\{7,3\}: patas abiertas \[([^\]]+)\]")
        got = [int(v) for v in m.group(1).split(",")]
        assert got[s] == legs, (s, got)

    def test_crofton_constant(self, run_section):
        """Legs/S fluctuates about the constant 2.4097 of the tiling."""
        run = run_section(40)
        run.value(
            r"constante de Crofton ([\d.]+)", want=2.4097, tol=5e-5,
            label="Crofton",
        )

    @pytest.mark.parametrize(
        "s,pairs,best",
        [(0, 172, (20, 3, 3)), (1, 22, None), (2, 2, None), (3, 1, None),
         (4, 0, None)],
    )
    def test_pairs_that_reproduce_s_on_average(self, s, pairs, best, run_section):
        """Of the 50340 (tiling, chi) pairs only 172 give S within 1%."""
        run = run_section(40)
        assert run.has("pares (teselado, chi<=16), p,q<=60: 50340")
        m = run.match(r"a menos de 1e-2\.\.1e-6: \[([^\]]+)\]")
        got = [int(v) for v in m.group(1).split(",")]
        assert got[s] == pairs, (s, got)
        if best is not None:
            run.has("mejor (20, 3, 3) a 3.34e-06")

    def test_unweighted_count_tends_to_a_fixed_fraction(self):
        """F_{s+4} -> 0.9757 S: the limit is phi^4/(sqrt5 pi)."""
        limit = PHI**4 / (math.sqrt(5) * math.pi)
        assert round(limit, 4) == 0.9757, limit

    @pytest.mark.parametrize("power,printed", [(2, 3.32), (3, 2.099)])
    def test_equivalent_bond_dimensions(self, power, printed):
        """e^(pi/phi^2) = 3.32 and e^(pi/phi^3) = 2.099 are not integers."""
        got = math.exp(math.pi / PHI**power)
        assert round(got, 3) == printed, (power, got)

    @pytest.mark.parametrize("s,area", [(1.483259, 2 * math.pi / PHI**3)])
    def test_two_prototiles_keep_their_areas(self, s, area):
        """The long prototile has area 2pi/phi^3, the short one is that / phi."""
        assert s == pytest.approx(area, rel=1e-6)
        assert area / PHI == pytest.approx(0.916704, rel=1e-6)

    def test_distinct_arc_weights_of_73(self, run_section):
        """{7,3} needs 115 distinct arc weights over sigma = 0..9, the throat 2."""
        run = run_section(40)
        m = run.match(
            r"por nivel \[([^\]]+)\] , 115 en total; el throat: 2 en todos los niveles"
        )
        got = [int(v) for v in m.group(1).split(",")]
        assert got == [1, 2, 3, 3, 5, 7, 10, 16, 27, 41], got

    @pytest.mark.parametrize(
        "s,count,floor_s",
        [(0, 5, 3), (3, 13, 13), (6, 57, 56)],
    )
    def test_lattice_points_again(self, s, count, floor_s):
        """Section 40 repeats the Z[i] count of section 12 (same numbers)."""
        r2 = PHI**s
        c = sum(1 for a in range(-20, 21) for b in range(-20, 21)
                if a * a + b * b <= r2)
        assert c == count, (s, c)
        assert math.floor(math.pi * PHI**s) == floor_s


# ══════════════════════════════════════════════════════════ section 41 ══
class TestSection41FiveRegularTilings:
    """section 41 -- 'Cinco teselados regulares frente a los niveles (Figura 5)'"""

    def test_circumradius_inradius_and_edge(self):
        """cosh e = phi for {5,4}, sinh r = phi for {6,10} (exact)."""
        e = 2 * math.acosh(math.cos(math.pi / 5) / math.sin(math.pi / 4))
        assert math.cosh(e) == pytest.approx(PHI, abs=1e-10)
        r = math.acosh(math.cos(math.pi / 10) / math.sin(math.pi / 6))
        assert math.sinh(r) == pytest.approx(PHI, abs=1e-10)

    @pytest.mark.parametrize("n", [15, 20, 25])
    def test_hurwitz_constant_of_phi(self, n):
        """|phi - F_{n+1}/F_n| F_n^2 -> 1/sqrt5 = 0.44721.

        n is kept in 15..25: below it the convergent has not converged, above
        it the product loses float64 precision (at n = 40 it underflows to 0).
        """
        f = [0, 1]
        for _ in range(n + 3):
            f.append(f[-1] + f[-2])
        q, p = f[n + 1], f[n + 2]
        const = abs(PHI - p / q) * q * q
        assert const == pytest.approx(1 / math.sqrt(5), abs=1e-5), (n, const)

    @pytest.mark.parametrize("n", [5, 10, 15])
    def test_hurwitz_constant_of_sqrt2(self, n):
        """sqrt(2) has constant 1/(2 sqrt2) = 0.35355 < 1/sqrt5."""
        p, q = 1, 1
        for _ in range(n):                 # convergents of [1;2,2,2,...]
            p, q = p + 2 * q, p + q
        const = abs(math.sqrt(2) - p / q) * q * q
        assert const == pytest.approx(1 / (2 * math.sqrt(2)), abs=5e-5), (n, const)
        assert const < 1 / math.sqrt(5)

    @pytest.mark.parametrize(
        "tiling,printed",
        [((7, 3), 2.618), ((3, 7), 1.6), ((5, 4), 2.618), ((12, 5), 10.824),
         ((6, 10), 4.992)],
    )
    def test_layer_growth(self, tiling, printed, run_section):
        """Only {7,3} and {5,4} grow by phi^2 per layer (the level step)."""
        run = run_section(41)
        full = re.search(r"crecimiento por capa \(aristas\): (\{.*?\}) ;", run.stdout)
        assert full, run.stdout
        got = {
            (int(a), int(b)): float(v)
            for a, b, v in re.findall(r"\((\d+), (\d+)\): ([\d.]+)", full.group(1))
        }
        assert got[tiling] == pytest.approx(printed, abs=5e-4), (tiling, got)

    @pytest.mark.parametrize(
        "tiling,series",
        [
            ((7, 3), [1, 8, 8, 29, 29, 57, 99]),
            ((12, 5), [1, 1, 1, 1, 1, 1, 1]),
            ((6, 10), [1, 1, 1, 1, 7, 7, 7]),
        ],
    )
    def test_tiles_inside_the_disc(self, tiling, series, run_section):
        run = run_section(41)
        p, q = tiling
        m = run.match(rf"\{{{p},{q}\}}: \[([^\]]+)\]")
        got = [int(v) for v in m.group(1).split(",")]
        assert got == series, (tiling, got)

    @pytest.mark.slow
    def test_section41_prints_its_conclusions(self, run_section):
        """Full stdout contract of the slow section 41 (figure 5)."""
        run = run_section(41)
        assert "fig_tilings_strip.pdf" in run.figures
        run.has("{3,7} por vertices compartidos: [1, 15, 45, 120, 315, 825, 2160]")
        run.has("0.999902 (Hurwitz: phi es el peor aproximado)")
        run.has("borde de un nivel tangente a aristas: solo {6,10}")
        run.has("{5,4} con qubits: 1.4907 S")

    @pytest.mark.slow
    def test_qubit_bond_dimension_of_54(self, run_section):
        """One qubit per bond on {5,4} gives 1.4907 S (main.tex quotes it)."""
        run_section(41).value(
            r"\{5,4\} con qubits: ([\d.]+) S", want=1.4907, tol=5e-4,
            label="{5,4} qubits",
        )


# ══════════════════════════════════════════════════════════ section 42 ══
class TestSection42TwoCoordinatesAndTheStep:
    """section 42 -- 'Las dos coordenadas, el paso de nivel, la ortogonalizacion, el paso racional y el operador de imp:A1'"""

    F = [0, 1] + [0] * 40

    @classmethod
    def fib(cls):
        f = [0, 1]
        for _ in range(40):
            f.append(f[-1] + f[-2])
        return f

    @pytest.mark.parametrize("s", [1, 2, 3, 6, 12])
    def test_phi_to_the_s_is_a_unit(self, s):
        """phi^s = a + b phi with norm (-1)^s, and M|a + b phi_bar| = M phi^-s.

        The second coordinate is the weld time tau(s) of main.tex.
        """
        f = self.fib()
        a, b = f[s - 1], f[s]
        assert a * a + a * b - b * b == (-1) ** s
        psi = (1 - 5 ** 0.5) / 2                      # Galois conjugate of phi
        m = 6 * math.sqrt(3) * math.pi / LN_PHI
        assert abs(m * abs(a + b * psi) - m * PHI**-s) < 1e-9, s

    def test_weld_time_at_the_bottom(self):
        """tau(12) = M_PCF phi^-12 = 0.2107 (main.tex: 'at the bottom, tau(12)=0.2107')."""
        assert M_PCF * PHI**-12 == pytest.approx(0.2107, abs=5e-5)

    @staticmethod
    def sub(w):
        return "".join("AB" if c == "A" else "A" for c in w)

    @pytest.mark.parametrize("s,counts", [(0, (1, 2)), (5, (8, 13)), (11, (144, 233))])
    def test_ring_word_is_the_fibonacci_rotations(self, s, counts):
        """I3: (B, A) = (F_{s+2}, F_{s+3}) in the word of ring s."""
        w = "AAB"
        f = self.fib()
        for _ in range(s):
            w = self.sub(w)
        assert (w.count("B"), w.count("A")) == (f[s + 2], f[s + 3]), s

    def test_substitution_matrix_is_exchange_times_shift(self):
        """I2: [[0,1],[1,0]] [[1,0],[1,1]] = [[1,1],[1,0]] (A -> AB, B -> A)."""
        ex, sh = [[0, 1], [1, 0]], [[1, 0], [1, 1]]
        prod = [[sum(ex[i][k] * sh[k][j] for k in range(2)) for j in range(2)]
                for i in range(2)]
        assert prod == [[1, 1], [1, 0]]

    @pytest.mark.parametrize("p,expected", [(0.3, 0.4), (0.5, 0.0), (0.7, 0.4)])
    def test_orthogonalisation_at_the_half_turn(self, p, expected):
        """I4: |1 - p + p e^{i pi}| = |1 - 2p| vanishes only at p = 1/2."""
        ov = abs((1 - p) + p * complex(math.cos(math.pi), math.sin(math.pi)))
        assert ov == pytest.approx(expected, abs=1e-12)
        assert (ov < 1e-12) == (p == 0.5)

    @pytest.mark.parametrize(
        "p,q,dev_bg,dev_obs",
        [(21, 13, 0.8, 71.2), (34, 21, 0.3, 27.1), (55, 34, 0.1, 10.4),
         (89, 55, 0.0, 4.0), (144, 89, 0.0, 1.5), (233, 144, 0.0, 0.6)],
    )
    def test_rational_step_versus_the_contrast(self, p, q, dev_bg, dev_obs):
        """I5: a rational step p/q moves the background and the observer level."""
        f = LN_PHI / math.log(p / q)
        bg = abs(11.97 * f - 11.97) / 0.05
        obs = abs(583.789 * f - 583.789) / 0.028
        assert round(bg, 1) == dev_bg, (p, q, bg)
        assert round(obs, 1) == dev_obs, (p, q, obs)

    def test_three_sigma_criterion(self):
        """From 144/89 on the reading stays within 3 sigma of the golden one."""
        devs = []
        for p, q in [(21, 13), (34, 21), (55, 34), (89, 55), (144, 89),
                     (233, 144)]:
            f = LN_PHI / math.log(p / q)
            devs.append(abs(583.789 * f - 583.789) / 0.028)
        assert devs[0] > 70
        assert devs[3] > 3
        assert devs[4] < 3
        assert all(d < 3 for d in devs[4:])

    @pytest.mark.parametrize(
        "s,norm", [(1, -1), (2, 1), (3, -1), (4, 1), (5, -1), (6, 1)]
    )
    def test_alternating_norm(self, s, norm):
        f = self.fib()
        a, b = f[s - 1], f[s]
        assert a * a + a * b - b * b == norm

    def test_trace_three_and_the_shortest_geodesic(self):
        """I6: tr = phi^2 + phi^-2 = 3, and 2 arccosh(3/2) = 4 log phi = 1.924847."""
        assert PHI**2 + PHI**-2 == pytest.approx(3.0, abs=1e-12)
        assert 2 * math.acosh(1.5) == pytest.approx(4 * LN_PHI, abs=1e-12)
        assert round(2 * math.acosh(1.5), 6) == 1.924847

    @pytest.mark.parametrize(
        "n,printed",
        [(0, 1.99), (1, 1.48), (2, 1.31), (4, 1.17), (5, 1.13), (11, 1.02)],
    )
    def test_mass_ratios_of_imp_a1(self, n, printed):
        """I7: successive mass ratios of imp:A1 at n = 6; none of them is phi."""
        nlev = 6
        m = [2 * math.sin(k * math.pi / (4 * (nlev + 1))) / LN_PHI
             for k in range(1, 2 * nlev + 2)]
        r = [m[k + 1] / m[k] for k in range(len(m) - 1)]
        assert round(r[n], 2) == printed, (n, r[n])
        assert all(abs(x - PHI) > 0.05 for x in r)


# ══════════════════════════════════════════════════════════ section 43 ══
class TestSection43ThreeColumns:
    """section 43 -- 'Las tres columnas y por que no encajaban'"""

    @staticmethod
    def _collisions(slope):
        seen = set()
        count = 0
        for m in range(-60, 61):
            for k in range(-60, 61):
                v = round(m + k * slope, 9)
                if v in seen:
                    count += 1
                seen.add(v)
        return count

    @pytest.mark.parametrize("slope,printed", [(1.5, 14042), (PHI, 0)])
    def test_rational_step_has_a_kernel(self, slope, printed):
        """A step p/q collapses pairs of Z^2; phi collapses none (Lean:
        rational_step_kernel, golden_rotation_aperiodic)."""
        assert self._collisions(slope) == printed, slope

    def test_the_three_columns_of_irrational_unimodular_pisot(self):
        """R11: two-letter primitive substitutions with entries <= 3."""
        ok123, ok4 = set(), set()
        for a, b, c, d in itertools.product(range(4), repeat=4):
            if b == 0 or c == 0:
                continue
            tr, de = a + d, a * d - b * c
            disc = tr * tr - 4 * de
            if disc <= 0:
                continue
            r = math.sqrt(disc)
            lam, mu = (tr + r) / 2, (tr - r) / 2
            if int(round(r)) ** 2 != disc and abs(de) == 1 and abs(mu) < 1:
                ok123.add(round(lam, 4))
                if (tr, de) == (1, -1):
                    ok4.add(round(lam, 4))
        assert round(1 + 2 ** 0.5, 4) in ok123
        assert ok4 == {round(PHI, 4)}, ok4
        assert sorted(ok123) == [1.618, 2.4142, 2.618, 3.3028, 3.7321, 4.2361]

    def test_cube_diagonal_projection(self):
        """The three projected axes have length sqrt(2/3) at 120 degrees."""
        n = np.array([1, 1, 1]) / 3 ** 0.5
        p = [e - (e @ n) * n for e in np.eye(3)]
        ang = {
            round(math.degrees(math.acos(
                p[i] @ p[j] / (np.linalg.norm(p[i]) * np.linalg.norm(p[j]))
            )), 6)
            for i, j in [(0, 1), (1, 2), (0, 2)]
        }
        assert ang == {120.0}
        assert np.allclose(sum(p), 0)
        assert np.linalg.norm(p[0]) == pytest.approx(math.sqrt(2 / 3), abs=1e-12)

    def test_binet_deviation_of_the_tile_count(self):
        """F_{s+4} - phi^4 S/(sqrt5 pi) = +- phi^{-(s+4)}/sqrt5 for s = 0..24."""
        f = [0, 1]
        for _ in range(40):
            f.append(f[-1] + f[-2])
        for s in range(25):
            s_ent = math.pi * PHI**s
            dev = f[s + 4] - PHI**4 * s_ent / (math.sqrt(5) * math.pi)
            assert abs(abs(dev) - PHI ** -(s + 4) / math.sqrt(5)) < 1e-6, s

    @pytest.mark.parametrize("n,printed", [((2, 3), 0.95), ((1, 2), 0.88),
                                           ((1, 1), 0.70)])
    def test_bragg_peaks_of_the_fibonacci_chain(self, n, printed):
        """Fourier amplitudes of the cut-and-project chain: 0.95, 0.88, 0.70
        at the module points, at most 0.010 at random ones (N = 46368)."""
        w = "A"
        for _ in range(22):
            w = "".join("AB" if ch == "A" else "A" for ch in w)
        x = np.concatenate([[0], np.cumsum([PHI if ch == "A" else 1.0
                                            for ch in w])])[:-1]
        assert len(x) == 46368
        amp = lambda k: abs(np.exp(2j * math.pi * k * x).sum()) / len(x)
        d = PHI + 2
        m_, n_ = n
        got = amp((m_ + n_ * PHI) / d)
        assert round(got, 2) == printed, (n, got)

    def test_bragg_random_level(self):
        w = "A"
        for _ in range(22):
            w = "".join("AB" if ch == "A" else "A" for ch in w)
        x = np.concatenate([[0], np.cumsum([PHI if ch == "A" else 1.0
                                            for ch in w])])[:-1]
        amp = lambda k: abs(np.exp(2j * math.pi * k * x).sum()) / len(x)
        rng = np.random.default_rng(1)
        rnd = max(amp(k) for k in rng.uniform(0.05, 2.5, 200))
        assert round(rnd, 3) == 0.010, rnd
        assert rnd < 0.02

    @pytest.mark.parametrize(
        "block",
        [
            "pendiente 3/2 -> 14042 coincidencias; pendiente phi -> 0",
            "cuenta de teselas: F_{s+4} - 0.9757 S",
            "Bragg (N = 46368): (2,3) 0.95, (1,2) 0.88, (1,1) 0.70",
        ],
    )
    def test_section43_stdout(self, run_section, block):
        run_section(43).has(block)
