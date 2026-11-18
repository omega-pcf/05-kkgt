"""Deep numeric tests for sections 45 and 46.

Section 45 is the (F10) block: the observer level along LCDM with the
Planck values, the compression limit where 4 pi z^2/(4 G_N) meets pi z,
the two constants (W4 patch, W8 throat) that coincide only in d = 4, and
the causal chart whose two halves cross at the static patch.  Section 46
is the Hopf foliation of the window: the flat tori of modulus i tan eta,
the antipodal map J of the base, the SU(2) transitivity of the fibres and
the window weight that crosses 1/2 at n = 1.5702.

Everything the sections assert, these tests recompute from the closed
form, and ``observer_level_statements`` / ``hopf_foliation_statements``
carry the two sections' own bodies into this module (SPEC-002 §1): every
number a section printed is asserted on its value, at the width of that
print, and no test here reads a section's stdout.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from kkgt.constants import LN_PHI, MPC_M, PHI

# Planck 2018 values section 45 uses: t_P = 5.391247e-44 s, the observer
# length l = sqrt2 t_P, 1 Mpc = kkgt.constants.MPC_M, H0 = 67.36 km/s/Mpc,
# Omega_m = 0.3153, Omega_r = 9.0e-5 (the section prints the levels they give).
_T_PLANCK_S = 5.391247e-44
_H0 = 67.36e3 / MPC_M
_OM, _OR = 0.3153, 9.0e-5
_OL = 1 - _OM - _OR
_L = math.sqrt(2) * _T_PLANCK_S          # the observer length


def _level(hubble: float) -> float:
    """sigma = log_phi(6 / (3 (H l)^2)), the level of section 45."""
    return math.log(6 / (3 * (hubble * _L) ** 2)) / LN_PHI


# ═══════════════════════════ section 45's own statements (migrated) ════
def observer_level_statements() -> None:
    """Every statement section 45 checked for the (F10) block.

    Migrated from the section itself (SPEC-002 §1): the body used to run
    behind the section-run fixture, and this module read ``asymptotic
    level 583.88`` and nine more lines back from its stdout.  Each of
    those numbers now fails here, on its value, at the width of the print
    the section gave it; every assertion the section already made keeps
    its own tolerance, unchanged.  The Planck values are the module's,
    the golden ratio, its logarithm and the megaparsec come from
    ``kkgt.constants``.
    """
    def cell(level: float) -> float:
        """z = phi^sigma, the cell of level sigma."""
        return PHI ** level

    def entropy(level: float) -> float:
        """S = pi phi^sigma, the entropy of that cell."""
        return math.pi * PHI ** level

    def cosmological(level: float | np.ndarray) -> float | np.ndarray:
        """Lambda = 6 phi^-sigma: constant along the tower (w = -1)."""
        return 6 * PHI ** -level

    def horizon_ratio(level: float) -> float:
        """H l = sqrt(Lambda/3), the horizon in Planck units."""
        return math.sqrt(cosmological(level) / 3)

    # ── the horizon level in LCDM, with the Planck values ─────────────
    grid = np.logspace(-34, 4, 4000)
    hubble = _H0 * np.sqrt(_OR * grid ** -4 + _OM * grid ** -3 + _OL)
    levels = np.array([_level(h) for h in hubble])
    asymptotic = _level(_H0 * math.sqrt(_OL))
    today = _level(_H0)
    assert np.all(np.diff(levels) > -1e-9) and abs(levels[-1] - asymptotic) < 1e-2
    assert abs(asymptotic - 583.877) < 5e-3 and abs(today - 583.090) < 5e-3
    # printed: "asymptotic level {asymptotic:.2f}; horizon of today {today:.2f}"
    assert asymptotic == pytest.approx(583.88, abs=5e-3)
    assert today == pytest.approx(583.09, abs=5e-3)
    assert np.allclose(3 * (hubble * _L) ** 2 * np.pi * PHI ** levels, 6 * np.pi)
    # printed: "N bound: 3pi/(Lambda G_N) ... = S_obs = pi phi^{asymptotic:.3f}"
    assert asymptotic == pytest.approx(583.877, abs=5e-4)

    # ── the compression limit: 4 pi z^2/(4 G_N) meets pi z ────────────
    compression = math.log(2) / LN_PHI       # sigma where the two meet
    zz = np.linspace(0.01, 3, 30000)
    crossing = zz[np.argmin(np.abs(2 * np.pi * zz ** 2 - np.pi * zz))]
    assert abs(crossing - 0.5) < 1e-3
    assert np.isclose(cell(-compression), 0.5)
    assert np.isclose(entropy(-compression), np.pi / 2)
    assert np.all(2 * np.pi * zz[zz < 0.5] ** 2 < np.pi * zz[zz < 0.5])
    # printed: "compression limit: ... sigma = {-compression:.4f}, S = pi/2"
    assert -compression == pytest.approx(-1.4404, abs=5e-5)
    # the first expansion doubles the radius: half a cell becomes a cell
    assert np.isclose(cell(0) / cell(-compression), 2)
    assert np.isclose(entropy(0), 2 * entropy(-compression))
    # printed: "a doubling is not a bit: Delta S = {bits:.3f} bits"
    bits = (entropy(0) - entropy(-compression)) / math.log(2)
    assert bits == pytest.approx(2.266, abs=5e-4)

    # ── the constant of the first patch and that of the throat ────────
    g_n = 0.5
    assert np.isclose(3 * np.pi / (g_n * entropy(0)), 6)
    assert np.isclose(4 * 3 / 2, 6)

    def sphere_area(dimension: float) -> float:
        """Omega_k = 2 pi^((k+1)/2) / Gamma((k+1)/2), the k-sphere area."""
        return 2 * math.pi ** ((dimension + 1) / 2) / math.gamma((dimension + 1) / 2)

    shared = [
        d for d in range(3, 30)
        if np.isclose(
            (d - 1) * (d - 2) / 2
            * (sphere_area(d - 2) / (4 * g_n * math.pi)) ** (2 / (d - 2)),
            d * (d - 1) / 2,
        )
    ]
    # printed: "with patch and throat at the same d, only d = 4"
    assert shared == [4]

    # ── where the two constants meet, and the weight of the window ────
    level_grid = np.linspace(-5, 600, 200001)
    equal_level = level_grid[np.argmin(np.abs(cosmological(level_grid) - 6))]
    assert abs(equal_level) < 1e-2          # printed: "... is sigma = 0"
    # printed: "H(0) l = {horizon_ratio(0):.4f}, throat radius 1"
    assert horizon_ratio(0) == pytest.approx(math.sqrt(2), abs=5e-5)

    def window_weight(n: float) -> float:
        """w = e^{-pi phi^-2n}, the weight of the window at level n."""
        return np.exp(-np.pi * PHI ** (-2.0 * n))

    assert window_weight(1) < 0.5 < window_weight(2)
    assert horizon_ratio(1) > 1 > horizon_ratio(2)

    # printed: "3H^2(0)/Lambda_obs = phi^583.79 = 10^{pi_cells:.2f} pi cells"
    pi_cells = 583.79 * math.log10(PHI)
    assert abs(pi_cells - 122.0) < 0.01
    assert pi_cells == pytest.approx(122.00, abs=5e-3)
    assert np.isclose(cosmological(583.79) * entropy(583.79), 6 * entropy(0))

    # ── the half: the causal chart and its static patch ───────────────
    rng = np.random.default_rng(45)
    sample = 200000
    time = rng.uniform(-math.pi / 2, math.pi / 2, sample) * 0.999
    chi = rng.uniform(0, math.pi, sample)
    tau = np.arcsinh(np.tan(time))
    x0, x4 = np.sinh(tau), np.cosh(tau) * np.cos(chi)
    future = chi < time + math.pi / 2
    past = chi < math.pi / 2 - time
    assert np.array_equal(x0 + x4 > 0, future)
    assert np.array_equal(x4 - x0 > 0, past)
    assert np.array_equal(future & past, chi < math.pi / 2 - np.abs(time))
    for length, instant, radius in [(1, 0.3, 2), (2.5, -1, 0.7), (0.4, 3, 5)]:
        plane = (
            length * np.sinh(instant / length)
            + radius ** 2 / (2 * length) * np.exp(instant / length)
        ) + (
            length * np.cosh(instant / length)
            - radius ** 2 / (2 * length) * np.exp(instant / length)
        )
        assert np.isclose(plane, length * np.exp(instant / length))


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
        assert s_inf == pytest.approx(583.877, abs=5e-4)
        assert s_hoy == pytest.approx(583.090, abs=5e-4)
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

    def test_section45s_planck_levels_hold(self):
        """The numbers the (F10) item quotes, asserted on their values.

        This test used to run the section through the section-run fixture
        and read ``asymptotic level 583.88`` and nine more lines back
        from its stdout; the whole body of the section now lives in
        ``observer_level_statements`` and fails here, on a value, with
        pytest's assertion rewriting (SPEC-002 §1).
        """
        observer_level_statements()


# ═══════════════════════════ section 46's own statements (migrated) ════
def hopf_foliation_statements() -> None:
    """Every statement section 46 checked for the window tori.

    Migrated from the section itself (SPEC-002 §1): the body used to run
    behind the section-run fixture, and this module read the four lines
    of the P7 block back from its stdout.  Those lines carried one
    number, the crossing of the window weight at 1/2, now asserted on its
    value at the width of the print; every assertion the section already
    made keeps its own tolerance, unchanged.
    """
    rng = np.random.default_rng(46)

    def torus(eta: float, alpha: float, beta: float) -> np.ndarray:
        """A point of the torus of modulus i tan eta."""
        return np.array([np.cos(eta) * np.exp(1j * alpha),
                         np.sin(eta) * np.exp(1j * beta)])

    levels = np.arange(-12, 13)
    eta = np.arctan(PHI ** (-2.0 * levels))
    assert np.allclose(np.tan(eta), PHI ** (-2.0 * levels))

    e, alpha, beta, step = 0.4, 1.1, 2.3, 1e-6

    def inner(u: np.ndarray, v: np.ndarray) -> float:
        """The real inner product of the two directions of the torus."""
        return float(np.real(np.vdot(u, v)))

    d_alpha = (torus(e, alpha + step, beta) - torus(e, alpha - step, beta)) / 2 / step
    d_beta = (torus(e, alpha, beta + step) - torus(e, alpha, beta - step)) / 2 / step
    assert np.allclose(
        [inner(d_alpha, d_alpha), inner(d_beta, d_beta), inner(d_alpha, d_beta)],
        [np.cos(e) ** 2, np.sin(e) ** 2, 0], atol=1e-8,
    )
    assert np.allclose(np.pi / 2 - eta, eta[::-1])
    assert np.isclose(eta[levels == 0][0], np.pi / 4)
    # the Clifford circle of every torus, and the ratio R/r from z1 = 0
    for n, angle in zip(levels, eta):
        circle = np.linspace(0, 2 * np.pi, 50)
        sine = np.sin(angle)
        rho = np.cos(angle) / (1 - sine * np.sin(circle))
        height = sine * np.cos(circle) / (1 - sine * np.sin(circle))
        assert np.allclose((rho - 1 / np.cos(angle)) ** 2 + height ** 2,
                           np.tan(angle) ** 2, rtol=1e-9)
        assert np.isclose(1 / np.sin(angle), np.sqrt(1 + PHI ** (4.0 * n)))

    # ── J: the antipode of the base, the mirror of the tori ───────────
    z = rng.normal(size=2) + 1j * rng.normal(size=2)
    z /= np.linalg.norm(z)

    def hopf(map_: np.ndarray) -> np.ndarray:
        """The base point w0/w1 of the Hopf fibre of ``map_``."""
        return map_[..., 0] / map_[..., 1]

    def antipode(map_: np.ndarray) -> np.ndarray:
        """J = (-conj w1, conj w0): J^2 = -1, J^4 = 1."""
        return np.array([-np.conj(map_[1]), np.conj(map_[0])])

    assert np.allclose(-z, np.exp(1j * np.pi) * z)
    assert np.isclose(hopf(-z), hopf(z))          # the half turn is invisible
    assert np.isclose(hopf(antipode(z)), -1 / np.conj(hopf(z)))
    assert np.allclose(antipode(antipode(z)), -z)
    assert np.allclose(antipode(antipode(antipode(antipode(z)))), z)
    assert np.isclose(abs(antipode(torus(e, alpha, beta))[0]), np.sin(e))

    # ── homogeneity, the tori and the axis ────────────────────────────
    for _ in range(100):
        p = rng.normal(size=2) + 1j * rng.normal(size=2)
        p /= np.linalg.norm(p)
        q = rng.normal(size=2) + 1j * rng.normal(size=2)
        q /= np.linalg.norm(q)
        a_mat = np.array([[p[0], -p[1].conj()], [p[1], p[0].conj()]])
        b_mat = np.array([[q[0], -q[1].conj()], [q[1], q[0].conj()]])
        u = b_mat @ np.linalg.inv(a_mat)
        assert np.allclose(u @ p, q)
        assert np.allclose(u.conj().T @ u, np.eye(2))

    e0 = 0.5
    aa = rng.uniform(0, 2 * np.pi, 500)
    bb = rng.uniform(0, 2 * np.pi, 500)
    parallel = np.stack([np.cos(e0) * np.exp(1j * aa),
                         np.sin(e0) * np.exp(1j * bb)], -1)
    assert np.allclose(abs(hopf(parallel)), 1 / np.tan(e0))
    rotation = np.array([[np.cos(.7), -np.sin(.7) * np.exp(-.3j)],
                         [np.sin(.7) * np.exp(.3j), np.cos(.7)]])
    rotated = parallel @ rotation.T
    assert np.std(abs(rotated[:, 0])) > 1e-2
    assert np.allclose(abs(hopf(rotated @ np.linalg.inv(rotation).T)), 1 / np.tan(e0))
    diagonal = np.diag([np.exp(.4j), np.exp(-1.1j)])
    assert np.allclose(abs((parallel @ diagonal.T)[:, 0]), np.cos(e0))

    # ── the weight of the window ──────────────────────────────────────
    def window_weight(n: float | np.ndarray) -> float | np.ndarray:
        """w = e^{-pi phi^-2n}, the weight of the window at level n."""
        return np.exp(-np.pi * PHI ** (-2.0 * n))

    crossing = 0.5 * math.log(math.pi / math.log(2)) / math.log(PHI)
    assert np.allclose(window_weight(levels), np.exp(-np.pi * np.tan(eta)))
    assert abs(crossing - 1.5702) < 1e-4
    # printed: "it crosses 1/2 at n = {crossing:.4f}"
    assert crossing == pytest.approx(1.5702, abs=5e-5)
    assert np.exp(-np.pi * PHI ** (-2.0 * crossing)) == pytest.approx(0.5, abs=1e-12)


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

    def test_section46s_window_tori_hold(self):
        """The four lines of the P7 block, asserted on their values.

        This test used to run the section through the section-run fixture
        and read those four lines back from its stdout; the whole body of
        the section now lives in ``hopf_foliation_statements`` and fails
        here, on a value, with pytest's assertion rewriting (SPEC-002 §1).
        """
        hopf_foliation_statements()
