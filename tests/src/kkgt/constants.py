"""Constants shared by the tests of the manuscript.

Every value here is either a closed form (golden ratio, M_PCF, ...), a
number the manuscript prints and ``main.tex`` cites, or a physical
constant the tests need; the comment on each line records the section
that produces it, so the section->test mapping of the suite stays
auditable.  Constants with two live definitions used to be
re-typed per file -- the tau mass and the CODATA values below are now
single-sourced here (SEC-001, layer 1).
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
M_GEV = M_KOIDE_MEV / 1000                # GeV: the same scale in the unit of the paper
U_MEV = M_KOIDE_MEV / M_PCF               # 4.6258 MeV, the unit of (F1)
M_PLANCK_GEV = 1.22089e19                 # section 24 prints 1.22089e+19 (from hbar, c, G)

# ── Sections 1, 16, 24: the tau mass that goes into M (F1) ───────────────
# One origin: only 1776.86 reproduces the printed M = 313.84 MeV (the
# former tau mass gave 313.851), matching sections 1, 16 and 24 and both reproduction
# scripts (AUD-001 section 9).  Every user of m_tau imports it from here.
M_TAU_MEV = 1776.86                       # MeV

# ── Physical constants (CODATA 2018 / SI), as the sections use them ──────
HBAR = 1.054571817e-34                    # J s
C_LIGHT = 299792458.0                     # m/s
G_NEWTON = 6.67430e-11                    # m^3 kg^-1 s^-2
MPC_M = 3.0856775814913673e22             # m

# ── Sections 10, 44, 13, 39, 41: the five figures of the manuscript ───────
# main.tex includes exactly these five files and attributes each to a section.
FIGURES = {
    10: "fig_granularity.pdf",
    44: "fig_background.pdf",
    13: "fig_mobius_throat.pdf",
    39: "fig_throat_tiling.pdf",
    41: "fig_tilings_strip.pdf",
}

# ── Byte-stability pin of those five figures (SPEC-002 §1.1) ──────────────
# md5 of ``images/<file>`` as committed.  ``pnpm run figures`` regenerates
# them byte for byte (SOURCE_DATE_EPOCH + pinned rcParams, see
# scripts/figures/generators/rc.py), so a different digest here means the
# pipeline changed: regenerate, review the diff of images/, and move the pin
# in the same commit.  Generation never happens inside a test.
FIGURE_MD5 = {
    "fig_background.pdf": "fb1c7f8f2872f6ee1293b951ac6f0bc3",
    "fig_granularity.pdf": "ab37500a351a265611d672769673b3b5",
    "fig_mobius_throat.pdf": "d63b8545ace9b1cf39d8ff4c3305b7e5",
    "fig_throat_tiling.pdf": "7acf424e21cf86ae2307fa00c07cb52d",
    "fig_tilings_strip.pdf": "b6b961d2bc9cdc76f6f047be4944888c",
}

# ── Sections measured slower than 10 s on this machine ───────────────────
# section 41: 12.7 s for its checks (33.1 s while it still drew figure 5;
# the drawing moved to scripts/figures, SPEC-002 §1.1). Everything else
# runs in < 10 s: section 40 (9.1 s), section 44 (2.2 s), section 12 (0.8 s).
SLOW_SECTIONS = frozenset({41})
