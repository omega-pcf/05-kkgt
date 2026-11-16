# Figure pipeline: deterministic, text-extractable PDFs

| Field | Value |
|---|---|
| **document** | `docs/figures.md` |
| **status** | active |
| **version** | 1.1 (desfragmented: the figure-1 incident moved to a report) |
| **date** | 2026-11-16 |
| **scope** | The family figure pipeline: what `pnpm run generate:figures` guarantees and why. Repository-tied incidents live in `docs/reports/` — the prose de-embed of figure 1 is [FIG-001](reports/20261116_FIG-001_figure_1_deembed.md). |

`pnpm run generate:figures` runs `scripts/figures/main.py`, which registers the
author's five generators (`scripts/figures/figuras_v134.py`, shipped with the
v134 round) and redirects their `savefig` into `images/`. The author's file is
left alone except for `seccion_44` (figure 1), which was adapted in place —
that adaptation is a repository-tied incident and is recorded in
[FIG-001](reports/20261116_FIG-001_figure_1_deembed.md), not here; every other
setting below lives in our layer (`scripts/figures/generators/rc.py`).

## What the pipeline guarantees

1. **The math glyphs are extractable.** Every generated PDF carries a
   `/ToUnicode` CMap, so `pdftotext` reads `σ`, `φ`, `π`, `→` back instead of
   `¾`, `'`, `¼`, `!`.
2. **Two consecutive runs are byte-identical.** `SOURCE_DATE_EPOCH` is pinned,
   so the PDF `/CreationDate` no longer follows the wall clock, and
   `git status --porcelain images/` does not change between runs.
3. **No host font is a prerequisite.** The fonts are pinned to DejaVu, which
   matplotlib itself bundles; a machine-local `matplotlibrc` (the round that
   produced the committed `images/` resolved plain text to *Inter*) cannot
   change the output.

## The settings and why

| Setting | Value | Reason |
| --- | --- | --- |
| `pdf.fonttype` | `42` | On matplotlib 3.10.x (the version in `uv.lock`) the default `3` embeds Type 3 fonts **without** `/ToUnicode`, which is what lost the math glyphs. Type 42 embeds the same TrueType outlines as CID fonts **with** `/ToUnicode`. |
| `font.family` / `font.sans-serif` | `sans-serif` → DejaVu Sans | Explicit, so a user `matplotlibrc` cannot leak a different family in. |
| `mathtext.fontset` | `dejavusans` | Same reason; the author switches it to `cm` himself in figure 1. |
| `SOURCE_DATE_EPOCH` | `1794274263` | The author's round timestamp (2026-11-09 19:31:03 -06:00). The pdf, ps and svg backends all honour it; without it every run rewrote four bytes of `/CreationDate` and dirtied the tree. |

`apply_rc()` is called before **every** generator, not once at start-up:
`seccion_44` (figure 1) ends with
`plt.rcParams.update(matplotlib.rcParamsDefault)`, which would otherwise reset
`pdf.fonttype` back to `3` for the remaining four figures.

## Prerequisites

None beyond the repository's own Python environment (`uv`, `pyproject.toml`).
No system font package is required: DejaVu ships inside matplotlib, and
`fc-cache`/`fonts-inter` are **not** part of the build.

## Verifying

```bash
pnpm run generate:figures          # run once
sha256sum images/*.pdf > /tmp/a    # run twice
pnpm run generate:figures
sha256sum images/*.pdf > /tmp/b && diff /tmp/a /tmp/b   # must be silent

pdffonts images/fig_granularity.pdf        # emb sub uni: yes yes yes
pdftotext images/fig_granularity.pdf -     # reads {nφ}, σ, φ², …
```

## Provenance: why the bytes are not the author's zip bytes

The PDFs shipped in the author's `articulo9_v134.zip` were produced on his
machine with **matplotlib 3.11.2**, plain text resolved to **Inter** (his
`matplotlibrc`, not the code — `figuras_v134.py` sets no font), and a
`/CreationDate` of his wall clock. Regenerating byte-identically would require
reproducing his clock and his font configuration, which is not possible, so the
committed `images/` are regenerated once with the settings above and then stay
fixed: after that commit, `pnpm run generate:figures` leaves `git status
images/` clean.

Measured difference against the zip at 72 dpi (best integer alignment):
mean |Δ| = 1.2–3.3/255 on four of five figures, ~12/255 on
`fig_tilings_strip` — the latter is the 3.10.8 vs 3.11.2 text-layout pipeline
(the page is 1.3 pt wider), not a font substitution. Same page geometry
within a pixel, same drawing, same asserted content.

Docker (`kjarosh/latex`) is **not** involved in figure generation: it is only
the LaTeX engine of `pnpm run build`. Figures are produced on the host by
`uv run python scripts/figures/main.py`.

## Sources

- Fonts in Matplotlib (Type 3 vs TrueType/Type 42, how matplotlib picks a
  font): https://matplotlib.org/stable/users/explain/text/fonts.html
- What's new in Matplotlib 3.11.0 — *Improved font embedding in PDF* and the
  text-rendering overhaul that makes 3.10 and 3.11 pixels differ:
  https://matplotlib.org/stable/release/prev_whats_new/whats_new_3.11.0.html
- `SOURCE_DATE_EPOCH`, the standardised variable for reproducible outputs:
  https://reproducible-builds.org/docs/source-date-epoch/
- Community guidance on avoiding Type 3 in matplotlib PDFs:
  http://phyletica.org/matplotlib-fonts/
- Installing fonts on Linux is a host prerequisite handled by fontconfig
  (`fc-cache`, per-user font directories) — the route this pipeline avoids:
  https://wiki.archlinux.org/title/Font_configuration and
  https://linux.die.net/man/5/fonts-conf
- The LaTeX image used by `pnpm run build` (and by `04-mersenne-cr`'s figure
  script): https://github.com/kjarosh/latex-docker


## Related

- [FIG-001 — figure 1 (`seccion_44`): the prose moved to the caption](reports/20261116_FIG-001_figure_1_deembed.md)
  — the concrete incident behind the one adapted generator: what was taken
  out of the canvas, why the type had to grow, why the include narrowed and
  what the build reported afterwards.
