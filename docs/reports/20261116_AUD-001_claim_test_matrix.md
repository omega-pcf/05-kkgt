# Claim ↔ test ↔ original-code matrix — the AUD-001 audit of `main.tex`

| Field | Value |
|---|---|
| **id** | `AUD-001` |
| **title** | Claim ↔ test ↔ original-code matrix — audit of every numeric claim in `main.tex` |
| **status** | report only — no source file of the manuscript, the suite or the scripts was modified |
| **date** | 2026-11-16 |
| **version** | 1.0 |
| **repository** | `05-kk-golden-throat` (public as `omega-pcf/05-kkgt`); audit snapshot `8084490`, committed on `main` after `38b33d8` |
| **evidence** | `CLAIMS_FINAL.json` (350 claims), `FINAL_table.json`, `b_categorias_final.json`, `_parsed_matriz.json`, `cite_numbers.json`, `false_tie`/`divergence` artefacts, `run93/out.txt`, `run108/out.txt`, the audit transcripts `deleg_ab8150b0` (analysis) and `deleg_5023ff81` (synthesis), and the re-derivation scripts `_verify_AUD001.py` and `check_report_AUD001.py` |

**Scope.** This report is the *deliverable* of a five-hour read-only audit that
exhausted its budget before emitting anything: every numeric claim of the
manuscript was matched against (i) the test the manuscript cites for it with
`\testref{...}`, (ii) any other test in the suite that asserts the same figure,
and (iii) the author's original reproduction scripts. The analysis had already
been completed on disk; this file consolidates it, adds the three pieces that
were still missing (`sections.py` dependencies, divergence against the
originals, and the citation-verification pass) and re-derives every headline
count from the JSON artefacts before publishing it. Nothing outside this file
was touched.

**Line numbers.** All `L###` references are line numbers of `main.tex` in the
snapshot the audit verified (350 of 350 claims checked against HEAD
`8084490`), and they are the numbers the appendices carry. `main.tex` moved
while the audit ran: `line_map_head38b33d8.json` maps every row to `38b33d8`
(340 of the 350 shifted, by up to 21 lines), and two further commits
(`8aafc43`, `30f54ff` — 3 insertions and 4 deletions in `main.tex`) moved them
again. The anchors quoted by name in this report were re-read against the
current file and now coincide with the audited numbering: `L647` (the figure
caption), `L804` (`67.846`) and `L805` (`M = 313.84`) all sit on those lines
today. A site quoted at a HEAD other than the audited one is said so
explicitly.

---

## 1. Method and corpus

* **Corpus.** 350 distinct numeric claims, from `main.tex` L169 to L2472
  (audited numbering), each recorded as `(line, literal, class, cited tests,
  asserting tests, original-code column)`.
* **The suite.** 243 test functions in nine files plus `conftest.py`, computed
  by the importable package `tests/src/kkgt/` (`sections.py`, `constants.py`,
  `harness.py`); 64 distinct tests are cited from the manuscript.
* **The originals.** `tmp/reproduce_v93.py` (git-ignored, 1525 lines) and the
  v108/v136 copies under the session scratch (`reproduce_v108.py`,
  `reproduce_v136.py`), each executed once to capture stdout —
  `run93/out.txt` (606 lines) and `run108/out.txt` (654 lines).
* **Classes.** `a` = the cited test asserts the figure literally · `a~` = the
  figure is in the cited test's code but not in an assertion · `a?` = only in a
  docstring · `b` = the cited test does not assert the figure · `c` = no test
  anywhere in the suite asserts it · `d` = a test asserts it but no `\testref`
  cites that test (`d~` / `d?` = in test text, unasserted or docstring-only).
* **Re-derivation.** Every count below is produced by
  `_verify_AUD001.py` (scratch), which reads the JSON artefacts and the repo
  directly. Where an earlier transcript figure disagreed with the JSON, the
  JSON wins and the disagreement is stated in §13.

## 2. Coverage

