"""Test-support package for the manuscript's suite (kkgt = KK golden throat).

Lives in ``tests/src/kkgt`` (same layout as ``tests/src/cw6`` in
03-crystalline-worldsheet).  Three modules:

* ``kkgt.sections`` -- the computation of the note: forty-three numbered
  sections registered in ``SECCIONES``, run one at a time by the suite;
* ``kkgt.constants`` -- closed forms and the numbers the sections print;
* ``kkgt.harness`` -- runs one section in a temporary directory, captures
  its stdout and reports expected/got/diff instead of a bare ``False``.
"""

from kkgt.constants import (  # noqa: F401
    EPS0,
    FIGURES,
    LN_PHI,
    M_KOIDE_MEV,
    M_PCF,
    OBS_G,
    PHI,
    PHI_BAR,
    SLOW_SECTIONS,
)
from kkgt.harness import (  # noqa: F401
    REPO_ROOT,
    SectionRun,
    load_sections,
    run_section,
)

__all__ = [
    "EPS0",
    "FIGURES",
    "LN_PHI",
    "M_KOIDE_MEV",
    "M_PCF",
    "OBS_G",
    "PHI",
    "PHI_BAR",
    "REPO_ROOT",
    "SLOW_SECTIONS",
    "SectionRun",
    "load_sections",
    "run_section",
]
