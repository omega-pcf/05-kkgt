"""Deep numeric tests for sections 1-8 of the note.

Section identity: the manuscript cites the tests that check a number
(``\testref{...}``), and every test docstring here names the section it
checks.

Two kinds of check:
  * independent -- the quantity is recomputed here from the closed form,
    with an explicit tolerance (this is the real regression net);
  * migrated    -- the computation itself lives in this module (SPEC-002
    1): the bodies of sections 1-8 these tests consume were moved out of
    the package, and every number the file used to read back from a
    section's stdout is asserted on its value, at the section's own print
    precision and with the section's own tolerance.

No test of this file runs a section any more.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from functools import lru_cache
from typing import Any

import mpmath as mp
import numpy as np
import pytest
from scipy.linalg import eigh, eigvalsh, expm
from scipy.optimize import brentq, minimize_scalar
from scipy.special import j0, j1, jn_zeros, jv, y0, y1

from kkgt.constants import (
    LN_PHI,
    M_GEV,
    M_KOIDE_MEV,
    M_PCF,
    M_PLANCK_GEV,
    M_TAU_MEV,
    OBS_G,
    PHI,
)

# Half the last digit of the figure each constant guards (decision (ii) of
# AUD-001): .3f -> 5e-4, .4f -> 5e-5.  R2 guards two-decimal figures, whose
# width would be 5e-3, but every one of them is compared after the section's
# own round(..., 2), where the figure is already exact, so it keeps the .3f
# width: tighter than the rule asks, never looser.
R2 = 5e-4
R3 = 5e-4   # .3f
R4 = 5e-5   # .4f

# ── figures and data that kkgt.constants does not carry ────────────────────
IR_SCALE_GEV = 99.12                  # section 1's fitted scale (its v2 block)
M_ELECTRON_MEV = 0.51099895           # electron mass in the Koide mean (F1)
M_MUON_MEV = 105.6583755              # muon mass in the Koide mean (F1)
M_PROTON_GEV = 0.938272               # proton mass: section 1's m_p/3 choice
M_ELECTRON_GEV = 0.000510999          # electron mass: section 1's m_e choice
M_PLANCK_REDUCED_GEV = 2.435e18       # reduced Planck mass: section 1's second top
TWO_BRANE_M1 = 3.83182                # exact two-brane m1 (section 1's convergence)
GLUON_GEV = 3600.0                    # first gluon candidate: section 7's scale
LYR_VECTOR_TABLE = (2.45, 5.57, 8.7, 11.84)   # LYR vector zeros: section 1's label
E5_RATIOS = {700: 1.842, 1000: 2.632, 1322: 3.479}  # section 7's E5 line figures


# ═══════════════════════════ migrated bodies of sections 1-8 (SPEC-002 1) ══
# English identifiers, annotated signatures, module-level imports, numbers
# single-sourced in kkgt.constants where the package defines them.  The
# sections themselves stay registered until the package-deletion unit
# (SPEC-002 4.3): the order pin and the run driver still need all 47.

@lru_cache(maxsize=None)
def chain_masses(
    a: float,
    b: float,
    steps: int,
    stiffness_power: float,
    weight_power: float,
    count: int = 4,
) -> np.ndarray:
    """The first ``count`` nonzero masses of the golden chain on ``[a, b]``.

    The shared body of sections 1, 6 and 7: ``steps`` substeps per golden
    level, midpoint stiffness ``phi^{-stiffness_power A}`` and the mass
    weight ``phi^{-weight_power A}`` with half weight at the two end nodes
    (trapezoid), then ``m = sqrt(eigenvalue)`` with the zero mode dropped.
    Section 1's reversed orientation (its ``sl_r``) is
    ``(-4, -2)``; section 6 runs the chain with ``(4, 2)`` and, without the
    ``e^{2A}`` weight, ``(4, 0)``.
    """
    s = np.linspace(a, b, int(round((b - a) * steps)) + 1)
    h = LN_PHI / steps
    n = len(s)
    p = PHI ** (-stiffness_power * (s[:-1] + 0.5 / steps))
    stiffness = np.zeros((n, n))
    for i in range(n - 1):
        stiffness[i, i] += p[i]
        stiffness[i + 1, i + 1] += p[i]
        stiffness[i, i + 1] -= p[i]
        stiffness[i + 1, i] -= p[i]
    weight = np.diag(PHI ** (-weight_power * s))
    weight[0, 0] /= 2
    weight[-1, -1] /= 2
    eigenvalues = eigh(stiffness / h ** 2, weight, eigvals_only=True)
    masses = np.sqrt(np.clip(eigenvalues, 0, None))
    return masses[1:1 + count]


def scale_fit_rms(masses: np.ndarray) -> float:
    """RMS (percent) of the best scale fit ``obs = A * masses``.

    Sections 1, 5 and 6 print the same quantity: the amplitude that best
    fits the four LYR candidates to the tower, as a percentage.
    """
    obs = np.array(OBS_G)
    amplitude = (obs @ masses) / (masses @ masses)
    return float(100 * np.sqrt(np.mean(((obs - amplitude * masses) / obs) ** 2)))


@lru_cache(maxsize=None)
def tower_operator() -> tuple[np.ndarray, np.ndarray]:
    """``(K, eta)`` of the seven-level tower (sections 1 and 4).

    ``K = -L / log(phi)^2`` with the hoppings ``phi^2, phi^-2`` (the mass
    operator of section 4, the same matrix section 1's section-3 block
    diagonalises) and ``eta = diag(phi^{-4 sigma})``, the metric.
    """
    n = 7
    laplacian = np.diag(np.full(n, -2.0))
    for i in range(1, n):
        laplacian[i, i - 1] = PHI ** 2
        laplacian[i - 1, i] = PHI ** -2
    k = -laplacian / LN_PHI ** 2
    eta = np.diag(PHI ** (-4.0 * np.arange(n)))
    return k, eta


def bracketed_roots(equation: Callable[[float], float], count: int) -> np.ndarray:
    """First ``count`` roots of ``equation`` on the scan of sections 1 and 3."""
    grid = np.linspace(0.5, 15, 6000)
    roots = []
    for left, right in zip(grid[:-1], grid[1:]):
        if equation(float(left)) * equation(float(right)) < 0:
            roots.append(brentq(equation, float(left), float(right)))
    return np.array(roots[:count])


def graviton_two_brane_roots(epsilon: float, count: int = 4) -> np.ndarray:
    """Zeros of ``J1(eps x) Y1(x) - Y1(eps x) J1(x)`` (sections 1 and 3)."""
    return bracketed_roots(
        lambda x: float(j1(epsilon * x) * y1(x) - y1(epsilon * x) * j1(x)), count
    )


def vector_two_brane_roots(epsilon: float, count: int = 4) -> np.ndarray:
    """Zeros of ``J0(eps x) Y0(x) - Y0(eps x) J0(x)`` (sections 1 and 3)."""
    return bracketed_roots(
        lambda x: float(j0(epsilon * x) * y0(x) - y0(epsilon * x) * j0(x)), count
    )


def koide_scale_mev() -> float:
    """``M = ((sqrt m_e + sqrt m_mu + sqrt m_tau)/3)^2`` in MeV (section 1, F1)."""
    return float(
        ((np.sqrt(M_ELECTRON_MEV) + np.sqrt(M_MUON_MEV) + np.sqrt(M_TAU_MEV)) / 3) ** 2
    )


def fitted_scale_gev() -> float:
    """The weighted fit of the J1 tower to the four candidates: scale in GeV.

    Section 1's section-7 block: the errors 20, 20, 30, 40 keV weight the
    four candidates, ``sc = sum(w obs j1) / sum(w j1^2)``.
    """
    j1_zeros = jn_zeros(1, 4)
    weights = 1 / np.array([20.0, 20.0, 30.0, 40.0]) ** 2
    obs = np.array(OBS_G)
    return float(np.sum(weights * obs * j1_zeros) / np.sum(weights * j1_zeros ** 2))


def kpi_r_from_scale(planck_mass: float, scale_gev: float) -> float:
    """``k pi r = log(M_Pl' / scale)``, the depth of the UV top (sections 1, 3)."""
    return math.log(planck_mass / scale_gev)


def cw6_sine_band_max_diffs() -> tuple[float, float]:
    """The two max-diff figures of section 1's CW6 block, at its ``.1e`` print.

    ``(max |eig(K) - (2 - 2 cos(pi k/8))/log^2 phi|, max |2 sin^2(k pi/16)/log^2 phi - eig(K)|)``
    for the seven-level operator of the tower.
    """
    k, _eta = tower_operator()
    eigen = np.sort(np.linalg.eigvals(k).real)
    closed = np.sort((2 - 2 * np.cos(np.pi * np.arange(1, 8) / 8)) / LN_PHI ** 2)
    sine = np.sort((2 * np.sin(np.pi * np.arange(1, 8) / 16) / LN_PHI) ** 2)
    return (
        float(f"{np.max(np.abs(eigen - closed)):.1e}"),
        float(f"{np.max(np.abs(sine - eigen)):.1e}"),
    )


def boundary_lowest_mass_squared(dirichlet: bool) -> float:
    """Lowest ``m^2`` of the golden-grid operator (section 1's zero-mode block).

    ``Q = 32`` substeps on ``[0, 12]``, Neumann at both edges or Dirichlet
    (the interior grid), returned as the section prints it: the Neumann
    value through ``.1e``, the Dirichlet one rounded to one decimal.
    """
    q = 32
    s = np.linspace(0, 12, 12 * q + 1)
    h = LN_PHI / q
    n = len(s)
    p = PHI ** (4 * (s[:-1] + 0.5 / q))
    stiffness = np.zeros((n, n))
    for i in range(n - 1):
        stiffness[i, i] += p[i]
        stiffness[i + 1, i + 1] += p[i]
        stiffness[i, i + 1] -= p[i]
        stiffness[i + 1, i] -= p[i]
    mass = np.diag(PHI ** (2 * s))
    if dirichlet:
        stiffness, mass = stiffness[1:-1, 1:-1], mass[1:-1, 1:-1]
    return float(eigh(stiffness / h / h, mass, eigvals_only=True)[0])


def sym_t_min_eigenvalues(weighted: bool) -> list[float]:
    """min eig sym(T) for a = 0.05, 0.2, 1 (section 4), at its ``.3e`` print.

    ``weighted`` selects the eta product ``<f, T f>_eta`` instead of the
    standard one; the metric is what restores positivity.
    """
    k, eta = tower_operator()
    minima = []
    for a in (0.05, 0.2, 1.0):
        t = expm(-a * k)
        sym = eta @ t if weighted else t
        minima.append(float(f"{eigvalsh((sym + sym.T) / 2).min():.3e}"))
    return minima


@lru_cache(maxsize=None)
def casimir_sums(exact_zeros: int) -> tuple[float, float, float, float]:
    """``(A, B, log s*, depth)`` of the regularized tower sum (section 2).

    McMahon tail + Hurwitz zeta with the exact J1 zeros, mpmath at 30
    digits; each figure comes back the way the section printed it, with
    ``mp.nstr(..., 8)`` -- eight significant digits.
    """
    mp.mp.dps = 30
    phi = (1 + mp.sqrt(5)) / 2
    c1 = mp.mpf(-3) / 8
    c3 = mp.mpf(36) / 1536
    c5 = -mp.mpf(32 * 3 * 1179) / (15 * 32768)

    def perturbation(u: Any) -> Any:
        return c1 * u ** 2 + c3 * u ** 4 + c5 * u ** 6

    p_coef = mp.taylor(lambda u: (1 + perturbation(u)) ** 4, 0, 8)
    q_coef = mp.taylor(
        lambda u: 2 * (1 + perturbation(u)) ** 4 * mp.log(1 + perturbation(u))
        if u != 0 else 0,
        0, 8,
    )
    a = mp.mpf(5) / 4

    def zeta_sum(power: int, conlog: bool) -> Any:
        z, dz = mp.zeta(-power, a), mp.zeta(-power, a, 1)
        return mp.pi ** power * ((2 * mp.log(mp.pi) * z - 2 * dz) if conlog else z)

    def asymptotic(beta: Any, conlog: bool) -> Any:
        log_beta = mp.log(beta ** 2)
        total: Any = 0
        for n in range(0, 9, 2):
            total += beta ** (4 - n) * (
                (p_coef[n] * log_beta + q_coef[n]) if conlog else p_coef[n]
            )
        return total

    def regularized_sum(conlog: bool) -> Any:
        reg = sum(
            (p_coef[n] * zeta_sum(4 - n, True) + q_coef[n] * zeta_sum(4 - n, False))
            if conlog else p_coef[n] * zeta_sum(4 - n, False)
            for n in range(0, 9, 2)
        )
        correction: Any = 0
        for k in range(1, exact_zeros + 1):
            zero = mp.besseljzero(1, k)
            beta = mp.pi * (k + mp.mpf(1) / 4)
            term = zero ** 4 * mp.log(zero ** 2) if conlog else zero ** 4
            correction += term - asymptotic(beta, conlog)
        return reg + correction

    a_value = regularized_sum(True)
    b_value = regularized_sum(False)
    log_s = -a_value / (2 * b_value) - mp.mpf(1) / 4
    depth = -log_s / mp.log(phi)
    return (
        float(mp.nstr(a_value, 8)),
        float(mp.nstr(b_value, 8)),
        float(mp.nstr(log_s, 8)),
        float(mp.nstr(depth, 8)),
    )


def jnu_zeros(order: float, count: int = 4) -> np.ndarray:
    """First ``count`` zeros of ``J_order`` (section 5's phase block)."""

    def equation(x: float) -> float:
        return float(jv(order, x))

    grid = np.linspace(0.5, 20, 4000)
    roots = []
    for left, right in zip(grid[:-1], grid[1:]):
        if equation(float(left)) * equation(float(right)) < 0:
            roots.append(brentq(equation, float(left), float(right)))
    return np.array(roots[:count])


def free_phase_fit() -> tuple[float, float]:
    """``(optimal theta, rms%)`` of the two-parameter phase fit (section 5)."""
    best = min(
        (scale_fit_rms(np.arange(1, 5) + t), t) for t in np.linspace(-0.5, 1, 3001)
    )
    return float(best[1]), float(best[0])


def measured_phase(d: int) -> tuple[float, float, float]:
    """``((d-3)/4, measured phase, rms%)`` for the ``J_{d/2-1}`` zeros (section 5)."""
    zeros = jnu_zeros(d / 2 - 1)
    rms = scale_fit_rms(zeros)
    phase = float(np.mean(zeros / np.pi - np.arange(1, 5)))
    return (d - 3) / 4, phase, rms


def sector_scales() -> tuple[float, float]:
    """``(graviton, gluon)`` scale per first zero of its operator (section 7)."""
    graviton = chain_masses(-6, 6, 32, 4, 2, count=3)
    vector = chain_masses(-6, 6, 32, 2, 0, count=3)
    return OBS_G[0] / graviton[0], GLUON_GEV / vector[0]


def golden_ladder_rms() -> float:
    """rms (percent) of the one-parameter golden ladder ``m = m0 phi^{k/2}``."""
    obs = np.array(OBS_G)

    def cost(log_m0: float) -> float:
        levels = np.round((np.log(obs) - log_m0) / LN_PHI)
        return float(np.sum((np.log(obs) - log_m0 - levels * LN_PHI) ** 2))

    fit = minimize_scalar(
        cost,
        bounds=(np.log(obs.min()) - 1, np.log(obs.min()) + 1),
        method="bounded",
    )
    levels = np.round((np.log(obs) - fit.x) / LN_PHI)
    prediction = np.exp(fit.x + levels * LN_PHI)
    return float(np.sqrt(np.mean(((obs - prediction) / obs) ** 2)) * 100)


def section1_summary_blocks() -> dict[str, object]:
    """The six summary values section 1's stdout carried (SPEC-002 1).

    The blocks used to be substring-matched against the section's output;
    each now resolves to the value its line printed, at print precision.
    """
    k, eta = tower_operator()
    q_values = [
        round(float(chain_masses(0, 12, q, -4, -2, count=1)[0]), 3)
        for q in (16, 32, 64, 128)
    ]
    return {
        "eta K symmetric": bool(np.allclose(eta @ k, (eta @ k).T)),
        "eta == e^{4A}, A=-sigma log phi": bool(
            np.allclose(np.diag(eta), np.exp(-4 * np.arange(7) * LN_PHI))
        ),
        "Q = 16, 32, 64, 128": q_values,
        "[3.832, 3.832, 3.832, 3.832]": q_values,
        "sigma_IR with m0 = M": round(
            math.log(IR_SCALE_GEV / M_GEV) / LN_PHI, 2
        ),
        "M_PCF log phi = 6 sqrt3 pi (framework units): M_PCF": round(M_PCF, 3),
    }


# the values the six blocks of section 1 must carry
SECTION1_BLOCK_EXPECTED: dict[str, object] = {
    "eta K symmetric": True,
    "eta == e^{4A}, A=-sigma log phi": True,
    "Q = 16, 32, 64, 128": [3.832, 3.832, 3.832, 3.832],
    "[3.832, 3.832, 3.832, 3.832]": [3.832, 3.832, 3.832, 3.832],
    "sigma_IR with m0 = M": 11.96,
    "M_PCF log phi = 6 sqrt3 pi (framework units): M_PCF": 67.846,
}


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
    def test_section1_stdout_blocks(self, block):
        """Contract: the six summary values section 1's summary block carried.

        The blocks used to be substring-matched against the section's
        stdout; each is now asserted on the value its line printed, at the
        section's print precision (SPEC-002 1).
        """
        got = section1_summary_blocks()[block]
        want = SECTION1_BLOCK_EXPECTED[block]
        assert got == want, (block, got)

    def test_alternatives_for_the_bottom_level(self):
        """v2 of section 1: the level read from the scale depends on m0.

        One node rather than a parametrised triple: the manuscript cites
        this test by name, and a parametrised id carries its parameters.

        The three levels used to be read back from the section's stdout;
        they are asserted on their values here, at the two decimals the
        section printed them with (SPEC-002 1).
        """
        for label, mass, printed in (
            ("M", M_GEV, 11.96),
            ("m_p/3", M_PROTON_GEV / 3, 11.97),
            ("m_e", M_ELECTRON_GEV, 25.3),
        ):
            got = round(math.log(IR_SCALE_GEV / mass) / LN_PHI, 2)
            assert got == pytest.approx(printed, abs=5e-3), (label, got)

    def test_mpcf_framework_unit(self):
        """M_PCF log phi = 6 sqrt(3) pi -> 67.846 (same value as section 12).

        The figure carries the printed .3f width (half a unit, 5e-4); the
        value comes from the constant now, not from the section's stdout
        (SPEC-002 1).
        """
        got = round(M_PCF, 3)
        assert got == pytest.approx(6 * math.sqrt(3) * math.pi / LN_PHI, abs=5e-4)

    def test_dirichlet_lowest_eigenvalue_is_positive(self):
        """Boundary conditions: Neumann has the zero mode, Dirichlet starts at 26.4.

        main.tex: "with them the lowest eigenvalue is 0, the massless
        four-dimensional graviton; with Dirichlet ... there is no zero mode".

        Both eigenvalues used to come from the section's stdout; they are
        computed here at the section's print precision (SPEC-002 1).
        """
        neumann = float(f"{boundary_lowest_mass_squared(False):.1e}")
        dirichlet = round(boundary_lowest_mass_squared(True), 1)
        assert abs(neumann) < 1e-6, neumann
        assert dirichlet == pytest.approx(26.4, abs=0.05), dirichlet

    def test_second_order_convergence_on_the_golden_grid(self):
        """Relative error of m1 on [0,12] at Q = 16,32,64,128 vs 3.83182.

        The four errors used to be read from the section's stdout as
        ``.1e`` strings; they are produced here the same way (SPEC-002 1),
        so each carries its own half unit of that print.
        """
        errs = []
        for q in (16, 32, 64, 128):
            m1 = chain_masses(0, 12, q, -4, -2, count=1)[0]
            relative = abs(m1 - TWO_BRANE_M1) / TWO_BRANE_M1
            errs.append(float(f"{relative:.1e}"))
        # every entry is printed as ``.1e``, so each carries its own half
        # unit: 5e-6 on 1.2e-4 and 5e-7 on the three smaller ones
        for got_, want_, half in zip(
            errs, [1.2e-4, 2.9e-5, 7.3e-6, 1.8e-6], [5e-6, 5e-7, 5e-7, 5e-7]
        ):
            assert abs(got_ - want_) <= half, (got_, want_)
        # second order: every refinement divides the error by ~4
        for a, b in zip(errs, errs[1:]):
            assert a / b == pytest.approx(4.0, rel=0.3), (a, b)

    def test_one_node_per_level_degrades_the_residual(self):
        """One node per golden level: the residual rounds to 11-12 %.

        The section prints 12.4 for sigma[0,6] and 10.8 for sigma[-6,6];
        both round to the integers the sentence quotes.  The two residuals
        are computed here now, at the section's one-decimal print
        (SPEC-002 1).
        """
        vals = [
            round(scale_fit_rms(chain_masses(a, 6, 1, 4, 2)), 1) for a in (0, -6)
        ]
        assert len(vals) == 2, vals
        assert sorted(round(v) for v in vals) == [11, 12], vals

    def test_m_phi_11_is_62_5_gev(self):
        """The level 11 of M-theory read as a scale: M phi^11 = 62.5 GeV."""
        got = round(M_GEV * PHI**11, 1)
        assert got == pytest.approx(62.5, abs=0.05), got

    def test_cw6_sine_band_matches_the_eigenvalues(self):
        """m_k = 2 sin(k pi/16)/log phi is the spectrum of (K), to 1e-10.

        Both max diffs used to be read from the section's stdout as
        ``.1e`` strings; they are computed here the same way (SPEC-002 1).
        """
        closed, band = cw6_sine_band_max_diffs()
        assert closed < 1e-10, closed
        assert band < 1e-10, band

    def test_the_three_spacings_have_the_variance_of_the_ensemble(self):
        """main.tex L1366: the three spacings of eq:data /mean have variance 0.001.

        The GUE reference for that variance is 3pi/8 - 1 = 0.178; section 1
        prints both ('Additions A-C', B5 rigidity).  The section's figures
        are asserted here at its own print precision -- .4f for the
        variance, .3f for the GUE value (SPEC-002 1).
        """
        obs = np.array(OBS_G)
        sp = np.diff(obs)
        sp = sp / sp.mean()
        assert round(float(np.var(sp)), 3) == 0.001
        assert round(3 * math.pi / 8 - 1, 3) == 0.178
        assert round(float(np.var(sp)), 4) == pytest.approx(0.001, abs=R3)

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
    # value the section prints (decision (ii)).  All four used to be read
    # back from the section's stdout; they are computed here now
    # (SPEC-002 1), at the section's print precision.

    def test_the_printed_koide_scale_is_313_84(self):
        """main.tex L805 and L1464: M = 313.84 MeV (AUD-001, class b).

        Cited to test_reconstruction_is_below_one_part_in_ten_thousand and
        test_alternatives_for_the_bottom_level; section 1 prints the figure
        with ``round(M_lep, 2)``.
        """
        got = round(koide_scale_mev(), 2)
        assert got == pytest.approx(M_KOIDE_MEV, abs=5e-3), got

    def test_the_ir_level_in_phi_units_is_the_printed_3_8319(self):
        """main.tex L1454: m1/phi^sigma_IR = 3.8319 (AUD-001, class b).

        Cited to test_second_order_convergence_on_the_golden_grid; the value
        is printed with ``round(..., 4)``.
        """
        got = round(float(chain_masses(0, 12, 32, -4, -2, count=1)[0]), 4)
        assert got == pytest.approx(3.8319, abs=5e-5), got

    def test_the_scale_in_powers_of_two_is_the_printed_8_30(self):
        """main.tex L1475: the same scale in powers of 2 = 8.30.

        Section 1 prints 8.3 (``round(..., 2)``); 8.30 is the manuscript's
        two-decimal reading of it (AUD-001, class b, cited to
        test_alternatives_for_the_bottom_level).
        """
        got = round(math.log2(fitted_scale_gev() * 1000 / koide_scale_mev()), 2)
        assert got == pytest.approx(8.30, abs=5e-3), got
        assert round(got, 2) == 8.30, got

    def test_the_log_pi_of_the_scale_is_the_printed_5_03(self):
        """main.tex L1557: log_pi(scale/M) = 5.03 (AUD-001, class b).

        Section 1 prints the value with ``round(..., 3)`` as 5.028 and the
        label carries the manuscript's two-decimal 5.03.
        """
        ratio = fitted_scale_gev() * 1000 / koide_scale_mev()
        got = round(math.log(ratio) / math.log(math.pi), 3)
        assert got == pytest.approx(5.028, abs=5e-4), got
        assert round(got, 2) == 5.03, got

    def test_the_j0_limit_is_the_printed_2_295(self):
        """main.tex L1594 and L1601: m2/m1 -> 2.295 at the J0 limit.

        AUD-001, class b, cited to test_vector_ratio_range; the value is
        printed with ``round(..., 3)``.
        """
        zeros = jn_zeros(0, 2)
        got = round(zeros[1] / zeros[0], 3)
        assert got == pytest.approx(2.295, abs=5e-4), got

    def test_the_two_uv_tops_in_levels_are_the_printed_two(self):
        """main.tex L1610: the UV top at the two Planck masses.

        k pi r = 39.33 at M_Pl and 37.72 at the reduced M_Pl, with
        sigma_UV = 93.74 and 90.39 (AUD-001, class b, cited to
        test_vector_ratio_range); both pairs are printed with
        ``round(..., 2)``.  They come out of the section's own k pi r now,
        not out of a regex on its stdout (SPEC-002 1).
        """
        scale = koide_scale_mev() * PHI**12 / 1000     # GeV per zero at sigma_IR = 12
        for planck, printed in (
            (M_PLANCK_GEV, (39.33, 93.74)),
            (M_PLANCK_REDUCED_GEV, (37.72, 90.39)),
        ):
            kpr = kpi_r_from_scale(planck, scale)
            got = (round(kpr, 2), round(12 + kpr / LN_PHI, 2))
            assert got == pytest.approx(printed, abs=5e-3), (planck, got)

    def test_the_four_graviton_zeros_are_the_printed_four(self):
        """main.tex L1612 and L1613: 3.8317, 7.0156, 10.1735, 13.3237.

        AUD-001, class b, cited to test_vector_ratio_range; section 1
        prints them with ``np.round(g_, 4)`` at both Planck masses.
        """
        scale = koide_scale_mev() * PHI**12 / 1000
        epsilon = math.exp(-kpi_r_from_scale(M_PLANCK_GEV, scale))
        got = np.round(graviton_two_brane_roots(epsilon), 4)
        assert got == pytest.approx(
            [3.8317, 7.0156, 10.1735, 13.3237], abs=5e-5
        ), got

    def test_the_lyr_vector_table_is_the_printed_four(self):
        """main.tex L1617 and L1618: the LYR vector zeros 2.45, 5.57, 8.7, 11.84.

        AUD-001, class b, cited to test_vector_ratio_range: the four LYR
        figures live in the label section 1 prints, and the section's own
        four-decimal zeros are asserted beside them.  The label check is
        now the value check that the zeros sit within one unit of the
        LYR table's last digit (SPEC-002 1).
        """
        scale = koide_scale_mev() * PHI**12 / 1000
        epsilon = math.exp(-kpi_r_from_scale(M_PLANCK_GEV, scale))
        got = np.round(vector_two_brane_roots(epsilon), 4)
        assert got == pytest.approx(
            [2.4448, 5.5615, 8.6958, 11.834], abs=5e-5
        ), got
        assert got == pytest.approx(LYR_VECTOR_TABLE, abs=0.01), got

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

    def test_a_converges_with_the_number_of_exact_zeros(self):
        """A(K=20) and A(K=60) agree to 5e-5 (McMahon tail + Hurwitz zeta).

        Both sums used to be read from the section's stdout as eight
        significant digits; ``casimir_sums`` produces them that way here
        (SPEC-002 1).
        """
        a20 = casimir_sums(20)[0]
        a60 = casimir_sums(60)[0]
        assert a20 == pytest.approx(0.22327442, abs=5e-9), a20
        assert abs(a60 - a20) < 5e-5, (a20, a60)

    def test_b_is_positive(self):
        """B(K=60) > 0 -- the section's own ``sign B: +`` line, as a value."""
        b = casimir_sums(60)[1]
        assert b > 0, b

    def test_depth_is_minus_log_s_over_log_phi(self):
        """log_phi(1/s*) = -log s* / log phi, checked against the printed depth.

        The two figures used to be read from the section's K=60 line as
        eight significant digits; they come out of ``casimir_sums`` that
        way now (SPEC-002 1), so the check keeps its 5e-8 window.
        """
        _a, _b, log_s, depth = casimir_sums(60)
        assert -log_s / LN_PHI == pytest.approx(depth, abs=5e-8)
        assert depth == pytest.approx(1.0694864, abs=5e-8)


# ═══════════════════════════════════════════════════════════ section 3 ══
class TestSection3TwoBraneSpectra:
    """section 3 -- 'Two-brane spectra (Proposition of the two-brane model)'"""

    @pytest.mark.parametrize("depth,printed", [(6, 2.093), (12, 2.171), (30, 2.241)])
    def test_vector_ratio_grows_with_the_depth(self, depth, printed):
        """Exact two-brane condition: m2/m1 -> 2.295 as the throat deepens.

        The quotient used to be read from the section's stdout at its
        three-decimal print; ``vector_two_brane_roots`` produces it here
        (SPEC-002 1).
        """
        roots = vector_two_brane_roots(PHI**-depth, count=3)
        got = round(float(roots[1] / roots[0]), 3)
        assert got == pytest.approx(printed, abs=R3), (depth, got)

    def test_graviton_zeros_are_the_j1_zeros(self):
        """The graviton tower at the Planck top is the J1 table (section 3)."""
        scale = M_GEV * PHI**12
        epsilon = math.exp(-kpi_r_from_scale(M_PLANCK_GEV, scale))
        got = np.round(graviton_two_brane_roots(epsilon, count=3), 4)
        assert got == pytest.approx(list(jn_zeros(1, 3)), abs=5e-5), got

    def test_vector_zeros_against_the_lyr_table(self):
        """x_1^vec/x_1^grav = 0.6381; the vector zeros track LYR 2.45, 5.57, 8.7.

        The zeros, the quotient and the LYR gluon band used to come from
        the section's stdout; they are computed here now (SPEC-002 1), at
        the section's print precision.
        """
        scale = M_GEV * PHI**12
        epsilon = math.exp(-kpi_r_from_scale(M_PLANCK_GEV, scale))
        graviton = graviton_two_brane_roots(epsilon, count=3)
        vec_roots = vector_two_brane_roots(epsilon, count=3)
        vec = np.round(vec_roots, 4)
        assert vec == pytest.approx([2.4448, 5.5615, 8.6958], abs=5e-5), vec
        # both factors are printed at 4 decimals, so the quotient of the
        # printed values carries up to 1e-4 of rounding propagation
        assert vec[0] / jn_zeros(1, 1)[0] == pytest.approx(0.6381, abs=1e-4)
        assert round(float(vec_roots[0] / graviton[0]), 4) == pytest.approx(
            0.6381, abs=5e-5
        )
        # the LYR gluon band in units of the graviton, as section 3 prints it
        assert (round(3600 / 380, 2), round(4000 / 380, 2)) == (9.47, 10.53)

    def test_uv_depth_in_levels(self):
        """k pi r = 39.33 = 81.74 levels, sigma_UV = 12 + 81.74 = 93.74.

        The three figures used to be read from the section's stdout at its
        two-decimal print; they are computed here the same way
        (SPEC-002 1).
        """
        kpr_raw = kpi_r_from_scale(M_PLANCK_GEV, M_GEV * PHI**12)
        levels_raw = kpr_raw / LN_PHI
        kpr = round(kpr_raw, 2)
        levels = round(levels_raw, 2)
        sigma_uv = round(12 + levels_raw, 2)
        assert levels * LN_PHI == pytest.approx(kpr, abs=5e-3)
        assert 12 + levels == pytest.approx(sigma_uv, abs=5e-3)
        assert sigma_uv == pytest.approx(93.74, abs=5e-3)

    def test_lyr_gluon_over_graviton(self):
        assert round(3600 / 380, 2) == 9.47
        assert round(4000 / 380, 2) == 10.53


# ═══════════════════════════════════════════════════════════ section 4 ══
class TestSection4MetricPositivity:
    """section 4 -- 'Metric and reflection positivity (Proposition of the metric, §4)'"""

    def test_standard_product_is_not_positive(self):
        """In the standard product sym(T) has a negative eigenvalue for a >= 0.2.

        The three minima used to be read from the section's stdout at its
        ``.3e`` print; ``sym_t_min_eigenvalues`` produces them here
        (SPEC-002 1).
        """
        vals = sym_t_min_eigenvalues(weighted=False)
        assert len(vals) == 3, vals
        assert vals[0] > 0 and vals[1] < 0 and vals[2] < 0, vals

    def test_sym_t_eigenvalues_are_the_printed_three(self):
        """The three magnitudes: +0.35 at a=0.05, -0.06 at a=0.2, -2.83 at a=1."""
        vals = sym_t_min_eigenvalues(weighted=False)
        assert len(vals) == 3, vals
        assert vals == pytest.approx([0.35, -0.06, -2.83], abs=5e-3), vals

    def test_eta_weighted_product_is_positive(self):
        """<f,Tf>_eta > 0 for a = 0.05, 0.2, 1.0: the metric restores positivity."""
        vals = sym_t_min_eigenvalues(weighted=True)
        assert len(vals) == 3, vals
        assert all(v > 0 for v in vals), vals

    def test_eta_is_the_sqrt_minus_g_of_the_metric(self):
        """eta_sigma == e^{4A(sigma)} with A = -sigma log phi (section 4's claim)."""
        _k, eta = tower_operator()
        warp = -np.arange(7) * LN_PHI
        assert np.allclose(np.diag(eta), np.exp(4 * warp))

    def test_K_is_self_adjoint_in_the_eta_product_only(self):
        k, eta = tower_operator()
        assert not np.allclose(k, k.T), "not in the standard product"
        assert np.allclose(eta @ k, (eta @ k).T), "self-adjoint in <u,v>_eta"


# ═══════════════════════════════════════════════════════════ section 5 ══
class TestSection5QuarterPhase:
    """section 5 -- 'Phase 1/4 (Corollary of the phase)'"""

    def test_measured_phase_in_d4_is_a_quarter(self):
        """d=4: measured phase 0.233 against the asymptotic (d-3)/4 = 0.25.

        The three figures used to be read from the section's stdout at its
        print precision (.2f, .3f, .2f); they are computed here the same
        way (SPEC-002 1).
        """
        asym, measured, rms = measured_phase(4)
        asym, measured, rms = round(asym, 2), round(measured, 3), round(rms, 2)
        assert asym == pytest.approx(0.25, abs=1e-9)
        assert abs(measured - asym) <= 0.02, (measured, asym)
        assert rms <= 0.6, rms

    def test_free_phase_fit_is_not_better(self):
        """Two parameters (theta free) give rms 0.57%, no better than the 1/4.

        Both figures used to be read from the section's stdout at its
        .3f/.2f print; ``free_phase_fit`` produces them here (SPEC-002 1).
        """
        theta, rms = free_phase_fit()
        theta, rms = round(theta, 3), round(rms, 2)
        assert theta == pytest.approx(0.217, abs=R3), theta
        assert rms <= 0.6, rms


# ═══════════════════════════════════════════════════════════ section 6 ══
class TestSection6BesselChain:
    """section 6 -- 'Bessel chain (Bessel theorem, Observation of levels)'"""

    @pytest.mark.parametrize(
        "window,printed_rms", [("0,6", 1.00), ("-6,6", 0.54), ("-20,6", 0.54)]
    )
    def test_rms_against_the_lyr_table(self, window, printed_rms):
        """rms of the M=32 chain against the LYR table, per window.

        The rms used to be read from the section's stdout at its
        two-decimal print; ``chain_masses`` and ``scale_fit_rms`` produce
        it here (SPEC-002 1).
        """
        start, end = (int(v) for v in window.split(","))
        masses = chain_masses(start, end, 32, 4, 2)
        rms = round(scale_fit_rms(masses), 2)
        assert rms == pytest.approx(printed_rms, abs=R2), (window, rms)
        assert len(masses) == 4

    def test_deep_chain_yields_the_j1_zeros(self):
        """sigma[-6,6], M=32 -> 1.8308, 2.6545, 3.4757: within 0.05% of J1.

        The residual 1.5e-3 on the fourth ratio is the discretisation error
        of the M=32 chain (the section itself reports rms 0.54% against data).
        main.tex L1296: the shallow window's m2/m1 (1.8421) differs from the
        deep value (1.8308) by 0.011, i.e. 0.6%.  Both ratio lists used to
        be read from the section's stdout at its four-decimal print; they
        are computed here the same way (SPEC-002 1).
        """
        deep = chain_masses(-6, 6, 32, 4, 2)
        got = list(np.round(deep / deep[0], 4))
        j = jn_zeros(1, 4)
        want = list(j / j[0])
        assert got[0] == pytest.approx(1.0, abs=1e-12)
        assert got[1:] == pytest.approx(want[1:], rel=2e-3), got
        shallow = chain_masses(0, 6, 32, 4, 2)
        shallow_ratios = list(np.round(shallow / shallow[0], 4))
        diff = shallow_ratios[1] - got[1]
        assert round(diff, 3) == 0.011, diff
        assert round(100 * diff / got[1], 1) == 0.6, diff

    def test_without_the_weight_the_chain_degrades(self):
        """sigma[-6,6], M=32 without the e^{2A} weight: 1, 2.227, 3.458, 4.687."""
        masses = chain_masses(-6, 6, 32, 4, 0)
        ratios = np.round(masses / masses[0], 3)
        assert ratios == pytest.approx([1.0, 2.227, 3.458, 4.687], abs=5e-4), ratios


# ═══════════════════════════════════════════════════════════ section 7 ══
class TestSection7Prediction:
    """section 7 -- 'Prediction and what is not claimed (§10, §11)'"""

    @pytest.mark.parametrize(
        "m,dm,printed", [(700, 20, 0.110), (1000, 30, 0.159), (1322, 40, 0.211)]
    )
    def test_error_on_the_ratios(self, m, dm, printed):
        """sigma(m/380) = (m/380) hypot(dm/m, 20/380) -- recomputed here.

        The section's E5 line carried two figures; the ratio is the data
        ratio main.tex L691 quotes, and the error is recomputed below
        (SPEC-002 1).
        """
        ratio = m / 380.0
        err = ratio * math.hypot(dm / m, 20 / 380)
        assert round(ratio, 3) == E5_RATIOS[m], (m, ratio)
        assert round(err, 3) == printed, (m, err)

    def test_gluon_scale_needs_three_levels(self):
        """gluon scale: log_phi(scale/graviton) = 5.39, at the .2f print.

        The scale used to be read from the section's E4 line; it comes
        out of ``sector_scales`` now (SPEC-002 1).  The CW6 ladder the
        section prints next to it reads its gluon/graviton gap off itself:
        sigma_G = 2 and SU(3) = 5 are three levels apart.
        """
        graviton_scale, gluon_scale = sector_scales()
        got = round(math.log(gluon_scale / graviton_scale) / LN_PHI, 2)
        assert got == pytest.approx(5.39, abs=R2), got
        # CW6: sigma_G=2, U(1)=3, SU(2)=4, SU(3)=5 -> gluon/graviton would
        # require Delta sigma = 3
        sigma_gravity, _u1, _su2, gluon = 2, 3, 4, 5
        assert gluon - sigma_gravity == 3


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

    def test_rs_fit_beats_the_golden_fit(self):
        """rms RS = 0.5% against rms phi^k = 12.1% (one parameter each).

        The section printed both on one line; the RS figure is recomputed
        below and the golden one comes out of ``golden_ladder_rms`` now
        (SPEC-002 1), at the section's one-decimal print.
        """
        obs = np.array(OBS_G)
        xi = jn_zeros(1, 4)
        m_rs = (obs @ xi) / (xi @ xi)
        rms_rs = 100 * np.sqrt(np.mean(((obs - m_rs * xi) / obs) ** 2))
        assert round(rms_rs, 1) == 0.5, rms_rs
        assert round(golden_ladder_rms(), 1) == 12.1

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

    def test_discrete_kk_operator_matches_its_closed_form(self):
        """eig(L) = (-2 + 2 cos(k pi/8)) / ln^2 phi for the 7-level operator.

        The section also printed the symmetrised hopping that makes the
        similarity exact; it is asserted as a value now (SPEC-002 1).
        """
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
        assert math.sqrt(PHI**2 * PHI**-2) == 1.0