| Class | Rows | Share of 350 | Carries a `\testref` |
|---|---:|---:|---|
| `a` (asserted literally by the cited test) | 103 | 29.4% | yes |
| `a~` (in the cited test's code, not asserted) | 27 | 7.7% | yes |
| `a?` (docstring only) | 7 | 2.0% | yes |
| **a-family total** | **137** | **39.1%** | yes |
| `b` (cited test does not assert the figure) | 95 | 27.1% | yes |
| `c` (no test in the suite) | 24 | 6.9% | no |
| `d` (asserted, not cited) | 87 | 24.9% | no |
| `d~` / `d?` (in test text, unasserted) | 4 / 3 | 1.1% / 0.9% | no |
| **d-family total** | **94** | **26.9%** | no |
| **total** | **350** | 100% | 232 yes / 118 no |

* 232 claims carry at least one citation; the 118 without one are exactly the
  `c` and `d` families (24 + 94). Of the class-`b` rows, 76 cite one test and
  19 cite more than one.
* 64 distinct tests are cited. The most cited are
  `test_vector_ratio_range` (41 claims: 8 `a`, 26 `b`, 6 `a~`, 1 `a?`),
  `test_data_readings` (25: 11 `b`, 10 `a`, 4 `a~`),
  `test_desi_against_planck`, `test_the_planck_level_is_2_2_to_3_1_sigma_from_584`
  and `test_the_worst_case_is_deci` (19 each),
  `test_deep_chain_yields_the_j1_zeros`, `test_error_on_the_ratios`,
  `test_rms_against_the_lyr_table` (17 each),
  `test_alternatives_for_the_bottom_level` (12) and
  `test_cardy_correction_settles` (9).
* **Artefact note.** `FINAL_table.json` holds 363 rows: 13 rows that are not in
  `CLAIMS_FINAL.json` (e.g. L1119 `3.4`, L1456 `1.2`, L1609 `1.2209`,
  L2226 `1.05`) and 42 rows whose label differs (`a*`/`d*` vs `a?`/`d?`).
  `CLAIMS_FINAL.json` (350) is the count of record for this report; every
  count in §2 was read from it.

## 3. Class b — the cited test does not assert the figure (95 rows)

**Subcategories** (`b_categorias_final.json`, 29 + 61 + 5 + 0 = 95):

| Bucket | Rows | Meaning | Action |
|---|---:|---|---|
| `ninguno` | **29** | no test in the whole suite asserts the figure | add an assertion, or withdraw the citation |
| `mover` | **61** | another test *does* assert it; the `\testref` points elsewhere | move/add the `\testref` to that test |
| `codigo` | **5** | the figure appears in a test's code, unasserted | add the `assert` |
| `reclasificar` | 0 | — | — |

The per-row `action` of **Appendix A** carries these same buckets: six rows
(L877 `4.318`, L1617 `2.45`, L1618 `2.45`, L2012 `3.3×10^{122}`, L2080 `0.816`,
L2472 `5×10^{-5}`) had received a different action in the earlier
analysis-pass table, and the final JSON buckets were applied to them, so the
appendix now reproduces 29 / 61 / 5 row for row.

**The worst class: the 29 rows no test asserts.** Nineteen of them carry their
literal inside `sections.py` (in the `P(...)` print labels, where the expected
value is written into the label itself), so an assertion against the section's
stdout can be written for them; the other ten have no literal in `sections.py`
— `2.435×10^{18}` is there in numeric form (`2.435e18`, `sections.py:186` and
`:334`), and `67.846` is *printed* there (`sections.py:244`,
`round(6*sqrt(3)*pi/log(phi), 3)`) but never written as a literal: the string
67.846 survives only in a comment (`constants.py:19`) and in a docstring
(`test_sections_01_08.py:119`).

| # | claim (audited line) | cited test | literal in `sections.py`? |
|---|---|---|---|
| 1 | L647 `61,127` | `test_section_writes_its_figure[section-44]` | no |
| 2 | L804 `67.846` | `test_reconstruction_is_below_one_part_in_ten_thousand` | no |
| 3 | L805 `313.84` | `test_reconstruction_is_below_one_part_in_ten_thousand` | yes |
| 4 | L1454 `3.8317` | `test_second_order_convergence_on_the_golden_grid` | yes |
| 5 | L1454 `3.8319` | `test_second_order_convergence_on_the_golden_grid` | yes |
| 6 | L1464 `313.84` | `test_alternatives_for_the_bottom_level` | yes |
| 7 | L1475 `8.30` | `test_alternatives_for_the_bottom_level` | yes |
| 8 | L1557 `5.03` | `test_a_random_scale_lands_within_point_zero_four_of_an_integer_level` | yes |
| 9 | L1594 `2.295` | `test_vector_ratio_range` | yes |
| 10 | L1601 `2.295` | `test_vector_ratio_range` | yes |
| 11 | L1609 `1.2209×10^{19}` | `test_vector_ratio_range` | no |
| 12 | L1609 `2.435×10^{18}` | `test_vector_ratio_range` | numeric only |
| 13 | L1610 `37.72` | `test_vector_ratio_range` | yes |
| 14 | L1610 `39.33` | `test_vector_ratio_range` | yes |
| 15 | L1610 `90.39` | `test_vector_ratio_range` | yes |
| 16 | L1612 `3.8317` | `test_vector_ratio_range` | yes |
| 17 | L1612 `7.0156` | `test_vector_ratio_range` | yes |
| 18 | L1613 `10.1735` | `test_vector_ratio_range` | yes |
| 19 | L1613 `13.3237` | `test_vector_ratio_range` | yes |
| 20 | L1615 `11.834` | `test_vector_ratio_range` | no |
| 21 | L1617 `11.84` | `test_vector_ratio_range` | yes |
| 22 | L1617 `5.57` | `test_vector_ratio_range` | yes |
| 23 | L1618 `5.57` | `test_vector_ratio_range` | yes |
| 24 | L1788 `46.25` | `test_cardy_correction_settles` | no |
| 25 | L1789 `56.37` | `test_cardy_correction_settles` | no |
| 26 | L2005 `2.42` | `test_pairs_that_give_s_on_average` | no |
| 27 | L2005 `2.75` | `test_pairs_that_give_s_on_average` | no |
| 28 | L2005 `3.40` | `test_pairs_that_give_s_on_average` | no |
| 29 | L2108 `39.33` | `test_depth_of_the_clock`, `test_scales`, `test_vector_ratio_depends_only_on_the_depth` | yes |

Two corrections to the automatic bucket, both verified in this pass:

* **L647 `61,127` is asserted after all**, just not by the cited test: the
  components are the parametrize data of
  `test_the_windows_of_the_panel_cast_their_shadows`
  (`tests/test_sections_44.py:106–113`, `[(3, 19), (5, 61), (7, 127)]`, asserted
  as `got == shadows == 3*side*side - 3*side + 1`). The right action is to
  retarget the citation, not to write an assertion. In the manuscript the
  literal `61,127` occurs once, in the caption at `main.tex:647` (current
  `main`); the same projection series is quoted in
  `docs/reports/20261115_DEC-001_witness_decisions.md` (D29), and no test,
  script or section writes the string.
* **L804 `67.846` is in the tests' text but unasserted**: it appears as a
  docstring of `test_mpcf_framework_unit` (`test_sections_01_08.py:119`) and in
  `constants.py:19–20` as a comment on `M_PCF`; the asserted quantity is the
  full-precision `M_PCF`, not the printed figure.

**The five rows whose figure sits in test code without an assertion:**

| claim | test carrying the figure | action |
|---|---|---|
| L877 `4.318` | `test_ring_constant_mode_equals_the_bf_bound_scale` | add the `assert` |
| L2028 `0.028` | `test_rational_step_versus_the_contrast` (also `test_three_sigma_criterion`) | add the `assert` |
| L2028 `583.789` | idem | add the `assert` |
| L2028 `\pm0.028` | idem | add the `assert` |
| L2472 `5×10^{-5}` | `test_offset_of_j1_zeros_tends_to_one_quarter`, `test_free_phase_fit_is_not_better` | add the `assert` |

**The 61 rows to retarget** each have a concrete target test and assertion
snippet in `b_categorias_final.json`; examples: L810 `4.626` →
`test_koide_scale_and_unit` (`assert u * 1e3 == pytest.approx(4.6259, abs=5e-4)`);
L1290 `2.6551` → `test_j1_ratios`; L1589–L1593 vector-table entries →
`test_section12_runs_all_of_its_checks` / `test_uv_level` /
`test_first_gluon_at_the_background`; L2014 `380.31` →
`test_w4_equals_w8_in_the_gravitational_unit`. The complete table, one row per
claim with the cited test, what that test really asserts, the original-code
column and the action, is **Appendix A**.

## 4. Class c — no test in the whole suite (24 rows)

Thirteen of the 24 are absent from *both* originals' stdout as well (the
`NO` column); eleven are printed by the originals but never asserted by the
suite. Six of them (`L703 0.0036`, `L703 0.3027`, `L703 68.17`,
`L703 \pm0.0036`, `L2460 1.18`, `L2460 3.13`) exist **only in `sections.py`**
under this pass's rule (literal search in the package, plus a rounding-aware
numeric match against both captured stdouts) — if `sections.py` were emptied,
those six would leave the codebase entirely. Action for every row: add an
assertion, or mark the figure in the manuscript as external data with its own
citation.

| claim | cited test | what the cited test actually asserts | original code | action |
|---|---|---|---|---|
| L431 `63.5` | — | — | NO (not in stdout) | add an assertion or mark it as cited external data |
| L432 `53.4` | — | — | NO (not in stdout) | add an assertion or mark it as cited external data |
| L683 `3.6` | — | — | v93/v108 | add an assertion or mark it as cited external data |
| L684 `8.6` | — | — | NO (not in stdout) | add an assertion or mark it as cited external data |
| L703 `0.0036` | — | — | NO (not in stdout) | add an assertion or mark it as cited external data |
| L703 `0.28` | — | — | NO (not in stdout) | add an assertion or mark it as cited external data |
| L703 `0.3027` | — | — | NO (not in stdout) | add an assertion or mark it as cited external data |
| L703 `68.17` | — | — | NO (not in stdout) | add an assertion or mark it as cited external data |
| L703 `\pm0.0036` | — | — | NO (not in stdout) | add an assertion or mark it as cited external data |
| L703 `\pm0.28` | — | — | NO (not in stdout) | add an assertion or mark it as cited external data |
| L704 `0.975` | — | — | NO (not in stdout) | add an assertion or mark it as cited external data |
| L746 `3.8317` | — | — | v93/v108 | add an assertion or mark it as cited external data |
| L746 `7.0156` | — | — | v93/v108 | add an assertion or mark it as cited external data |
| L747 `13.3237` | — | — | v93/v108 | add an assertion or mark it as cited external data |
| L893 `313.84` | — | — | v93/v108 | add an assertion or mark it as cited external data |
| L895 `312.8` | — | — | NO (not in stdout) | add an assertion or mark it as cited external data |
| L1229 `9.41` | — | — | v93/v108 | add an assertion or mark it as cited external data |
| L1319 `6.25` | — | — | v93/v108 | add an assertion or mark it as cited external data |
| L1321 `4.77` | — | — | v93/v108 | add an assertion or mark it as cited external data |
| L1322 `8.83` | — | — | v93/v108 | add an assertion or mark it as cited external data |
| L2239 `3.6` | — | — | v93/v108 | add an assertion or mark it as cited external data |
| L2239 `5.61` | — | — | v93/v108 | add an assertion or mark it as cited external data |
| L2460 `1.18` | — | — | NO (not in stdout) | add an assertion or mark it as cited external data |
| L2460 `3.13` | — | — | NO (not in stdout) | add an assertion or mark it as cited external data |

