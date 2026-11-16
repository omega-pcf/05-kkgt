# Criterion sites — the applied inline/own-line inventory

| Field | Value |
|---|---|
| **id** | `WIT-001` |
| **title** | Criterion sites — the applied inline/own-line inventory |
| **status** | applied (2026-11-15 pass); snapshot, superseded by the manuscript |
| **date** | 2026-11-15 |
| **version** | 1.0 |

**Scope.** This report holds the *concrete* material of
`docs/citations.md` §8.5: the site table of the quantified criterion
(`k/L/r/d/i`), the sentence tails each flagged mark closes, and the state
after the 2026-11-15 application pass. The generic rule — quantities,
thresholds, gates, heuristics and the review method — lives in
`docs/citations.md` §8.5; the justification of the device lives in
`docs/witness-rationale.md`. This file is a **snapshot**: line numbers are
those of the manuscript when the table was written, and the manuscript is
edited concurrently; the tail of the sentence identifies each site when a
line number moves.

**Repository:** `05-kk-golden-throat`.

---

## 1. The sites the rule flags

Every inline mark with `k ≥ 2` whose sentence ends at the mark (`r = 0`),
with the tail of the sentence it closes.  Thirteen sites; twelve of them
pass gates 1–3 (`L ≥ 35`), and gate 4 keeps four of those inline (the
`stereo_ratio` row fails it too once the `tan_eta` row below it takes its
line — see the note under the table).

| `main.tex` | `k` | `L` | `r` | `d` | `i` | the sentence ends with | verdict |
|---|---|---|---|---|---|---|---|
| 310 | 3 | 71 | 0 | — | 0 | `…which is transcendental by the Gelfond--Schneider theorem~\cite{Sch35}` | **→ block** |
| 946 | 2 | 29 | 0 | — | 0 | `…those of $S$ and $ST$, are computed in Lean` | stays inline — `L = 29 < 35`, gate 2 |
| 1128 | 2 | 36 | 0 | — | 1 | `…with $G_N=\tfrac12$, the entropy law of a de~Sitter horizon` | stays inline — closes a `\item` of the W list, gate 4 |
| 1170 | 3 | 48 | 0 | — | 0 | `…monodromy $\pi$, and the maximum of the binary entropy` | **→ block** |
| 1500 | 3 | 47 | 0 | — | 1 | `…the clock $24$, and $\eta^{12}$ picks up exactly $e^{i\pi}=-1$` | stays inline — closes an `\item`, gate 4 |
| 1748 | 2 | 41 | 0 | — | 0 | `…the phase is $\pi\golden^{2\sigma}$, a half-turn only at $\sigma=0$` | **→ block** |
| 1766 | 2 | 42 | 0 | 70 | 0 | `…with Fibonacci numbers, $\golden^{2\sigma}$ is irrational` | stays inline — a block already stands 70 words away, gate 4 |
| 1781 | 2 | 61 | 0 | 94 | 0 | `…so $\pi z<z^{2}$ for every $\sigma\geq3$` | **→ block** |
| 1799 (`stereo_ratio, clifford_stereographic_torus`) | 2 | 42 | 0 | 61* | 0 | `…of revolution with $R/r=\sqrt{1+\golden^{4n}}$, $\sqrt2$ at the level $0$` | stays inline — `d = 61 < 75` once `tan_eta` takes its line, gate 4 (*148 before that move) |
| 1799 (`tan_eta, level_zero_is_clifford, clifford_square`) | 3 | 48 | 0 | 197 | 0 | `…$0$, where the window torus is the Clifford torus` | **→ block** |
| 1809 | 2 | 35 | 0 | — | 0 | `…and the throat` | **→ block** |
| 1837 | 3 | 69 | 0 | — | 0 | `…tends to $\int fg-\int f\int g$` | **→ block** |
| 2033 | 2 | 70 | 0 | — | 0 | `…$5.0$ standard deviations from it` | **→ block** |

The line numbers are those of the manuscript as this section was written;
the tail of the sentence identifies the site when a concurrent editing
pass moves it.

## 2. Applied 2026-11-15: eight of the nine rows

The manuscript stood at **26 blocks** (18 + 8) and left **26 inline marks
with two ids or more** (34 − 8).  The `stereo_ratio` row reverted on
re-reading it against the applied text: once `tan_eta` took its line, the
distance to the block above it fell to **61 words**, so gate 4 keeps it
inline — the outcome the note above the table had predicted.

## 3. State after the application pass (2026-11-15, updated 2026-11-16)

**27 blocks** — 17 `P` and 10 `N`, every one of them with `k ≥ 2`,
`L ≥ 35`, `r = 0`, `i = 0` and `d ≥ 75` (or no block in its paragraph);
**no single-id block is left**.  **25 inline marks carry two ids or
more** — 23 `P` and 2 `N` — of which **13 close their sentence** and are
the table above.  The two multi-id `N` marks left are `main.tex:1033` and
`main.tex:2121`, whose sentence goes on after the claim.  `\Lean{}` and
`\LeanCW{}`: **0 occurrences** in `main.tex`.

The twenty-seventh block is the one verdict of the two heuristics of
`docs/citations.md` §8.5 (`u`, `p`): `main.tex:940` closes a paragraph
(`p = 1`) inside the `imported` sequence, whose census of marks is mixed
and so leaves the run to `p` and the gates.  The full verdict table is
`20261116_WIT-002_u_p_verdicts.md`; inline marks fell from 231 to 230.

## 4. Calibrations of the thresholds (moved from `docs/citations.md` §8.5)

The generic gates state the numbers; these are the concrete facts the numbers
were calibrated against, kept here so §8.5 stays portable. Line numbers are
those of the 2026-11-15 pass; the manuscript has moved since
(`certainty_principle` now sits at `main.tex:893`, the tightest pair at
`main.tex:2073` and `main.tex:2081`) — the ids and sentence tails identify
them.

- **Gate 1 (`k ≥ 2`).** The seven single-id blocks of the 2026-11 pass moved
  inline for exactly this reason (`\tier[sq\_add\_inv\_sq]{P}` and its six
  siblings).
- **Gate 2 (`L ≥ 35`).** 35 characters is the shortest id list the
  manuscript already prints as a block — `certainty_principle,
  log_from_scale`, `main.tex:899` at the time.
- **Gate 3 (`r = 0`).** `\witness` issues `\par … \par` (preamble,
  `main.tex:94-98` at the time), so it always ends the paragraph where it
  sits.
- **Gate 4 (`d ≥ 75`).** 75 words is the tightest block-to-block distance
  the manuscript already accepts — the two blocks of `main.tex:2075` and
  `main.tex:2083` at the time.

---

## Related documents

- `docs/citations.md` §8.5 — the generic criterion (quantities, gates,
  heuristics, review method).
- `docs/reports/20261116_WIT-002_u_p_verdicts.md` — the verdict table of
  the two heuristics (`u`, `p`) for the current manuscript, pending
  application.
- `docs/witness-rationale.md` — why the device exists and why the
  criterion is quantitative.
- `docs/reports/20261115_DEC-001_witness_decisions.md` — the decision log
  behind the witness tiers.
