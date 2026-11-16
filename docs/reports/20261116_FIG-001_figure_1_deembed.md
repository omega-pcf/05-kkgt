# Figure 1 (`seccion_44`): the prose moved to the caption

| Field | Value |
|---|---|
| **id** | `FIG-001` |
| **title** | Figure 1 (`seccion_44`) — the prose moved to the caption |
| **status** | applied and committed (`ff44a61`); snapshot |
| **date** | 2026-11-16 |
| **version** | 1.0 |

**Scope.** This report holds the *concrete* material of the figure-1
incident: what was taken out of the canvas of `seccion_44`, why the type
had to grow, why the include narrowed and what the build reported
afterwards. The generic pipeline — determinism, `SOURCE_DATE_EPOCH`,
`pdf.fonttype=42`, byte-stability, `generate:figures` — lives in
[`docs/figures.md`](../figures.md); this file records only what happened
to one figure of one repository.

**Repository:** `05-kk-golden-throat`. **Evidence:** §1–§5 and §7 are
carried over verbatim from `docs/figures.md`, where they lived before the
desfragmentation; §5's caption counts and §6 are the measurements of the
pass that produced them (commit `ff44a61`).

---

## 1. What the author asked for

The author asked for two things on `fig:background`: the sentences the
drawing used to carry should not be drawn (they were duplicated word for
word in the caption of `main.tex`), and what is left should be readable —
"el texto es muy pequeño de leer, es pésimo en UX". Section 44 of
`scripts/figures/figuras_v134.py` was therefore adapted in place; the
numerics, the asserts and the panel layout were not touched.

## 2. Taken out of the canvas (it all lives in the caption now)

| What | Where it was |
| --- | --- |
| the title `One structure, seen at once` | `fig.suptitle` |
| the four band headings (rows 1–4) | `band(y, txt)` ×4, and the `band` helper itself |
| the eight panel headings with their phrases, e.g. `(a)  the torus` + `T²=ℂ/M…` | `head(x, y, txt, sub)` — only the letter is drawn now |
| the five sub-panel labels of row 2 (`along (1,1,1): axes at 120°…`, `turning, 1/3`, `an axis faces us: the square face [R]`, …) | the `TT` list and its `fig.text` — one of them still carried `[R]`, the class removed from the alphabet |
| the note under row 2 (`… is a reading [R]; … (phase_on_cell, §11.1)`) | `fig.text(0.5, 0.6090, …)` |
| the note under panel (f) (`{0,…,L−1}³ casts 3L²−3L+1 shadows: 19, 61, 127 …`) | `fig.text(X3[1], 0.3770, …)` — the numbers moved into the caption |
| the two footnotes (the tile list and `987=610+377`; the colour legend) | `fig.text(0.5, 0.072, …)` and `fig.text(0.5, 0.05, …)` |

## 3. Left in the drawing

The panel letters `(a)`…`(i)` — `(d)` was added
above row 2, because only the band heading used to mark that row — the
axis labels (`x=a+bφ`, `x̄=a+bφ̄`, `level σ`), the numbers (tile counts
`5=3+2` … `55=34+21`, the side lengths, the `σ` labels, the tick labels,
the angles, `(1,1,1)`, the `P`/`C`/`F` of the triad), the `→` between the
sub-panels, and the colours.

## 4. Why the fonts had to grow

The canvas is 17 in wide and the manuscript
prints it at `0.85\textwidth` = 399.3 pt over a canvas of 1193.78 pt, i.e.
one point of the canvas lands at **0.33 pt on the page**. The old sizes
(7–9 pt for axis labels, ticks and numbers, 12 pt for the panel headings)
therefore printed at 2.3–3.0 pt. They are now 15–26 pt on the canvas
(letters 12 → 26, `P`/`C`/`F` 11 → 24 and 9.5 → 20, numbers 7 → 18, axis
labels 8 → 20, ticks 7 → 15, `σ` rows 9 → 20, throat numbers 10 → 22,
arrows 18 → 24, `font.size` 9 → 12), which print at 5.0–8.7 pt.

## 5. Why the figure got narrower (0.93 → 0.85 `\textwidth`)

With the prose
gone from the canvas the tight bbox shrank from 1450.82 to 1329.84 pt
(height/width 1.224 → 1.114), but the caption still has to state every
claim the drawing no longer states, and at 0.93 it made the float
**116.7 pt taller than the page** (`LaTeX Warning: Float too large … on
input line 653`, present before this pass). At 0.85 the float fits and the
warning is gone; the in-canvas type is still 2.4× larger on the page than
it was.

The caption of `fig:background` in `main.tex` went **from 2417 to 2012
characters** in `ff44a61` (brace-matched extraction of the `\caption{...}`
argument: 2417 at `ff44a61~1`, 2012 from `ff44a61` onwards). What left the
canvas is what the caption now carries, and the caption is what made the
float too tall at `0.93\textwidth`.

## 6. Comparison with the author's render

The author's own render was the untouched generator output with a shorter
caption (**1264 characters**), so the generator is what changed here; his
caption would have overflowed too. Two independent facts therefore agree
on the diagnosis: the canvas carried prose the caption repeated (§2), and
the type on the canvas was unreadable at the printed scale (§4, §5).

## 7. Verified

Two consecutive `pnpm run generate:figures` runs are
byte-identical for all five PDFs (`md5sum -c` OK); `pdftotext
images/fig_background.pdf -` returns only `(a)`…`(i)`, numbers and the two
axis labels — no sentence of the caption appears in the image; and
`pnpm run build` reports 0 errors, the one pre-existing overfull hbox
(bibliography) and no `Float too large` for figure 1.

## 8. Related

- [`docs/figures.md`](../figures.md) — the generic figure pipeline this
  incident belongs to: guarantees, rc settings, prerequisites, how to
  verify byte-stability, provenance and sources.
- [`docs/reports/README.md`](README.md) — the index of the reports of this
  repository.