## 5. Class d — asserted by a test, never cited (94 rows)

**Criterion.** A claim is class `d` when some test in the suite asserts the
figure (literally, `d`; in test text without an assertion, `d~`; in a
docstring, `d?`) while the manuscript's `\testref{...}` at that site either is
absent or names a different test. Class `d` is a *listing only*: no claim of
this class is wrong, and the manuscript's evidence for it is simply not
pointed at the strongest place it could be. The action is uniform — point the
citation at the asserting test — and the census pin that guards `\testref`
names has to move with it, since it asserts exact set equality.

The 94 entries fall into **37 groups — 36 named tests plus one unresolved
group**; the grouped list (target test, then every `(line, literal)` it
asserts) is **Appendix B**. The largest targets are
`test_probability_of_a_phi_coincidence` (15 claims), `test_vector_ratio_range`
(7), `test_gluon_background_level` (6), `test_bottom_level_is_twelve` (5),
`test_the_number_of_pi_cells_is_122` (5) and `test_free_phase_fit_is_not_better`
(4). Three entries (`L747 10.1735`, `L891 67.846`, `L2146 0.31384`) have no
resolving target recorded in the artefact and are marked `?`.

## 6. False ties — one citation standing for a whole table

A *false tie* is a sentence whose single `\testref{...}` is asked to certify
more numbers than its test asserts. The artefact records **10 sentences with
26 unasserted numbers** (`my_false_ties_final.json`):

| site (audited lines) | cited test | numbers in the sentence the test does not assert |
|---|---|---|
| L803–L855 | `test_reconstruction_is_below_one_part_in_ten_thousand` | `67.846`, `313.84`, `4.626` |
| L1205–L1215 | `test_sym_t_eigenvalues_are_the_printed_three` | `0.05`, `0.2` |
| L1453–L1461 | `test_second_order_convergence_on_the_golden_grid` | `3.8319`, `3.8317` |
| L1609–L1619 | `test_vector_ratio_range` | `5.57`, `2.45`, `81.74` |
| L1672–L1697 | `test_section_writes_its_figure[section-13]` | `0.92` |
| L1705–L1720 | `test_section_writes_its_figure[section-41]` | `0.9` |
| L1755–L1794 | `test_cardy_correction_settles` | `7.30`, `46.25`, `224.41`, `13.33`, `56.37`, `238.80` |
| L2005–L2006 | `test_pairs_that_give_s_on_average` | `2.23`, `2.75`, `3.40`, `2.42`, `2.41` |
| L2062–L2101 | `test_distance_to_the_measured_lambda` | `0.202`, `3.5` |
| L2106–L2118 | `test_depth_of_the_clock`, `test_scales`, `test_vector_ratio_depends_only_on_the_depth` | `10500000` |

The four patterns the mission called out are all present in that table or in
the citation counts:

* **`test_vector_ratio_range` cited for the whole mass/vector table
  L1582–L1618** — it is the manuscript's single most cited test (41 claims,
  26 of them class `b`) while it asserts only the band `(2.15, 2.39)` with
  `abs=0.005` and `planck_top = 2.275` with `abs=0.0005`. **Fifteen of the 29
  unasserted rows of §3 are cited to it** — and 30 of the 32 claims in the
  L1594–L1618 block (only L1605 `17.6`/`17.8` cite
  `test_gluon_background_level`).
* **`test_data_readings`** — 25 claims (11 class `b`) cite a test whose body is
  `got == pytest.approx(printed, abs=0.0005)` for a handful of readings; the
  surrounding values (`0.1809`, `0.2928`, `0.4737`, `583.789`, `10.5` …) are
  asserted elsewhere or nowhere.
* **`test_alternatives_for_the_bottom_level`** — 12 claims (9 class `b`) cite a
  test that only checks `got == pytest.approx(printed, abs=0.005)` for the
  alternatives it itself computes.
* **`test_section_writes_its_figure[section-N]`** — a *figure* test
  (`FIGURES[n] in run.figures`), cited at three claim sites (L647 ×2,
  L1702) and carrying two more false ties in captions (`0.92`, `0.9`); it can
  never certify a number.

## 7. Tolerances

* `tests/*.py` carries **116 tolerance literals (`abs=` / `rel=`), 20 distinct
  values**; the package `tests/src/kkgt/` carries **none** (0 occurrences), so
  every tolerance lives in the tests and not in the code under test.
* The distribution: `5e-4` ×27, `1e-12` ×21, `5e-3` ×16, `1e-9` ×8, `5e-5` ×8,
  `1e-6` ×6, `1e-3` ×5, `0.05` ×4, `0.01` ×4, `1e-10` ×4, `1e-4` ×2, `1e-5` ×2,
  `0.02` ×2, and one each of `0.3`, `1e-7`, `2e-3`, `0`, `1`, `1e-15`, `1e-8`.
* Two readings of "the widest tolerance" are both true and must not be
  conflated: **among exponent-form tolerances the widest is `5e-3`** (16 uses —
  the audit transcript's "13 distinct values, largest 5e-3" counts only that
  form), while **the loosest literal overall is `rel=0.3`**
  (`assert a / b == pytest.approx(4.0, rel=0.3)`, second-order convergence) and
  `abs=0.05` (4 uses). The tightest is `1e-15`.
* The family rule (D7: one tolerance helper = the printed precision) is not
  violated, but neither is it fully applicable: most of these literals *are*
  the printed precision of the figure they guard (`abs=0.0005` for a
  four-decimal figure, `abs=5e-4` for a three-decimal one), while the loosest
  (`rel=0.3`, `rel=0.05`) guard a convergence rate or a ratio, not a printed
  number. Which claims are tolerance-guarded rather than string-matched was not
  materialised in any artefact, so §7 cannot say.

## 8. Divergences against the original code

Four independent artefacts, each a different question. `divergences.json` is
**empty (0 rows)** and is a superseded first attempt; the results below are the
later ones.

| Artefact | Rows | Question | Result |
|---|---:|---|---|
| `orig_divergences.json` | 772 (411 unique `(test, value)`) | does a value asserted by the suite appear in the original's stdout? | every row has a near value in the original, but at a different precision/path: gap ≤0.1% for 18 rows, 0.1–0.5% for 210, 0.5–1% for 123, **>1% for 421**, max **2.98%**; >0.5%: 544 |
| `my_value_divergences.json` | 50 | is the manuscript's figure present in either original's stdout at its printed precision? | **39 absent from both** (`a` 32, `a~` 6, `a?` 1); 11 present in v108 only; 0 in v93 only |
| `my_stdout_divergences.json` | 17 | present in the originals but with a different value | relative gap **0.0154% … 1.124%**; by class `c` 9, `b` 2, `d` 2, `a` 1, `a~` 1, `a?` 1, `d?` 1 — e.g. L704 `0.975` vs `0.9757`, L877 `4.318` vs `4.299`, L431 `63.5` vs `64` |
| `strict_div.json` | 8 rows / **5 claims** | no original value lies inside the rounding tolerance of the printed decimals | `L1119 1.001` (nearest 0.9972), `L2016 585.3` (583.877), `L2028 583.789` (583.877), `L2112 1.05×10⁷` (1.048×10⁷), `L2226 1.05×10¹⁸` (1.048×10¹⁸) |

**The `original code` column of the matrix** (`v93/v108` = printed by both
originals, `v108` = only by the later one, `NO` = by neither) distributes as
**280 / 23 / 47** over the 350 rows. This pass re-derived the column
independently, from the captured stdout only, with the claim's own printed
precision as the tolerance: of 347 numeric claims, **319 agree and 28
disagree**; 15 of the 28 are `\pm` rows (an uncertainty bound read as a value),
leaving **13 substantive disagreements**:

