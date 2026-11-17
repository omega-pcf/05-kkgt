"""Section 47 of the v138 provenance: the figures the manuscript will quote.

«La tríada como código, la cuerda como corte, y el código pentagonal» is
the section the author added with the v138 round (``reproduce_v138.py``,
47/47).  Since the W4 port it lives in ``kkgt.sections`` as
``seccion_47`` (the registry holds 1..47 and the census pins that), and
``test_section_runs.py`` runs it; every check here stays the
*independent* kind — the quantity is recomputed from its closed form and
compared with the figure the original prints, at the width of that print
(decision (ii) of AUD-001).  The stdout quoted in each docstring was
captured from ``reproduce_v138.py 47`` on 2026-11-17 and matches what the
ported section prints.
"""

from __future__ import annotations

import math

import numpy as np
import pytest

from kkgt.constants import PHI


def _pentagon_side() -> float:
    """The side a of the {5,4} pentagon: cosh a = phi, sinh a = sqrt(phi)."""
    return 2 * math.acosh(math.cos(math.pi / 5) / math.sin(math.pi / 4))


def _layer_counts(layers: int = 6) -> list[tuple[int, int]]:
    """(pentagons, boundary legs) per layer of the {5,4} construction.

    The reflection walk of the original section 47: the decagon at the
    half-level radius, reflected across each adjacent edge, six times.
    """
    J = np.diag([-1.0, 1.0, 1.0])
    mink = lambda u, x: u @ J @ x
    r0 = math.acosh(1 / (math.tan(math.pi / 5) * math.tan(math.pi / 4)))
    t0 = [np.array([math.cosh(r0), math.sinh(r0) * math.cos(2 * math.pi * k / 5),
                    math.sinh(r0) * math.sin(2 * math.pi * k / 5)])
          for k in range(5)]

    def refl(p, q):
        n = J @ np.cross(p, q)
        n = n / math.sqrt(mink(n, n))
        return np.eye(3) - 2 * np.outer(n, J @ n)

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


class TestSection47ThePentagonalCode:
    """section 47 -- 'La tríada como código, la cuerda como corte, y el
    código pentagonal' (v138; not yet registered in ``kkgt.sections``)."""

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
