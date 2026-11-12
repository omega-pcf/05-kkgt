"""Constants shared by the tests of the manuscript.

Every value here is either a closed form (golden ratio, M_PCF, ...) or a
number ``kkgt.sections`` prints and ``main.tex`` cites; the comment on each
line records the section that produces it, so the section->test mapping of
the suite stays auditable.
"""

from __future__ import annotations

import math

# ── Golden ring ──────────────────────────────────────────────────────────
PHI = (1 + 5 ** 0.5) / 2                 # golden ratio
PHI_BAR = (1 - 5 ** 0.5) / 2             # Galois conjugate, |phi_bar| = 1/phi
LN_PHI = math.log(PHI)                   # 0.48121182505960347

# ── Sections 12, 33, 42: the two units of the ring ───────────────────────
# M_PCF = 6 sqrt(3) pi / log phi  (section 12 prints it as "M_PCF = 67.846...")
M_PCF = 6 * math.sqrt(3) * math.pi / LN_PHI      # 67.84618925807165
EPS0 = LN_PHI / (6 * math.sqrt(3))               # 0.04630462945589886, eps0*M = pi

# ── Sections 1, 7, 8, 20, 21: the four graviton candidates of LYR (GeV) ──
OBS_G = (380.0, 700.0, 1000.0, 1322.0)

# ── Sections 16, 17, 18, 24: the scale M of (F1) and its unit ────────────
M_KOIDE_MEV = 313.84                      # MeV, (F1), used by sections 16-18
U_MEV = M_KOIDE_MEV / M_PCF               # 4.6258 MeV, the unit of (F1)
M_PLANCK_GEV = 1.22089e19                 # section 24 prints 1.22089e+19

# ── Sections 10, 44, 13, 39, 41: the five figures of the manuscript ───────
# main.tex includes exactly these five files and attributes each to a section.
FIGURES = {
    10: "fig_granularity.pdf",
    44: "fig_background.pdf",
    13: "fig_mobius_throat.pdf",
    39: "fig_throat_tiling.pdf",
    41: "fig_tilings_strip.pdf",
}

# ── Sections measured slower than 10 s on this machine ───────────────────
# section 41: 33.1 s (figure 5). Everything else runs in < 10 s: section 40
# (9.2 s), section 44 (2.2 s, figure 1), section 12 (0.8 s, checks only).
SLOW_SECTIONS = frozenset({41})