| line | claim | column says | v93 | v108 |
|---:|---|---|---|---|
| L684 | `8.6` | `NO` | found | found |
| L700 | `4.2` | `v108` | found | found |
| L704 | `0.975` | `NO` | found | found |
| L877 | `4.318` | `NO` | found | found |
| L1231 | `4.32` | `NO` | found | found |
| L1232 | `4.318` | `NO` | found | found |
| L1582 | `4×10^{-4}` | `NO` | found | found |
| L2005 | `3×10^{-6}` | `NO` | not found | found |
| L2080 | `0.816` | `v93/v108` | not found | not found |
| L2094 | `0.202` | `NO` | found | found |
| L2104 | `4.2` | `v108` | found | found |
| L2375 | `4.2` | `v108` | found | found |
| L2472 | `5×10^{-5}` | `NO` | found | found |

Direction of the residual: **21 claims print only in v108** (14 of them class
`a`, 4 class `b` …), **0 only in v93**, and **21 appear in neither** (by class:
`c` 11, `b` 4, `a~` 4, `a` 1, `d?` 1). The matrix's `NO` cells that this
re-derivation overturns are almost all `\pm` rows and figures that the
original prints with fewer digits than the manuscript quotes.

**Location probes** for five figures the matrix could not place
(transcript of the analysis pass):

| figure | where it actually is |
|---|---|
| `61,127` | `main.tex:647` (current `main`) caption only — and, as separate numbers, the parametrize data of `test_the_windows_of_the_panel_cast_their_shadows` |
| `4.299` | not in `sections.py` nor in any test; printed by both originals (`run93/out.txt:249`, `run108/out.txt:249`, `RS (J1 zeros) x_k/x_1: [1. 1.831 2.655 3.477 4.299 5.119 5.94]`) |
| `2.435×10^{18}` | `sections.py:186` and `:334` as `2.435e18` (reduced Planck mass) |
| `583.09` | `sections.py:2079` — `assert abs(s_inf-583.877)<5e-3 and abs(s_hoy-583.090)<5e-3` |
| `312.8` | nowhere in `sections.py` (0 hits); absent from both originals' stdout |

## 9. The Koide `m_τ` divergence

The manuscript prints the charged-lepton scale `M = 313.84` MeV at **`main.tex`
805, 896 and 1484** on the current `main` — the first site is the audited row
`L805`, which still sits there. Two different tau masses are used to compute
it:

| site | `m_τ` | computed `M` | rounds to |
|---|---:|---:|---:|
| `tests/src/kkgt/sections.py:118` (label printed at `:119`) | 1776.86 | 313.8411 MeV | **313.84** ✓ |
| `scratch/v136/reproduce_v136.py:113` — *identical line* | 1776.86 | 313.8411 MeV | **313.84** ✓ |
| `tmp/reproduce_v93.py:113` — *identical line* | 1776.86 | 313.8411 MeV | **313.84** ✓ |
| `tests/test_sections_17_28.py:270` (`test_koide_scale_and_unit`, also `:283`, `:293`) | **1776.93** | 313.8509 MeV | 313.85 ✗ |

* **The originals and `sections.py` agree** (`m_τ = 1776.86`); the outlier is
  the *test*, which asserts `m * 1e3 == pytest.approx(313.851, abs=5e-4)` and
  `u * 1e3 == pytest.approx(4.6259, abs=5e-4)` with `m_τ = 1776.93`.
* Only `1776.86` reproduces the printed `313.84`: inverting the printed value
  with the same lepton masses gives `m_τ ≈ 1776.85` (computed in this pass),
  consistent with 1776.86 and 0.08 MeV away from 1776.93.
* Both literals are live in every file: `sections.py:1023` and
  `reproduce_v93.py:1069` also use `1776.93` in a later section, and
  `test_sections_09_16.py:405` (`OBS` of
  `test_reconstruction_is_below_one_part_in_ten_thousand`) uses `1776.86`. The
  suite therefore asserts two Koide scales 0.0098 MeV apart — **19.6 × the
  `abs=5e-4` tolerance of `test_koide_scale_and_unit`** — and both tests pass
  only because neither compares its constant against the other's.
* **Action:** pick one `m_τ` (the printed `313.84` requires 1776.86), move it
  to `constants.py`, and have both the section and the test import it.

## 10. Dependencies on `sections.py`

`tests/src/kkgt/sections.py` is the computation the manuscript's stdout comes
from: **2169 lines, 132 737 bytes, 46 `seccion_N` functions** (`seccion_1` …
`seccion_46`) plus a module-level `SECCIONES` registry.

* `tests/conftest.py:37` (`load_sections()` → `from kkgt import sections`),
  `:43` (`list(sections_module.SECCIONES)`) and `:47` (fixture
  `run_section(sections_module, ...)`) are the only entry points; no test
  imports a script.
* **70 of the 243 test functions are `sections.py`-dependent** (they take the
  `run_section` fixture — 65 uses — or the `sections` fixture — 4 uses):

| file | tests | sections-dependent |
|---|---:|---:|
| `test_sections_01_08.py` | 44 | 30 |
| `test_sections_09_16.py` | 29 | 3 |
| `test_sections_17_28.py` | 39 | 3 |
| `test_sections_29_38.py` | 46 | 14 |
| `test_sections_39_43.py` | 38 | 10 |
| `test_sections_44.py` | 12 | 1 |
| `test_sections_45_46.py` | 19 | 2 |
| `test_section_census.py` | 14 | 6 |
| `test_section_runs.py` | 2 | 1 |
| **total** | **243** | **70** |

* **What breaks if `sections.py` is emptied:** the import still succeeds but
  `SECCIONES` disappears, so the `sections_module` fixture raises and every
  dependent test fails at *setup* — 70 tests error rather than fail, including
  `test_forty_six_sections_in_order`, `test_every_section_is_callable` and
  `test_section_writes_its_figure`. The other **173 tests recompute their
  quantity from `constants.py` and keep passing**, which is why the suite would
  not go red in an obvious way.
* **Evidence at risk:** 20 of the 64 cited tests are sections-dependent, so
  **133 of the 232 cited claims lose their cited evidence** (by class: `b` 59,
  `a` 54, `a~` 14, `a?` 6). Counting also the tests that *assert* a claim
  without being cited for it, **228 of the 350 claims, on 119 distinct lines,
  depend on a sections-driven test**.
* Six class-`c` claims (`L703 0.0036 / 0.3027 / 68.17 / \pm0.0036`,
  `L2460 1.18`, `L2460 3.13`) exist **only** in `sections.py` — not in a test,
  not in either original's stdout.

## 11. Citation-only claims and the `donsetch` verification

Thirty-two sentences of the manuscript carry a decimal number and a `\cite`
but **no** `\testref` — the "external data" class. It holds **83 numbers under
36 distinct cite keys**, and **all 36 keys resolve in `src/bibliography.bib`**
(36 of 36). Sixty-nine of the 83 numbers also appear in the claim inventory
(by class: `b` 20, `d` 16, `a` 15, `c` 10, `a~` 5, `d?` 2, `d~` 1); the other
14 (`3.7`, `5.33`, `5.35`, `2.24`, `4.11`, `3.4`, `2.47`, …) are quoted only
from the cited works.

**Verification against the web was started and never concluded.** The
transcript holds **13 `donsetch` calls — 10 searches and 3 fetches — and no
verification summary**; the analysis pass ran out of budget immediately after
them. What the transcript actually establishes:

