# u/p verdicts — the two heuristics applied to `main.tex`

| Field | Value |
|---|---|
| **id** | `WIT-002` |
| **title** | u/p verdicts — the two heuristics applied to `main.tex` |
| **status** | applied — `main.tex` carries the verdict since `8e101f5` |
| **date** | 2026-11-16 (written and applied 2026-11-16, in `8e101f5`) |
| **version** | 1.0 |

**Scope.** This report holds the *concrete* material of the two heuristics
(`u`, `p`) added to `docs/citations.md` §8.5: the verdict table for every
site where the heuristics can act, identified by the tail of its sentence,
plus the resulting counters. The generic rule — quantities, gates, the two
heuristics and the decision order — lives in `docs/citations.md` §8.5; the
applied inventory of the 2026-11-15 pass lives in
`docs/reports/20261115_WIT-001_criterion_sites.md`. This file is a
**snapshot** — the convention is stated once, in `docs/reports/README.md`
— and its line numbers are those of `main.tex` at commit `7fa8994`, the
state the table was read in; the application in `8e101f5` and later edits
to `main.tex` have shifted them.

**Repository:** `05-kk-golden-throat`.

---

## 1. Method

Decision order for an inline mark with ids (as specified in
`docs/citations.md` §8.5):

1. gate 1 — `k ≥ 2`; 2. gate 3 — `r = 0`. Both **absolute**: no heuristic
   lifts them.
3. `u` — if the mark sits in a newline-separated run and the run is
   homogeneous, the run decides (inline or own-line); if the run is mixed,
   `u` abstains and the run is recorded as a uniformity defect.
4. `p` — if the mark is the last element of its paragraph (only punctuation
   and commands before the break), a line of its own: `p` lifts gates 2 and
   4 for that site.
5. gates 2 and 4 — `L ≥ 35`, `i = 0`, `d ≥ 75`.

Conventions used below: paragraphs are blank-line separated (the §8.5
convention); `d` and `r` count words with math and macros not counted (the
§8.5 convention for `r`); the census of a run excludes the mark under
review. `d` values marked † are the snapshot values of the committed §8.5
table (that pass counted a few more tokens); both counts stay below 75, so
the verdict does not depend on the convention.

## 2. The verdict table

Sites where `r = 0` (the candidate set gates 1–3 admit), plus the one site
that only looks like a candidate under macro-stripping.

| `main.tex` | ids | the sentence ends with | k | L | r | i | d | `u` | `p` | verdict | changes? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 940 | `pisano_orders, modular_orders` | `…those of $S$ and $ST$, are computed in Lean` | 2 | 29 | 0 | 0 | — | run = the imported-statement sequence: census **mixed** (4 blocks / 17 inline) → abstains | **1** (mark, `.`, `\end{imported}`, blank line) | **→ block** (`p` lifts gate 2, `L = 29 < 35`) | **YES — inline → block** |
| 1122 | `lambda_times_entropy, dS_entropy_law` | `…with $G_N=\tfrac12$, the entropy law of a de~Sitter horizon` | 2 | 36 | 0 | 1 | — | W list (`description`): homogeneous **inline** → decides **inline** | 0 | stays inline (was gate 4, now `u`) | no |
| 1495 | `eta_T, eta_power_T_phase, partition_T_invariant` | `…the clock $24$, and $\eta^{12}$ picks up exactly $e^{i\pi}=-1$` | 3 | 47 | 0 | 1 | — | enumeration: homogeneous **inline** → decides **inline** | 0 | stays inline (was gate 4, now `u`) | no |
| 1761 | `golden_pow_fib, ring_resolution_irrational` | `…with Fibonacci numbers, $\golden^{2\sigma}$ is irrational` | 2 | 42 | 0 | 0 | 70 † (≈54 §8.5-convention) | prose — no run | 0 (`So the half-turn…` follows) | stays inline — gate 4, `d < 75` | no |
| 1795 | `stereo_ratio, clifford_stereographic_torus` | `…of revolution with $R/r=\sqrt{1+\golden^{4n}}$, $\sqrt2$ at the level $0$` | 2 | 42 | 0 | 0 | 61 † (29 §8.5-convention) | prose — no run | 0 (`The map J…` follows) | stays inline — gate 4, `d < 75` | no |
| 1795 | `antipode_is_half_turn, hopf_blind_to_half_turn` | `…and its square is the half-turn of the fibre, $-z=e^{i\pi}z$, which the base does not see` | 2 | 46 | **12** (a closing `\testref` follows the mark — §8.5 gate 3 names it a residual; macro-stripping reads `r = 0`) | 0 | 74 (§8.5-convention) | prose — no run | 0 | stays inline — gate 3 (`r ≥ 1`); gate 4 also holds (`d = 74 < 75`) | no |

