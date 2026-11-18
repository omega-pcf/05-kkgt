"""Section 47 of the v138 provenance: the figures the manuscript will quote.

«La tríada como código, la cuerda como corte, y el código pentagonal» is
the section the author added with the v138 round (``reproduce_v138.py``,
47/47); the registry holds 1..47 and the census pins that.  Every check
here stays the *independent* kind — the quantity is recomputed from its
closed form and compared with the figure the original prints, at the
width of that print (decision (ii) of AUD-001) — and
``pentagonal_code_statements`` carries the section's own body into this
module (SPEC-002 §1): it fails on values, with pytest's assertion
rewriting, and no test here reads a section's stdout.  The stdout quoted
in each docstring was captured from ``reproduce_v138.py 47`` on
2026-11-17 and matches what the ported section prints.
"""

from __future__ import annotations

import itertools
import math

import numpy as np
import pytest

from kkgt.constants import PHI


def _pentagon_side() -> float:
    """The side a of the {5,4} pentagon: cosh a = phi, sinh a = sqrt(phi)."""
    return 2 * math.acosh(math.cos(math.pi / 5) / math.sin(math.pi / 4))


# The Minkowski signature of the hyperbolic space {5,4} lives in, and the
# decagon the reflection walk starts from: both used to be typed inside
# the walk and are shared now with the section's own statements below.
_SIGNATURE = np.diag([-1.0, 1.0, 1.0])


def _minkowski(u: np.ndarray, x: np.ndarray) -> float:
    """The Minkowski product of signature (-,+,+) on R^3."""
    return float(u @ _SIGNATURE @ x)


def _base_decagon() -> list[np.ndarray]:
    """The five vertices of the decagon at the half-level radius.

    cosh r0 = 1 / (tan pi/5 tan pi/4): the seed the walk reflects across
    each of its adjacent edges.
    """
    r0 = math.acosh(1 / (math.tan(math.pi / 5) * math.tan(math.pi / 4)))
    return [np.array([math.cosh(r0), math.sinh(r0) * math.cos(2 * math.pi * k / 5),
                      math.sinh(r0) * math.sin(2 * math.pi * k / 5)])
            for k in range(5)]


def _layer_counts(layers: int = 6) -> list[tuple[int, int]]:
    """(pentagons, boundary legs) per layer of the {5,4} construction.

    The reflection walk of the original section 47: the decagon at the
    half-level radius, reflected across each adjacent edge, six times.
    """
    t0 = _base_decagon()

    def refl(p, q):
        n = _SIGNATURE @ np.cross(p, q)
        n = n / math.sqrt(_minkowski(n, n))
        return np.eye(3) - 2 * np.outer(n, _SIGNATURE @ n)

    key = lambda p: (round(p[1] / (1 + p[0]), 6) + 0.0,
                     round(p[2] / (1 + p[0]), 6) + 0.0)
    tk = lambda vs: tuple(sorted(key(x) for x in vs))

    def counts(tiles):
        edges = {}
        for vs in tiles.values():
            for k in range(5):
                ed = tuple(sorted((key(vs[k]), key(vs[(k + 1) % 5]))))
                edges[ed] = edges.get(ed, 0) + 1
        return len(tiles), sum(1 for c in edges.values() if c == 1)

    tiles = {tk(t0): t0}
    last = [t0]
    res = [counts(tiles)]
    for _ in range(layers):
        nuevo = []
        for vs in last:
            for k in range(5):
                nv = [refl(vs[k], vs[(k + 1) % 5]) @ x for x in vs]
                if tk(nv) not in tiles:
                    tiles[tk(nv)] = nv
                    nuevo.append(nv)
        last = nuevo
        res.append(counts(tiles))
    return res