| check | evidence in the transcript | status |
|---|---|---|
| Le Yaouanc & Richard, *Evidence for Kaluza-Klein excitations of the graviton, gluon and quark at LHC* (key `LYR26`) | `web_fetch arxiv.org/abs/2610.31458` (submitted 22 Oct 2026, revised 27 Oct 2026) + `inspirehep.net/literature/3218179` (title and both authors) | **title/authors/ID confirmed**; the mass values (3600/4000/8600 GeV, 380/700 GeV, 1322/1000 GeV) were only *searched for*, never read in a source |
| Le Yaouanc & Richard, *Influence of the KK graviton decay into hh on the triple Higgs measurement at LHC* (key `LYR26b`, cited outside this class) | `web_fetch arxiv.org/abs/2606.29922` (submitted 29 Jun 2026, revised 28 Sep 2026) | **title/ID confirmed**; numbers not verified |
| Riess 2022 `H0 = 73.04 ± 1.04` | search snippet from `arXiv:2112.04510`: "Our baseline result from the Cepheid-SN sample is H0=73.04+-1.04 km/s/Mpc" | **snippet-level confirmation only** (no fetch) |
| DESI DR2 `Ω_m h² = 0.3027 ± 0.0036`, `H0 = 68.17 ± 0.28`, correlation `−0.975` | three searches returned candidate pages; no page was fetched | **not verified** |
| Akrami–Alestas–Nesseris λ = 0.698 / 0.173 / 0.202 | one search; no fetch | **not verified** |
| the remaining 32 cite keys | no call at all | **not verified** |

So the honest statement for the record is: **the citation-verification pass is
incomplete — no conclusion exists on disk.** Two preprint identities are
confirmed, one constant is confirmed at snippet level, and nothing else in the
36-key set has been checked. This is recorded as a gap (§13), not as a result.

## 12. Action list

1. **Retarget the 61 class-`b` citations** to the test that asserts the figure;
   each row of Appendix A already names the target and its assertion.
2. **Close the 29 rows no test asserts** — 19 of them can be asserted against a
   `sections.py` stdout label today; the other 10 need a decision: compute and
   assert, or mark the manuscript's figure as external data.
3. **L647 `61,127`: retarget, do not add** — the pair is already asserted by
   `test_the_windows_of_the_panel_cast_their_shadows`
   (`tests/test_sections_44.py:106–113`); the citation points at a figure test.
4. **Add the five missing `assert`s** (L877 `4.318`, L2028 `0.028`,
   L2028 `583.789`, L2028 `\pm0.028`, L2472 `5×10^{-5}`) — the values are in
   the tests' code already.
5. **Resolve class `c` (24)**: assertion or external-data marking; the 13 rows
   the matrix marks `NO` are the priority, and the 6 that live only in
   `sections.py` disappear with it.
6. **Publish class `d` (94)**: move each `\testref` to the asserting test
   (Appendix B gives the mapping), updating the census pin in the same pass —
   the two files move together or the suite goes red.
7. **Break the 10 false ties** (26 numbers): split the citations so each number
   names the test that asserts it; `test_vector_ratio_range` carries 41 claims
   while asserting only a band and `2.275`.
8. **Reconcile `m_τ`**: `sections.py:118`, `reproduce_v93.py:113`,
   `reproduce_v136.py:113` and `test_sections_09_16.py:405` use 1776.86 while
   `test_sections_17_28.py:270/283/293` use 1776.93; only 1776.86 prints the
   manuscript's `313.84`. Hoist the constant into `constants.py`.
9. **Re-check the 13 substantive original-code cells** of §8 and the 5
   `strict_div` claims against the originals; the `NO` cells that are really
   "printed with fewer digits" should be corrected in the matrix, not in the
   manuscript.
10. **Finish the citation verification** (§11): none of the 36 cite records has
    been checked against its source — only four keys (`LYR26`, `Rie22`,
    `DESI25`, `AAN25`) were even searched, and the other 32 were never touched.

## 13. Gaps, and where the numbers disagree

* **No verification conclusion for the citations** (§11) — recorded, not
  resolved.
* **`FINAL_table.json` (363) vs `CLAIMS_FINAL.json` (350)** — 13 extra rows and
  42 relabelled rows; this report follows the JSON of record and states so (§2).
* **Class-`b` subcategory counts moved during the audit**: an intermediate run
  reported `21 / 70 / 3 / 1`; the final artefact `b_categorias_final.json`
  reports **29 / 61 / 5 / 0**, which is what this report publishes.
* **The tolerance landscape** is quoted two ways in the sources (20 distinct
  values over all `abs=`/`rel=` literals, 13 over exponent-form literals); both
  are given in §7 with the rule that produced them.
* **The matrix's `NO` column disagrees with a stdout re-derivation on 28 rows**
  (§8); the re-derivation is this pass's, the column is the audit's, and the
  13 substantive disagreements are listed rather than silently resolved.
* **Line numbers** are those of the audited snapshot; the map
  `line_map_head38b33d8.json` carries them through `38b33d8`, and `main.tex`
  has been edited twice since (3 insertions, 4 deletions). A named anchor in
  this report was therefore re-read against the current file — `L647`, `L804`
  and `L805` still sit where the audit put them.
* Class `d`'s three unresolved entries (`L747 10.1735`, `L891 67.846`,
  `L2146 0.31384`) have no target test recorded in the artefact.
* No test-suite run is claimed by this report: the last recorded run in the
  audit transcript is `533 passed` (2026-11-16 18:38).

---

## Appendix A — class b in full (95 rows)

Columns: claim (audited line) · the test the manuscript cites for it · what
that test actually asserts · the original-code column · the action. The
`action` column is the bucket of `b_categorias_final.json`, reconciled row by
row as described in §3; §3 also records the two rows where this pass's check of
the suite qualifies the bucket's action — L647 (`61,127`: the components *are*
asserted by another test, so the practical fix is a retarget) and L804
(`67.846`: the figure survives only in a docstring and a comment).

