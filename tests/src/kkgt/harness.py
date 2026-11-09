"""Harness for the ``reproduce_v108.py`` test suite.

The manuscript cites the script by section number (``section~38 of
\\code{reproduce_v108.py}``), so the tests keep a 1:1 identity with the
original sections: every number is read from the stdout of the section that
produces it, or recomputed independently and compared with an explicit
tolerance.

``SectionRun.expect/value`` replace the ad-hoc checks of the original
script: a missing pattern or a violated tolerance fails with the section
number, the label, expected, got and the diff instead of a bare ``False``.
"""

from __future__ import annotations

import contextlib
import io
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path

# tests/src/kkgt/harness.py -> repo root is four levels up
REPO_ROOT = Path(__file__).resolve().parents[3]


def load_repro():
    """Import the manuscript's script (module level only builds SECCIONES)."""
    root = str(REPO_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
    import reproduce_v108  # noqa: PLC0415  (path set above)

    return reproduce_v108


def section_registry(repro) -> dict:
    """Number -> (title, function), in file order."""
    return {num: (title, fn) for num, title, fn in repro.SECCIONES}


@dataclass
class SectionRun:
    """Result of executing one numbered section of reproduce_v108.py."""

    number: int
    title: str
    stdout: str
    seconds: float
    figures: tuple[str, ...]

    # ── reading stdout ────────────────────────────────────────────────
    def match(self, pattern: str, flags: int = re.M) -> re.Match:
        m = re.search(pattern, self.stdout, flags)
        assert m, (
            f"section {self.number}: no match for {pattern!r}\n"
            f"--- stdout of section {self.number} ---\n{self.stdout}"
        )
        return m

    def value(self, pattern: str, *, want: float | None = None,
              tol: float | None = None, label: str = "") -> float:
        """Extract group(1) as float; optionally require |got - want| <= tol."""
        got = float(self.match(pattern).group(1))
        if want is not None:
            assert tol is not None, "value(..., want=...) needs tol=..."
            diff = abs(got - want)
            assert diff <= tol, (
                f"section {self.number}: {label or pattern}: "
                f"got {got!r}, want {want!r} +/- {tol} (diff {diff:.3e})"
            )
        return got

    def text(self, pattern: str, *, want: str | None = None,
             label: str = "") -> str:
        got = self.match(pattern).group(1)
        if want is not None:
            assert got == want, (
                f"section {self.number}: {label or pattern}: "
                f"got {got!r}, want {want!r}"
            )
        return got

    def has(self, snippet: str) -> bool:
        """Assert that the section printed `snippet`; returns True."""
        assert snippet in self.stdout, (
            f"section {self.number}: expected {snippet!r} in stdout\n"
            f"--- stdout ---\n{self.stdout}"
        )
        return True


def run_section(repro, n: int, cwd: Path | str) -> SectionRun:
    """Run section ``n`` with cwd set to ``cwd`` (figures land there)."""
    registry = section_registry(repro)
    assert n in registry, f"section {n} does not exist (1..{len(registry)})"
    title, fn = registry[n]
    cwd = Path(cwd)
    cwd.mkdir(parents=True, exist_ok=True)

    buf = io.StringIO()
    t0 = time.perf_counter()
    prev = os.getcwd()
    os.chdir(cwd)
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            fn()
    finally:
        os.chdir(prev)
        # sections 10/12/13/39/41 leave figures open; keep the session light
        try:
            import matplotlib.pyplot as plt  # noqa: PLC0415

            plt.close("all")
        except Exception:  # matplotlib not imported at all
            pass

    figures = tuple(sorted(p.name for p in cwd.glob("*.pdf")))
    return SectionRun(
        number=n,
        title=title,
        stdout=buf.getvalue(),
        seconds=time.perf_counter() - t0,
        figures=figures,
    )


def close_enough(got: float, want: float, tol: float) -> bool:
    """Explicit absolute tolerance; used by the independent checks."""
    return abs(got - want) <= tol
