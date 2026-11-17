"""Harness for the test suite of the manuscript.

The manuscript cites the tests that check each number (``\\testref{...}``),
so the tests keep a 1:1 identity with the forty-six numbered sections of
``kkgt.sections``: every number is read from the stdout of the section that
produces it, or recomputed independently and compared with an explicit
tolerance.

``SectionRun.value/has`` replace the ad-hoc checks of the original
sections: a missing pattern or a violated tolerance fails with the section
number, the label, expected, got and the diff instead of a bare ``False``.
"""

from __future__ import annotations

import contextlib
import io
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path

from .constants import C_LIGHT, G_NEWTON, HBAR, MPC_M

# tests/src/kkgt/harness.py -> repo root = Path(...).parents[3]
REPO_ROOT = Path(__file__).resolve().parents[3]


def lam_planck(h0: float, omega_l: float) -> float:
    """``Lambda l_P^2`` from H0 (km/s/Mpc) and Omega_L -- sections 22/23.

    The same formula existed twice, as ``kkgt.sections._LamP`` and as the
    local ``lam_planck`` of the section 17-28 tests; this is its single
    origin (SEC-001, layer 1).  ``kkgt.sections`` aliases it as ``_LamP``.
    """
    h = h0 * 1e3 / MPC_M
    l_p2 = HBAR * G_NEWTON / C_LIGHT ** 3
    return 3 * h * h * omega_l / C_LIGHT ** 2 * l_p2


def load_sections():
    """The ``kkgt.sections`` module (its top level only builds SECCIONES)."""
    from kkgt import sections  # noqa: PLC0415  (importable via tests/src)

    return sections


def section_registry(module) -> dict:
    """Number -> (title, function), in file order."""
    return {num: (title, fn) for num, title, fn in module.SECCIONES}


@dataclass
class SectionRun:
    """Result of executing one numbered section of ``kkgt.sections``."""

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


def run_section(module, n: int, cwd: Path | str) -> SectionRun:
    """Run section ``n`` of ``kkgt.sections`` with cwd set to ``cwd``."""
    registry = section_registry(module)
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