| claim | cited test | what the cited test actually asserts | original code | action |
|---|---|---|---|---|
| L647 `61,127` | test_section_writes_its_figure[section-44] | FIGURES[n] in run.figures | NO (not in stdout) | no test asserts it → add an assertion or withdraw the citation |
| L647 `\pm1` | test_section_writes_its_figure[section-44] | FIGURES[n] in run.figures | NO (not in stdout) | move/add `\testref{test_offset_of_j1_zeros_tends_to_one_quarter}` (that test asserts it) |
| L804 `67.846` | test_reconstruction_is_below_one_part_in_ten_thousand | rel < 0.0001 | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L805 `313.84` | test_reconstruction_is_below_one_part_in_ten_thousand | rel < 0.0001 | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L810 `4.626` | test_reconstruction_is_below_one_part_in_ten_thousand | rel < 0.0001 | v93/v108 | move/add `\testref{test_koide_scale_and_unit}` (that test asserts it) |
| L818 `0.05` | test_the_compression_limit_is_half_a_cell | PHI ** (-lam) == pytest.approx(0.5, abs=1e-12) ; math.pi * PHI ** (-lam) == pytest.approx(math.pi / 2, abs=1e-12) ; cruce == pytest.approx(0.5, abs=0.001) | v93/v108 | move/add `\testref{test_probability_of_a_phi_coincidence}` (that test asserts it) |
| L818 `11.97` | test_the_compression_limit_is_half_a_cell | PHI ** (-lam) == pytest.approx(0.5, abs=1e-12) ; math.pi * PHI ** (-lam) == pytest.approx(math.pi / 2, abs=1e-12) ; cruce == pytest.approx(0.5, abs=0.001) | v93/v108 | move/add `\testref{test_bottom_level_is_twelve}` (that test asserts it) |
| L818 `\pm0.05` | test_the_compression_limit_is_half_a_cell | PHI ** (-lam) == pytest.approx(0.5, abs=1e-12) ; math.pi * PHI ** (-lam) == pytest.approx(math.pi / 2, abs=1e-12) ; cruce == pytest.approx(0.5, abs=0.001) | v93/v108 | move/add `\testref{test_probability_of_a_phi_coincidence}` (that test asserts it) |
| L877 `4.318` | test_mass_ratios_of_imp_a1 | round(r[n], 2) == printed ; all((abs(x - PHI) > 0.05 for x in r)) | NO (not in stdout) | in the code of test_ring_constant_mode_equals_the_bf_bound_scale but unasserted → add the assert |
| L1006 `4.3` | test_cardy_slope_of_the_count, test_entropy_modes_and_bits | run.value('ln W \+ \(3/2\) ln L0 = a S \+ b: a = ([\d.]+)', {'want': '1.001', 'tol': '0.0005', 'label': "'Cardy slope'"}) | v93/v108 | move/add `\testref{test_ring_constant_mode_equals_the_bf_bound_scale}` (that test asserts it) |
| L1064 `\pm1` | test_weld_time_at_the_bottom | M_PCF * PHI ** (-12) == pytest.approx(0.2107, abs=5e-05) | NO (not in stdout) | move/add `\testref{test_offset_of_j1_zeros_tends_to_one_quarter}` (that test asserts it) |
| L1068 `\pm1` | test_weld_time_at_the_bottom | M_PCF * PHI ** (-12) == pytest.approx(0.2107, abs=5e-05) | NO (not in stdout) | move/add `\testref{test_offset_of_j1_zeros_tends_to_one_quarter}` (that test asserts it) |
| L1119 `1.001` | test_w2_integer_dimension | run.value('fit lnD = a S \+ b ln L \+ c \(sigma=3\.\.9\): a = ([\d.]+)', want=0.9972, tol=0.0005, label='W2 slope') | v93/v108 | move/add `\testref{test_cardy_slope_of_the_count}` (that test asserts it) |
| L1290 `1.8309` | test_deep_chain_yields_the_j1_zeros, test_error_on_the_ratios, test_rms_against_the_lyr_table | got[0] == pytest.approx(1.0, abs=1e-12) ; got[1:] == pytest.approx(want[1:], rel=0.002) ; round(diff, 3) == 0.011 | v93/v108 | move/add `\testref{test_ratio_700_over_380_is_the_bessel_ratio}` (that test asserts it) |
| L1290 `2.6551` | test_deep_chain_yields_the_j1_zeros, test_error_on_the_ratios, test_rms_against_the_lyr_table | got[0] == pytest.approx(1.0, abs=1e-12) ; got[1:] == pytest.approx(want[1:], rel=0.002) ; round(diff, 3) == 0.011 | v93/v108 | move/add `\testref{test_j1_ratios}` (that test asserts it) |
| L1290 `3.4772` | test_deep_chain_yields_the_j1_zeros, test_error_on_the_ratios, test_rms_against_the_lyr_table | got[0] == pytest.approx(1.0, abs=1e-12) ; got[1:] == pytest.approx(want[1:], rel=0.002) ; round(diff, 3) == 0.011 | v93/v108 | move/add `\testref{test_j1_ratios}` (that test asserts it) |
| L1454 `3.8317` | test_second_order_convergence_on_the_golden_grid | errs == pytest.approx([0.00012, 2.9e-05, 7.3e-06, 1.8e-06], rel=0.05) ; a / b == pytest.approx(4.0, rel=0.3) | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1454 `3.8319` | test_second_order_convergence_on_the_golden_grid | errs == pytest.approx([0.00012, 2.9e-05, 7.3e-06, 1.8e-06], rel=0.05) ; a / b == pytest.approx(4.0, rel=0.3) | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1464 `313.84` | test_alternatives_for_the_bottom_level | got == pytest.approx(printed, abs=0.005) | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1469 `0.05` | test_alternatives_for_the_bottom_level | got == pytest.approx(printed, abs=0.005) | v93/v108 | move/add `\testref{test_probability_of_a_phi_coincidence}` (that test asserts it) |
| L1469 `99.6` | test_alternatives_for_the_bottom_level | got == pytest.approx(printed, abs=0.005) | v93/v108 | move/add `\testref{test_free_scale_versus_the_throat_scale}` (that test asserts it) |
| L1469 `\pm0.05` | test_alternatives_for_the_bottom_level | got == pytest.approx(printed, abs=0.005) | v93/v108 | move/add `\testref{test_probability_of_a_phi_coincidence}` (that test asserts it) |
| L1471 `0.6` | test_alternatives_for_the_bottom_level | got == pytest.approx(printed, abs=0.005) | v93/v108 | move/add `\testref{test_free_phase_fit_is_not_better}` (that test asserts it) |
| L1472 `0.03` | test_alternatives_for_the_bottom_level | got == pytest.approx(printed, abs=0.005) | v93/v108 | move/add `\testref{test_probability_of_a_phi_coincidence}` (that test asserts it) |
| L1472 `\pm0.03` | test_alternatives_for_the_bottom_level | got == pytest.approx(printed, abs=0.005) | v93/v108 | move/add `\testref{test_probability_of_a_phi_coincidence}` (that test asserts it) |
| L1475 `1.4404` | test_alternatives_for_the_bottom_level | got == pytest.approx(printed, abs=0.005) | NO (not in stdout) | move/add `\testref{test_the_compression_limit_is_half_a_cell}` (that test asserts it) |
| L1475 `8.30` | test_alternatives_for_the_bottom_level | got == pytest.approx(printed, abs=0.005) | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1557 `1.9` | test_a_random_scale_lands_within_point_zero_four_of_an_integer_level | round(p, 2) == 0.08 | v93/v108 | move/add `\testref{test_trace_three_and_the_shortest_geodesic}` (that test asserts it) |
| L1557 `5.03` | test_a_random_scale_lands_within_point_zero_four_of_an_integer_level | round(p, 2) == 0.08 | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1577 `\pm30` | test_masses_at_the_bottom_of_the_throat, test_predictions_at_sigma_12, test_the_two_models_differ_by_one_point_four_percent | got == [387, 709, 1028, 1346] | NO (not in stdout) | move/add `\testref{test_error_on_the_ratios}` (that test asserts it) |
| L1577 `\pm40` | test_masses_at_the_bottom_of_the_throat, test_predictions_at_sigma_12, test_the_two_models_differ_by_one_point_four_percent | got == [387, 709, 1028, 1346] | NO (not in stdout) | move/add `\testref{test_error_on_the_ratios}` (that test asserts it) |
| L1582 `81.74` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | move/add `\testref{test_first_gluon_at_the_background}` (that test asserts it) |
| L1589 `2.093` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | move/add `\testref{test_section12_runs_all_of_its_checks}` (that test asserts it) |
| L1590 `2.171` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | move/add `\testref{test_section12_runs_all_of_its_checks}` (that test asserts it) |
| L1592 `2.241` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | move/add `\testref{test_section12_runs_all_of_its_checks}` (that test asserts it) |
| L1593 `81.74` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | move/add `\testref{test_first_gluon_at_the_background}` (that test asserts it) |
| L1593 `93.74` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | move/add `\testref{test_uv_level}` (that test asserts it) |
| L1594 `2.295` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1601 `2.295` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1609 `1.2209\times10^{19}` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1609 `2.435\times10^{18}` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | NO (not in stdout) | no test asserts it → add an assertion or withdraw the citation |
| L1610 `37.72` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1610 `39.33` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1610 `81.74` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | move/add `\testref{test_first_gluon_at_the_background}` (that test asserts it) |
| L1610 `90.39` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1610 `93.74` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | move/add `\testref{test_uv_level}` (that test asserts it) |
| L1612 `3.8317` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1612 `7.0156` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1613 `10.1735` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1613 `13.3237` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1615 `11.834` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1617 `11.84` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1617 `2.45` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | move/add `\testref{test_cardy_correction_settles}` (that test asserts it) |
| L1617 `5.57` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1618 `2.45` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | move/add `\testref{test_cardy_correction_settles}` (that test asserts it) |
| L1618 `5.57` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1618 `81.74` | test_vector_ratio_range | (low, high) == pytest.approx((2.15, 2.39), abs=0.005) ; planck_top == pytest.approx(2.275, abs=0.0005) ; low <= symmetric <= high | v93/v108 | move/add `\testref{test_first_gluon_at_the_background}` (that test asserts it) |
| L1702 `0.9757` | test_section_writes_its_figure[section-39] | FIGURES[n] in run.figures | v108 | move/add `\testref{test_unweighted_count_tends_to_a_fixed_fraction}` (that test asserts it) |
| L1711 `1.49` | test_crofton_constant | run.value('Crofton constant ([\d.]+)', {'want': '2.4097', 'tol': '5e-05', 'label': "'Crofton'"}) | v108 | move/add `\testref{test_section41_prints_its_conclusions}` (that test asserts it) |
| L1711 `1.6` | test_crofton_constant | run.value('Crofton constant ([\d.]+)', {'want': '2.4097', 'tol': '5e-05', 'label': "'Crofton'"}) | v93/v108 | move/add `\testref{test_layer_growth}` (that test asserts it) |
| L1788 `224.41` | test_cardy_correction_settles | vals == pytest.approx(printed, abs=0.0005) ; vals[-1] < vals[0] | v93/v108 | move/add `\testref{test_count_against_the_entropy}` (that test asserts it) |
| L1788 `46.25` | test_cardy_correction_settles | vals == pytest.approx(printed, abs=0.0005) ; vals[-1] < vals[0] | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1788 `7.30` | test_cardy_correction_settles | vals == pytest.approx(printed, abs=0.0005) ; vals[-1] < vals[0] | v93/v108 | move/add `\testref{test_count_against_the_entropy}` (that test asserts it) |
| L1789 `13.33` | test_cardy_correction_settles | vals == pytest.approx(printed, abs=0.0005) ; vals[-1] < vals[0] | v93/v108 | move/add `\testref{test_count_against_the_entropy}` (that test asserts it) |
| L1789 `238.80` | test_cardy_correction_settles | vals == pytest.approx(printed, abs=0.0005) ; vals[-1] < vals[0] | v93/v108 | move/add `\testref{test_count_against_the_entropy}` (that test asserts it) |
| L1789 `56.37` | test_cardy_correction_settles | vals == pytest.approx(printed, abs=0.0005) ; vals[-1] < vals[0] | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L1857 `\pm1` | test_icosaedral_contact_spheres_do_not_touch | m == pytest.approx(2.1029, abs=5e-05) ; m >= 2 | NO (not in stdout) | move/add `\testref{test_offset_of_j1_zeros_tends_to_one_quarter}` (that test asserts it) |
| L2005 `2.23` | test_pairs_that_give_s_on_average | run.has('pairs (tiling, chi<=16), p,q<=60: 50340') ; got[s] == pairs | v93/v108 | move/add `\testref{test_vector_ratio_depends_only_on_the_depth}` (that test asserts it) |
| L2005 `2.41` | test_pairs_that_give_s_on_average | run.has('pairs (tiling, chi<=16), p,q<=60: 50340') ; got[s] == pairs | v108 | move/add `\testref{test_crofton_constant}` (that test asserts it) |
| L2005 `2.42` | test_pairs_that_give_s_on_average | run.has('pairs (tiling, chi<=16), p,q<=60: 50340') ; got[s] == pairs | v108 | no test asserts it → add an assertion or withdraw the citation |
| L2005 `2.75` | test_pairs_that_give_s_on_average | run.has('pairs (tiling, chi<=16), p,q<=60: 50340') ; got[s] == pairs | v108 | no test asserts it → add an assertion or withdraw the citation |
| L2005 `3.40` | test_pairs_that_give_s_on_average | run.has('pairs (tiling, chi<=16), p,q<=60: 50340') ; got[s] == pairs | v108 | no test asserts it → add an assertion or withdraw the citation |
| L2006 `2.10` | test_pairs_that_give_s_on_average | run.has('pairs (tiling, chi<=16), p,q<=60: 50340') ; got[s] == pairs | v93/v108 | move/add `\testref{test_icosaedral_contact_spheres_do_not_touch}` (that test asserts it) |
| L2006 `3.32` | test_pairs_that_give_s_on_average | run.has('pairs (tiling, chi<=16), p,q<=60: 50340') ; got[s] == pairs | v108 | move/add `\testref{test_equivalent_bond_dimensions}` (that test asserts it) |
| L2012 `3.3\times10^{122}` | test_data_readings | got == pytest.approx(printed, abs=0.0005) | v93/v108 | move/add `\testref{test_equivalent_bond_dimensions}` (that test asserts it) |
| L2013 `0.04` | test_data_readings | got == pytest.approx(printed, abs=0.0005) | v93/v108 | move/add `\testref{test_scale_weights}` (that test asserts it) |
| L2013 `\pm0.04` | test_data_readings | got == pytest.approx(printed, abs=0.0005) | v93/v108 | move/add `\testref{test_scale_weights}` (that test asserts it) |
| L2014 `380.31` | test_data_readings | got == pytest.approx(printed, abs=0.0005) | v93/v108 | move/add `\testref{test_w4_equals_w8_in_the_gravitational_unit}` (that test asserts it) |
| L2015 `203.56` | test_the_asymptotic_and_today_levels_are_the_printed_two | s_inf == pytest.approx(583.877, abs=0.005) ; s_hoy == pytest.approx(583.09, abs=0.005) ; s_hoy < s_inf | v93/v108 | move/add `\testref{test_regge_masses_in_both_units}` (that test asserts it) |
| L2016 `585.3` | test_the_asymptotic_and_today_levels_are_the_printed_two | s_inf == pytest.approx(583.877, abs=0.005) ; s_hoy == pytest.approx(583.09, abs=0.005) ; s_hoy < s_inf | v93/v108 | move/add `\testref{test_cw6_equation_is_w4_plus_log_phi_two}` (that test asserts it) |
| L2026 `0.1809` | test_data_readings, test_desi_against_planck, test_the_planck_level_is_2_2_to_3_1_sigma_from_584, test_the_worst_case_is_deci | got == pytest.approx(printed, abs=0.0005) | v93/v108 | move/add `\testref{test_required_omega_per_level}` (that test asserts it) |
| L2026 `0.2928` | test_data_readings, test_desi_against_planck, test_the_planck_level_is_2_2_to_3_1_sigma_from_584, test_the_worst_case_is_deci | got == pytest.approx(printed, abs=0.0005) | v93/v108 | move/add `\testref{test_required_omega_at_level_584}` (that test asserts it) |
| L2026 `0.4737` | test_data_readings, test_desi_against_planck, test_the_planck_level_is_2_2_to_3_1_sigma_from_584, test_the_worst_case_is_deci | got == pytest.approx(printed, abs=0.0005) | v93/v108 | move/add `\testref{test_required_omega_per_level}` (that test asserts it) |
| L2028 `0.028` | test_data_readings, test_desi_against_planck, test_the_planck_level_is_2_2_to_3_1_sigma_from_584, test_the_worst_case_is_deci | got == pytest.approx(printed, abs=0.0005) | v93/v108 | in the code of test_rational_step_versus_the_contrast but unasserted → add the assert |
| L2028 `583.789` | test_data_readings, test_desi_against_planck, test_the_planck_level_is_2_2_to_3_1_sigma_from_584, test_the_worst_case_is_deci | got == pytest.approx(printed, abs=0.0005) | v93/v108 | in the code of test_rational_step_versus_the_contrast but unasserted → add the assert |
| L2028 `\pm0.028` | test_data_readings, test_desi_against_planck, test_the_planck_level_is_2_2_to_3_1_sigma_from_584, test_the_worst_case_is_deci | got == pytest.approx(printed, abs=0.0005) | v93/v108 | in the code of test_rational_step_versus_the_contrast but unasserted → add the assert |
| L2029 `10.5` | test_data_readings, test_desi_against_planck, test_the_planck_level_is_2_2_to_3_1_sigma_from_584, test_the_worst_case_is_deci | got == pytest.approx(printed, abs=0.0005) | v93/v108 | move/add `\testref{test_lyr_gluon_over_graviton}` (that test asserts it) |
| L2079 `0.707` | test_canonical_distance_along_the_tower, test_condition_on_the_moduli_kinetic_term | round(got, 1) == printed | v93/v108 | move/add `\testref{test_fisher_time_and_binary_entropy}` (that test asserts it) |
| L2080 `0.816` | test_canonical_distance_along_the_tower, test_condition_on_the_moduli_kinetic_term | round(got, 1) == printed | v93/v108 | move/add `\testref{test_tcc_bound_is_not_met}` (that test asserts it) |
| L2095 `3.5` | test_distance_to_the_measured_lambda | round((self.LAM - c) / up, 2) == 0.05 ; round((math.sqrt(2 / 3) - c) / up, 2) == 0.68 ; round((math.sqrt(2) - c) / up, 2) == 4.14 | v93/v108 | move/add `\testref{test_the_measure_that_gives_the_spectrum}` (that test asserts it) |
| L2104 `0.92` | test_the_number_of_pi_cells_is_122, test_three_h_squared_is_the_entropy_of_the_horizon | abs(r - 122.0) < 0.01 ; PHI ** (-583.79) * PHI ** 583.79 == pytest.approx(1.0, abs=1e-12) | v93/v108 | move/add `\testref{test_cpl_projection}` (that test asserts it) |
| L2104 `2.8` | test_the_number_of_pi_cells_is_122, test_three_h_squared_is_the_entropy_of_the_horizon | abs(r - 122.0) < 0.01 ; PHI ** (-583.79) * PHI ** 583.79 == pytest.approx(1.0, abs=1e-12) | v93/v108 | move/add `\testref{test_section38_stdout}` (that test asserts it) |
| L2104 `4.2` | test_the_number_of_pi_cells_is_122, test_three_h_squared_is_the_entropy_of_the_horizon | abs(r - 122.0) < 0.01 ; PHI ** (-583.79) * PHI ** 583.79 == pytest.approx(1.0, abs=1e-12) | v108 | move/add `\testref{test_sensitivity_and_arithmetic}` (that test asserts it) |
| L2108 `39.33` | test_depth_of_the_clock, test_scales, test_vector_ratio_depends_only_on_the_depth | round(24 * LN_PHI, 2) == 11.55 | v93/v108 | no test asserts it → add an assertion or withdraw the citation |
| L2472 `5\times10^{-5}` | test_bottom_of_the_throat | c == 1005 ; math.floor(math.pi * PHI ** 12) == 1011 | NO (not in stdout) | in the code of test_offset_of_j1_zeros_tends_to_one_quarter and test_free_phase_fit_is_not_better but unasserted → add the assert |

