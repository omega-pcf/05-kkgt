"""Test-support package for the manuscript's suite (kkgt = KK golden throat).

Lives in ``tests/src/kkgt`` (same layout as ``tests/src/cw6`` in
03-crystalline-worldsheet).  Two modules:

* ``kkgt.constants`` -- closed forms and the numbers the tests assert;
* ``kkgt.harness`` -- generic utilities: the repository root, the
  committed figure artifacts and their byte pin, and the single origin
  of the Planck-Lambda formula.

There is no computation module: each claim test owns the code that
produces its numbers (SPEC-002).
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
from kkgt.harness import REPO_ROOT  # noqa: F401

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
]
