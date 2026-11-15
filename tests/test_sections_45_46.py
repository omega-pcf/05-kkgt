"""Deep numeric tests for sections 45 and 46 of kkgt.sections.

Section 45 is the (F10) block: the observer level along LCDM with the
Planck values, the compression limit where 4 pi z^2/(4 G_N) meets pi z,
the two constants (W4 patch, W8 throat) that coincide only in d = 4, and
the causal chart whose two halves cross at the static patch.  Section 46
is the Hopf foliation of the window: the flat tori of modulus i tan eta,
the antipodal map J of the base, the SU(2) transitivity of the fibres and
the window weight that crosses 1/2 at n = 1.5702.

Everything the sections assert, these tests recompute from the closed
form; the numbers that only exist inside a section are read from its
stdout with the width of the printed precision as tolerance.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from kkgt.constants import LN_PHI, PHI

# Planck 2018 values section 45 uses: t_P = 5.391247e-44 s, the observer
# length l = sqrt2 t_P, 1 Mpc = 3.0856775814913673e22 m, H0 = 67.36 km/s/Mpc,
# Omega_m = 0.3153, Omega_r = 9.0e-5 (the section prints the levels they give).
_T_PLANCK_S = 5.391247e-44
_MPC_M = 3.0856775814913673e22
_H0 = 67.36e3 / _MPC_M
_OM, _OR = 0.3153, 9.0e-5
_OL = 1 - _OM - _OR
_L = math.sqrt(2) * _T_PLANCK_S          # the observer length


def _level(hubble: float) -> float:
    """sigma = log_phi(6 / (3 (H l)^2)), the level of section 45."""
    return math.log(6 / (3 * (hubble * _L) ** 2)) / LN_PHI


# ══════════════════════════════════════════════════════════ section 45 ══
class TestSection45ObserverLevel:
    """section 45 -- 'The observer level in LCDM, the story of (F10), the throat constant and the half'"""

    @pytest.mark.parametrize("log_a,level", [(-34, None), (-10, None),
                                              (0, 583.09), (4, 583.88)])
    def test_the_level_along_lcdm_rises_to_the_asymptote(self, log_a, level):
        """3H^2 = 6pi/S_H: the level falls as 3H^2 falls, so it rises with a.

        Today (a = 1) it is 583.09 and it settles at the asymptote 583.88;
        between the two it never goes down (the section asserts the same
        monotonicity on the 4000 points of logspace(-34, 4)).
        """
        a = 10.0 ** log_a
        hubble = _H0 * math.sqrt(_OR * a ** -4 + _OM * a ** -3 + _OL)
        if level is not None:
            assert _level(hubble) == pytest.approx(level, abs=5e-3)
        grid = np.logspace(-34, 4, 4000)
        s = np.array([_level(_H0 * math.sqrt(_OR * x ** -4 + _OM * x ** -3 + _OL))
                      for x in grid])
        assert np.all(np.diff(s) > -1e-9)
        assert s[0] < s[-1]

    def test_the_asymptotic_and_today_levels_are_the_printed_two(self):
        """Planck: 583.88 asymptotic, 583.09 today, the latter below."""
        s_inf = _level(_H0 * math.sqrt(_OL))
        s_hoy = _level(_H0)
        assert s_inf == pytest.approx(583.877, abs=5e-3)
        assert s_hoy == pytest.approx(583.090, abs=5e-3)
        assert s_hoy < s_inf

    def test_three_h_squared_is_the_entropy_of_the_horizon(self):
        """3 (H l)^2 pi phi^sigma = 6 pi at every scale factor (rel. 1e-12)."""
        for a in np.logspace(-34, 4, 500):
            hubble = _H0 * math.sqrt(_OR * a ** -4 + _OM * a ** -3 + _OL)
            s = _level(hubble)
            got = 3 * (hubble * _L) ** 2 * math.pi * PHI ** s
            assert got == pytest.approx(6 * math.pi, rel=1e-12), a

    def test_the_compression_limit_is_half_a_cell(self):
        """4 pi z^2/(4 G_N) = pi z only at z = 1/2: sigma = -log_phi 2, S = pi/2."""
        lam = math.log(2) / LN_PHI
        assert PHI ** -lam == pytest.approx(0.5, abs=1e-12)
        assert math.pi * PHI ** -lam == pytest.approx(math.pi / 2, abs=1e-12)
        # the crossing of 2 pi z^2 and pi z on (0, 1/2)
        z = np.linspace(0.01, 3, 30000)
        cruce = z[np.argmin(np.abs(2 * np.pi * z ** 2 - np.pi * z))]
        assert cruce == pytest.approx(0.5, abs=1e-3)
        assert np.all(2 * np.pi * z[z < 0.5] ** 2 < np.pi * z[z < 0.5])
        assert -lam == pytest.approx(-1.4404, abs=5e-5)

    def test_a_doubling_is_not_a_bit(self):
        """The first expansion doubles the radius: Delta S = 2.266 bits."""
        lam = math.log(2) / LN_PHI
        s0, shalf = math.pi, math.pi * PHI ** -lam
        assert s0 == pytest.approx(2 * shalf, abs=1e-12)
        delta_bits = (s0 - shalf) / math.log(2)
        assert delta_bits == pytest.approx(2.266, abs=5e-4)

    def test_only_four_dimensions_share_the_two_constants(self):
        """Lambda(0) = 3/G_N = 6 (W4) and |Lambda_5| = d(d-1)/2 (W8): d = 4 only."""
        g_n = 0.5
        omega = lambda k: 2 * math.pi ** ((k + 1) / 2) / math.gamma((k + 1) / 2)
        equal = [
            d for d in range(3, 30)
            if math.isclose(
                (d - 1) * (d - 2) / 2 * (omega(d - 2) / (4 * g_n * math.pi))
                ** (2 / (d - 2)),
                d * (d - 1) / 2, rel_tol=1e-9, abs_tol=1e-12)
        ]
        assert equal == [4]
        assert 3 * math.pi / (g_n * math.pi) == 6          # Lambda(0) = 3/G_N
        assert 4 * 3 / 2 == 6                              # |Lambda_5| at d = 4

    def test_the_number_of_pi_cells_is_122(self):
        """3H^2(0)/Lambda_obs = phi^583.79 = 10^122.00 pi cells (by construction)."""
        r = 583.79 * math.log10(PHI)
        assert abs(r - 122.0) < 0.01
        # Lambda S = 6 pi along the whole tower
        assert PHI ** -583.79 * PHI ** 583.79 == pytest.approx(1.0, abs=1e-12)

    def test_the_static_patch_is_a_quarter(self):
        """X0 + X4 > 0 is the causal future; the two halves meet on a quarter."""
        rng = np.random.default_rng(1)
        n = 50000
        t = rng.uniform(-math.pi / 2, math.pi / 2, n) * 0.999
        chi = rng.uniform(0, math.pi, n)
        tau = np.arcsinh(np.tan(t))
        x0, x4 = np.sinh(tau), np.cosh(tau) * np.cos(chi)
        future = chi < t + math.pi / 2
        past = chi < math.pi / 2 - t
        assert np.array_equal(x0 + x4 > 0, future)
        assert np.array_equal(x4 - x0 > 0, past)
        assert np.array_equal(future & past, chi < math.pi / 2 - np.abs(t))
        assert abs(future.mean() - 0.5) < 0.02

    @pytest.mark.parametrize("l_,t_,r_",
                             [(1, 0.3, 2), (2.5, -1, 0.7), (0.4, 3, 5)])
    def test_the_planar_patch_is_positive(self, l_, t_, r_):
        """X0 + X4 = l e^{t/l} > 0 for every (l, t, r) the section checks."""
        left = (l_ * math.sinh(t_ / l_) + r_ ** 2 / (2 * l_) * math.exp(t_ / l_)) \
            + (l_ * math.cosh(t_ / l_) - r_ ** 2 / (2 * l_) * math.exp(t_ / l_))
        assert left == pytest.approx(l_ * math.exp(t_ / l_), abs=1e-9)
        assert left > 0

    def test_section45_prints_the_planck_levels(self, run_section):
        """Contract: the stdout carries the numbers the (F10) item quotes."""
        run = run_section(45)
        run.value(r"asymptotic level ([\d.]+);", want=583.88, tol=5e-3,
                  label="s_inf")
        run.value(r"horizon of today ([\d.]+),", want=583.09, tol=5e-3,
                  label="s_hoy")
        run.value(r"= pi phi\^([\d.]+)", want=583.877, tol=5e-4,
                  label="N bound")
        run.value(r"sigma = (-?[\d.]+), S = pi/2", want=-1.4404, tol=5e-5,
                  label="compression limit")
        run.value(r"Delta S = ([\d.]+) bits", want=2.266, tol=5e-4,
                  label="doubling in bits")
        run.value(r"H\(0\) l = ([\d.]+),", want=math.sqrt(2), tol=5e-5,
                  label="H(0) l")
        run.has("the level where they are equal is sigma = 0")   # flip_level
        run.value(r"= 10\^([\d.]+) pi cells", want=122.00, tol=5e-3,
                  label="pi cells")
        run.has("only d = 4")
        run.has("(planar_patch_positive): ok")


# ══════════════════════════════════════════════════════════ section 46 ══
class TestSection46HopfFoliation:
    """section 46 -- 'The Hopf foliation and J'"""

    @staticmethod
    def _etas(ns=None):
        ns = np.arange(-12, 13) if ns is None else np.asarray(ns)
        return ns, np.arctan(PHI ** (-2.0 * ns))

    def test_the_flat_tori_have_modulus_i_tan_eta(self):
        """tan eta_n = phi^-2n, eta symmetric about pi/4, eta_0 = pi/4."""
        ns, eta = self._etas()
        assert np.allclose(np.tan(eta), PHI ** (-2.0 * ns))
        assert np.allclose(math.pi / 2 - eta, eta[::-1])
        assert eta[ns == 0][0] == pytest.approx(math.pi / 4, abs=1e-15)

    @pytest.mark.parametrize("n", [-12, -1, 0, 1, 12])
    def test_the_radius_ratio_is_sqrt_one_plus_phi_four_n(self, n):
        """R/r = sqrt(1 + phi^4n) from z1 = 0 (the Clifford circle at 0)."""
        eta = math.atan(PHI ** (-2.0 * n))
        assert 1 / math.sin(eta) == pytest.approx(
            math.sqrt(1 + PHI ** (4.0 * n)), rel=1e-12)

    def test_the_metric_of_the_flat_torus_is_cos_sin(self):
        """|de|^2 = cos^2 e, |db|^2 = sin^2 e, the two directions orthogonal."""
        e, a, b, h = 0.4, 1.1, 2.3, 1e-6
        tor = lambda e_, a_, b_: np.array(
            [np.cos(e_) * np.exp(1j * a_), np.sin(e_) * np.exp(1j * b_)])
        da = (tor(e, a + h, b) - tor(e, a - h, b)) / (2 * h)
        db = (tor(e, a, b + h) - tor(e, a, b - h)) / (2 * h)
        g = lambda u, v: np.real(np.vdot(u, v))
        assert [g(da, da), g(db, db), g(da, db)] == pytest.approx(
            [np.cos(e) ** 2, np.sin(e) ** 2, 0], abs=1e-8)

    def test_j_squares_to_minus_one_and_the_half_turn_is_invisible(self):
        """J^2 = -1, J^4 = 1; hopf(-z) = hopf(z); hopf(J z) = -1/conj hopf z."""
        rng = np.random.default_rng(7)
        z = rng.normal(size=2) + 1j * rng.normal(size=2)
        z /= np.linalg.norm(z)
        hopf = lambda w: w[..., 0] / w[..., 1]
        j = lambda w: np.array([-np.conj(w[1]), np.conj(w[0])])
        assert np.allclose(-z, np.exp(1j * math.pi) * z)
        assert np.isclose(hopf(-z), hopf(z))               # the half turn
        assert np.isclose(hopf(j(z)), -1 / np.conj(hopf(z)))  # antipode
        assert np.allclose(j(j(z)), -z)
        assert np.allclose(j(j(j(j(z)))), z)

    def test_j_is_the_antipode_on_the_tori(self):
        """|J(tor)[0]| = sin e: the mirror of the torus keeps its radius."""
        e, a, b = 0.4, 1.1, 2.3
        tor = np.array([np.cos(e) * np.exp(1j * a), np.sin(e) * np.exp(1j * b)])
        j = np.array([-np.conj(tor[1]), np.conj(tor[0])])
        assert abs(j[0]) == pytest.approx(np.sin(e), abs=1e-12)

    def test_su2_takes_any_fibre_to_any_other(self):
        """SU(2) is transitive on the fibres; U(1)xU(1) keeps each torus."""
        rng = np.random.default_rng(11)
        for _ in range(50):
            p = rng.normal(size=2) + 1j * rng.normal(size=2)
            p /= np.linalg.norm(p)
            q = rng.normal(size=2) + 1j * rng.normal(size=2)
            q /= np.linalg.norm(q)
            a_mat = np.array([[p[0], -p[1].conj()], [p[1], p[0].conj()]])
            b_mat = np.array([[q[0], -q[1].conj()], [q[1], q[0].conj()]])
            u = b_mat @ np.linalg.inv(a_mat)
            assert np.allclose(u @ p, q)
            assert np.allclose(u.conj().T @ u, np.eye(2))

    def test_a_torus_is_the_preimage_of_a_parallel_and_asks_for_an_axis(self):
        """|hopf| = 1/tan e0 on the torus; an axis is needed, U(1)xU(1) fixes it."""
        e0 = 0.5
        aa = np.random.default_rng(12).uniform(0, 2 * np.pi, 500)
        bb = np.random.default_rng(13).uniform(0, 2 * np.pi, 500)
        tz = np.stack([np.cos(e0) * np.exp(1j * aa),
                       np.sin(e0) * np.exp(1j * bb)], -1)
        hopf = lambda w: w[..., 0] / w[..., 1]
        assert np.allclose(np.abs(hopf(tz)), 1 / np.tan(e0))
        # a change of axis spreads the first coordinate (std > 1e-2) but
        # |hopf| is SU(2)-invariant, and a diagonal phase keeps |coord 0|
        rot = np.array([[np.cos(.7), -np.sin(.7) * np.exp(-.3j)],
                        [np.sin(.7) * np.exp(.3j), np.cos(.7)]])
        tr = tz @ rot.T
        assert np.std(np.abs(tr[:, 0])) > 1e-2
        assert np.allclose(np.abs(hopf(tr @ np.linalg.inv(rot).T)), 1 / np.tan(e0))
        diag = np.diag([np.exp(.4j), np.exp(-1.1j)])
        assert np.allclose(np.abs((tz @ diag.T)[:, 0]), np.cos(e0))

    def test_the_window_weight_crosses_half(self):
        """w(n) = e^{-pi tan eta_n}; it crosses 1/2 at n = 1.5702."""
        ns, eta = self._etas()
        w = np.exp(-np.pi * PHI ** (-2.0 * ns))
        assert np.allclose(w, np.exp(-np.pi * np.tan(eta)))
        n12 = 0.5 * math.log(math.pi / math.log(2)) / math.log(PHI)
        assert abs(n12 - 1.5702) < 1e-4
        assert np.exp(-np.pi * PHI ** (-2.0 * n12)) == pytest.approx(0.5, abs=1e-12)

    def test_section46_prints_the_window_tori(self, run_section):
        """Contract: the stdout carries the four lines of the P7 block."""
        run = run_section(46)
        run.has("flat tori of modulus i tan eta, tan eta_n = phi^-2n")
        run.has("J^2 = -1, J^4 = 1; on the base, the antipode of W10")
        run.has("SU(2) takes any fibre to any other")
        run.value(r"it crosses 1/2 at n = ([\d.]+)", want=1.5702, tol=5e-5,
                  label="window weight")
