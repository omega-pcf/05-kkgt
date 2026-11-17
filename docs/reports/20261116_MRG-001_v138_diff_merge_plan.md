# MRG-001 — the v138 provenance: zone diffs and a merge plan

| Field | Value |
|---|---|
| **id** | `MRG-001` |
| **title** | The v138 provenance — per-zone diffs against the v136 base and this session, conflict table, and a wave-by-wave merge plan |
| **status** | report only — nothing of v138 was integrated; only this file was added to the repository |
| **date** | 2026-11-16 |
| **version** | 1.0 |
| **repository** | `05-kk-golden-throat` (public as `omega-pcf/05-kkgt`); `main.tex` at analysis time is byte-identical (md5 `9009256f9bdfb46e9765906ed1e6cbf2`) to the `ours_head.tex` snapshot the diffs were built from; `HEAD` moved during the analysis only under `tests/` (other agents), which this report does not touch |
| **evidence** | `~/…/cache/scratch/v138/`: `base_v136.tex`, `ours_head.tex`, `kk_golden_throat_v138.tex`, `merged3.tex`, `conflicts.json` (+`conflicts_classified.json`), `base_ours.diff`, `base_theirs.diff`, `base_ours_changes.txt`, `lean_v34_v35.diff`, `lean_code_v34_v35.diff`, `fig_repo_v138.diff`, `fig_v136_v138.diff`, `repro_v136_v138.diff`, `repro_v134_v138.diff`, `secdiff.py`, `decls.py`, `sigs.py`, `repro_run.log`, `repro_tail.log`, and the ten unzipped files of `~/Downloads/articulo9_v138.zip` |

---

## 1. Corpus and method

The zip contains ten files: the v138 PDF and `kk_golden_throat_v138.tex` (2643 lines), `TorreKK_LYR_v35.lean`, `reproduce_v138.py`, `figuras_v138.py`, and the five `fig_*.pdf` figures. They were extracted **outside** the repository, into the session scratch.

Three text sides were compared:

| Side | File | Lines |
|---|---|---|
| base (v136) | `git show 2b244e…:main.tex` → `base_v136.tex` | 2492 |
| ours (HEAD) | `main.tex` → `ours_head.tex` | 2532 |
| theirs (v138) | `kk_golden_throat_v138.tex` | 2643 |

Counts come from `git diff --no-index --numstat`, GNU `diff -u`, `git merge-file -p --diff3` (exit 67 = 67 conflict blocks, saved as `merged3.tex` and parsed into `conflicts.json`), `md5sum`, `pdftotext -q`, and small purpose-built parsers (`decls.py`, `sigs.py`, the classifiers recorded in §3). Every number below is reproducible from those artefacts; no assertion in this report rests on the predecessor's transcript alone (two of its results were re-derived and corrected, see §2.6).

---

## 2. Zone summaries

### 2.1 Manuscript (`main.tex`)

| Diff | Added | Removed | Hunks |
|---|---|---|---|
| base → theirs (author) | +441 | −290 | 80 |
| base → ours (this session) | +280 | −240 | 74 |
| ours → theirs | +587 | −476 | — |

Author-side change by section (top of `secdiff.py`; 23 sections touched in total):

| +/− | hunks | section |
|---|---|---|
| +270 −9 | 2 | Code and data |
| +18 −123 | 3 | (preamble) |
| +27 −33 | 14 | The physical retroduction |
| +26 −29 | 13 | The mathematical retroduction |
| +24 −23 | 12 | Physical axioms |
| +12 −12 | 2 | The criteria a single object must meet |
| +8 −8 | 3 | Third condition: the arity fixes the phase |
| +8 −8 | 2 | The two-brane model is the golden throat |
| +7 −6 | 3 | Second condition |
| +6 −7 | 2 | Contrast with the data |
| +6 −5 | 4 | Fourth condition: the clock fixes the bottom |
| +5 −5 | 3 | First condition |
| +6 −4 | 6 | Conclusions and summary |
| +4 −4 … +1 −1 | 1 each | Introduction, Delimitation, The data, Discussion, What is not claimed, … |

