"""Harness for the test suite of the manuscript.

Generic utilities only: the repository root, the committed figure
artifacts (``pnpm run figures`` writes them; a test only verifies their
bytes) and the Planck-Lambda formula, whose single origin this module is
(SEC-001 layer 1).  No test runs a section any more (SPEC-002): every
claim test owns the computation that produces its numbers.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from .constants import C_LIGHT, FIGURE_MD5, G_NEWTON, HBAR, MPC_M

# tests/src/kkgt/harness.py -> repo root = Path(...).parents[3]
REPO_ROOT = Path(__file__).resolve().parents[3]

# Committed figure artifacts; only ``pnpm run figures`` writes them.
FIGURES_DIR = REPO_ROOT / "images"


def figure_artifact(name: str) -> Path:
    """Path of the committed figure ``name``; asserts that it exists."""
    path = FIGURES_DIR / name
    assert path.is_file(), (
        f"missing figure artifact {path}\n"
        "regenerate it with `pnpm run figures` and commit the result"
    )
    return path


def md5_of(path: Path) -> str:
    """Hex md5 of a file's bytes (artifact stability pin)."""
    return hashlib.md5(path.read_bytes()).hexdigest()  # noqa: S324


def verify_figure_artifact(name: str) -> str:
    """The committed figure exists and still carries its pinned bytes.

    Returns the md5.  Generation is not a test concern (SPEC-002 §1.1):
    only ``pnpm run figures`` writes ``images/``, and this check fails if
    the artifact is missing or its bytes drifted from ``FIGURE_MD5``.
    """
    got = md5_of(figure_artifact(name))
    want = FIGURE_MD5[name]
    assert got == want, (
        f"{name}: artifact bytes changed\n"
        f"  got  {got}\n"
        f"  want {want}\n"
        "regenerate with `pnpm run figures`, review the diff of images/, "
        "and move the pin in the same commit"
    )
    return got


def lam_planck(h0: float, omega_l: float) -> float:
    """``Lambda l_P^2`` from H0 (km/s/Mpc) and Omega_L.

    The same formula existed twice, as a private helper of the old
    computation module and as the local ``lam_planck`` of the section
    17-28 tests; this is its single origin (SEC-001, layer 1).
    """
    h = h0 * 1e3 / MPC_M
    l_p2 = HBAR * G_NEWTON / C_LIGHT ** 3
    return 3 * h * h * omega_l / C_LIGHT ** 2 * l_p2