# ═══════════════════════════ section 47's own statements (migrated) ════
def pentagonal_code_statements() -> None:
    """Every statement section 47 checked for the pentagonal code.

    Migrated from the section itself (SPEC-002 §1): the triad, the
    string as a cut, the six-leg tensor of the five-qubit code, the side
    of the pentagon and the reflection walk.  The side and the walk are
    the module's own ``_pentagon_side`` / ``_layer_counts``; each number
    the section printed is asserted at the width of that print, and
    every tolerance is the section's own, unchanged.
    """
    # ── the triad: a code with a one-dimensional subspace ─────────────
    omega = np.exp(2j * np.pi / 3)
    triad = 0.5 * omega ** np.arange(3)
    code = (triad / np.linalg.norm(triad)).reshape(3, 1)
    projector = code @ code.conj().T
    assert np.allclose(code.conj().T @ code, 1)
    assert np.linalg.matrix_rank(projector) == 1
    assert np.allclose(projector @ projector, projector)
    fourier = np.array([[omega ** (j * k) for k in range(3)]
                        for j in range(3)]) / np.sqrt(3)
    assert np.allclose(code[:, 0], fourier[:, 1])
    assert np.allclose(fourier.conj().T @ fourier, np.eye(3))
    assert abs(triad.sum()) < 1e-12

    # ── the string as a cut: half the ring at every level ─────────────
    for level in (0, 3, 6, 12):
        assert np.isclose(2 * np.pi * PHI ** level / 2, np.pi * PHI ** level)

    # ── the six-leg perfect tensor of the [[5,1,3]] code ──────────────
    identity = np.eye(2)
    bit_flip = np.array([[0, 1], [1, 0]])
    phase_flip = np.diag([1, -1])

    def kron(*matrices: np.ndarray) -> np.ndarray:
        """The Kronecker product of any number of matrices."""
        product = np.array([[1.0]])
        for matrix in matrices:
            product = np.kron(product, matrix)
        return product

    code_projector = np.eye(32)
    for gate in (
        kron(bit_flip, phase_flip, phase_flip, bit_flip, identity),
        kron(identity, bit_flip, phase_flip, phase_flip, bit_flip),
        kron(bit_flip, identity, bit_flip, phase_flip, phase_flip),
        kron(phase_flip, bit_flip, identity, bit_flip, phase_flip),
    ):
        code_projector = code_projector @ (np.eye(32) + gate) / 2
    assert np.linalg.matrix_rank(code_projector) == 2
    eigenvalues, eigenvectors = np.linalg.eigh(
        code_projector
        @ kron(phase_flip, phase_flip, phase_flip, phase_flip, phase_flip)
        @ code_projector
    )
    six_leg = np.stack([
        eigenvectors[:, np.argmax(eigenvalues)],
        eigenvectors[:, np.argmin(eigenvalues)],
    ]).reshape([2] * 6)
    for left in itertools.combinations(range(6), 3):
        right = [i for i in range(6) if i not in left]
        block = np.transpose(six_leg, list(left) + right).reshape(8, 8)
        gram = block @ block.conj().T
        assert np.allclose(gram, np.eye(8) * np.trace(gram) / 8)

    # ── the side of the pentagon of {5,4} ─────────────────────────────
    side = _pentagon_side()
    assert np.isclose(np.cosh(side), PHI)
    assert np.isclose(np.sinh(side), PHI ** 0.5)
    assert np.isclose(side, np.arcsinh(PHI ** 0.5))
    # printed: "lado del pentagono: ... a = {side:.6f} = arsinh(phi^(1/2))"
    assert f"{side:.6f}" == "1.061275"
    decagon = _base_decagon()
    assert np.isclose(np.arccosh(-_minkowski(decagon[0], decagon[1])), side)

    # ── the counts, layer by layer ────────────────────────────────────
    pentagons, legs = (list(counts) for counts in zip(*_layer_counts()))
    fibonacci, lucas = [0, 1], [2, 1]
    for _ in range(20):
        fibonacci.append(fibonacci[-1] + fibonacci[-2])
        lucas.append(lucas[-1] + lucas[-2])
    assert pentagons == [5 * fibonacci[2 * n + 1] - 4 for n in range(7)]
    assert legs == [5 * lucas[2 * n + 1] for n in range(7)]
    # printed: "capas por arista: pentagonos [...] = 5F(2n+1)-4; ..."
    rate = pentagons[6] / legs[6]
    # printed: "tasa en la capa 6: {rate:.4f}; limite F/L = 1/sqrt5 = ..."
    assert f"{rate:.4f}" == "0.4457"
    assert f"{5 ** -0.5:.4f}" == "0.4472"
    assert abs(rate - 5 ** -0.5) < 2e-3
    assert f"{PHI ** 2:.4f}" == "2.6180"

    # ── the cut: crossings per unit of length ─────────────────────────
    crossings = 10 * side / math.pi ** 2
    assert np.isclose(crossings, 2 / math.pi * (5 * side / 2) / (math.pi / 2))
    # printed: "Crofton: {crossings:.4f} cruces por unidad de longitud; ..."
    assert f"{crossings:.4f}" == "1.0753"
    assert f"{crossings * math.log(2):.3f}" == "0.745"
    assert f"{crossings * math.log(2) / 0.5:.2f}" == "1.49"
    assert f"{math.exp(0.5 / crossings):.3f}" == "1.592"