**The remaining 20 of the 26 inline multi-id marks** have `r ≥ 1`: gate 3
keeps them inline before `u` or `p` is consulted, and `u` would agree — the
seven of them that sit in lists are all in homogeneous-inline runs. Three of
those 20 are paragraph-closing (`p = 1`) but `r > 0`, so gates 1 and 3 still
decide: `main.tex:1733` (`stereographic_meridian_deriv, …`, `r = 2`),
`main.tex:1894` (`golden_rotation_aperiodic, …`, `r = 28`) and
`main.tex:2192` (`area_law_4d_meets_weld_iff, …`, `r = 10`) — all stay
inline. `u` is never reached for a single-id mark: gate 1 keeps it inline.

## 3. Counter delta if the table is applied

| counter | today | after applying |
|---|---|---|
| blocks | **26** — 16 `P`, 10 `N` | **27** — 17 `P`, 10 `N` |
| inline marks with two ids or more | **26** — 24 `P`, 2 `N` | **25** — 23 `P`, 2 `N` |
| inline marks, total | **231** | **230** |

Both columns predate a brief addition of the class `W` to the *Evidence
tags* gloss, since removed: the gloss declares the two classes only and
the label `W1`–`W12` is defined at its list, so a `grep` at HEAD reads
**230** inline marks — the "after" column; the delta of this report is
unchanged. Exactly one verdict changes (`main.tex:940`, `P`). Its
promoted block sits in its own blank-line paragraph (no block in range), so gate 4's `d`-clause
holds vacuously; the ids are Lean names, not `\testref`s, so
`tests/test_section_census.py` is unaffected. The sentence it closes is
unchanged — only its shape.

## 4. Judgement calls flagged for the author

1. **`u`'s census for the imported statements is sequence-level** (all 17
   imported statements together → mixed → abstain → `p` decides → block).
   A per-statement census would call statement `main.tex:932–941`
   homogeneous inline and keep `940` inline — then the table changes
   nothing. Sequence-level is the reading that addresses the mixing Víctor
   flagged.
2. **`p` does not lift gate 1.** "Independent of `k`/`L`" is read as *the
   condition does not use `k` or `L`*; gates 1 and 3 stay absolute, as
   required by the conserved thresholds. If `p` were also meant to lift
   `k ≥ 2`, every single-id paragraph-final mark would become a block —
   that contradicts the applied state of the 2026-11 pass ("no single-id
   block is left") and was not applied here.
3. **Mixed runs abstain, they do not follow the majority.** The defined
   behaviour of a mixed run is: no verdict from `u`, record the run as a
   uniformity defect for a later harmonising pass, fall through to `p` and
   the gates. Majority-wins would have been the alternative; it was not
   chosen, because it entrenches the existing mix instead of flagging it.

---

## Related documents

- `docs/citations.md` §8.5 — the generic rule (quantities, four gates, the
  two heuristics, decision order, review method).
- `docs/reports/20261115_WIT-001_criterion_sites.md` — the applied
  inventory of the 2026-11-15 pass (site table, sentence tails, counters).
- `docs/witness-rationale.md` — why the device exists and why the criterion
  is quantitative.
- `docs/reports/20261115_DEC-001_witness_decisions.md` — the decision log
  behind the witness tiers.