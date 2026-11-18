"""pytest configuration for the suite of the manuscript.

Mirrors 03-crystalline-worldsheet/tests/conftest.py: shared fixtures live
here, the importable support code lives in tests/src/kkgt, and the
computation itself is ``kkgt.sections`` -- no test imports a script.

The suite is headless and generates nothing: the five figures belong to
the generators of ``scripts/figures`` (the tests only verify the
committed artifacts of ``images/``), ``MPLBACKEND`` is forced to Agg
before any module can import pyplot, and every section still runs
inside a temporary directory so its stdout dump never touches the repo.
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

import pytest  # noqa: E402

from kkgt.harness import (  # noqa: E402
    SectionRun,
    load_sections,
    run_section as _run_section,
)


@pytest.fixture(scope="session")
def sections_module():
    """The ``kkgt.sections`` module, imported once per session."""
    return load_sections()


@pytest.fixture(scope="session")
def sections(sections_module):
    """``SECCIONES`` registry: [(number, title, function), ...]."""
    return list(sections_module.SECCIONES)


@pytest.fixture(scope="session")
def run_section(sections_module, tmp_path_factory):
    """Run one numbered section, once per session, in a temp directory.

    Sections are deterministic (all random generators are seeded inside the
    package), so the captured stdout is cached and shared by every test that
    needs it.  Returns ``SectionRun``.
    """
    base = tmp_path_factory.mktemp("section_runs")
    cache: dict[int, SectionRun] = {}

    def _run(n: int) -> SectionRun:
        if n not in cache:
            cache[n] = _run_section(sections_module, n, base / f"section_{n:02d}")
        return cache[n]

    return _run