class TestSection47ThePentagonalCode:
    """section 47 -- 'La tríada como código, la cuerda como corte, y el
    código pentagonal' (v138, section 47 of the census)."""

    def test_the_pentagon_side_is_the_printed_1_061275(self):
        """The original prints ``a = 1.061275`` with ``.6f``.

        cosh a = phi and sinh a = phi^(1/2), the radius of the level-1/2
        disc; the three relations are the ones the section asserts.
        """
        a = _pentagon_side()
        assert f"{a:.6f}" == "1.061275"
        assert math.cosh(a) == pytest.approx(PHI, abs=1e-12)
        assert math.sinh(a) == pytest.approx(PHI ** 0.5, abs=1e-12)
        assert a == pytest.approx(math.asinh(PHI ** 0.5), abs=1e-12)

    def test_the_layer_counts_are_five_f_odd_minus_four_and_five_l_odd(self):
        """``pentágonos [1, 6, 21, 61, 166, 441, 1161] = 5F(2n+1)-4`` and
        ``patas de frontera [5, 20, 55, 145, 380, 995, 2605] = 5L(2n+1)``.

        main.tex will quote the ratio 5F(2n+1)-4 / 5L(2n+1); both sequences
        are re-derived here from the reflection walk, not copied.
        """
        res = _layer_counts()
        pentagons = [r[0] for r in res]
        legs = [r[1] for r in res]
        fib, luc = [0, 1], [2, 1]
        for _ in range(20):
            fib.append(fib[-1] + fib[-2])
            luc.append(luc[-1] + luc[-2])
        assert pentagons == [5 * fib[2 * n + 1] - 4 for n in range(7)]
        assert legs == [5 * luc[2 * n + 1] for n in range(7)]

    def test_the_layer_six_rate_tends_to_one_over_root_five(self):
        """``tasa en la capa 6: 0.4457; límite F/L = 1/sqrt5 = 0.4472``.

        The section's own bound is ``abs(rate - 1/sqrt(5)) < 2e-3``; the
        printed rate carries the ``.4f`` width, so it is asserted at 5e-5
        and the limit at half a unit of 0.4472.
        """
        res = _layer_counts()
        rate = res[6][0] / res[6][1]
        assert f"{rate:.4f}" == "0.4457"
        assert f"{5 ** -0.5:.4f}" == "0.4472"
        assert abs(rate - 5 ** -0.5) < 2e-3, rate
        assert f"{PHI ** 2:.4f}" == "2.6180"

    def test_the_chosen_cut_is_the_printed_0_745(self):
        """``Crofton: 1.0753 cruces por unidad de longitud; con chi=2,
        0.745 frente a 1/2: 1.49 S en promedio``.

        cro = 10 a / pi^2 with the side a above; each figure carries the
        width of its own print (.4f, .3f, .2f).
        """
        cro = 10 * _pentagon_side() / math.pi ** 2
        assert f"{cro:.4f}" == "1.0753"
        assert f"{cro * math.log(2):.3f}" == "0.745"
        assert f"{cro * math.log(2) / 0.5:.2f}" == "1.49"

    def test_the_chi_that_would_give_s_is_the_printed_1_592(self):
        """``chi que daría S: 1.592`` — exp(0.5 / cro), the .3f print."""
        cro = 10 * _pentagon_side() / math.pi ** 2
        assert f"{math.exp(0.5 / cro):.3f}" == "1.592"

    def test_section47s_own_statements_hold(self):
        """The body of section 47, asserted here on its values.

        ``pentagonal_code_statements`` carries every check the section
        made -- the triad, the string as a cut, the six-leg tensor, the
        pentagon side and the layer counts -- into this module
        (SPEC-002 §1): nothing here reads a section's stdout, and each
        number the section printed is asserted at the width of that
        print, with pytest's assertion rewriting.
        """
        pentagonal_code_statements()
