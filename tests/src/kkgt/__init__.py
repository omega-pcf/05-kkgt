"""Test-support package for the ``reproduce_v108.py`` suite (kkgt = KK golden throat).

Lives in ``tests/src/kkgt`` (same layout as ``tests/src/cw6`` in
03-crystalline-worldsheet): constants shared by the tests, the section
harness that runs one numbered section of the script and captures its
stdout, and the assertion helpers that report expected/got/diff instead of
a bare ``False``.
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
from kkgt.harness import REPO_ROOT, SectionRun, load_repro, run_section  # noqa: F401

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
    "load_repro",
    "run_section",
]
