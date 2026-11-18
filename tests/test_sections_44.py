"""Deep numeric tests for section 44 of kkgt.sections.

Section 44 draws figure 1 (``fig_background.pdf``) and checks every
statement it draws before drawing it: the torus and the third direction,
the frame along the diagonal, the turn of each cell, the projections of
the windows, the contact geometry of the icosahedron and the Fibonacci
words of the tiling.  What the section asserts, this class recomputes.

The figure contract itself (the section writes the file, the caption names
the test) lives in ``test_section_census.py``.
"""

from __future__ import annotations

import itertools
import math

import numpy as np
import pytest

from kkgt.constants import EPS0, M_PCF, PHI, PHI_BAR
from kkgt.harness import verify_figure_artifact

# words of the substitution A -> AB, B -> A with seed AAB (section 44
# asserts over the thirteen words it draws)
_WORDS = ["AAB"]
for _ in range(12):
    _WORDS.append("".join({"A": "AB", "B": "A"}[c] for c in _WORDS[-1]))


# ══════════════════════════════════════════════════════════ section 44 ══
class TestSection44BackgroundFigure:
    """section 44 -- 'The Background figure: one structure seen at once (Figure 1)'"""

    def test_the_triad_sits_on_the_ring_of_radius_half(self):
        """(a)(b) the three v_k = 1/2 omega^k lie on |z| = 1/2 (I12)."""
        w = np.exp(2j * np.pi / 3)
        v3 = [0.5 * w**k for k in range(3)]
        assert np.allclose([abs(v) for v in v3], 0.5)

    def test_the_clifford_torus_projects_to_a_surface_of_revolution(self):
        """(a) stereographic image: (rho - sqrt2)^2 + z^2 = 1 (atol 1e-9)."""
        aa, bb = np.meshgrid(np.linspace(0, 2 * np.pi, 40),
                             np.linspace(0, 2 * np.pi, 40))
        xc = np.stack([np.cos(aa), np.sin(aa), np.cos(bb), np.sin(bb)]) / np.sqrt(2)
        p = xc[:3] / (1 - xc[3])
        rho = np.hypot(p[0], p[1])
        assert np.allclose((rho - np.sqrt(2)) ** 2 + p[2] ** 2, 1, atol=1e-9)

    @staticmethod
    def _project(d, up):
        """The frame section 44 uses: an orthonormal pair spanning the plane."""
        d = np.array(d, float)
        d /= np.linalg.norm(d)
        up = np.array(up, float)
        a1 = np.cross(up, d)
        a1 /= np.linalg.norm(a1)
        a2 = np.cross(d, a1)
        return lambda p: np.array([np.array(p, float) @ a1, np.array(p, float) @ a2])

    def test_the_frame_along_the_diagonal_is_at_120_degrees(self):
        """(d) seen along (1,1,1): three axes at 120 degrees, |.|^2 = 2/3."""
        f = self._project((1, 1, 1), (0, 0, 1))
        pr = [f(e) - f((0, 0, 0)) for e in np.eye(3)]
        angles = [math.degrees(math.acos(pr[i] @ pr[j]
                                         / np.linalg.norm(pr[i])
                                         / np.linalg.norm(pr[j])))
                  for i, j in [(0, 1), (1, 2), (0, 2)]]
        assert np.allclose(angles, 120)
        assert np.allclose([np.linalg.norm(p) ** 2 for p in pr], 2 / 3)

    @pytest.mark.parametrize("s", range(6))
    def test_every_cell_carries_the_phase(self, s):
        """(d) eps0 phi^s M phi^-s = pi at every level the panel draws (1e-12)."""
        cell_phase = EPS0 * PHI**s * M_PCF * PHI**-s
        assert abs(cell_phase - math.pi) < 1e-12, s
        assert abs(EPS0 * M_PCF - math.pi) < 1e-12

    def test_phi_and_its_conjugate_multiply_to_minus_one(self):
        """(e) phi^n phibar^n = (-1)^n for the levels drawn in the window."""
        for n in range(-4, 6):
            x, y = PHI**n, PHI_BAR**n
            assert abs(x * y - (-1) ** n) < 1e-9, n

    def test_the_window_cut_gives_the_fibonacci_gaps(self):
        """(e) the window [-1, phi-1) cuts the line into gaps 1 and phi."""
        pts = [(a, b) for a in range(-12, 13) for b in range(-9, 10)]
        x1 = np.array([a + b * PHI for a, b in pts])
        x2 = np.array([a + b * PHI_BAR for a, b in pts])
        keep = (abs(x1) < 12) & (abs(x2) < 4) & (x2 >= -1) & (x2 < PHI - 1)
        ch = np.sort(x1[keep])
        gaps = set(np.round(np.diff(ch), 6))
        assert gaps == {round(1.0, 6), round(PHI, 6)}
        assert len(gaps) == 2

    def test_the_3x3x3_cube_casts_nineteen_shadows(self):
        """(f) {0,1,2}^3 projects along (1,1,1) onto 19 points, in 3 layers."""
        n3 = np.ones(3) / 3 ** 0.5
        p3 = np.array(list(itertools.product(range(3), repeat=3)), float)
        proj = p3 - ((p3 - np.array([-1.3] * 3)) @ n3)[:, None] * n3
        sh: dict = {}
        for p, q in zip(p3, proj):
            sh.setdefault(tuple(np.round(q, 9)), []).append(p)
        assert len(sh) == 19
        assert all(len({int(p.sum()) % 3 for p in ps}) == 1 for ps in sh.values())

    @pytest.mark.parametrize("side,shadows", [(3, 19), (5, 61), (7, 127)])
    def test_the_windows_of_the_panel_cast_their_shadows(self, side, shadows):
        """(f) {0..L-1}^3 casts 3L^2-3L+1 shadows for L = 3, 5, 7."""
        e1 = np.array([1, -1, 0]) / 2 ** 0.5
        e2 = np.cross(np.ones(3) / 3 ** 0.5, e1)
        pts = np.array(list(itertools.product(range(side), repeat=3)), float)
        got = len({tuple(np.round([p @ e1, p @ e2], 9)) for p in pts})
        assert got == shadows == 3 * side * side - 3 * side + 1

    def test_the_twelve_contact_points_have_thirty_edges(self):
        """(g) |v|^2 = phi + 2 < 4 and 30 pairs sit exactly at distance 2."""
        v = []
        for s1 in (1, -1):
            for s2 in (1, -1):
                p = (0, s1, s2 * PHI)
                v += [p, (p[1], p[2], p[0]), (p[2], p[0], p[1])]
        v = np.array(v, float)
        assert np.allclose((v ** 2).sum(1), PHI + 2)
        assert PHI + 2 < 4
        edges = [(i, j) for i, j in itertools.combinations(range(12), 2)
                 if abs(((v[i] - v[j]) ** 2).sum() - 4) < 1e-9]
        assert len(edges) == 30

    def test_the_rectangle_of_the_third_direction_is_golden(self):
        """(g) each of the three rectangles has its sides in the ratio phi."""
        for ii in range(3):
            rr = np.array([[0, 1, PHI], [0, -1, PHI], [0, -1, -PHI],
                           [0, 1, -PHI]], float)[:, [(0 - ii) % 3, (1 - ii) % 3,
                                                     (2 - ii) % 3]]
            s1 = np.linalg.norm(rr[0] - rr[1])
            s2 = np.linalg.norm(rr[1] - rr[2])
            assert abs(max(s1, s2) / min(s1, s2) - PHI) < 1e-12, ii

    @pytest.mark.parametrize("s", range(13))
    def test_the_words_of_the_tiles_are_fibonacci(self, s):
        """(h) len = F_{s+4}, A = F_{s+3}, B = F_{s+2}, and S = pi phi^s."""
        f = [0, 1]
        for _ in range(20):
            f.append(f[-1] + f[-2])
        w = _WORDS[s]
        a, b = w.count("A"), w.count("B")
        assert len(w) == f[s + 4] and a == f[s + 3] and b == f[s + 2]
        assert abs(math.pi * (a / PHI**2 + b / PHI**3)
                   - math.pi * PHI**s) < 1e-9, s

    @pytest.mark.figure
    def test_section44_draws_the_background_figure(self, run_section):
        run = run_section(44)
        run.has("background statements: all checks ok")
        # section 44 checks figure 1 but no longer draws it (SPEC-002 §1.1)
        verify_figure_artifact("fig_background.pdf")
