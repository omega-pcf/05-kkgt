"""pytest configuration for the suite of the manuscript.

Mirrors 03-crystalline-worldsheet/tests/conftest.py: shared fixtures live
here, the importable support code lives in ``tests/src/kkgt`` (constants
and generic harness only), and no test imports a script.

The suite is headless and generates nothing: the five figures belong to
the generators of ``scripts/figures`` (the tests only verify the
committed artifacts of ``images/``) and ``MPLBACKEND`` is forced to Agg
before any module can import pyplot (SPEC-002 §1.1).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

TESTS_DIR = Path(__file__).resolve().parent
for _p in (str(TESTS_DIR / "src"),):
    if _p not in sys.path:
        sys.path.insert(0, _p)
