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

---

# Wave W1 — applied

| Field | Value |
|---|---|
| **wave** | W1 of §4 — *freeze the grammar* (preamble, classes, anchors) |
| **date** | 2026-11-17 |
| **scope** | `main.tex` + this report only; `tests/`, `scripts/`, `citation.csl.json`, `lean/`, `images/` untouched |
| **commits** | one conventional commit for this section; **no push** |
| **outcome** | every gate green; `main.tex` needed **zero byte changes** — measured below, not assumed |

## W1.0 The measured state, and why `main.tex` did not move

The R/L/P\*/`\Lean{}` marks of this wave live in **the author's file**, not in ours. Whole-file
counts (`grep -o -F … | wc -l`, so occurrences and not lines):

| token | `kk_golden_throat_v138.tex` | `main.tex` (HEAD `e77b015`) |
|---|---|---|
| `\tier{R}` | 20 | **0** |
| `\tier{L}` | 8 | **0** |
| `\tier{P*}` | 22 | **0** (only the colour hook `main.tex:53`) |
| `\Lean{` | 185 | **0** |
| `\LeanCW{` | 6 | **0** |
| classes printed by the body | N 80, P\* 22, R 20, P 12, L 8 | **P 172, N 58** (the other 3 hits are the preamble comment `main.tex:28,60,64`) |

So "migrating" them means deciding, claim by claim, what each becomes in our grammar and
applying it **only where our text still disagrees**. It does not mean a blind `sed` over
`main.tex`: the classes were already removed once (`923358d`) and the names already migrated
once (`bcee5eb`, DEC-001 §6). The three tables below are that decision record; the
`main.tex` column is the evidence that each row is already in its target form.

The author's prose was **not** ported in this wave. Three of the sites are new author content
(R4, R13, R14 below) and one new Lean name (`pentagon_side_golden`); porting them now would
introduce `\cite{ADH15}`, `\cite{Mar18}` (Wave 2 keys) and a name absent from `v34`, i.e. it
would break the very gates this wave freezes. They are queued, not guessed.

## W1.1 The 28 `R`/`L` sites, claim by claim

`R` → prose (no mark) and `L` → the citation stays, is what `docs/citations.md` §8.3 already
rules ("Why there is no `R`", "Why there is no `L`"); where the claim *is* witnessed, the
target is `P` with an external source or `N` with a test, per the W1 rule. `status` is
`resolved` (our text already holds the target), `new` (the claim is not in our text → Wave 3),
`bring-up` (ambiguous or blocked — not guessed).

### `R` — 20 sites (1 legend + 19 body)

