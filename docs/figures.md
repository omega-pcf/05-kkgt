# Figure pipeline: deterministic, text-extractable PDFs

`pnpm run generate:figures` runs `scripts/figures/main.py`, which registers the
author's five generators (`scripts/figures/figuras_v134.py`, shipped with the
v134 round) and redirects their `savefig` into `images/`. The author's file is
left alone except for `seccion_44` (figure 1), which was adapted in place —
see the last section of this document; every other setting below lives in our
layer (`scripts/figures/generators/rc.py`).

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

## Figure 1 (`seccion_44`): the prose moved to the caption

The author asked for two things on `fig:background`: the sentences the
drawing used to carry should not be drawn (they were duplicated word for
word in the caption of `main.tex`), and what is left should be readable —
"el texto es muy pequeño de leer, es pésimo en UX". Section 44 of
`scripts/figures/figuras_v134.py` was therefore adapted in place; the
numerics, the asserts and the panel layout were not touched.

**Taken out of the canvas** (it all lives in the caption now):

| What | Where it was |
| --- | --- |
| the title `One structure, seen at once` | `fig.suptitle` |
| the four band headings (rows 1–4) | `band(y, txt)` ×4, and the `band` helper itself |
| the eight panel headings with their phrases, e.g. `(a)  the torus` + `T²=ℂ/M…` | `head(x, y, txt, sub)` — only the letter is drawn now |
| the five sub-panel labels of row 2 (`along (1,1,1): axes at 120°…`, `turning, 1/3`, `an axis faces us: the square face [R]`, …) | the `TT` list and its `fig.text` — one of them still carried `[R]`, the class removed from the alphabet |
| the note under row 2 (`… is a reading [R]; … (phase_on_cell, §11.1)`) | `fig.text(0.5, 0.6090, …)` |
| the note under panel (f) (`{0,…,L−1}³ casts 3L²−3L+1 shadows: 19, 61, 127 …`) | `fig.text(X3[1], 0.3770, …)` — the numbers moved into the caption |
| the two footnotes (the tile list and `987=610+377`; the colour legend) | `fig.text(0.5, 0.072, …)` and `fig.text(0.5, 0.05, …)` |

**Left in the drawing:** the panel letters `(a)`…`(i)` — `(d)` was added
above row 2, because only the band heading used to mark that row — the
axis labels (`x=a+bφ`, `x̄=a+bφ̄`, `level σ`), the numbers (tile counts
`5=3+2` … `55=34+21`, the side lengths, the `σ` labels, the tick labels,
the angles, `(1,1,1)`, the `P`/`C`/`F` of the triad), the `→` between the
sub-panels, and the colours.

**Why the fonts had to grow.** The canvas is 17 in wide and the manuscript
prints it at `0.85\textwidth` = 399.3 pt over a canvas of 1193.78 pt, i.e.
one point of the canvas lands at **0.33 pt on the page**. The old sizes
(7–9 pt for axis labels, ticks and numbers, 12 pt for the panel headings)
therefore printed at 2.3–3.0 pt. They are now 15–26 pt on the canvas
(letters 12 → 26, `P`/`C`/`F` 11 → 24 and 9.5 → 20, numbers 7 → 18, axis
labels 8 → 20, ticks 7 → 15, `σ` rows 9 → 20, throat numbers 10 → 22,
arrows 18 → 24, `font.size` 9 → 12), which print at 5.0–8.7 pt.

**Why the figure got narrower (0.93 → 0.85 `\textwidth`).** With the prose
gone from the canvas the tight bbox shrank from 1450.82 to 1329.84 pt
(height/width 1.224 → 1.114), but the caption still has to state every
claim the drawing no longer states, and at 0.93 it made the float
**116.7 pt taller than the page** (`LaTeX Warning: Float too large … on
input line 653`, present before this pass). At 0.85 the float fits and the
warning is gone; the in-canvas type is still 2.4× larger on the page than
it was.

**Verified:** two consecutive `pnpm run generate:figures` runs are
byte-identical for all five PDFs (`md5sum -c` OK); `pdftotext
images/fig_background.pdf -` returns only `(a)`…`(i)`, numbers and the two
axis labels — no sentence of the caption appears in the image; and
`pnpm run build` reports 0 errors, the one pre-existing overfull hbox
(bibliography) and no `Float too large` for figure 1.
