"""pytest configuration for the reproduce_v108.py suite.

Mirrors 03-crystalline-worldsheet/tests/conftest.py: shared fixtures live
here, the importable support code lives in tests/src/kkgt.

The suite is headless: the backend is forced to Agg before any section can
import pyplot, and every section runs inside a temporary directory so the
five figures and the ``kk_vs_cw6_out.txt`` dump never touch the repo.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

TESTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = TESTS_DIR.parent
for _p in (str(REPO_ROOT), str(TESTS_DIR / "src")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import pytest  # noqa: E402

from kkgt.harness import SectionRun, load_repro, run_section as _run_section  # noqa: E402


@pytest.fixture(scope="session")
def repro():
    """The manuscript's script, imported once per session."""
    return load_repro()


@pytest.fixture(scope="session")
def sections(repro):
    """``SECCIONES`` registry: [(number, title, function), ...]."""
    return list(repro.SECCIONES)


@pytest.fixture(scope="session")
def run_section(repro, tmp_path_factory):
    """Run one numbered section, once per session, in a temp directory.

    Sections are deterministic (all random generators are seeded inside the
    script), so the captured stdout is cached and shared by every test that
    needs it.  Returns ``SectionRun``.
    """
    base = tmp_path_factory.mktemp("section_runs")
    cache: dict[int, SectionRun] = {}

    def _run(n: int) -> SectionRun:
        if n not in cache:
            cache[n] = _run_section(repro, n, base / f"section_{n:02d}")
        return cache[n]

    return _run