Our side concentrates in the same three sections (mathematical retroduction +74 −64, Physical axioms +63 −49, preamble +50 −41), i.e. **the two sessions edited the same regions**, which is why 67 blocks conflict rather than a handful.

Macro and taxonomy census (whole file):

| Token | base | ours | theirs |
|---|---|---|---|
| `\Lean{` | 170 | **0** | 185 |
| `\LeanCW{` | 6 | **0** | 6 |
| `\tier[` (ids form) | 61 | **216** | **0** |
| `\tier{` (class-only) | 32 | 17 | 142 |
| `\testref{` | 88 | **99** | **0** |
| `\wtag{` | 12 | **12** | **0** |
| tier classes | N 75, P 16, X 2 | P 172, N 58, X 3 | N 80, P\* 22, R 20, P 12, L 8 |

The author removed every `\testref` and every `\wtag`, dropped the ids bracket from `\tier`, redefined the macro itself (§3, conflict 3), and introduced three new classes (**R, P\***, **L**) while dropping **X**. This session did the opposite migration: `\Lean{}` → `\tier[ids]{…}` (commit history `6140d05`, `2488097`).

### 2.2 Figures (5 PDFs)

md5 of the author's zip figures against `images/`:

| figure | v136 zip | v138 zip | repo `images/` | text: repo vs v138 | text: v136 vs v138 |
|---|---|---|---|---|---|
| fig_background | `4cf7f443…` | `d5156739…` | `fb1c7f8f…` | **differs** | **differs** |
| fig_granularity | `b7c19927…` | `b7c19927…` | `ab37500a…` | identical | identical |
| fig_mobius_throat | `c3f76ca2…` | `c3f76ca2…` | `d63b8545…` | identical | identical |
| fig_throat_tiling | `0b16d8e1…` | `0b16d8e1…` | `7acf424e…` | blank lines only | identical |
| fig_tilings_strip | `30faed76…` | `30faed76…` | `b6b961d2…` | identical | identical |

