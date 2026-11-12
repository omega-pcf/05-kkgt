"""Deterministic matplotlib settings for the figure pipeline.

Why this module exists (do not delete):

1. **ToUnicode / text extraction.**  With matplotlib 3.10.x (the version
   locked in ``uv.lock``) the default ``pdf.fonttype: 3`` embeds Type 3
   fonts *without* a ``/ToUnicode`` CMap, so ``pdftotext`` cannot read the
   mathematical glyphs out of the generated PDFs (σ, φ, π, → … come out as
   junk).  ``pdf.fonttype: 42`` embeds the same TrueType outlines as CID
   fonts *with* ``/ToUnicode``, which is what the author's own round
   produced and what the manuscript tests rely on.

2. **Byte-for-byte determinism.**  matplotlib writes the current wall clock
   into the PDF ``/CreationDate`` unless ``SOURCE_DATE_EPOCH`` is set, so
   two consecutive runs of ``pnpm run generate:figures`` used to differ in
   four bytes and left ``git status images/`` dirty.  ``SOURCE_DATE_EPOCH``
   is honoured by the pdf, ps and svg backends (reproducible-builds.org);
   we pin it to the timestamp of the author's round that shipped the
   figures (2026-11-09 19:31:03 -06:00).

3. **No dependence on a machine-local matplotlibrc.**  The fonts are pinned
   explicitly, so a user ``matplotlibrc`` that prefers another sans-serif
   (the round that produced ``images/`` resolved plain text to Inter) can
   never change what is rendered here.  DejaVu is bundled with matplotlib
   itself, so the pipeline needs no font installed on the host.

The author's code (``figuras_v134.py``) is never modified: it sets its own
``font.family``/``mathtext.fontset`` per figure and resets the rcParams at
the end of figure 1, which is exactly why :func:`apply_rc` is called again
before *every* generator instead of once at start-up.

References:
  https://matplotlib.org/stable/users/explain/figure/backends.html
  https://reproducible-builds.org/docs/source-date-epoch/
"""

from __future__ import annotations

import os

# Author's round timestamp (2026-11-09 19:31:03 -06:00) -> UTC epoch.
# setdefault: an explicitly exported SOURCE_DATE_EPOCH still wins.
os.environ.setdefault("SOURCE_DATE_EPOCH", "1794274263")

import matplotlib  # noqa: E402  (after the env pin, on purpose)

# rcParams that decide what the PDF bytes look like.  They are re-applied
# before every figure because ``seccion_44`` ends with
# ``plt.rcParams.update(matplotlib.rcParamsDefault)``.
DETERMINISTIC_RCP = {
    # fonts: explicit so a machine-local matplotlibrc cannot leak in
    "font.family": "sans-serif",
    "font.sans-serif": ["DejaVu Sans", "Arial", "Liberation Sans", "sans-serif"],
    "mathtext.fontset": "dejavusans",
    "pdf.use14corefonts": False,
    # Type 42 (TrueType/CID) embeds /ToUnicode; Type 3 on matplotlib 3.10
    # does not, and pdftotext then loses every math glyph.
    "pdf.fonttype": 42,
}


def apply_rc() -> None:
    """Pin the rcParams that make the generated PDFs extractable and stable."""
    matplotlib.rcParams.update(DETERMINISTIC_RCP)
