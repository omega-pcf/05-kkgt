"""Execution contract: all 43 sections of reproduce_v108.py run clean.

Each case is one numbered section, identified as ``section-NN`` (the id is
what the mapping table in the report uses).  Running a section executes the
checks the author left inside it (64 ``assert`` statements spread over
sections 11-13, 29, 37, 39-43) plus the number contract below: the exact
line of stdout that carries the number the manuscript cites.

Nothing is relaxed here: if a section raises, the test fails.
"""

from __future__ import annotations

import pytest

from kkgt.constants import FIGURES, SLOW_SECTIONS

# section -> the stdout line that pins its headline number.
# Sources: the captured stdout of each section, cross-checked against the
# number quoted in main.tex where the tex quotes one.
MARKERS = {
    1: "residual J1 (0.54%, abstract 0.5%)",
    2: "profundidad log_phi(1/s*) = 1.0694317",
    3: "x1_vec/x1_grav = 0.6381",
    4: "K autoadjunto en <u,v>_eta = u.eta.v : True",
    5: "fase medida=0.233",
    6: "rms LYR=0.54%",
    7: "log_phi(escala/graviton)=5.39",
    8: "rms RS=0.5%",
    9: "N=1000 1.336",
    10: "peor razon de huecos, phi, N<=5000: 2.618",
    11: "cadena: |A5|/5 = 12",
    12: "todas las verificaciones: ok",
    13: "ok",
    14: "huecos(100,1e3,1e4)=[3, 3, 3]",
    15: "L0=N/2  ln#estados",
    16: "Koide desde M:  1776.8761",
    17: "sigma_obs = 380.315",
    18: "sigma = 583.877",
    19: "8  0.2454",
    20: "(0.6 desviaciones de 12)",
    21: "escala libre ajustada: 99.64 GeV",
    22: "585.317 = W4 + log_phi 2",
    23: "phi^12 = 89 + 144 phi",
    24: "sigma_UV = log_phi(M_Pl/M) = 93.737",
    25: "161+261phi = 583.31",
    26: "primer nivel entero activo por las dos rutas: 2 = sigma_G = n - 1 (CW6)",
    27: "log2 * phi^pi = 3.143254",
    28: "theta_3(e^-pi) = 1.086434811213",
    29: "Omega_L h^2 = 0.2928",
    30: "escala IR = M phi^12 = 101.06 GeV",
    31: "pendiente 0.7071 < cota 0.8165",
    32: "0.4737, 0.2928, 0.1809",
    33: "0.9140, 0.9140, 0.9140",
    34: "1/sqrt2 a +0.05 sigma",
    35: "f = 0.5: tau_F/tau_D = 1/sqrt(2f) = 1.0000",
    36: "S(12) = 1011.58",
    37: "ajuste lnD = a S + b ln L + c (sigma=3..9): a = 0.9972",
    38: "ley de area: 0.5 por ell^2 = 0.25 por ell_P^2",
    39: "(2, 1), (3, 2), (5, 3), (8, 5), (13, 8), (21, 13), (34, 21)",
    40: "pares (teselado, chi<=16), p,q<=60: 50340",
    41: "{5,4} con qubits: 1.4907 S",
    42: "tau(12) = 0.2107",
    43: "14042 coincidencias",
}


def _params():
    out = []
    for n in range(1, 44):
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
        assert FIGURES[n] in run.figures, (n, run.figures)


def test_all_sections_covered():
    """The marker table must cover every registered section."""
    assert sorted(MARKERS) == list(range(1, 44))