* **1 of 5** figures changed inside the author's own provenance (v136 → v138): `fig_background.pdf`, byte and text level. The other four are byte-identical between the two author zips.
* All five md5s differ from `images/`, but that is the producer environment (our pipeline pins matplotlib 3.11.2, `SOURCE_DATE_EPOCH`, `pdf.fonttype=42` — commits `2a24a64`, `c90064d`), not content: text extraction is identical for three figures and differs only in blank lines for a fourth.
* `fig_background` differs repo-vs-author in **both** directions: our session deliberately removed the in-figure prose (commit `ff44a61`, report `docs/reports/20261116_FIG-001_figure_1_deembed.md` — at the author's own request, “el texto es muy pequeño de leer, es pésimo en UX”), while the author's v138 still embeds it and edits it further (panel reflows, axis ticks in panel (g), `x¹ = a + b¹'` block moved).

### 2.3 Generators

| Diff | Hunks | + / − | Scope |
|---|---|---|---|
| author `figuras_v136.py` → `figuras_v138.py` | 11 | +173 −15 | **all inside figure 1** (`seccion_44` helpers `cliff`, `cubeview`, `bd`, `hgt`, `head`, `band`) plus the version docstring |
| repo `scripts/figures/figuras_v134.py` → `figuras_v138.py` | 13 | +200 −32 | same region, plus our de-embed (`head(x,y,txt)` letter-only, `suptitle`/`band` removed, label fonts 20 → 8.8 on our side vs the author shrinking prose fonts 12 → 9) |
| repo generator vs author `figuras_v136.py` | 28 | +40 −30 | ratio 0.936 — our generator descends from v134 plus this session's determinism and de-embed work |

The author's substantive addition is a **text-legibility auto-shrink block** (`_DIAG`, `_bb`, `_slot`, `_contenido0`, `_choca` — “textos legibles sin cambiar el tamaño de la figura (v138)”, ~160 lines appended in `hgt`), which grows each label to a target size and shrinks it only on collision. It solves the same readability problem our FIG-001 solved by removing the prose — the two solutions are mutually exclusive on the same canvas.

### 2.4 Tests / `reproduce_v138.py`

* Section counts: v134 = **44**, v136 = **46**, v138 = **47** (new `seccion_47`, “la tríada como código, la cuerda como corte, y el código pentagonal”). Our suite mirrors sections 1–46 (`tests/test_sections_01_08.py` … `test_sections_45_46.py`); AUD-001 records 243 test functions and 350 audited claims.
* `repro_v136_v138.diff`: 11 hunks, **+239 −13**, of which **10 added `assert` lines**, a ~150-line `seccion_47`, and the ~160-line figure-legibility machinery (also present in `figuras_v138.py`). Against v134 the script adds **35** assert lines.
* New numeric content in theirs (vs base): `0.745` (`10a log2/π²` vs the area law's `½`), pentagon side `a = 1.061275` (`cosh a = φ`, `sinh a = √φ`), layer counts `[1, 6, 21, 61, 166, 441, 1161] = 5F₂ₙ₊₁ − 4`, boundary legs `[5, 20, 55, 145, 380, 995, 2605] = 5L₂ₙ₊₁`, rate `0.4457 → 1/√5 = 0.4472` (per layer φ² = 2.6180), Crofton `1.0753` crossings per unit with `χ = 2` giving `1.49 S` on average and `χ(S) = 1.592`, “the **2000** spacings checked”, `PYHP15` mentions 4 → 10, and **`11.98` at one site** where base and ours have `11.97` (8 / 8 occurrences; theirs has 7 + 1).
* Against our suite (grep evidence): `0.745` — 0 hits; pentagon-code assertions — 0 (only `{5,4}: pentagons` tiling names, `tests/src/kkgt/sections/_rest.py:1217`); `11.98` — 0 hits; `11.97` — asserted in at least six places (`s17_24.py:145`, `_rest.py:618`, `_rest.py:1335`, `test_sections_01_08.py:112`, `test_sections_17_28.py:138`, `test_sections_17_28.py:267`). **The v138-47 claims are uncovered, and the 11.97/11.98 divergence is a live conflict between the author's text and our tests.**
* Execution gate run for this report: `reproduce_v138.py` was executed in full — sections 1–43 in `repro_run.log` (killed at the section-44 banner by a tooling timeout) and sections 44–47 re-run in `repro_tail.log` — **47/47 sections, 0 tracebacks, 0 assertion errors**; section 47 printed exactly the numbers listed above.

### 2.5 Citations

| Measure | base/ours | theirs |
|---|---|---|
| bibliography entries | `src/bibliography.bib`: **199** keys | embedded `thebibliography`: **201** `bibitem`s |
| v136 zip embedded (reference) | 199 | — |
| keys added / removed / changed | — | **+2** (`ADH15`, `Mar18`), −0, changed 0 |
| distinct keys cited in the text | **194** | **196** (theirs-only: `ADH15` ×3, `Mar18` ×3; ours-only: none) |

The two entries to port:

* `ADH15` — A. Almheiri, X. Dong, D. Harlow, *Bulk locality and quantum error correction in AdS/CFT*, JHEP **04** (2015) 163, doi:10.1007/JHEP04(2015)163.
* `Mar18` — M. Marcolli, *Holographic codes on Bruhat–Tits buildings and Drinfeld symmetric spaces*, arXiv:1801.09623.

An earlier pass counted an ours-only key `key`; it comes from a **comment** (`main.tex:72–73`, “`[N]~\cite{key}`” inside the witness-grammar documentation) and is not a citation. 17 shared keys show a title-fragment mismatch against theirs' `bibitem` — all are `{Sitter}` brace-style differences, cosmetic.

### 2.6 Lean, v34 → v35

| Measure | v34 | v35 |
|---|---|---|
| total lines | 1523 | 1517 |
| code lines (comments stripped, non-blank) | 949 | 942 |
| top-level decls (`def/theorem/lemma/instance/structure/abbrev/axiom/opaque`, comments stripped) | 186 | 187 |
| axioms | **6** | **6** — same names, same statements |

Raw file diff: 63 hunks, +403 −409 (812 changed lines, of which **391 are pure comment lines** — the docstrings were translated to Spanish). Code-only diff (`lean_code_v34_v35.diff`): **58 hunks, +83 −90**; whitespace-normalised: 33 hunks, +82 −89.

* **ADDED 2**: `eta` (the rename target) and `pentagon_side_golden` (genuinely new, +8 lines immediately before `end TorreKK`; statement `2*(cos(π/5)/sin(π/4))^2 − 1 = (1+√5)/2`).
* **REMOVED 1**: `etaMetric` — a **rename** `etaMetric → eta` (8 occurrences in v34, 0 in v35).
* **Signatures changed (comments stripped): 10** — 3 via the rename (`D_sq_eq_eta`, `eta_eq_exp_fourA`, `eta_symmetrizes`) and 7 via `‖·‖ → Complex.abs` (`angle_has_modulus_one`, `area_coefficient_every_level`, `bulk_boundary_isometry`, `J_swaps_moduli`, `partition_T_invariant`, `triad_modulus`, `worldline_modulus`).
* **Statements changed: 170** including comments; **45** with comments stripped — of those, 3 are the rename alone and **42 are genuine proof/statement maintenance**; the other ~125 decls changed only because their docstrings were translated.
* Other code changes: `set_option linter.style.longLine false` removed; `set_option maxRecDepth 100000` removed (before a `decide`); mathlib API migrations (`lt_div_iff₀/div_lt_iff₀ → lt_div_iff/div_lt_iff`, `Irrational.ratCast_add/div_ratCast/intCast_mul/mul_natCast → rat_add/div_rat/int_mul/int_mul`, `isAlgebraic_natCast → isAlgebraic_nat`, `Nat.dvd_one.mp → Nat.mul_eq_one.mp`, new `pow_left_injective₀`); `field_simp → field_simp <;> ring` at ~18 sites; proof simplifications (`capacity_exceeded` calc → `nlinarith`, `stereo_ratio` gains a `have`, `ring_resolution_*` rewritten).
* **Axioms: unchanged** — `bessel_J1_zeros`, `exp_pi_mul_algebraic_transcendental`, `stereographic_meridian_deriv`, `dedekindEta`, `eta_T`, `weyl_equidistribution`. Nothing new is assumed.

**Statement guard (enunciado).** Every Lean id cited by our manuscript — **133 unique ids** from `\tier[ids]{…}` in `main.tex` (comments stripped) — exists in **v35** (and in v34); **zero** ids cited by us vanish in v35. Every id cited by the author's v138 text — **169 unique names** from `\Lean{…}` — also exists in v35; the base's 137 names are a subset of theirs (the author dropped none), and the only cited name absent from v34 is `pentagon_side_golden` (new in v35). **The guard passes in both directions: porting v35 satisfies both manuscripts.**

**Corrections to the predecessor's transcript.** Its “REMOVED … `def ETA_X`” line is an artefact: `ETA_X` occurs **0** times in both Lean files (the real removal is `etaMetric`, renamed to `eta`). Its “10 names cited by theirs missing in v35” (`tower_first_law`, `H_half_one_bit`, …) is an extraction bug: those strings occur **0** times in theirs, base and ours alike. The counts in this section were re-derived from the files.

---

## 3. The conflict table

`git merge-file -p --diff3 ours_head.tex base_v136.tex kk_golden_throat_v138.tex` exits **67** (67 conflict blocks). By section:

| n | section | | n | section |
|---|---|---|---|---|
| 16 | The mathematical retroduction | | 2 | The two-brane model |
| 14 | Physical axioms | | 2 | Contrast with the data |
| 11 | The physical retroduction | | 1 each | Delimitation · The data · Second condition · Third condition · The factor π · What is not claimed · Conclusions · Code and data |
| 6 | The criteria a single object must meet | | 4 | (preamble) |
| 4 | Fourth condition: the clock fixes the bottom | | | |

Primary classification (each block assigned once; precedence: front matter → figure → genuine numeric content → test anchor → witness label → mark grammar → prose):

| n | class | meaning |
|---|---|---|
| **27** | C — test anchor | ours keeps `\tier[\testref{…}]{…}`; theirs replaces it with `(section NN of \code{reproduce\_v138.py})` |
| **12** | G1 — ids grammar | ours `\tier[ids]{cls}` vs theirs `\Lean{ids} \tier{cls}` |
| **9** | E — numeric content | real number/paragraph divergence (listed below) |
| **7** | G2 — class marks | theirs appends `\tier{N}` / `\tier{P\*}` / `\tier{R}` where ours carries no class mark |
| **5** | B — witness label | ours `\item[\wtag{W2}{W01}.]` vs theirs `\item[W2 (W01).]` |
| **2** | D2 — preamble macros | macro definitions (blocks `16–46`, `50–180`) |
| **2** | G1/G2 mixed | both grammars in one block |
| **1** | D1 — title/date block | `194–261` |
| **1** | D3 — keywords / tier legend | `299–321` |
| **1** | F — figure include | `785–794` |

Issue presence (a block may carry several): ids-form `\tier[` 48 · author class marks 48 · `\Lean{` 46 · `\testref` 35 · reproduce-anchor 18 · `\wtag` 7 · imported-statement site 14 · emphasis/gloss rewritten on both sides 4 · ours-only closing-mark line-breaking (`6140d05`) 2.

### The ten most delicate conflicts

| # | block (merged3 lines) | conflict | why delicate |
|---|---|---|---|
| 1 | **194–261** | title/date: ours `\date{261116; last modified \today; v0.1.0}` + `\renewcommand{\datename}{Received}` + amsart byline comments (commit `2488097`) vs theirs plain `\date{November 6, 2026}` | the version metadata the session added for the author is exactly what the author's own front matter does not carry; taking theirs silently reverts it |
| 2 | **50–180** | preamble macro system: ours `\code`, `\tier[2][]`, witness-gate comment (O61/B63/T3) vs theirs `\Lean`/`\LeanCW` definitions | our whole citation grammar hangs on this block; theirs re-introduces the macros we migrated away from |
| 3 | **16–46** | `\tier` **arity**: base/ours `\providecommand{\tier}[2][]` (ids + class) vs theirs `\providecommand{\tier}[1]` (class only) | taking theirs' definition breaks **all 216** `\tier[ids]{…}` calls at once |
| 4 | **1836–1842** | `11.97 (\eqref{eq:sigmaIR}) \tier[\testref{…}]{N}` vs `11.98 \tier{N}` | a numeric divergence: our tests assert 11.97 in ≥6 places; the author changed one occurrence of eight |
| 5 | **2677–2683** | ours three-test list `\tier[\testref{test_depth_of_the_clock}, \testref{test_scales}, …]{…}` vs `(section~37 of \code{reproduce\_v138.py})` | the pytest-anchor grammar vs the reproduce-script anchor — the same collision as the 27 class-C blocks, at its most extreme |
| 6 | **2084–2089** + **2073–2082** | author **deletes** the paragraph “Two fixed weights, and why a count does not reach them.” (T0; ours-only numbers `1.00000`, `0.9757`, `1.00000/√5` …) and rewrites its neighbour (T4) | silent content loss if taken wholesale; the numbers were audited by AUD-001 |
| 7 | **785–794** | `\includegraphics[width=0.85…]` vs `0.93` | our narrowing is part of FIG-001 (de-embed); the author's 0.93 is the prose-embedded layout |
| 8 | **299–321** | ours keeps `\keywords{…}`, theirs replaces it with the five-class legend “Tiers: P, P\*, N, L, R …” | the class taxonomy itself: base/ours know P/N/X, the author adds R/P\*/L and drops X — legend, census (233 vs 142 marks) and every inline mark must move together |
| 9 | **3076–3091** | Code and data: ours “one package `\code{kkgt}` … **forty-six** numbered sections” vs theirs “one script `reproduce_v138.py`, in **forty-seven** sections” | the reproducibility narrative of the paper; ours-only numbers 529/533/10/5, theirs-only 47 |
| 10 | **16–46** | our 16-line witness-gate comment (docs/citations.md §8.5 gates) vs a single `\providecommand` line | documents the session's placement rules; trivially lost in a line-based merge |

The genuine numeric divergences inside class E are: `11.97 → 11.98` (#4), the added “2000 spacings” (`1708–1715`), the deleted “Two fixed weights” paragraph (`2084–2089`), the new pentagon passage with `0.745` (`2537–2545`), and the Code-and-data enumeration (`3076–3091`); `1860/1871` differ only in a `90` vs `π/2` rendering, `2598` in one stray token.

---

## 4. Merge plan, by waves

Nothing below is executed; each wave lists what to port, its gate, and its risk. Order matters: the grammar is frozen first, because every later prose port is expressed in it.

### Wave 1 — freeze the grammar (preamble, classes, anchors)
* **Port:** nothing mechanical. **Decide and record:** keep `\providecommand{\tier}[2][]` (arity conflict #3); keep `\Lean{}` retired; keep the 99 `\testref` anchors and 12 `\wtag` labels; keep the `\date{261116; …}` metadata (or agree a joint format with the author); reconcile the class taxonomy — either adopt R/P\*/L into our legend and census (233 marks to re-review) or ask the author to keep P/N/X.
* **Gate:** preamble compiles; `grep -c '\\Lean{' main.tex` stays 0; tier legend and keywords both present; a written decision recorded in this report's successor.
* **Risk:** highest leverage of the whole merge — one wrong macro line invalidates 216 marks.

### Wave 2 — bibliography
* **Port:** the two entries `ADH15`, `Mar18` into `src/bibliography.bib` (verbatim from §2.5); no other entry changed.
* **Gate:** LaTeX run reports no undefined citations; key count 199 → 201.
* **Risk:** negligible.

### Wave 3 — manuscript prose (the +441 −290 author side, re-expressed in our grammar)
* **Port:** all author prose edits in the 23 touched sections, including the expanded pentagon-code passage (`PYHP15` ×4→×10, `0.745`, `5F/5L` counts, `Mar18` p-adic sentence, `pentagon_side_golden` mark), the “2000 spacings” completion, and the class-mark additions where we agree on the taxonomy — each mark rewritten as `\tier[ids]{…}` with our classes, each reproduce anchor **kept** as `\testref`.
* **Resolve block by block:** all 67 conflicts, starting with the ten in §3; for #6 (deleted paragraph) confirm with the author before dropping audited content; for #4 do not take `11.98` until the author confirms it against `eq:sigmaIR`.
* **Gate:** full compile; zero `\Lean{`; `\testref` count ≥ 99; `\tier[` count ≈ 216 + new marks; every `\ref{imp:…}` closing mark still starts its line (`6140d05`); no number from AUD-001's 350-claim list disappears without a recorded decision.
* **Risk:** high — this is the bulk of the diff and the home of the 27 class-C and 12+7 class-G conflicts.

### Wave 4 — Code and data, tests, AUD-001 delta
* **Port:** the v138 *content* of Code and data (47-section parity statement) into our pytest narrative — keep `\code{kkgt}` as the primary vehicle, add the reproduce-parity sentence; add tests for the uncovered claims: pentagon side `a = 1.061275`, counts `5F₂ₙ₊₁−4` / `5L₂ₙ₊₁`, rate `→ 1/√5`, `0.745` vs `½`, `χ(S) = 1.592`, the `2000` spacings, and section 47's triad/perfect-tensor statements (rank-1 projector, `rank(Pc) = 2`, 20 isometries).
* **Gate:** full pytest green (sections 1–46 + the new 47); `reproduce_v138.py` 47/47 already ran clean here (§2.4) — re-run after integration; AUD-001 matrix extended with the new claims and the 11.97/11.98 decision.
* **Risk:** medium — `tests/` is being migrated by other agents (`SEC-001`); this wave must sequence behind them and touch only new test code.

### Wave 5 — figures
* **Port:** **no binary figure.** Do not take the author's `fig_background.pdf` — it re-embeds the prose FIG-001 removed at the author's request. Port only what survives review: the author's layout numbers in `seccion_44` that do not reintroduce prose (panel geometry `0.15→0.132`, `0.17→0.19`, `0.685→0.62`), and decide whether the auto-shrink machinery (`_DIAG`…) is wanted *after* the de-embed (it is written for the embedded-prose layout).
* **Gate:** regenerate all five figures through `npm run generate:figures`; byte-stable across two runs; text extraction of `fig_background` still contains no prose sentences; the other four stay text-identical to today's.
* **Risk:** medium — the two readability solutions (de-embed vs auto-shrink) are contradictory; reconciling them may need the author.

### Wave 6 — Lean v35
* **Port:** the file wholesale (`TorreKK_LYR_v35.lean` replaces v34): rename `etaMetric → eta`, add `pentagon_side_golden`, drop the two `set_option`s, take the Spanish docstrings and the mathlib-API maintenance.
* **Gate:** `lake build` green on `leanprover/lean4:v4.33.1` (`.lake` is prebuilt, 7.3 GB); axiom count stays **6** with the same names; re-run the §2.6 guard (133 our ids + 169 author ids ⊆ v35); `grep -c etaMetric` = 0 in the repo.
* **Risk:** low–medium — statements changed in 42 decls (proof maintenance), so a build failure is possible and would need the author's proof, not ours.

---

## 5. What is **not** ported

* The author's `\Lean{}` / `\LeanCW{}` markup (185 + 6 occurrences) — our migration to `\tier[ids]{…}` stands.
* The one-argument `\tier` definition — it would break every ids-bearing call.
* The removal of all 99 `\testref` anchors and all 12 `\wtag` labels — the pytest citation grammar is this session's product (`6140d05`, AUD-001 depends on it).
* The removal of `\keywords{…}` from the front matter.
* The prose-embedded `fig_background.pdf` (FIG-001 / the author's UX request) and the width `0.93` that goes with it.
* The plain `\date{November 6, 2026}` unless the author confirms it against our received/modified/version line.
* The deleted “Two fixed weights…” paragraph and the bare `11.98`, until the author confirms both (they are audited content on our side).
* The reproduce-script version of Code and data as the *only* narrative (ours keeps `\code{kkgt}` as primary).

## 6. Gaps

* **v35 has not been compiled** in this session; the `lake build` gate is Wave 6 (the predecessor's toolchain check was interrupted; toolchain and `.lake` size were verified here, the build was not run).
* `reproduce_v138.py` ran 47/47 clean, but its outputs were only compared to our suite **by literal grep**, not by a systematic number-by-number diff against the AUD-001 JSONs.
* The conflict classifier is rule-based; the class counts are reproducible from `conflicts_classified.json`, but 33 blocks carry more than one issue (presence counts in §3).
* 17 bibliography keys differ only in `{Sitter}` bracing; the reconciliation was not performed.
* Whether the author's `figuras_v136.py`→`v138` layout numbers interact with our determinism patches was not executed (no figure regeneration was run).
* Section-47 tests do not exist yet (Wave 4); `tests/` is owned by other agents during this analysis and was left untouched.
* The author's per-section prose was counted, not line-by-line proofread; the report trusts the diff for what changed, not for what it means.