## Appendix B — class d in full (94 entries, grouped by the test that asserts them)

- **test_probability_of_a_phi_coincidence** (15): L169 `0.05`, L169 `\pm0.05`, L174 `0.03`, L174 `\pm0.03`, L335 `0.05`, L335 `\pm0.05`, L2349 `0.05`, L2349 `\pm0.05`, L2393 `0.05`, L2393 `\pm0.05`, L2394 `0.1`, L2412 `0.03`, L2412 `0.05`, L2412 `\pm0.03`, L2412 `\pm0.05`
- **test_vector_ratio_range** (7): L2117 `2.275`, L2118 `2.15`, L2118 `2.39`, L2231 `2.275`, L2307 `2.15`, L2307 `2.275`, L2307 `2.39`
- **test_gluon_background_level** (6): L172 `17.6`, L172 `17.8`, L2232 `17.6`, L2232 `17.8`, L2243 `17.6`, L2243 `17.8`
- **test_bottom_level_is_twelve** (5): L169 `11.97`, L335 `11.97`, L2349 `11.97`, L2393 `11.97`, L2412 `11.97`
- **test_the_number_of_pi_cells_is_122** (5): L174 `583.79`, L2060 `583.79`, L2351 `583.79`, L2413 `583.79`, L2449 `583.79`
- **test_free_phase_fit_is_not_better** (4): L169 `0.6`, L1552 `0.6`, L2393 `0.6`, L2394 `0.6`
- **?** (3): L747 `10.1735`, L891 `67.846`, L2146 `0.31384`
- **test_offset_of_j1_zeros_tends_to_one_quarter** (3): L493 `\pm1`, L684 `4.0`, L2239 `4.0`
- **test_rational_step_versus_the_contrast** (3): L2330 `0.028`, L2330 `583.789`, L2330 `\pm0.028`
- **test_the_measure_that_gives_the_spectrum** (3): L679 `1.831`, L679 `2.655`, L2394 `1.831`
- **test_the_worst_case_is_deci** (3): L175 `7.6`, L2330 `7.6`, L2413 `7.6`
- **test_autodual_width** (2): L1908 `3.1433`, L2332 `0.002`
- **test_entropy_modes_and_bits** (2): L2144 `1011.6`, L2146 `1011.6`
- **test_error_on_the_ratios** (2): L685 `\pm30`, L686 `\pm40`
- **test_observed_ratios** (2): L677 `2.632`, L677 `3.479`
- **test_ratio_700_over_380_is_the_bessel_ratio** (2): L677 `1.842`, L2394 `1.842`
- **test_residual_of_the_j1_fit_is_half_a_percent** (2): L680 `0.54`, L1320 `0.54`
- **test_ring_constant_mode_equals_the_bf_bound_scale** (2): L1231 `4.32`, L1232 `4.318`
- **test_section38_stdout** (2): L700 `2.8`, L2375 `2.8`
- **test_sensitivity_and_arithmetic** (2): L700 `4.2`, L2375 `4.2`
- **test_the_584_point_is_excluded_by_both_datasets** (2): L699 `1.04`, L699 `\pm1.04`
- **test_vector_ratio_depends_only_on_the_depth** (2): L2117 `2.228`, L2307 `2.228`
- **test_alternatives_for_the_bottom_level** (1): L2412 `11.96`
- **test_area_law** (1): L1436 `0.5`
- **test_cpl_projection** (1): L2100 `0.11`
- **test_data_readings** (1): L699 `73.04`
- **test_gluon_scale_needs_three_levels** (1): L2238 `5.39`
- **test_j1_ratios** (1): L679 `3.477`
- **test_koide_scale_and_unit** (1): L893 `4.626`
- **test_observed_ratio_against_the_nearest_phi_power** (1): L1513 `2.1`
- **test_open_legs_of_73** (1): L682 `\pm7`
- **test_regge_masses_in_both_units** (1): L2218 `203.56`
- **test_second_entry_near_the_observer** (1): L2307 `0.02`
- **test_star_discrepancy** (1): L2460 `2.5`
- **test_the_levels_that_break_the_phi_squared_ratio** (1): L685 `\pm20`
- **test_the_window_weight_crosses_half** (1): L2418 `1.5702`
- **test_three_golds_with_ratio_phi_squared** (1): L683 `0.06`

## Appendix C — how the counts were re-derived

```bash
python3 _verify_AUD001.py      # scratch: .../cache/scratch/kkgt_audit
python3 check_report_AUD001.py # the same counts, asserted against this file
```

`_verify_AUD001.py` reads `CLAIMS_FINAL.json`, `FINAL_table.json`,
`b_categorias_final.json`, `_parsed_matriz.json`, `cite_numbers.json`,
`my_false_ties_final.json`, `my_value_divergences.json`,
`my_stdout_divergences.json`, `strict_div.json`, `orig_divergences.json`,
`run93/out.txt`, `run108/out.txt` and the repo, and prints every count quoted
in §2–§10. `check_report_AUD001.py` re-derives 47 of them, asserts that this
file's tables carry the same buckets (95 / 24 / 94 rows) and that the literal
figures quoted in the prose are present; it exits 0 with `MISMATCHES: 0`.
Where a count in an earlier transcript disagreed with the JSON, the JSON value
is the one published here (§13).
