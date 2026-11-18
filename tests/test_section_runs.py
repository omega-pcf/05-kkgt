"""Execution contract: all 47 sections of kkgt.sections run clean.

Each case is one numbered section, identified as ``section-NN`` (the id is
what the mapping table in the report uses).  Running a section executes the
checks the author left inside it (``assert`` statements spread over
sections 11-13, 29, 37, 39-46) plus the number contract below: the exact
line of stdout that carries the number the manuscript cites.

Nothing is relaxed here: if a section raises, the test fails.
"""

from __future__ import annotations

import pytest

from kkgt.constants import FIGURES, SLOW_SECTIONS
from kkgt.harness import verify_figure_artifact

# section -> the stdout line that pins its headline number.
# Sources: the captured stdout of each section, cross-checked against the
# number quoted in main.tex where the tex quotes one.
MARKERS = {
    1: "residual J1 (0.54%, abstract 0.5%)",
    2: "depth log_phi(1/s*) = 1.0694317",
    3: "x1_vec/x1_grav = 0.6381",
    4: "K self-adjoint in <u,v>_eta = u.eta.v : True",
    5: "measured phase=0.233",
    6: "rms LYR=0.54%",
    7: "log_phi(scale/graviton)=5.39",
    8: "rms RS=0.5%",
    9: "N=1000 1.336",
    10: "worst gap ratio, phi, N<=5000: 2.618",
    11: "chain: |A5|/5 = 12",
    12: "all checks: ok",
    13: "ok",
    14: "gaps(100,1e3,1e4)=[3, 3, 3]",
    15: "L0=N/2  ln#states",
    16: "Koide from M:  1776.8761",
    17: "sigma_obs = 380.315",
    18: "sigma = 583.877",
    19: "8  0.2454",
    20: "(0.6 standard deviations from 12)",
    21: "fitted free scale: 99.64 GeV",
    22: "585.317 = W4 + log_phi 2",
    23: "phi^12 = 89 + 144 phi",
    24: "sigma_UV = log_phi(M_Pl/M) = 93.737",
    25: "161+261phi = 583.31",
    26: "first active integer level along both routes: 2 = sigma_G = n - 1 (CW6)",
    27: "log2 * phi^pi = 3.143254",
    28: "theta_3(e^-pi) = 1.086434811213",
    29: "Omega_L h^2 = 0.2928",
    30: "IR scale = M phi^12 = 101.06 GeV",
    31: "slope 0.7071 < bound 0.8165",
    32: "0.4737, 0.2928, 0.1809",
    33: "0.9140, 0.9140, 0.9140",
    34: "1/sqrt2 at +0.05 sigma",
    35: "f = 0.5: tau_F/tau_D = 1/sqrt(2f) = 1.0000",
    36: "S(12) = 1011.58",
    37: "fit lnD = a S + b ln L + c (sigma=3..9): a = 0.9972",
    38: "area law: 0.5 per ell^2 = 0.25 per ell_P^2",
    39: "(2, 1), (3, 2), (5, 3), (8, 5), (13, 8), (21, 13), (34, 21)",
    40: "pairs (tiling, chi<=16), p,q<=60: 50340",
    41: "{5,4} with qubits: 1.4907 S",
    42: "tau(12) = 0.2107",
    43: "14042 collisions",
    44: "background statements: all checks ok",
    45: "N bound: 3pi/(Lambda G_N) with G_N=1/2 = 6pi/Lambda = S_obs = pi phi^583.877",
    46: "the window weight is e^(-pi tan eta_n); it crosses 1/2 at n = 1.5702",
    47: "lado del pentágono: cosh a = phi, sinh a = phi^(1/2), a = 1.061275",
}


def _params():
    out = []
    for n in range(1, 48):
        marks = [pytest.mark.section]
        if n in SLOW_SECTIONS:
            marks.append(pytest.mark.slow)
        if n in FIGURES:
            marks.append(pytest.mark.figure)
        out.append(pytest.param(n, marks=marks, id=f"section-{n:02d}"))
    return out


@pytest.mark.parametrize("n", _params())
def test_section_runs_and_prints_its_number(run_section, n):
    run = run_section(n)
    run.has(MARKERS[n])
    if n in FIGURES:
        # The section writes nothing any more (SPEC-002 §1.1): the figure
        # is an artifact of `pnpm run figures`, pinned by its bytes.
        verify_figure_artifact(FIGURES[n])


def test_all_sections_covered():
    """The marker table must cover every registered section."""
    assert sorted(MARKERS) == list(range(1, 48))