| # | theirs | claim | ours | status |
|---|---|---|---|---|
| R1 | L81 | the legend line itself (`R` a reading …) | our gloss `main.tex:253-258` declares `P`,`N` only | not ported — **our gloss stands** (the taxonomy decision) |
| R2 | L165 | "its relation to the $AdS_2$ throat is a comparison of form" | `main.tex:288` same sentence, no mark | resolved → prose |
| R3 | L538 | caption (d): "the turn to the face is a reading" | `main.tex:661` "the turn is a reading, and the passage the paper proves is (c)" | resolved → prose (§8.2 rule 8: no tags in captions) |
| R4 | L878 | "…one microstate, and no ensemble" — a QEC reading citing `ADH15,PYHP15` | absent: no `ADH15`, no "code subspace" in `main.tex` | **new** → Wave 2 (`ADH15`) + Wave 3; target = prose, no mark |
| R5 | L915 | "each level reaches a distinguishable state in exactly its own time, and only with the weight $\tfrac12$" | `main.tex:1050`, no mark (the sentence's Lean names carry `P[…]`) | resolved → prose |
| R6 | L1533 | "a translation … that loses nothing of what is counted" | `main.tex:1665` | resolved → prose |
| R7 | L1758 | "that they are one twelve is a reading" | `main.tex:1901` "…and that they are one twelve is a reading." | resolved → prose |
| R8 | L1786 | "so the three columns are a comparison of form" | `main.tex:1931` | resolved → prose |
| R9 | L1854 | "$\varepsilon\tau=\pi$ … alternates as the half-turn does from level to level" | `main.tex:2000`, no mark (`P[closure_each_level]` sits earlier in the sentence) | resolved → prose |
| R10 | L1854 | "in five, the throat, whose step $\log\golden$ is the regulator of $\mathbb Z[\golden]$" | `main.tex:2000` "(read through `\S\ssec:math`)" | resolved → prose |
| R11 | L1887 | "Both are comparisons of form" | `main.tex:2033` | resolved → prose |
| R12 | L1893 | "both read the golden lattice through rational ratios" | `main.tex:2040` | resolved → prose |
| R13 | L1893 | "a holographic code is built from perfect tensors of several legs `\cite{PYHP15}` (section 47 of `\code{reproduce_v138.py}`)" | absent (`perfect tensors`, section 47 → 0 hits) | **new** → Wave 3 (section 47) |
| R14 | L1893 | "exists only for $p=2$ `\cite{Mar18}`" | absent (`Mar18` → 0 hits) | **new** → Wave 2 (`Mar18`) + Wave 3; target = prose |
| R15 | L1936 | "the particles of a level observe it" | `main.tex:2084` "…observe it---a reading of the records, not a result about them." | resolved → prose |
| R16 | L1959 | `\tier{R}` standing **after** a full stop, marking "…which the note does not compute." | `main.tex:2107` the sentence is kept, no mark | resolved → prose |
| R17 | L2007 | "…with weight $e^{-\pi}$, not at the edge of the window" | `main.tex:2160` | resolved → prose |
| R18 | L2019 | "the comparison is of form, not an identification" | `main.tex:2172` | resolved → prose |
| R19 | L2038 | "of the gravitational response of about a thousand bits at the scale of the leptons" | `main.tex:2191`, no mark; the next sentence carries `\tier{P} in~\cite{CW6} for the weld` | resolved → prose |
| R20 | L2260 | "Read with (F10), three more of these accounts change place" | `main.tex:2412` | resolved → prose |

**16 of the 19 body `R` claims are already prose in our text; 3 are author-new (R4, R13, R14).**

### `L` — 8 sites (1 legend + 7 body)

| # | theirs | claim | ours | status | target under the W1 rule |
|---|---|---|---|---|---|
| L1 | L81 | the legend line itself (`L` cited) | our gloss `main.tex:253-258` | not ported — **our gloss stands** | — |
| L2 | L834 | "the Euler characteristic is classical `\cite{Ser71}`" — preceded by $\chi(\mathrm{SL}_2(\mathbb Z))=\tfrac14+\tfrac16-\tfrac12=\zeta(-1)$, tagged `\tier{N}\tier{L}` | `main.tex:966` citation only, **no mark** | **bring-up (blocked)** | `N[\testref{test_the_chain_of_twelves}]` — that test asserts `-1/zeta(-1) == 12` — but the id is **not** in the census's pinned set and `tests/` belongs to another worker, so the `\testref` and its census line must land together in one pass that owns both files |
| L3 | L989 | "the lemniscatic value `\cite{WW27}`" | `main.tex:1126-1127` `N[\testref{test_theta3_at_tau_i}]` | resolved | **N** ✓ |
| L4 | L1178 | "`\tier{L}` for the continuum statement `\cite{RS99,DHR00}`" | `main.tex:1314` "For the continuum statement *see* `\cite{RS99,DHR00}`" | resolved — a cross-reference, not a claim (§8.3) | no mark |
| L5 | L1273 | "$\Gamma\propto x^{3}$ `\cite{DHR00}`" | `main.tex:1408` citation only, no mark | **bring-up (ambiguous)** | literal W1 rule → `[P] in~\cite{DHR00}` *or* `[N]~\cite{DHR00}`; §8.3 would keep the bare citation. Not guessed |
| L6 | L1349 | "the two-brane masses on a deep throat are $m_k=j_{1,k}\,k\,e^{-k\pi r}$ `\cite{RS99,DHR00}`" | `main.tex:1482-1484` citation kept; the proof closes `\tier{P}.` | resolved | **P** ✓ |
| L7 | L1399 | "`partition_T_invariant` `\cite{Apo90}` for the transformation law of $\eta$" | `main.tex:1578` `N[\testref{test_the_lambda_transformation_laws_hold_to_1e_16}]` | resolved | **N** ✓ |
| L8 | L1980 | "below the bound of trans-Planckian censorship `\tier{N}~\tier{L}`" | `main.tex:2131-2132` `\cite{BV20}` + `N[\testref{test_distance_to_the_measured_lambda}]` | resolved | **N** ✓, `L` dropped |

**5 of the 7 body `L` claims are resolved (3 → `N`, 1 → `P`, 1 → citation only); 2 are
bring-up (L2 blocked on the census, L5 ambiguous).**

## W1.2 The 22 `P*` sites — reconciled

Our `P*` is internal (`docs/citations.md` §8.2 rule 7, §8.3): it renders `[P*]` in ochre for a
draft between builds, is **not** in the gloss and is never printed by the released text — the
body marks those claims `P`. Every author site below is therefore either an internal mark we
already carry as `P[…]`, or a line of his prose we already hold without the mark.

| # | theirs | content | ours | status |
|---|---|---|---|---|
| P\*1 | L80 | the legend line `\tier{P*} written in Lean, not yet compiled` | our gloss `main.tex:253-258` | **not ported** — internal class, never in the gloss |
| P\*2 | L752 | "those marked `\tier{P*}` are proved again in this note's Lean module" | `main.tex:877-878` "…collected here so that the note can be read on its own, and this note's Lean module proves several of them again." | resolved → prose |
| P\*3 | L773 | `sq_add_inv_sq` | `main.tex:901` `\tier[sq\_add\_inv\_sq]{P}` | resolved |
| P\*4 | L784 | `certainty_principle, log_from_scale` | `main.tex:913` `\witness{P}{…}` | resolved |
| P\*5 | L800 | `lattice_radius_conjugate` | `main.tex:931` `\tier[…]{P}` | resolved |
| P\*6 | L806 | `additive_law_forces_golden` | `main.tex:938` `\tier[…]{P}` | resolved |
| P\*7 | L812 | "the level of $\golden$ are one quantity, in the unit $\lambda$" | `main.tex:944-945` `\witness{P}{golden\_valuation\_on\_tower, two\_adic\_is\_level}` | resolved |
| P\*8 | L822 | `golden_eq_two_cos_pi_div_five, golden_self_reference` | `main.tex:955-956` `\witness{P}{…}` | resolved |
| P\*9 | L840 | `exponent_angle_radius, angle_has_modulus_one` | `main.tex:974` `\witness{P}{…}` | resolved |
| P\*10 | L844 | `spectral_angle_ratio` | `main.tex:978` `\tier[…]{P}` | resolved |
| P\*11 | L1094 | `eta_symmetrizes, eta_eq_exp_fourA, D_sq_eq_eta, D_conjugated_hops_equal` | `main.tex:1231` `\witness{P}{…}` | resolved |
| P\*12 | L1132 | `bloch_complexified, bloch_factor_is_hop, …, ring_constant_mode, ring_mode_below_BF` | `main.tex:1269-1270` `\witness{P}{…}` | resolved |
| P\*13 | L1207 | "$d=n+1$, axiom (F2), the arity $n=3$, $\nu=1$ and the phase is $\tfrac14$" | `main.tex:1344` `\witness{P}{phase\_of\_dimension, phase\_quarter\_iff, phase\_from\_arity}` | resolved |
| P\*14 | L1247 | `D_conjugated_hop_is_one` (beside a `\tier{N}`) | `main.tex:1383` `\tier[D\_conjugated\_hop\_is\_one]{P}` | resolved |
| P\*15 | L1326 | `rs_warp_is_golden, rs_depth_is_levels, rs_scale_is_H_at_bottom, rs_kpir_from_uv` | `main.tex:1461-1462` `\witness{P}{…}` | resolved |
| P\*16 | L1344 | `scale_operator_at_bottom` | `main.tex:1478` `\tier[…]{P}` | resolved |
| P\*17 | L1350 | the proof of the two-brane masses closes `\tier{P*}.` | `main.tex:1484` `\tier{P}.` | resolved → `P` |
| P\*18 | L1692 | "the torus $\eta=\pi/4$ is fixed by the mirror, and the levels $\eta_n$ are placed by $\golden$ (section 46)" — `\tier{P*}~\tier{N}` | `main.tex:1832` `\witness{P}{tan\_eta, level\_zero\_is\_clifford, clifford\_square}` + `main.tex:1833` `\witness{N}{\testref{test\_a\_torus…}, \testref{test\_the\_flat\_tori…}}` | resolved → `P` + `N` |
| P\*19 | L1961 | `window_crosses_half, hubble_below_bulk_crossing` | `main.tex:2110` `\witness{P}{…}` | resolved |
| P\*20 | L2038 | "`\tier{P*}` for the weld" | `main.tex:2191` `\tier{P} in~\cite{CW6} for the weld` | resolved → `P` with the external source |
| P\*21 | L2076 | "`\tier{P*}` for the identities; the reading is axioms (F6) and (F7)" | `main.tex:2229` `\tier[area\_law\_4d\_meets\_weld\_iff, phase\_equals\_inverse\_dimension\_iff]{P} for the identities` | resolved |
| P\*22 | L2150 | `old_symmetrizer_fails` | `main.tex:2302` `\tier[…]{P}` | resolved |

**21 of 21 body `P*` sites resolved; 0 new; 1 legend line not ported by decision.**

## W1.3 The 185 `\Lean{}` and 6 `\LeanCW{}` sites

| measure | value |
|---|---|
| `\Lean{` occurrences in theirs | **185** (169 unique internal names) |
| occurrences whose **every** name already sits in one of our `\tier[names]{P}` / `\witness{P}{…}` marks | **184 / 185** |
| occurrences not yet carried | **1** — theirs L1893, `pentagon_side_golden` (the new pentagon passage) |
| `\LeanCW{` occurrences | **6** (11 unique names, all external CW6 declarations) — all resolved: ours keeps `\tier{P} in~\cite{CW6}` (`main.tex:987`, `1027`, `1032`) and the bracket of external names is gone, per §8.2 rule 8 (an external source is the citation, never a bracket with a name) |
| names our text carries that the author does **not** cite | **0** |
| names the author cites that our text does not carry | **1** — `pentagon_side_golden` |

Reconciled as sets: `ours ⊂ theirs` exactly, with the single difference
`theirs − ours = {pentagon_side_golden}`.

The 184 carried occurrences are not listed one by one here: each is already visible at the
`main.tex` line shown in §W1.2 (the same marks carry them), and the invariant that matters is
the set identity above plus the enunciado guard of §W1.4.

**Action taken:** nothing mechanical to apply — the migration `bcee5eb`/DEC-001 performed is
complete for every name our text holds; `grep -c 'Lean{' main.tex` is `0` before and after.

## W1.4 Enunciado guard (every cited name must exist in the Lean file)

| guard | result |
|---|---|
| every name in our `\tier[names]{P}` and `\witness{P}{…}` in `main.tex` exists in `lean/TorreKK_LYR_v34.lean` | **168 / 168 ✓** (the only extraction artefact is the literal `ids` token of the preamble comment `main.tex:28`) |
| every internal name of the author's 185 `\Lean{}` occurrences exists in `v34` | **168 / 169** — `pentagon_side_golden` **absent** |
| the same name in `kk_golden_throat_v138` `v35` (`scratch/v138/TorreKK_LYR_v35.lean`) | **present** — it is one of the two decls `v34 → v35` adds (§2.6) |
| spellings | no divergence found: `rs_kpir_from_uv` is lowercase in theirs, in ours and in `v34`/`v35` |

Consequence: `pentagon_side_golden` **cannot** be migrated in this wave — it would raise the
guard. It lands with Wave 3 (the sentence) after Wave 6 (the Lean file), in that order.

## W1.5 The date block

Ours is intact and theirs was not ported:

```
main.tex:142  \renewcommand{\datename}{Received}
main.tex:155  \date{261116; last modified \today; v0.1.0}   (selfcite:begin id="version")
```

`kk_golden_throat_v138.tex` still carries the plain `\date{November 6, 2026}`; conflict D1 of
§3 stays resolved in our favour, and the line keeps being rewritten by the build
(`selfcitations`), not by hand.

## W1.6 Gates at the close of W1

| gate | command | result |
|---|---|---|
| type-check | `pnpm run type-check` | **exit 0**, no output ✓ |
| tests | `uv run pytest tests/ -q` | **533 passed** in 62 s ✓ |
| census | `uv run pytest tests/test_section_census.py -q` | **18 passed** ✓ |
| build | `pnpm run build` | exit 0, **63 pages**, `grep -c '^!' build/main.log` = **0**, `grep -ci undefined build/main.log` = **0** ✓ |
| `\Lean{` | `grep -c 'Lean{' main.tex` | **0** ✓ |
| anchors | `grep -o -F '\testref{' main.tex \| wc -l` | **99** ✓ (the MRG-001 §2.1 invariant) |
| anchors (literal brief form) | `grep -c 'testref' main.tex` | **80 lines** — the brief's `≥99` is an *occurrence* count: `grep -o 'testref' \| wc -l` = **104**, of which **99** are the anchors `\testref{`. The line count can never reach 99 while several anchors share a line; reported as measured, not silently passed |
| labels | `grep -o -F '\wtag{' main.tex \| wc -l` | **12** ✓ |
| ids grammar | `grep -o -F '\tier[' main.tex \| wc -l` | **216** ✓ (arity `\providecommand{\tier}[2][]` at `main.tex:80` untouched) |
| legend + keywords | `main.tex:253-258`, `main.tex:193` | both present ✓ |
| tree | `git status` at commit time | only this report staged |

## W1.7 Bring-up for the principal author

Nothing here was decided in his place.

1. **L2 — the Euler characteristic.** Theirs tags $\chi=\zeta(-1)$ `\tier{N}\tier{L}`; ours
   carries only `\cite{Ser71}`. The `N` is available and honest:
   `N[\testref{test_the_chain_of_twelves}]` (it asserts `-1/zeta(-1) == 12`), **but** that id
   is not in the census's pinned set, so the tag and its census line must land in one pass
   that owns `main.tex` *and* `tests/`. Tick to queue it; leave bare otherwise.
2. **L5 — $\Gamma\propto x^{3}$ `\cite{DHR00}`.** Read off an external source, so the literal
   W1 rule gives `[P] in~\cite{DHR00}` or `[N]~\cite{DHR00}`; §8.3 would keep the bare
   citation. Which of the three is his call.
3. **R4, R13, R14 — three `R` claims that do not exist in our text yet.** They ride on author
   content that is *not* in the manuscript: the QEC reading of R4 (`ADH15`), the section-47
   perfect-tensor sentence of R13 (`PYHP15`, §47), the $p=2$ Mumford sentence of R14
   (`Mar18`). Both new bib keys are Wave 2. When they land the target is **prose, no mark**.
4. **`pentagon_side_golden`.** Blocked on Wave 6 (present in `v35`, absent from `v34`) —
   flagged so no later pass migrates it early and trips the guard.
5. **Two readings of the `testref` gate.** See §W1.6: the `≥99` figure holds for occurrences
   of the anchor `\testref{` (99) and for the substring (104), and fails for lines (80). The
   brief's literal `grep -c` reads lines; the intent is the anchor count. Recorded rather than
   reinterpreted.

## W1.8 Left to the later waves (nothing done here)

* **Wave 2** — `ADH15`, `Mar18` into `src/bibliography.bib`.
* **Wave 3** — the author's prose, including R4/R13/R14 and the pentagon passage; all 67
  conflicts of §3, of which W1 has now settled the *grammar* side (arity, classes, anchors,
  date, gloss).
* **Wave 4** — section-47 tests and the `11.97`/`11.98` divergence.
* **Wave 6** — `TorreKK_LYR_v35.lean`, after which `pentagon_side_golden` becomes migratable.
* **Not ported, by decision** — the author's legend (P, P\*, N, L, R), his one-argument
  `\tier`, his removal of the 99 anchors and 12 labels, his `\date{November 6, 2026}`.

---

# Wave W3 — applied

| Field | Value |
|---|---|
| **wave** | W3 of §4 — the manuscript prose (the author's +441 −290 side) re-expressed in our grammar |
| **date** | 2026-11-17 |
| **scope** | `main.tex` + this report only; `tests/`, `scripts/`, `citation.csl.json`, `lean/`, `images/` untouched |
| **commits** | 3 content commits + this report; **no push** |
| **base** | `ea73175` (tree clean at start); content commits `8504309`, `b5d5b01`, `653fc10` |
| **outcome** | all 80 author hunks dispositioned; **4 blocks ported**; every gate green at the close of every tanda |

## W3.1 Method

The author side (`base_theirs.diff`, +441 −290, 80 hunks, 23 counted sections) was parsed
hunk by hunk and each hunk split at word level into *grammar* changes and *prose* changes.
Grammar changes were then answered with the W1-frozen form (brief decisions 5–7): our
`\tier[ids]{cls}` arity, our 99 `\testref` anchors (never the author's
`section~NN of \code{reproduce\_v138.py}`), our 12 `\wtag` labels, our `\witness` blocks, no
`\Lean{`/`\LeanCW{`, no R/L/P\* class marks (an `R`/`L` mark in theirs is *prose* or *the
citation* in ours), no tags in captions, no id renames, an external source only as
`in~\cite{…}` outside the bracket. Prose changes were ported only after the **numeral gate**
of the triage §3.3: before/after numeric tokens compared per block, `simple` (rounding /
tolerance / anchor artifact) resolved in our favour and noted, `real` not ported but queued
as bring-up.

Two census tests turned out to be additional, hard guards on this wave (both green before
and after; neither was modified):

* `test_the_manuscript_cites_no_numbered_section` — `main.tex` may contain no `section~N`
  at all, so *every* one of the author's `(section~NN of \code{reproduce\_v138.py})` anchors
  (25 of the 80 hunks) is excluded by construction, not only by the class-C decision.
* `test_the_manuscript_does_not_name_the_old_entry_point` — the substring `reproduce` may
  never appear in `main.tex` ("the word is out of the text of the paper for good"). This
  blocks the author's terminology shift at seven sites (§W3.4).

## W3.2 Disposition of the 80 hunks, by section

Primary disposition per hunk (a partially ported hunk is counted where it landed):

| n | disposition | hunks |
|---|---|---|
| 57 | grammar — frozen by W1 / brief 5–7 (anchors, `\Lean`, `\witness`, `\wtag`, class and citation moves) | incl. h3, h5–h9, h11–h30 (except h16), h32, h34, h36, h37, h40–h42, h47–h57, h59–h72 |
| 5 | census word ban (`reproduce`) | h10, h33, h74, h75, h76 |
| 4 | numeral gate — real change, not ported | h31 (2000), h35 (11.98), h38 (1.07), h43 (T0 rewrite) |
| 4 | figure captions / layout (FIG-001, §5) | h4, h44, h45, h46 |
| 3 | front matter (preamble, title/byline, keywords/legend — W1 + brief 3) | h0, h1, h2 |
| 3 | Code and data / bibliography (§5, Waves 4–6, W2 already landed) | h77, h78, h79 |
| **4** | **partially ported** | h16, h39, h58, h73 |

Per section (hunks → ported blocks):

| hunks | section | ported |
|---|---|---|
| 14 | The physical retroduction | **1** (h58) |
| 13 | The mathematical retroduction | 0 |
| 12 | Physical axioms | **1** (h16) |
| 6 | Conclusions and summary | **1** (h73) |
| 4 | Fourth condition | 0 |
| 3 | (preamble / front matter) | 0 |
| 3 | First condition | 0 |
| 3 | Second condition | 0 |
| 3 | Third condition | 0 |
| 2 | The criteria a single object must meet | 0 |
| 2 | The two-brane model is the golden throat | 0 |
| 2 | Contrast with the data | **1 word** (h39) |
| 2 | The ultraviolet end | 0 |
| 2 | What is not claimed | 0 |
| 2 | Code and data | 0 |
| 1 each | Introduction · Delimitation · This article · The data · Axioms that are mathematical and physical at once · The factor π · The factor φ: the scale | 0 |
| **80** | **total** | **4 blocks, in 4 sections** |

## W3.3 The four ported blocks

1. **Physical retroduction, dictionary paragraph** (h58, two new sentences after
   "gives $S$ at every level."): the cut counted in bonds vs the closed string of the
   throat, and the triad $V$ as the tensor of the throat with the perfect tensors of
   ~\cite{PYHP15}. Dropped from the author's text: the `(section~47 of …)` anchor (banned
   by the numbered-section census) and the trailing `\tier{R}` (left as prose, W1 gloss
   rule). Commit `8504309`.
2. **Physical axioms, after Imported statement `imp:adscft`** (h16): the new
   quantum-error-correction sentence (`\cite{ADH15,PYHP15}`, both keys landed in W2),
   no R mark, no anchor. Resolves W1 bring-up item **R4**; the perfect-tensor half of
   **R13** lands with it (minus its section-47 anchor). Commit `b5d5b01`.
3. **Contrast with the data** (h39): "for *its* next two modes" → "for *the* next two
   modes". Commit `b5d5b01`.
4. **Conclusions, summary table** (h73): the new row *The dictionary and the networks*
   (`\S\ref{ssec:phys}`), no new numeral. Its "rate" clause rides on the pentagon block
   still queued (§W3.6 item 4). Commit `653fc10`.

## W3.4 The numeral gate — every differing numeric token

| site (hunk) | ours | theirs | class | disposition |
|---|---|---|---|---|
| ported block h16 | "one state" | "dimension one" | **simple** — same value, a restatement of claim (a) | ported |
| ported block h58 | $2\pi\golden^{\sigma}$, $\tfrac12$, $1/(4G_N)$ already in the text | identical values | **simple** — no differing token | ported |
| ported block h39 | 1014, 1328, 1664, 1982, 1.4 %, 15, ±30, ±40 | identical | **simple** — no differing token | ported |
| ported block h73 | $\tfrac12$ (existing), "one", $\golden$, $\chi$ | same | **simple** — no differing token | ported |
| Fourth condition (h35) | $11.97$ (`\eqref{eq:sigmaIR}`) | $11.98$ (no eqref) | **simple** — rounding of two scale faces (triage §1); correct figure for this sentence is 11.97 = `log_φ(99.6/0.31384)` | **ours kept**; ask the author (bring-up 1) |
| Mathematical retroduction, T0 (h43) | $1.00000/(\sqrt5 q^2)$ | $0.99990/(\sqrt5 q^2)$ | **simple** — float64 cancellation, documented in `test_sections_39_43.py:169-217` | **ours kept** (triage row 3) |
| The factor π (h31) | "the spacings checked" | "the **2000** spacings checked" | **real** — `reproduce_v138.py` has no 2000-spacings count; DEC-001 D16 removed it earlier | **not ported** → bring-up 3 |
| Fourth condition (h38) | — | "the extremum … lies **1.07** levels down for renormalisation scale $1/\ell$" | **real** — 0 test hits (`1.07` in `tests/` is an unrelated plot radius) | **not ported** → bring-up 5 |
| Physical retroduction, pentagon block (h58) | — | $\chi=2$, $\cosh a=\golden$, $\sinh a=\golden^{1/2}$, $5F_{2n+1}-4$, $5L_{2n+1}$, rate $1/\sqrt5$, signature $(2,4,5)$, $p=2$, $10a\log2/\pi^2=0.745$ | **real** — 0 hits in the suite for `0.745`, `1.061275`, `Lucas`, `Mumford`, `χ=2` (triage §3.5: sequence behind Wave 4) | **not ported** → bring-up 4 (also blocked by the `v34` guard on `pentagon_side_golden`, W1.4) |
| Code and data (h77, h78) | 46 sections, `\code{kkgt}`, 520/516/533/529 tests, `v34`/163/compiled | 47 sections, `\code{reproduce\_v138.py}`, item (47), `v35`/164/not yet compiled, new Mathlib row | **real** — maintenance; the counts move with Waves 4 and 6 | **not ported** → bring-up 6 (and §5 keeps `\code{kkgt}` as primary) |
| 27 class-C hunks | `\tier[\testref{…}]{N}` | `section~NN of …` | **simple** — anchor choice (triage §3 item 6) | **ours kept** (brief 6) |
| Delimitation caption (h4) | ours, FIG-001 de-embed, width 0.85 | shortened caption, width 0.93, prose re-embedded | layout, audited caption numbers $19,61,127$, $987=610+377$ | **ours kept** (§5) |

## W3.5 The census word ban — the author's *reproduce* terminology (new finding)

`tests/test_section_census.py::test_the_manuscript_does_not_name_the_old_entry_point`
asserts `"reproduce" not in main.tex.lower()`, concatenated at run time so no compiled test
carries the word either. The author's v138 shifts exactly this word in at **seven sites /
nine edits**: `re-derived → reproduced` (Physical axioms, L873), `match → reproduce`
(two-brane), `matches → reproduces` (Contrast), `must match → must reproduce` and
`selects to match → selects to reproduce` (dictionary), `derives → reproduces`
(postulates prose), `re-derived → reproduced` ×2 (postulates table), `computed → reproduced`
(Code and data opening). The new *Holographic codes* summary row (h76) is blocked too: its
predicate is "the pentagon code **reproduces** the golden structure".

Two of these were applied and reverted when the census failed the first tanda gate (the
revert is why the gate exists). Porting the author's wording therefore needs a Wave-4
decision on that census rule — `tests/` belongs to the parallel worker, so it was not
touched here. **Not guessed either way: our wording stands.**

## W3.6 Bring-up for the principal author (W3, new items)

Nothing below was decided in his place; items 1–2 are the brief's own, restated with the
measured evidence.

1. **`11.98`.** Not ported. Ours (`$11.97$ (\eqref{eq:sigmaIR})` +
   `\tier[\testref{test_alternatives_for_the_bottom_level}]{N}`) stands: 11.9699 is the
   value of the cited equation, 11.97066 the fit, 11.97 the author's other seven
   occurrences, and ≥6 tests assert it at `abs=5e-3`. If he insists on 11.98: drop the
   `\eqref` (his own edit), reword "the same value", keep the `\testref` only after the
   cited test is re-pointed, and record `log_φ(99.6/(m_p/3)) = 11.9770` in AUD-001.
2. **T0, the "Two fixed weights…" paragraph.** Not ported — the author's rewrite
   (`0.99990`, reproduce-anchors) was left exactly as our audited text carries it
   (`1.00000`, `\testref`s, AUD-001 numbers `0.9757`, `1,2,3,3,5,7,10,16,27,41`, `115`).
   His deletion/rewrite needs his confirmation before any of it moves.
3. **"the 2000 spacings checked"** — no source in `reproduce_v138.py` (grep: only
   `linspace` sizes); DEC-001 D16 already removed this count once. Needs his source.
4. **The pentagon-code block** (perfect tensor, $\cosh a=\golden$, $5F_{2n+1}-4$ /
   $5L_{2n+1}$, rate $1/\sqrt5$, $\chi=2$, the Mumford $(2,4,5)$/$p=2$ sentence with
   `\cite{Mar18}` — W1's **R14**, and the $0.745$ Crofton sentence) — queued behind
   **Wave 4** tests *and* **Wave 6**, because `\Lean{pentagon_side_golden}` does not exist
   in `v34` (W1.4 guard). With it would land the *Holographic codes* row (h76, also
   word-banned) and the row's "rate" clause (item 9).
5. **"the extremum of its regularised vacuum energy lies 1.07 levels down…"** — new
   claim, 0 tests. Wave 4 or his source.
6. **Code and data** — the 47-section enumeration with item (47), the
   `\code{reproduce\_v138.py}`-only narrative (§5 keeps `\code{kkgt}` primary), the
   test-suite paragraph with the 520/516/533/529 counts (to be recounted at merge),
   `v35`/164/the "not yet compiled" line and the new
   `Real.cos_pi_div_five & Real.sin_pi_div_four` Mathlib row: Waves 4 and 6.
7. **The `reproduce` census rule** (§W3.5) — either the rule is relaxed for the verb (a
   Wave-4 `tests/` decision) or the author's terminology stays out of the paper. Seven
   sites are queued behind this call.
8. **QEC sentence (ported):** the rank-1 projector / dimension-one statement is in the
   Wave-4 test list (§4 of this plan); the test should land with section 47's.
9. **Summary row (ported):** its "pentagon code … its rate" clause refers to the queued
   block of item 4; it carries no numeral of its own.
10. **W1 carry-overs still open:** L2 (Euler characteristic, census-pinned id), L5
    ($\Gamma\propto x^{3}$ mark choice), `pentagon_side_golden` (Wave 6).

## W3.7 Gates at the close of every tanda

Baseline before W3: type-check 0 · 533 passed · census 18 · build 63 pages, `^!` 0,
undefined 0 · `\testref{` 99 · `\tier[` 216 · `\wtag{` 12 · `Lean{` 0.

| gate | tanda 1 (`8504309`) | tanda 2 (`b5d5b01`) | tanda 3 (`653fc10`) |
|---|---|---|---|
| `pnpm run type-check` | 0 ✓ | 0 ✓ | 0 ✓ |
| `uv run pytest tests/ -q` | **533 passed** ✓ | 533 ✓ | 533 ✓ |
| census (`test_section_census.py`) | **18** ✓ | 18 ✓ | 18 ✓ |
| `pnpm run build` | exit 0, **63 pages** | 63 ✓ | 63 ✓ |
| `grep -c '^!' build/main.log` | 0 ✓ | 0 ✓ | 0 ✓ |
| `grep -ci undefined build/main.log` | 0 ✓ | 0 ✓ | 0 ✓ |
| `\testref{` occurrences | 99 ✓ | 99 ✓ | 99 ✓ |
| `\tier[` occurrences | 216 ✓ | 216 ✓ | 216 ✓ |
| `grep -c 'Lean{'` | 0 ✓ | 0 ✓ | 0 ✓ |
| `grep -ci reproduce` (census) | 0 ✓ | 0 ✓ | 0 ✓ |
| `grep -cE 'sections?~[0-9]'` (census) | 0 ✓ | 0 ✓ | 0 ✓ |
| tree at commit | only `main.tex` + rendered `build/document-v0.1.0.pdf` + `checksums.txt` (repo convention: content commits carry the render) | same | same |

The first tanda-1 attempt failed the census (`reproduce` in two dictionary edits); those
two edits were reverted before the green run above — recorded here rather than silently
dropped. No push at any point.

## W3.8 Stop point and gaps

* **Stop point: W3 is complete as scoped.** All 80 hunks are dispositioned, the four
  ported blocks are committed, the report is updated, the tree is clean, nothing pushed.
  Content commits: `8504309` → `b5d5b01` → `653fc10` (+ this report) on top of `ea73175`.
* Not ported and why, in one line each: 57 hunks of grammar frozen by W1/brief 5–7;
  5 hunks of the author's *reproduce* wording (census ban, item 7); 4 hunks of real
  numerals (2000, 11.98 kept ours, 1.07, T0 kept ours); 4 caption/layout hunks (FIG-001);
  3 front-matter hunks (date, keywords, legend); Code and data and the bibliography
  block (Waves 4–6, §5, W2).
* **Gaps:** the `reproduce`-terminology decision and the pentagon block are the two
  things this wave could not close without stepping on `tests/` or on Wave 4/6 content;
  the 533/529 counts inside Code and data were not recounted (they are quoted, not
  asserted, and belong to Wave 4); an untracked `fig_tilings_strip.pdf` appeared in the
  repository root during this wave from the parallel worker's figure run — it was **not**
  staged, committed or deleted here.
* An `R`/`L` mark of theirs that our prose already realises (16 of 19 body `R` sites per
  §W1.1, plus the clause "—a reading of the records, not a result about them" that the
  author replaced with `\tier{R}`) stays as our prose: in our grammar the mark *is* those
  words, so the conversion needs no edit.

---

# Wave W4 — applied

| Field | Value |
|---|---|
| **wave** | W4 of §4 — *Code and data, tests, AUD-001 delta* |
| **date** | 2026-11-17 |
| **scope** | `tests/**`, `main.tex`, this report; `scripts/`, `citation.csl.json`, `lean/`, `images/` untouched; `tests/README.md` and the root `README.md` counters only |
| **commits** | one per piece plus this report; **no push** (`1bd9c9f`, `7a0eb17`, then this) |
| **outcome** | piece 1 done end to end; piece 2 **8 of 61** retargets applied and **53** brought up with their reason; piece 3 = no guard relaxed |

## W4.1 Piece 1 — `seccion_47` inside the package

The section moves verbatim from `reproduce_v138.py` (lines 2328–2396) into
`tests/src/kkgt/sections/_rest.py`, so `SECCIONES` is 1..47 and
`python -m kkgt.sections 47` runs the author's own `assert`s. Captured after the
port (`PYTHONPATH=tests/src uv run python -m kkgt.sections 47`, 1.4 s — not
`slow`): the eight lines TST-001 §4 quotes, ending in
`lado del pentágono: … a = 1.061275 …` and `Crofton: 1.0753 … chi que daría S: 1.592`.

| file | change |
|---|---|
| `tests/src/kkgt/sections/_rest.py` | `seccion_47` + its `SECCIONES.append((47, …))`, code unchanged |
| `tests/test_section_runs.py` | docstring 46→47; `MARKERS[47]` = `lado del pentágono: cosh a = phi, sinh a = phi^(1/2), a = 1.061275`; `_params` and `test_all_sections_covered` → `range(1, 48)` |
| `tests/test_section_census.py` | `test_forty_six_sections_in_order` → `test_forty_seven_sections_in_order`, `range(1, 48)` |
| `tests/README.md` | forty-six→forty-seven, the `46`→`47` counts, map row `47`, the "not in `SECCIONES` yet" paragraph replaced |
| `tests/test_sections_47.py` | module docstring only — the five independent tests and their assertions are untouched |
| `main.tex` | the two *"forty-six sections"* phrases → *forty-seven* (L2496, L2507); counters `$549$/$545$` → `$550$/$546$`, recounted by running the commands |
| `README.md` | the same two counters and the same phrase, so no file of the repo still claims 46 or 549 |

`__init__.py` needed no edit: it already sorts the three lots, so 47 falls in place.

## W4.2 Piece 2 — the 61 class-`b` retargets

**Method.** The audited snapshot behind `AUD-001`'s `L###` numbers is commit
`8e101f5`: all 61 figures land on their audited line there and nowhere else in the
last 40 revisions of `main.tex`. The 99 `\testref{…}` anchors are in the same order
in `8e101f5` and at HEAD (same multiset, same sequence), so an anchor of the audit
maps to exactly one line of the current file. Each row's *cited test* (Appendix A,
column 2) was resolved to its anchor, the rows were grouped by anchor, and each
group was substituted only when the group agreed on a single destination.

**Result: 61 rows → 23 anchors → 8 applied, 53 brought up.**

### Applied (4 anchors, 8 rows), each destination executed first

| audited row (current line) | `\testref` before → after | run of the destination | how it affirms the figure |
|---|---|---|---|
| L810 `4.626` (`821`) | `test_reconstruction_is_below_one_part_in_ten_thousand` → `test_koide_scale_and_unit` | `1 passed` | `u * 1e3 == approx(4.6258, abs=5e-5)`; the line prints `M/M_PCF=4.626`, which is that value at three decimals |
| L1119 `1.001` (`1153`) | `test_w2_integer_dimension` → `test_cardy_slope_of_the_count` | `1 passed` | `run.value('… a = ([\d.]+)', want=1.0010, tol=5e-5)` — the line's *slope in S is 1.001* |
| L1577 `±30`, `±40` (`1612`) | `test_the_two_models_differ_by_one_point_four_percent` → `test_error_on_the_ratios` | `3 passed` | the parametrised rows `(1000, 30, …)` and `(1322, 40, …)`: the assertion `round(err,3) == printed` only holds for those two assumed errors, which is what the line says is *assumed in §data* |
| L1788 `7.30`, `224.41`; L1789 `13.33`, `238.80` (`1827`) | `test_cardy_correction_settles` → `test_count_against_the_entropy` | `5 passed` | params `(3, 9, 7.299, 13.329, …)` and `(9, 2889, 224.406, 238.802, …)` at `abs=5e-4` — the four cells of the table at `1822–1823` |

The census pin moved in the same commit: four names out
(`test_reconstruction_…`, `test_w2_integer_dimension`,
`test_the_two_models_differ_…`, `test_cardy_correction_settles` — none of them
cited anywhere else), two in (`test_koide_scale_and_unit`,
`test_count_against_the_entropy`; the other two destinations were already cited),
so `test_testref_set_is_pinned` still asserts exact set equality. The anchor count
stays **99** — retargets replace arguments, they do not add anchors. No number and
no sentence moved.

## W4.3 What the four moves de-cite (read before approving)

Each substituted mark also ended a sentence whose *other* numbers its previous test
does assert. Those numbers now carry no `\testref` at all and fall into AUD-001
class `d` (*asserted by a test, never cited* — §5: "a listing only: no claim of this
class is wrong"), not into class `b`:

| number (current line) | still asserted by | class before → after |
|---|---|---|
| `~10^{-4}` reconstruction (`821`) | `test_reconstruction_is_below_one_part_in_ten_thousand` | a → d |
| W2 slope `0.997` (`1153`) | `test_w2_integer_dimension` | a → d |
| `1.4 %` and *about* `15` GeV (`1612`) | `test_the_two_models_differ_by_one_point_four_percent` | a → d |
| Cardy settling `2.73`, `2.50`, `2.44` (`1827`) | `test_cardy_correction_settles` | a → d |

Eight class-`b` rows became class `a` at the cost of four claims moving to class `d`.
AUD-001 §6 lists three of these four anchors as *false ties* whose full fix is to
split the citations (action 7) — splitting adds anchors and is therefore outside
this wave's gate (99). Recorded here as a bring-up, not hidden.

## W4.4 Bring-ups from W4 (53 rows, three reasons)

**(a) One anchor, several claims, several destinations — 45 rows at 12 anchors.**
A single `\testref{…}` cannot name two tests, and splitting the ties is action 7
of AUD-001 §12 (it changes the anchor count the census pins). Rows listed by the
line of the anchor they all share:

| anchor line | rows (audited) | destinations named for them |
|---|---|---|
| `865` | L818 `0.05`, `11.97`, `±0.05` | `test_bottom_level_is_twelve`, `test_probability_of_a_phi_coincidence` |
| `1331` | L1290 `1.8309`, `2.6551`, `3.4772` | `test_j1_ratios`, `test_ratio_700_over_380_is_the_bessel_ratio` |
| `1511` | L1469 `0.05`, `99.6`, `±0.05`, L1471 `0.6`, L1472 `0.03`, `±0.03`, L1475 `1.4404` | `test_free_phase_fit_is_not_better`, `test_free_scale_versus_the_throat_scale`, `test_probability_of_a_phi_coincidence`, `test_the_compression_limit_is_half_a_cell` |
| `1636` | L1582 `81.74`, L1589 `2.093`, L1590 `2.171`, L1592 `2.241`, L1593 `81.74`, `93.74`, L1610 `81.74`, `93.74` | `test_first_gluon_at_the_background`, `test_section12_runs_all_of_its_checks`, `test_uv_level` |
| `1653` | L1617 `2.45`, L1618 `2.45`, `81.74` | `test_cardy_correction_settles`, `test_first_gluon_at_the_background` |
| `1745` | L1711 `1.49`, `1.6` | `test_layer_growth`, `test_section41_prints_its_conclusions` |
| `2040` | L2005 `2.23`, `2.41`, L2006 `2.10`, `3.32` | `test_crofton_constant`, `test_equivalent_bond_dimensions`, `test_icosaedral_contact_spheres_do_not_touch`, `test_vector_ratio_depends_only_on_the_depth` |
| `2048` | L2012 `3.3×10^{122}`, L2013 `0.04`, `±0.04`, L2014 `380.31` | `test_equivalent_bond_dimensions`, `test_scale_weights`, `test_w4_equals_w8_in_the_gravitational_unit` |
| `2051` | L2015 `203.56`, L2016 `585.3` | `test_cw6_equation_is_w4_plus_log_phi_two`, `test_regge_masses_in_both_units` |
| `2068` | L2026 `0.1809`, `0.2928`, `0.4737`, L2029 `10.5` | `test_lyr_gluon_over_graviton`, `test_required_omega_at_level_584`, `test_required_omega_per_level` |
| `2118` | L2079 `0.707`, L2080 `0.816` | `test_fisher_time_and_binary_entropy`, `test_tcc_bound_is_not_met` |
| `2138` | L2104 `0.92`, `2.8`, `4.2` | `test_cpl_projection`, `test_section38_stdout`, `test_sensitivity_and_arithmetic` |

**(b) The anchor is a figure caption the census requires — 2 rows.**
L647 `±1` (`661`) and L1702 `0.9757` (`1736`) sit on the `\caption{…}` of a figure
and their cited test is `test_section_writes_its_figure[section-44]` /
`[section-39]`; `test_every_figure_caption_cites_the_test_that_writes_it` requires
that string inside the caption, so the substitution would turn a green gate red.
(L647's destination, `test_offset_of_j1_zeros_tends_to_one_quarter`, does not assert
the caption's `x x̄=±1` either; L1702's destination does assert `0.9757` — the split
of this citation is the fix.)

**(c) The destination does not assert the line's figure — 6 rows.** Executed or
read at the definition; what the destination does assert is named so the decision
is reviewable:

| row | figure on the line | destination | what the destination actually asserts |
|---|---|---|---|
| L1006 `4.3` | the subsection number `\S4.3` of the `CW6` citation — a bibliography pointer, not a claim | `test_ring_constant_mode_equals_the_bf_bound_scale` | `m² = −1/(log φ)² = −4.3184` |
| L1064 `±1` | the hyperbola `xy=±1` | `test_offset_of_j1_zeros_tends_to_one_quarter` | the J1-zero offsets `0.2197 … 0.2454` |
| L1068 `±1` | *the norm of a unit is ±1* | idem | idem |
| L1557 `1.9` | *π^5.03 is 1.9 standard deviations from π^5* | `test_trace_three_and_the_shortest_geodesic` | `2 arccosh(3/2) = 4 log φ = 1.924847` — a different quantity that only rounds to `1.9` |
| L1857 `±1` | the icosahedron vertices `(0, ±1, ±φ)` | `test_offset_of_j1_zeros_tends_to_one_quarter` | the J1-zero offsets |
| L2095 `3.5` | *the data exclude λ=0 at about 3.5 standard deviations* | `test_the_measure_that_gives_the_spectrum` | the `e^{4A}`/`e^{6A}` measure rows `1.0, 1.8308, …` |

**Closed by this wave from TST-001 §6:** item 1 (port `seccion_47`) and item 3
(the `533/529` counters outside `tests/`, now `550/546` in `main.tex:2507` and
`README.md:60`, both recounted by running the commands). Still open there: the
`2000 spacings` figure (no source anywhere), the ten §3 rows that need assertions
or external-data marks, class `c`, and the citation pins of the new tests.

## W4.5 Guards — none relaxed

The census guards are untouched and green: `section~N` = 0 occurrences, the word
`repro`+`duce` = 0 occurrences of `main.tex`, and `test_testref_set_is_pinned`
still asserts exact set equality (it moved only because the citations moved). No
tolerance was edited, no test assertion was edited (`test_sections_47.py` lost no
assertion), no figure and no number was rewritten, and `lake` was not run.

## W4.6 Gates at the close of W4

| gate | value |
|---|---|
| `uv run pytest tests/ -q` | **550 passed** (549 before + `section-47`; TST-001 quoted 549/545) |
| `uv run pytest tests/ -q -m 'not slow'` | **546 passed, 4 deselected** |
| `uv run pytest tests/test_section_census.py -q` | **18 passed** |
| `pnpm run type-check` | exit 0, no output |
| `pnpm run build` | exit 0, **63 pages**, `grep -c '^!' build/main.log` 0, `grep -ci undefined` 0 |
| `grep -c 'Lean{' main.tex` | **0** |
| `grep -o '\testref{' \| wc -l` | **99** (four arguments replaced, no anchor added) |
| `grep -c 'forty-six' main.tex` | 0 (both phrases now read *forty-seven*) |

## W4.7 Commits and gaps

* `1bd9c9f` piece 1 (package, registry pins, README map, the two manuscript
  phrases, the counters) · `7a0eb17` piece 2 (four retargets + the pin) · this
  report. **No push.** Content commits carry the render, per repo convention.
* **Gaps:** the `L###` numbers are those of the audited snapshot `8e101f5`, so a
  row was located by figure + cited test + anchor order, not by line arithmetic
  against HEAD; 45 rows need the principal author's decision on splitting the ties
  (AUD-001 action 7) because the wave's gate keeps the anchor count at 99; the four
  moves of §W4.2 de-cite four numbers (§W4.3) and that trade should be confirmed,
  not assumed; `README.md` still points at the pre-package path
  `tests/src/kkgt/sections.py` (stale wording, outside this wave's file list).

# Wave W6 — applied

| Field | Value |
|---|---|
| **wave** | W6 of §4 — *Lean v35* |
| **date** | 2026-11-17 |
| **scope** | `lean/**` (the port + `lakefile.toml`), `main.tex` (file name, theorem count, one dangling id), `package.json`, `README.md`, `build/` + `checksums.txt` (the render), this report; `tests/`, `scripts/`, `citation.csl.json`, `images/` untouched |
| **commits** | one for the port, one for this report; **pushed** |
| **outcome** | `lean/TorreKK_LYR_v35.lean` builds green on `leanprover/lean4:v4.33.1`: **0 errors, 0 file warnings**, 164 theorems, the same 6 axioms, no `sorry`/`admit`/`native_decide` |

## W6.1 What was ported

The file is the author's v35 wholesale, as §4 asks: Spanish docstrings, `etaMetric → eta`
(8 occurrences → 0), `pentagon_side_golden` added (the one decl v34 → v35 adds), the two
snake renames already carried by the prepared copy (`golden_is_algebraic`,
`bin_entropy_half`), and every statement kept — only the norm notation was re-spelled
(`Complex.abs e` → `‖e‖`, equivalent definitionally) and Mathlib lemma names were moved to
the ones our pinned `mathlib v4.33.1` actually exports.

Two of §4's five instructions had to be corrected against the build, both recorded here
rather than silently:

* **`set_option maxRecDepth 100000 in` restored** before `pisano_orders`. §4 says *drop the
  two `set_option`s*; the author dropped it, and `decide` on the four Pisano blocks then
  fails with `maximum recursion depth has been reached` (error 1 of the 54). Restored at
  the same place v34 had it.
* **`set_option linter.style.longLine false` kept** at file scope (repo convention since
  `ecc0a80`); the author's v35 drops it, and the file then emits 17 *line exceeds the 100
  character limit* warnings. Keeping it costs nothing and keeps the file warning-free.

## W6.2 The previous attempt, and how each of its 54 errors was closed

The predecessor's attempt copied the author's file in and stopped at a red build:
**54 error lines over 43 source lines** (`/tmp/lake_w6b.log`). Every one of them sits in a
declaration that also exists in our compiled v34, so each fix is our toolchain's own
working script for that same statement — no statement was weakened, no proof was
replaced by `sorry`-grade material. The full correction list is the diff of the prepared
copy against the committed file; by class:

| error class (before) | n | how it was closed |
|---|---|---|
| `Unknown constant Complex.abs` (+ `Complex.abs_conj`) | 13 | the notation of our Mathlib: `‖·‖`, and `Complex.abs_exp_ofReal_mul_I → Complex.norm_exp_ofReal_mul_I`, `map_mul/map_pow → Complex.norm_mul/norm_pow`, `Complex.abs_exp → Complex.norm_exp`, `Complex.abs_conj → Complex.norm_conj` (7 theorems) |
| `unsolved goals` | 7 | the site's v34 script restored (`golden_irrational`, `ring_resolution_irrational`, `energy_per_bit_constant`, `area_coefficient_every_level`, `two_tile_entropy`, `weld_time_is_conjugate`, `stereo_ratio`) |
| `No goals to be solved` | 7 | the trailing `; ring` / `nlinarith` the author appended where `field_simp` already closes the goal, dropped (`golden_is_algebraic`, `lambda_times_entropy`, `fourier_width_iff`, `no_unit_below_golden` ×2, `S_acts_as_mirror`, `level_growth_not_power`) |
| `Unknown identifier lt_div_iff` | 4 | `lt_div_iff₀` (`no_unit_below_golden` ×2, `window_crosses_half`, `hubble_below_bulk_crossing`) |
| `Unknown identifier div_lt_iff` | 4 | `div_lt_iff₀` (same three theorems) |
| `linarith failed` | 3 | `rcases h with h\|h\|h <;> linarith` (`log_golden_div_pi_irrational`), `field_simp; nlinarith [h2, hsc]` (`clifford_stereographic_torus`), the `calc` + `mul_lt_mul_of_pos_left` of v34 (`capacity_exceeded`) |
| `Unknown constant golden_irrational.int_mul` | 2 | `Irrational.intCast_mul` (`golden_rotation_aperiodic`, `ring_resolution_irrational`) |
| `rewrite failed` | 2 | v34's `rw [pow_succ, pow_succ, mul_assoc, ← sq, h]; ring` (`two_tile_entropy`) and `rw [show (M * b ^ (-σ)) / M = … mul_div_cancel_right₀ …]` (`ring_resolution_is_square`) |
| `Unknown constant Nat.mul_eq_one.mp` | 2 | the `Nat.dvd_one` construction of v34 (`fibonacci_substitution_unique`, both branches) |
| `rcases failed` | 2 | the same two lines (cascade of `Nat.mul_eq_one.mp`) |
| `Invalid field rat_add` / `div_rat` / `div` | 3 | `Irrational.ratCast_add` / `Irrational.div_ratCast` (`golden_irrational`); `(golden_is_algebraic.pow σ).mul (IsAlgebraic.inv (isAlgebraic_natCast n))` (`level_growth_not_power`) |
| `maximum recursion depth` | 1 | `set_option maxRecDepth 100000 in` restored before `pisano_orders` |
| `Application type mismatch` | 1 | `IsAlgebraic.of_pow hp halg` — the author's `Nat.pos_iff_ne_zero.mp hp` proves `p ≠ 0` where `of_pow` wants `0 < p` |
| `Unknown identifier pow_left_injective₀` | 1 | v34's `Real.rpow_left_inj` block (`level_growth_not_power`) |
| `Lean exited with code 1`, `build failed` | 2 | the above |

**After: 0 error lines.** The same build also reported **28 linter warnings** against a
v34 baseline of 0 (`/tmp/lake_snake.log`: `Built TorreKK_LYR_v34 (603s)`, 0 errors, 0
warnings), all of them the author's unverified experiment `field_simp <;> ring` in places
where `field_simp` already closes: 10 → `field_simp` (the linter states `ring` is never
executed), 2 → `field_simp; ring_nf` (v34's line), the `first | (field_simp; done) |
(field_simp; ring)` block → `field_simp`, and `simp at h` → v34's `simp only […]`. Those
fourteen edits are exactly the lines v34 already compiled with. **After: 0 file warnings**
(9 remaining warnings are the pre-existing `has local changes` notices of the nine
`.lake/packages/*` checkouts).

## W6.3 The lakefile trap (the previous attempt's second finding)

The rename `TorreKK_LYR_v34.lean → _v35.lean` (commit `8b0342b`) left `lean/lakefile.toml`
pointing at v34 — `defaultTargets = ["TorreKK_LYR_v34"]` and `[[lean_lib]] name =
"TorreKK_LYR_v34"` — so `lake build` never reached the module and failed with
`TorreKK_LYR_v34: some modules have bad imports` / `unknown target`. Both entries now say
`TorreKK_LYR_v35`, as does `package.json` `verify:lean`, and the gate was run as
`pnpm run verify:lean`.

## W6.4 Name, count and coverage

| item | before | after |
|---|---|---|
| `lean/lakefile.toml` | `TorreKK_LYR_v34` (×2) | `TorreKK_LYR_v35` (×2) |
| `package.json` `verify:lean` | `lake build TorreKK_LYR_v34` | `lake build TorreKK_LYR_v35` |
| `main.tex:2509` | `TorreKK_LYR_v34.lean`, *one hundred and sixty-three* theorems | `TorreKK_LYR_v35.lean`, *one hundred and sixty-four* — counted with `grep -c '^theorem\|^lemma' lean/TorreKK_LYR_v35.lean` = **164** (v34 was 163; v35 adds `pentagon_side_golden`) |
| `README.md:53`, `README.md:70` | v34 name, 163 theorems, v34 command | v35, 164, v35 |
| `main.tex` id coverage | 168 cited ids, **1 dangling** — `\witness{P}{… golden\_isAlgebraic …}` stopped resolving when `fb477a2` renamed the decl | **168 / 168 present** in the file (the only unmatched token is the literal `ids` of the preamble comment at `main.tex:28`, the artefact W1 already recorded); the id now reads `golden\_is\_algebraic` |
| `grep -rn 'TorreKK_LYR_v34'` | 13 hits | 0 outside `docs/reports/` (DEC-001, PRF-001, WIT-003, this plan's own prose — historical) and `tests/REPORT.md` (historical, untouched); `tests/` has no other reference |

## W6.5 Gates at the close of W6

| gate | value |
|---|---|
| `pnpm run verify:lean` (= `cd lean && lake build TorreKK_LYR_v35`) | **exit 0**, `Built TorreKK_LYR_v35 (736 s)`, `Build completed successfully (8707 jobs)`; **0 error lines, 0 warnings from the module** |
| `grep -c '^axiom' lean/TorreKK_LYR_v35.lean` | **6**, the same names as v34 (`bessel_J1_zeros`, `exp_pi_mul_algebraic_transcendental`, `stereographic_meridian_deriv`, `dedekindEta`, `eta_T`, `weyl_equidistribution`) |
| `sorry` / `admit` / `native_decide` | **0** (the only `sorry` in the file is the header's *Sin sorry*), no new axioms |
| `grep -c '^theorem\|^lemma'` | **164** |
| `grep -c etaMetric` (code, `main.tex`, `package.json`, `lakefile`) | **0** — the only remaining occurrences are this plan's own prose at lines 138/146/229/230 |
| `uv run pytest tests/ -q` | **550 passed** |
| `uv run pytest tests/test_section_census.py -q` | **18 passed** |
| `pnpm run type-check` | exit 0, no output |
| `pnpm run build` | exit 0, **63 pages**, `grep -c '^!' build/main.log` **0**, `grep -ci undefined build/main.log` **0** |
| `grep -c 'Lean{' main.tex` | **0** |
| `grep -o -F '\testref{' main.tex \| wc -l` | **99** |
| `\wtag{` / `\tier[` | **12** / **216** (unchanged) |

## W6.6 Commits and gaps

* The port (`lean/`, `lakefile.toml`, `package.json`, `main.tex`, `README.md`, the render
  and `checksums.txt`), then this report. Pushed.
* **Gaps / decisions taken without the principal author:** §4's *drop the two
  `set_option`s* was half-reverted (`maxRecDepth` is required by the build, `longLine`
  by the file-scope convention of `ecc0a80`) — the alternative was a red build and 17
  long-line warnings respectively; the file's docstrings are now Spanish while the rest
  of the repository's prose is English (§4 asks for the Spanish docstrings, so this is
  the plan, not an accident); `main.tex` carries one id fix (`golden\_isAlgebraic` →
  `golden\_is\_algebraic`) beyond the name and count, because the coverage gate would
  otherwise be red through no change of this wave's; `pentagon_side_golden` now exists in
  the file but is still not cited by `main.tex` — that mark lands with Wave 3, as W1
  recorded.
* The build takes **736 s** for the module (`/tmp/lake_w6f.log`), against 603 s for
  v34 and 1128 s for the failing attempt; no other gate is anywhere near that cost.
