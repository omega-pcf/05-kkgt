# Witness decisions — gates for the principal author

**Applied, pending commit** — the rows marked `[x]` below are already edited
into `main.tex`, `docs/citations.md` and `tests/`: the unified witness form
`\tier[\testref{…}]{N}` → `N[test_name]` (tag first, its reference inside
the brackets; documented in `docs/citations.md` §8), the 16 tag moves of C5,
the lost periods of C1/C2 and of old L997, the T4 testref swap at L1234,
the T1 rewrite of `test_vector_ratio_range`, D20/C15's `11.97`, and C9, C10,
C16. Everything else in this file is still the author's to mark.

**Repository:** `05-kk-golden-throat` · **HEAD:** `d68386f` · **scope of this file:** decisions only.
Nothing in `main.tex`, `citation.csl.json`, `lean/` or `tests/` has been touched; this document is the
only artefact produced by the review.

---

## 0. How to use this file

1. Read §0.1 (executive summary) once — ten lines.
2. Go to **§2**, the per-`\tier{N}` decisions. Every row is one decision, marked
   `[ ]` — put a `✓` in the box you choose and nothing else. Each row is written so that it can be
   resolved in seconds: claim → what the evidence actually says → one recommended option → the exact
   replacement text.
3. §1 (code review) and §3 (prose consistency) are the same format, but they are *not* per-tag; they
   are read once and marked once.
4. After every `✓`, one editing pass applies the marked options. Three mechanical rules govern that pass:
   * every new `\testref{...}` must also be added to the pinned set in
     `tests/test_section_census.py:164` (`test_testref_set_is_pinned` fails otherwise);
   * every new/extended test must pass `uv run pytest` before the tag that cites it is written;
   * a tag always sits **inside** the sentence it marks, before the final punctuation (§3, C5).

**Gate status at the moment of writing**

| Gate | What it asks | State |
|---|---|---|
| **A** — does the evidence say what the claim says? | per tag, against the real test/cite | **74 closed**: **42 ✓**, **12 ✗** (overclaim / wrong witness / wrong class), **19 △** (evidence absent or partial), 1 exempt (legend). Of the 19, **3 are numbers with no provenance in any code** (L1223, L1026, L1135) |
| **B** — which option? | specific test / new test / reformulate / remove | **74 open** — awaiting the author's `✓` |
| **C** — is the prose even? | post-`L`/`R` removal | **21 findings, 0 applied** |

---

### 0.1 Executive summary (10 lines)

| Decision type | Count | Where |
|---|---|---|
| **(i)** cite an existing test — `\testref{...}` | **17** of the 41 untagged, **+4** fixes on already-tagged claims | §2.1, §2.2 |
| **(ii)** write a new test (or extend one) first | **15** of the 41 → **9 new tests** (2 pairs share one test) **+ 1 blocked** | §2.1 |
| **(iii)** reformulate the sentence | **4** | §2.1 |
| **(iv)** drop the tag as redundant/wrong-class | **5** | §2.1 |
| — | — | — |
| **Total `\tier{N}` decisions** | **74** (72 free + 2 fused) | §2 |
| **Prose-consistency findings** | **21** | §3 |
| **Code-review findings** | **18** (5 correctness) | §1 |
| **Effort** | 13 test changes (≈150 lines) · 21 tag insertions · 5 deletions · 4 rewrites · 17 census lines · 10 prose fixes | §4 |
| **Blocked on the author** | 3 numbers with no provenance in any code: `1.07` (L1223), `2000 spacings` (L1026), `11.98` vs `11.97` (L1135) | §1.5, §2.1 |

The single largest class of work is cheap: **17 tags need only the name of a test that already exists**
and is already green. The expensive class is small and explicit: **13 tests**.

---

## 1. Gap analysis and code review — `tmp/reproduce_v93.py` against the suite

### 1.1 Scope and method

* Original: `tmp/reproduce_v93.py` (1524 lines, 39 `seccion_N`, registry `SECCIONES`).
* Current computation: `tests/src/kkgt/sections.py` (1995 lines, **43** `seccion_N`), driven by
  `tests/src/kkgt/harness.py` and `tests/src/kkgt/constants.py`, checked by 451 tests in
  `tests/test_sections_*.py`, `tests/test_section_runs.py`, `tests/test_section_census.py`.
* Method: per-section structural diff, per-section numeric-literal diff (strings stripped separately
  from code), full extraction of `assert` / `isclose` / `allclose` / `atol` / `rtol` on both sides,
  and a reverse check of every number printed by the original against the text of the suite.

Sections **1–38** are line-for-line descendants of the original (same code, English comments);
**12, 29, 37, 39** were restructured and **40–43 are new**.

### 1.2 What the original computes and the suite does **not** verify

Each line is still *printed* by the current code, so the manuscript can quote it — but nothing asserts it.

| # | Original | Current code | Suite | Claim in `main.tex` |
|---|---|---|---|---|
| G1 | `tmp/reproduce_v93.py:195` — Dirichlet lowest `m² = 26.4` | `tests/src/kkgt/sections.py:197` | **none** | L931 (also L917) |
| G2 | `tmp/reproduce_v93.py:74` — one node per level → residual `11–12 %` | `tests/src/kkgt/sections.py:76` | **none** | L958 |
| G3 | `tmp/reproduce_v93.py:250` — relative error of `m₁` at `Q=16,32,64,128` → `1.2e-4 … 1.8e-6` | `tests/src/kkgt/sections.py:252` | **none** | L939, L1115 |
| G4 | `tmp/reproduce_v93.py:152-155` — unfolded spacing variance (`~0.001`) and GUE value `0.178` | `tests/src/kkgt/sections.py:154-155` | **none** | L1022 |
| G5 | `tmp/reproduce_v93.py:101` — error propagation `0.11 … 0.21` | `tests/src/kkgt/sections.py:103` | `test_error_on_the_ratios` ✓ | L953 (not cited there) |
| G6 | `tmp/reproduce_v93.py:60-61` — `min eig sym(T) = +0.35 / −0.06 / −2.8` | `sections.py:62-63` | `test_standard_product_is_not_positive` asserts **signs only** | L864 |
| G7 | `tmp/reproduce_v93.py:118` — scale `99.1`, `σ_IR 11.96 ± 0.03` | `sections.py:120` | `test_alternatives_for_the_bottom_level` ✓ | L1135 quotes `11.98` (a *different* input, see B7) |
| G8 | `tmp/reproduce_v93.py:460` — finite tower `1.8419 / 3.5284` vs infinite | `sections.py` §7 | **none** | (no tag; prose only) |
| G9 | `tmp/reproduce_v93.py:49,81` — LYR `0.06x³`, phase residuals `6.25 / 4.77 / 8.83` for `d=3,5,6` | `sections.py` §1, §5 | only `d=4` is asserted (`test_measured_phase_in_d4_is_a_quarter`) | (no tag; prose only) |

### 1.3 What the suite verifies that the original does not compute

* **Sections 40–43** (`tests/src/kkgt/sections.py:1588, 1737, 1878, 1934`) have no counterpart in
  `tmp/reproduce_v93.py`: the dictionary/Crofton numbers, the five tilings, the two coordinates and
  the three columns were added after the original was frozen.
* **≈40 new `assert`s** the original only printed: `sections.py:768-775` (lattice counts `5,5,9,13,21,37,57`,
  `1005/1011`, `0.9998`), `sections.py:880-896` (cube shadows, ratio table), `sections.py:1278`
  (`1.3 < min(ten) < 1.5`), `sections.py:1476-1485` (W2 dimensions, `a ≈ 0.9972`), `sections.py:1530-1534`
  (ring nesting, `S = π(A/φ²+B/φ³)`), `sections.py:1666-1693`, `sections.py:1716-1728`,
  `sections.py:1826-1980`.
* `tests/test_section_runs.py:19-63` adds a per-section stdout *marker* the original had no equivalent of.
* The **census** (`tests/test_section_census.py`) pins the testref set, the figure→test attribution and
  the absence of the old numbered-section citation. Nothing like it exists in the original.

### 1.4 Derivations from the code

| # | Finding | `archivo:línea` |
|---|---|---|
| D1 | **Assertions lost in the §39 rewrite.** The original verified the `{7,3}` tiling before drawing: `layers[:7]==[1,7,21,56,147,385,1008]`, `porvert==[(3,7),(7,3)]`, `Lq[1:]==[p*F(2k)]`, `Lb/(4G)==S`, tile series `[1,8,15,29,43,85,113]`, `b['z']/a['z']==phi`, `z*tau==1`. The rewritten section 39 keeps only two of them; the rest appear **nowhere** in `tests/`. | orig `1417,1425,1431,1439,1441,1442,1443` → new `sections.py:1515-1582` (only `1530,1534` survive) |
| D2 | **The lost numbers were replaced by a different convention, silently.** `sections.py:1826` counts *tiles whose centre is inside* the disc → `[1,8,8,29,29,57,99]`, not the original's `[1,8,15,29,43,85,113]` (tiles *intersecting*). Neither series is quoted in `main.tex`, so the manuscript is unaffected — but `tests/REPORT.md` and any reader comparing v93 with v108 will see two different numbers for "tiles inside the disc". | `tmp/reproduce_v93.py:1441` vs `sections.py:1826`, `tests/test_sections_39_43.py:205-215` |
| D3 | **Figure names diverged and stale artefacts remain.** `fig_torus_throat.pdf`, `fig_lattice_layers.pdf`, `fig_throat_disks_page.pdf` (orig `769,794,1509`) became `fig_one_structure.pdf` (`sections.py:910`) and `fig_throat_tiling.pdf` (`sections.py:1580`); a fifth figure `fig_tilings_strip.pdf` (`sections.py:1824`) is new. The old files are still lying in `tmp/`. | `tmp/*.pdf`, `constants.py:33-41` |
| D4 | **Original §12/§13 both wrote `fig_mobius_throat.pdf`** (orig `810` and `853`; the docstring of `seccion_13` says the later one replaces the provisional one). The suite fixes this: §12 writes `fig_one_structure.pdf`. **Improvement, not a bug** — but it means running the original does *not* reproduce the current figure set. | orig `810,853` → `sections.py:910,959` |
| D5 | **Two values of the same constant.** `M = 0.31384` (`sections.py:239,330,1090,1110,1441`) vs `M = 0.313851` (`sections.py:1290,1353`; also `test_sections_29_38.py:86,186,197,206`). Both are inherited from the original (`reproduce_v93.py:1170,1231`), so this is pre-existing — but `tests/src/kkgt/constants.py:27` defines `M_KOIDE_MEV = 313.84` precisely to be the single source and **`sections.py` never imports it**. | `constants.py:27` unused by `sections.py` |
| D6 | **Dead constants.** `M_PLANCK_GEV`, `U_MEV`, `EPS0` in `tests/src/kkgt/constants.py` have **0 references** anywhere in `tests/`. | `constants.py:29,28,21` |
| D7 | **Duplicated Planck mass.** `constants.py:30` `1.22089e19` vs `sections.py:1353` `1.2209e19`. Same quantity, two literals, no test compares them. | `constants.py:29` / `sections.py:1353` |
| D8 | **No tolerance policy.** The original relies on `np.allclose` defaults (`rtol=1e-5`, orig `56,57,351,357,666,673`) and on explicit `<1e-12 / 1e-9 / 1e-6·φ^{2s}` asserts (orig `709-724,829,1439,1442,1443`). The suite mixes `pytest.approx(abs=5e-3)` (`test_sections_01_08.py:51`), `abs=5e-4` (`test_sections_29_38.py:91`), `rel=5e-4` above `1e5` (`test_sections_29_38.py:89`), `tol=1e-12` (`harness.SectionRun.value`) and exact integer equality (`test_sections_17_28.py:149`). Nothing documents which number gets which tolerance. | both sides, see §1.5-T5 |
| D9 | **Duplicated `sl`/`sl_r` kernels.** The stiffness/weight eigenproblem is re-implemented in `seccion_1` (orig `31-45`), `seccion_4`, `seccion_5`, `seccion_6` and again as `spec()` in `seccion_37` (orig `1345-1350`); the suite inherits all of them. Five copies of one discretisation, five chances to drift. | orig `31,345,378,405,1345` |
| D10 | **Broken names.** `tmp/reproduce_v93.py` still contains Spanish identifiers (`seccion_*`, `SECCIONES`, `P(...)`, `trap`) and Spanish `print` labels; `tests/src/kkgt/sections.py` keeps the *same* function names (required by `test_section_function_body_has_an_identity`, `test_section_census.py:118`) but translated labels. Any tooling grepping the original's labels against the suite will not match. | both |
| D11 | **The original has no test layer at all** — `assert` statements fire only when the script is run (`if __name__ == "__main__"` at orig `1516`), and `ModuleNotFoundError` is swallowed (orig `1522-1524`): a missing `mpmath` silently skips §2 and the run still "succeeds". The suite cannot skip: `harness.py` fails on a missing pattern. **Improvement.** | orig `1520-1524` |
| D12 | **Section count.** 39 → 43. `tests/test_section_census.py:103` pins `1..43`; the original's registry has 1..39. Nothing maps old section numbers to new ones, so the `REPORT.md` table and any reference to "section N of v93" are ambiguous. | orig `SECCIONES` vs `test_section_census.py:106` |

### 1.5 Top-5 correctness findings

| T | Severity | Finding | Evidence |
|---|---|---|---|
| **T1** | **high** | `test_vector_ratio_range` — the test cited by `main.tex:1262` (and recommended for `main.tex:1280`) **asserts two literals and computes nothing**: `assert 2.15 <= 2.228 <= 2.39; assert 2.15 <= 2.275 <= 2.39`. It can never fail; the claim "the present data do not discriminate" is witnessed by a tautology. | `tests/test_sections_29_38.py:93-96` |
| **T2** | **high** | **`main.tex:1135` contradicts its own equation.** The sentence says "gives the same value, $11.98$ (\eqref{eq:sigmaIR})" while `eq:sigmaIR` (`main.tex:1127`) states `σ_IR = … = 11.97 ± 0.05`. Both numbers are *individually* right for their own denominator (`99.6/0.31384 → 11.97`, `99.6/0.312757 → 11.98`; verified by running §1 and §37), but the cross-reference points at a sentence that says something else, and no test asserts `11.98`. | `main.tex:1127,1135`; `sections.py:240` prints `11.97`, `sections.py:1455` prints `11.98`; `test_sections_01_08.py:106` expects `11.97` |
| **T3** | **high** | **`main.tex:1223` — `1.07 levels down` has no provenance anywhere.** Not in `tmp/reproduce_v93.py` (grep `1.07`, `extremum`, `s^4` → 0 hits), not in `tests/src/kkgt/sections.py`, not in `tests/`. The sentence even states the formula `V(s) ∝ s⁴ Σ j_k⁴ log(s²j_k²)`, which no file implements. | `main.tex:1221-1223`; 0 hits repo-wide |
| **T4** | **high** | **`main.tex:1234` cites the wrong test.** `(\testref{test_ratio_against_the_bessel_ratio})` guards the sentence whose numbers are `1664` and `1982` GeV, but that test only asserts `round(700/380,3)==1.842` and `j₁,₂/j₁,₁==1.831`. The test that actually recomputes `1664/1982` is `test_predictions_at_sigma_12` (`test_sections_17_28.py:143-149`). | `tests/test_sections_17_28.py:137-149` |
| **T5** | **medium** | **Two lost assertions + two tautologies + no tolerance policy.** D1 (7 asserts dropped in the §39 rewrite), T1 (tautology), `test_the_script_asserts_the_window_it_quotes` (`test_sections_29_38.py:67`: `assert 1.3 < 1.43 < 1.5 and 1.7 < 1.81 < 1.9` — literal again, though it *also* runs §29), and D8 (tolerances chosen ad hoc per test with no rule). | see above |

*(Runner-up: `main.tex:1235-1236` uses "the next two modes" twice in one paragraph for two different
pairs — `1664/1982` and `1014/1328` — see §3 C16.)*

---

## 2. Decisions per `\tier{N}`

**Counts:** 74 tags = 72 free `\tier{N}` + 2 fused (`main.tex:750` `WW27`, `main.tex:1759` `BV20`).
Of the 72 free: **30** already carry a `\testref` in their claim sentence, **41** do not, **1** is the
first-page legend (`main.tex:169`), which `docs/citations.md` §8.2 rule 6 exempts.

**Legend of marks:** `[ ]` unmarked → the author marks `✓` (or strikes) · **Gate A** `✓` the evidence
says what the claim says / `✗` overclaim or wrong witness / `△` the number exists nowhere ·
**Gate B** `(i)` specific test · `(ii)` new test · `(iii)` reformulate · `(iv)` drop the tag.

### 2.1 The 41 without a `\testref` — priority pass

---

#### D01 · L338 · the candidates are KK gravitons "by LYR26"
*Claim:* "…$\pm40$ at $1322$. **[N]** These candidates are identified in~\cite{LYR26} as Kaluza–Klein gravitons…"
**Gate A: ✗** — the only witness in the sentence is `\cite{LYR26}`, and `docs/citations.md` §8.2 rule 2
says explicitly: *"An external source is the citation, not a tag."* The tag carries no internal witness.
**Gate B: (iv) drop.**
Action: delete ` \tier{N}` after `1322$`.
`[ ] ✓`

---

#### D02 · L458 · Koide reconstruction to ∼10⁻⁴
*Claim:* "…reconstructs the electron, muon and tau masses to ${\sim}10^{-4}$~\cite{CW6} **[N]**"
**Gate A: ✓** — `test_reconstruction_is_below_one_part_in_ten_thousand`
(`test_sections_09_16.py:382-387`) recomputes the Koide formula and asserts `rel < 1e-4`.
**Gate B: (i).**
Action: insert `(\testref{test\_reconstruction\_is\_below\_one\_part\_in\_ten\_thousand})` immediately
before `\tier{N}`.
`[ ] ✓`

---

#### D03 · L595 · orders modulo 16, 9, 5, 10
*Claim:* (own line) **[N]** "The orders modulo $16$, $9$, $5$ and $10$, and those of $S$ and $ST$, are
computed in Lean \Lean{pisano\_orders, modular\_orders}."
**Gate A: ✗** — class mismatch: the only witness is a Lean name, and `docs/citations.md` §8.3 defines
`N` as *"verified numerically, with the name of the test that checks it"* and `P` as *"proved and
verified by machine (Lean)"*. The tag is also **orphaned on its own line** — a leftover of the
`\tier{N} \tier{L}` pair removed in `d68386f`.
**Gate B: (iii) reformulate.**
Action: delete the lone `\tier{N}` line (line 595) and end the next sentence with
`\Lean{pisano\_orders, modular\_orders} \tier{P}.`
`[ ] ✓`

---

#### D04 · L748 · Poisson summation / heat-kernel weight
*Claim:* "…the heat kernel on the ring whose modes are the left side \Lean{theta\_S\_law} **[N]**."
**Gate A: ✗** — same class mismatch as D03, and `main.tex:1600` already says of the same name
*"The theta series obeys the law under $S$ … by Mathlib \Lean{theta\_S\_law}, with no axiom"* — i.e.
machine-checked → `P`.
**Gate B: (iii) reformulate.**
Action: replace `\tier{N}` with `\tier{P}` (same position, after `\Lean{theta\_S\_law}`).
`[ ] ✓`

---

#### D05 · L864 · the three `sym(T)` eigenvalues
*Claim:* "the smallest eigenvalue of the symmetric part … is $+0.35$ at $a=0.05$, $-0.06$ at $a=0.2$
and $-2.8$ at $a=1$. **[N]**"
**Gate A: ✗ (overclaim)** — the only candidate test, `test_standard_product_is_not_positive`
(`test_sections_01_08.py:204-209`), asserts **signs only** (`vals[0]>0 and vals[1]<0 and vals[2]<0`).
It cannot distinguish `−0.06` from `−6.0`. The magnitudes are printed by `sections.py:62-63` and by
`tmp/reproduce_v93.py:60` but never asserted.
**Gate B: (ii) then (i).**
New test `test_sym_t_eigenvalues_are_the_printed_three` (in `TestSection4MetricPositivity`):
read the three values with `re.findall(r"min eigenvalue of sym\(T\)=([-\d.e+]+)")` and assert
`approx([0.35, -0.06, -2.8], abs=0.01)`.
Action: add the test, then insert `(\testref{test\_sym\_t\_eigenvalues\_are\_the\_printed\_three})`
**inside** the sentence, before the final period (see §3 C5).
`[ ] ✓`

---

#### D06 · L893 · `\witness{P}` followed by `[N]`
*Claim:* "The Kaluza–Klein tower is therefore open. `\witness{P}{bloch\_complexified, …,
ring\_mode\_below\_BF}` **[N]** for the complex spectrum."
**Gate A: ✗** — a `P` witness block and an `N` tag in one sentence; `N` promises "the name of the
test" and there is none.
**Gate B: (iv) drop** (alternative: (iii) → `\tier{P}` if the complex-spectrum clause is meant to be
proved rather than computed).
Action: delete ` \tier{N}` (the `\witness{P}` block already states how the claim was established).
`[ ] ✓` *(author: confirm P vs N for "for the complex spectrum")*

---

#### D07 · L917 · Dirichlet ⇒ no zero mode
*Claim:* "…with Dirichlet conditions … there is no zero mode and no four-dimensional gravity. **[N]**"
**Gate A: △** — nothing in `tests/` mentions Dirichlet; the original computed it
(`tmp/reproduce_v93.py:195`) and the current section still prints it (`sections.py:197`), but no test reads it.
**Gate B: (ii) then (i)** — shared with D08.
New test `test_dirichlet_lowest_eigenvalue_is_positive` (in `TestSection1…`): read
`lowest m^2: Neumann (~0) ; Dirichlet (26.4)` and assert `Dirichlet ≈ 26.4 (abs 0.05)` and `Neumann < 1e-6`.
Action: after the test exists, insert `(\testref{test\_dirichlet\_lowest\_eigenvalue\_is\_positive})`
before `\tier{N}` **and** move the tag inside the sentence (§3 C5).
`[ ] ✓`

---

#### D08 · L931 · the Dirichlet value `26.4`
*Claim:* "…the lowest $m^2$ on $[0,12]$ is $26.4$. **[N]**"
**Gate A: △** — same as D07 (tag currently dangles after the period at the end of a paragraph).
**Gate B: (i)** — reuse D07's test.
Action: rewrite as `…is $26.4$ (\testref{test\_dirichlet\_lowest\_eigenvalue\_is\_positive}) \tier{N}.`
`[ ] ✓`

---

#### D09 · L939 · second-order convergence on the golden grid
*Claim:* "…the second-order convergence of the three-point scheme to its eigenvalues is
classical~\cite{Pry94}; **[N]** for the values on the golden grid."
**Gate A: △** — the original computed the four relative errors
(`tmp/reproduce_v93.py:250`, printed by `sections.py:252`), no test reads them.
**Gate B: (ii) then (i)** — shared with D19.
New test `test_second_order_convergence_on_the_golden_grid`: run §7, parse the four `%.1e` values,
assert they equal `1.2e-4, 2.9e-5, 7.3e-6, 1.8e-6` (abs 1e-9) and that consecutive ratios are ≈4.
Action: then `(\testref{test\_second\_order\_convergence\_on\_the\_golden\_grid}) \tier{N} for the
values on the golden grid.` — keeping the tag **inside** the clause it marks.
`[ ] ✓`

---

#### D10 · L953 · residuals and mass errors
*Claim:* "…the residual is $1.0\%$; $m_2/m_1$ differs from the deep value by $0.011$ ($0.6\%$), ten
times smaller than its error $\pm0.11$ … (the other ratios carry $\pm0.16$ and $\pm0.21$). **[N]**"
**Gate A: △ → ✓ after citation** — `test_rms_against_the_lyr_table[0,6-1.0]` asserts the `1.0 %`
(`test_sections_01_08.py:258-271`) and `test_error_on_the_ratios` asserts the `0.11/0.16/0.21`
propagation (`test_sections_01_08.py:303-308`). The middle quantity, `0.011 (0.6 %)`, is asserted by
neither.
**Gate B: (i)** for the two covered quantities, plus a 1-line extension for `0.011`.
Action: insert `(\testref{test\_rms\_against\_the\_lyr\_table}; \testref{test\_error\_on\_the\_ratios})`
before `\tier{N}`, and add `assert abs(r0[1] - j1[1]/j1[0]) == approx(0.011, abs=1e-3)` to
`test_deep_chain_yields_the_j1_zeros` — **or** drop the `0.011 (0.6 %)` parenthesis.
`[ ] ✓` *(author: keep the `0.011` parenthesis? yes → extend the test / no → delete it)*

---

#### D11 · L958 · one node per level → `11–12 %`
*Claim:* "With one node per golden level the residual is $11$--$12\%$. … The number of nodes is a
resolution, not a physical parameter. **[N]**"
**Gate A: △** — printed by `tmp/reproduce_v93.py:74` and `sections.py:76`, asserted nowhere.
**Gate B: (ii) then (i).**
New test `test_one_node_per_level_degrades_the_residual`: read
`one node per level, sigma[a,6] residual (…)` for `a = 0, -6` and assert both lie in `[11.0, 12.5]`.
Action: then `…not a physical parameter (\testref{test\_one\_node\_per\_level\_degrades\_the\_residual}) \tier{N}.`
`[ ] ✓`

---

#### D12 · L983 · "d = 4 fixed by the arity"
*Claim:* "That $d=4$ fits is standard warped phenomenology. What the framework adds is that $d=4$ is
fixed by the arity, through (F2), rather than assumed. **[N]**"
**Gate A: ✗** — no number, no computation; the only support is the axiom (F2) already named in the
sentence. `N` promises a numerical verification that does not exist.
**Gate B: (iv) drop.**
Action: delete ` \tier{N}`.
`[ ] ✓`

---

#### D13 · L1005 · `\witness{P}` followed by `[N]` (second occurrence)
*Claim:* "…the weight $e^{2A}$ is what brings the phase to $\tfrac14$. `\witness{P}{D\_conjugated\_hop\_is\_one}` **[N]**"
**Gate A: ✗** — identical pattern to D06.
**Gate B: (iv) drop.**
Action: delete ` \tier{N}`.
`[ ] ✓`

---

#### D14 · L1016 · probability `0.08` of a φ-coincidence
*Claim:* "a random ratio in $[1.3,4.5]$ lies within $1\%$ of some $\golden^{k/2}$ with probability
$0.08$ ($2\times10^{5}$ ratios drawn log-uniformly, seed $1$, against $k=1,\dots,8$). **[N]**"
**Gate A: ✓** — `test_probability_of_a_phi_coincidence` (`test_sections_01_08.py:327-333`) rebuilds
exactly that experiment: `default_rng(1)`, `200000` draws, `grid = PHI**(arange(1,9)/2)`.
**Gate B: (i).**
Action: insert `(\testref{test\_probability\_of\_a\_phi\_coincidence})` before `\tier{N}` (and move the
tag inside the sentence — §3 C5).
`[ ] ✓`

---

#### D15 · L1022 · spacing variance `0.001` and the Wigner surmise
*Claim:* "The three spacings of~\eqref{eq:data}, divided by their mean, have variance $0.001$; the
ensemble value is that of the Wigner surmise for $\beta=2$. … whose spacings follow the statistics of
that ensemble~\cite{Mon73,Odl87}. **[N]** The two are degrees of one property."
**Gate A: △** — `sections.py:154-155` prints both numbers (`data unfolded spacing variance (~0)` and
`GUE (beta=2) spacing variance 3pi/8 - 1 (0.178)`); no test reads either. Note also that the tag sits
after a `\cite`, which §8.2 rule 2 forbids.
**Gate B: (ii) then (i).**
New test `test_the_three_spacings_have_the_variance_of_the_ensemble`: recompute the three spacings of
`eq:data`, assert `round(var,3) == 0.001` and `round(3*pi/8-1,3) == 0.178`.
Action: then move the tag **into** the sentence: "…have variance $0.001$
(\testref{test\_the\_three\_spacings\_have\_the\_variance\_of\_the\_ensemble}) \tier{N}; the ensemble
value is that of the Wigner surmise for $\beta=2$…" and delete the tag after `\cite{Mon73,Odl87}`.
`[ ] ✓`

---

#### D16 · L1026 · "the 2000 spacings checked"
*Claim:* "\Lean{bessel\_J1\_zeros} **[N]** for the $2000$ spacings checked."
**Gate A: △ — the number exists nowhere.** Grep for `2000 spacings` / `spacings checked` returns only
`main.tex:1027` and the archived `tmp/kk_golden_throat_v93.tex:943`; neither `reproduce_v93.py` nor
`sections.py` nor `tests/` counts 2000 spacings.
**Gate B: (iii) reformulate** *(preferred)* or (ii).
Action A (reformulate): `\Lean{bessel\_J1\_zeros} \tier{N} for the spacings of $J_1$ checked against
the tower.` — drops the unprovable count.
Action B (test): new `test_two_thousand_spacings_are_computed` asserting
`len(gaps(jn_zeros(1, 2001))) == 2000`.
`[ ] ✓` *(author: does a 2000-spacing run exist outside this repo? if yes → (i)/(ii), if no → (iii))*

---

#### D17 · L1052 · `M φ¹¹ = 62.5 GeV`
*Claim:* "the level $11$ of M-theory, read as a scale, would be $M\golden^{11}=62.5$~GeV, below the
bottom of the throat. **[N]**"
**Gate A: △** — printed by `sections.py:247` (`M phi^11 (GeV), CW6 M-theory level read as a scale`),
asserted nowhere; not present in the original either.
**Gate B: (ii) as a one-line extension, then (i).**
Add the parameter `(11, 62.5)` to `test_scales`
(`tests/test_sections_29_38.py:83-91`, which already covers `12 → 101.06` and `36 → 1.048e7`).
Action: then `…below the bottom of the throat (\testref{test\_scales}) \tier{N}.`
`[ ] ✓`

---

#### D18 · L1093 · Brent bracketing window
*Claim:* "…match the discretised spectra of~\eqref{eq:sl} and~\eqref{eq:vector} at every depth used
below; roots are bracketed on $6000$ points in $x\in[0.5,15]$ and refined by Brent's method. **[N]**"
**Gate A: △** — a method sentence: no test reads `6000`, `[0.5,15]` or Brent
(grep `6000` → 0 hits in `tests/`). `test_discrete_kk_operator_matches_its_closed_form`
(`test_sections_01_08.py:376`) checks the *7-level* operator against its closed form, not the
continuum match at every depth.
**Gate B: (iv) drop** *(recommended — it describes how the roots are found, not a result)*;
alternative (ii) `test_the_vector_ratio_matches_the_continuum_roots` asserting the discretised
`m₂/m₁` equals the root ratio of `J₀/Y₀` to `1e-4` at depths `24` and `81.74`.
Action: delete ` \tier{N}` (the sentence keeps its content).
`[ ] ✓` *(author: is the continuum match load-bearing? yes → (ii) instead)*

---

#### D19 · L1115 · the four grid errors
*Claim:* "…with $16$, $32$, $64$ and $128$ nodes the relative error is $1.2\times10^{-4}$,
$2.9\times10^{-5}$, $7.3\times10^{-6}$ and $1.8\times10^{-6}$, of second order. **[N]**"
**Gate A: △** — same evidence gap as D09 (`sections.py:252`, unasserted).
**Gate B: (ii) then (i)** — reuse D09's test.
Action: `…of second order (\testref{test\_second\_order\_convergence\_on\_the\_golden\_grid}) \tier{N}.`
`[ ] ✓`

---

#### D20 · L1135 · `11.98` against `eq:sigmaIR`
*Claim:* "The placement face of $M$, $m_p/3$, gives the same value, $11.98$ (\eqref{eq:sigmaIR}) **[N]**."
**Gate A: ✗ (two problems)** — (1) `eq:sigmaIR` (`main.tex:1127`) states **11.97**, so "the same
value, 11.98" contradicts the equation it points at (see §1.5-T2); (2) the existing test
`test_alternatives_for_the_bottom_level[m_p/3-11.97]` asserts **11.97** because it uses the *fitted*
scale `99.12`, whereas §37 prints `11.98` from `99.6/0.3128` (`sections.py:1455`). No test asserts `11.98`.
**Gate B: (ii) then (i) + (iii) for the wording.**
New test `test_placement_face_of_the_unit`: `assert round(log(99.6/(0.938272/3))/LN_PHI, 2) == 11.98`.
Rewrite: "The placement face of $M$, $m_p/3$, gives the same value to two digits,
$11.98$ (\eqref{eq:sigmaIR}) (\testref{test\_placement\_face\_of\_the\_unit}) \tier{N}."
`[x]` *(11.97 applied, per the equation at `eq:sigmaIR`; no new test)*

---

#### D21 · L1169 · "for the residues"
*Claim:* "…\Lean{half\_turn\_of\_clock24, not\_half\_turn\_of\_clock20}; **[N]** for the residues."
**Gate A: △** — the Lean names witness the *half-turn* clause; the residues (`φ¹² ≡ 1 mod 16`,
`≡ −1 mod 9`, clock `20 mod 5`, not an involution) have no witness and no test (grep `residue`, `mod 16`
→ 0 hits in `tests/`).
**Gate B: (ii) then (i)** *(preferred, the arithmetic is 4 lines)*; alternative (iv).
New test `test_the_residues_of_phi_to_the_twelve`: assert
`round(PHI**12) % 16 == 1`, `round(PHI**12) % 9 == 8`, and the order of `PHI` mod `5` is `20`.
Action: then `…; \Lean{half\_turn\_of\_clock24, not\_half\_turn\_of\_clock20}; for the residues
(\testref{test\_the\_residues\_of\_phi\_to\_the\_twelve}) \tier{N}.`
`[ ] ✓`

---

#### D22 · L1203 · "transformation laws, checked to 10⁻¹⁶"
*Claim:* "…both are the fixed point of an involution (\S\ref{sec:inputs}). **[N]** for the
transformation laws, checked to $10^{-16}$."
**Gate A: △** — no test mentions `1e-16` or "transformation"; the sentence's own witnesses are two
`\Lean{}` names for a *different* claim.
**Gate B: (iii) reformulate** *(preferred)* or (ii).
Action (iii): drop the uncheckable precision — "…both are the fixed point of an involution
(\S\ref{sec:inputs}); the transformation laws follow from them." and delete ` \tier{N}` **or** keep
`\tier{P}` next to the two Lean names.
Action (ii): if the `10⁻¹⁶` check really runs somewhere, name it: new
`test_the_transformation_laws_hold_to_ten_minus_sixteen`.
`[ ] ✓` *(author: where does the 10⁻¹⁶ check live?)*

---

#### D23 · L1223 · the Coleman–Weinberg extremum `1.07 levels`
*Claim:* "the extremum of its regularised vacuum energy lies $1.07$ levels down for renormalisation
scale $1/\ell$ and moves with that scale; here $V(s)\propto s^4\sum_k j_k^4\log(s^2j_k^2)$ … **[N]**"
**Gate A: △ — the number exists nowhere** (§1.5-T3). Not in `tmp/reproduce_v93.py`, not in
`sections.py`, not in `tests/`; the displayed formula is implemented in no file.
**Gate B: (ii)** — but only after the author supplies the computation — **or (iii)** remove the number.
Proposed test (needs the author's formula first): `test_coleman_weinberg_extremum_is_one_point_zero_seven_levels`
— maximise `V(s)` for `s` near the observed scale with the `k ≤ 60` exact zeros + Hurwitz tail and
assert the extremum is `1.07 ± 0.02` levels below the input.
Action: nothing can be written into `main.tex` until one of the two is chosen.
`[ ] ✓` **BLOCKED** *(author: supply the computation, or delete "lies 1.07 levels down")*

---

#### D24 · L1238 · `1.4 %` and `15 GeV`
*Claim:* "…the golden throat differs from it by $1.4\%$, so those modes separate the two only at a
mass resolution better than about $15$~GeV, against the $\pm30$ and $\pm40$~GeV assumed in
\S\ref{sec:data}. **[N]**"
**Gate A: △** — grep `1.4%` and `15 GeV` → 0 hits in `tests/`. The paragraph's other numbers are
covered (D25/T4), this pair is not. The tag also dangles at the end of the paragraph (§3 C14).
**Gate B: (ii) then (i).**
New test `test_the_two_models_differ_by_one_point_four_percent`:
`golden = [1028, 1346]`, `twobrane = [1014, 1328]`, assert
`round(100*abs(g-t)/g, 1) == 1.4` for both and `0.014*g[0] ≈ 15` (abs 1 GeV).
Action: then `…better than about $15$~GeV (\testref{test\_the\_two\_models\_differ\_by\_one\_point\_four\_percent}) \tier{N}, against…`
`[ ] ✓`

---

#### D25 · L1280 · the gluon ratio `2.275` inside `2.15–2.39`
*Claim:* "Their ratio $5.5615/2.4448=2.275$, which rounds to $5.57/2.45=2.27$, is the depth-$\golden^{81.74}$
entry of the vector table above, and it lies inside the range $2.15$--$2.39$ of the gluon candidates. **[N]**"
**Gate A: ✗ (overclaim)** — the natural witness `test_vector_ratio_range` is a **tautology**
(`test_sections_29_38.py:93-96`, §1.5-T1). The two operands *are* asserted elsewhere
(`test_vector_zeros_against_the_lyr_table`, `test_sections_01_08.py:171-183`), but their quotient and
its membership in the band are not.
**Gate B: (ii) as a rewrite of an existing test, then (i).**
Rewrite `test_vector_ratio_range` to compute:
```python
vec = [2.4448, 5.5615, 8.6958]          # from test_vector_zeros_against_the_lyr_table
ratio = vec[1] / vec[0]
assert ratio == pytest.approx(2.275, abs=5e-4)
assert 2.15 <= ratio <= 2.39
```
**This single fix also repairs the tag at `main.tex:1262` (D35).**
Action: then `…of the gluon candidates (\testref{test\_vector\_ratio\_range}) \tier{N}.`
`[ ] ✓`

---

#### D26 · L1329 (2nd tag) · `0.9757 S`
*Claim:* "the count alone is not $S$ and tends to $\golden^{4}S/(\sqrt5\,\pi)=0.9757\,S$ **[N]**
(Figure~\ref{fig:throattiling})."
**Gate A: ✓** — `test_unweighted_count_tends_to_a_fixed_fraction`
(`tests/test_sections_39_43.py:111-115`) asserts `round(limit,4) == 0.9757`.
**Gate B: (i).**
Action: `…$0.9757\,S$ (\testref{test\_unweighted\_count\_tends\_to\_a\_fixed\_fraction}) \tier{N} (Figure…).`
`[ ] ✓`

---

#### D27 · L1331 (a) · `115` distinct arc weights
*Claim:* "…$1,2,3,3,5,7,10,16,27,41$ distinct ones for $\{7,3\}$ at $\sigma=0,\dots,9$, $115$ in all,
so up to the levels computed no fixed set of weights turns a count of its arcs into $\pi\golden^{\sigma}$
**[N]** (Figure~\ref{fig:tilingstrip})."
**Gate A: ✓** — `test_distinct_arc_weights_of_73` parses the printed list and `115 in total`
(`tests/test_sections_39_43.py:130-133`).
**Gate B: (i).**
Action: `…$115$ in all (\testref{test\_distinct\_arc\_weights\_of\_73}) \tier{N} (Figure…).`
`[ ] ✓`

---

#### D28 · L1331 (d) · the shortest geodesic `4 log φ`
*Claim:* "…its closed geodesic, of length $2\operatorname{arccosh}(3/2)=4\log\golden$, the length of
four levels, is the shortest of the modular surface~\cite{Coh55} **[N]**."
**Gate A: ✓** — `test_trace_three_and_the_shortest_geodesic` exists in the collected suite.
**Gate B: (i).**
Action: `…shortest of the modular surface~\cite{Coh55} (\testref{test\_trace\_three\_and\_the\_shortest\_geodesic}) \tier{N}.`
*(the "shortest" half stays with the citation, the length with the test — consistent with §8.2 rule 2)*
`[ ] ✓`

---

#### D29 · L1336 · the cube-diagonal projections
*Claim:* "…their $8$, $27$, $125$, $343$ and $729$ points project onto $7$, $19$, $61$, $127$ and
$217$ points of the hexagonal lattice, $3L^2-3L+1$ …, the kernel being the diagonal
\Lean{cube\_diagonal\_kernel} **[N]**."
**Gate A: ✓** — `test_cube_diagonal_projection` exists (and `sections.py:880` asserts the identity).
**Gate B: (i).**
Action: `…the kernel being the diagonal \Lean{cube\_diagonal\_kernel} (\testref{test\_cube\_diagonal\_projection}) \tier{N}.`
`[ ] ✓`

---

#### D30 · L1363 · three gap lengths at rotation `1/N`
*Claim:* "The marks of the loops of Figure~\ref{fig:mobius} on the ring of level $\sigma$ are the same
construction at the rotation $1/N=\golden^{-2\sigma}$: at most three gap lengths, filling the ring
evenly **[N]**."
**Gate A: ✓** — `test_three_gaps_of_the_marks` runs exactly that construction (step `PHI**(-2*s)`,
`s = 1..6`, `k = 100,1000,10000`) and `test_discrepancy_stays_below_half_a_percent` covers "evenly".
Both are already in the pinned census.
**Gate B: (i).**
Action: `…filling the ring evenly (\testref{test\_three\_gaps\_of\_the\_marks}) \tier{N}.`
*(one testref, not two: the claim is the gap count; "evenly" is the discrepancy test already cited at L1432)*
`[ ] ✓`

---

#### D31 · L1388 · the ratio list and `0.9998`
*Claim:* "…its ratio to $S$, $1.59,0.98,1.09,0.98,0.98,1.06,1.01$ here, is $0.9998$ at $\sigma=22$ **[N]**."
**Gate A: ✓** — `test_ratio_at_sigma_22_is_unity_to_four_decimals`
(`tests/test_sections_09_16.py:228`) asserts the `0.9998`; the seven-value list is asserted inside the
section itself (`sections.py:771`) and reached by `test_section12_runs_all_of_its_checks`.
**Gate B: (i).**
Action: `…is $0.9998$ at $\sigma=22$ (\testref{test\_ratio\_at\_sigma\_22\_is\_unity\_to\_four\_decimals}) \tier{N}.`
`[ ] ✓`

---

#### D32 · L1456 · the Cardy correction `2.73, 2.50, 2.44`
*Claim:* "…$S-\log W-\tfrac32\log L_0$ settling to a constant ($2.73$, $2.50$, $2.44$), the
logarithmic correction $(c+3)/4$ of Cardy's formula at $c=3$ **[N]**."
**Gate A: ✓** — `test_cardy_correction_settles` (`test_sections_09_16.py:354-364`) recomputes all
seven values and asserts them (`2.7337, …, 2.5004, …, 2.4437` at `σ = 3,6,9`).
**Gate B: (i).**
Action: `…at $c=3$ (\testref{test\_cardy\_correction\_settles}) \tier{N}.`
`[ ] ✓`

---

#### D33 · L1489 · the worst gap ratios for `√2`, `e`, `π`
*Claim:* "…for $\golden$ their ratio is at most $\golden^{2}=2.618$, reached for every $N$ up to
$5000$ except when $N+1$ … is a Fibonacci number …, in the ratio $\golden$, against $3.414$ for
$\sqrt2$, $9.52$ for $e$ and $293.6$ for $\pi$ **[N]** (Figure~\ref{fig:granularity}, centre)."
**Gate A: ✗ (partial overclaim)** — `test_worst_gap_ratio_over_the_first_5000_levels`
(`test_sections_09_16.py:89-101`) asserts **only** `φ → 2.618` (plus an unrelated phase step). The
three comparison values `3.414 / 9.52 / 293.6` are asserted nowhere.
**Gate B: (ii) as a three-line extension, then (i).**
Add to the same test:
```python
for step, want in ((math.sqrt(2), 3.414), (math.e, 9.52), (math.pi, 293.6)):
    worst = max((lambda g: g.max()/g.min())(self._gaps(np.arange(1, N+1)*step)) for N in range(10, 5001))
    assert round(worst, 1) == want, (step, worst)
```
Action: then `…for $\pi$ (\testref{test\_worst\_gap\_ratio\_over\_the\_first\_5000\_levels}) \tier{N} (Figure…).`
`[ ] ✓`

---

#### D34 · L1547 · the threshold window `0.301 … 0.632`
*Claim:* "…the first integer level that passes the threshold $\tfrac12$ of W1 is $n=2$, for every
threshold between $0.301$ and $0.632$ **[N]**."
**Gate A: ✓** — `test_first_active_level_is_two` (`test_sections_17_28.py:348-355`) asserts both
thresholds `(0.301, 0.632)` *and* `active[0] == 2`.
**Gate B: (i).**
Action: `…between $0.301$ and $0.632$ (\testref{test\_first\_active\_level\_is\_two}) \tier{N}.`
`[ ] ✓`

---

#### D35 · L1585 · the moduli slope `1/√2`
*Claim:* "$|\partial_\Phi V|/V=\log\golden/(\sqrt2\log\golden)=1/\sqrt2$ \Lean{moduli\_slope} **[N]**, under the stated assumptions…"
**Gate A: △ → ✓ with a testref** — a Lean name under an `N` tag is the class mismatch of D03/D04,
but a numerical test exists: `test_canonical_slope` (`test_sections_29_38.py:103-106`) asserts
`LN_PHI / d ≈ 0.7071`.
**Gate B: (i)** *(keeps `N` consistent with §8.3)*; alternative (iii) → `\tier{P}`.
Action: `…=1/\sqrt2$ \Lean{moduli\_slope} (\testref{test\_canonical\_slope}) \tier{N}, under…`
`[ ] ✓` *(author: `N`+testref, or `P`+Lean?)*

---

#### D36 · L1591 · `log_φ(M_Pl/M) = 93.737`
*Claim:* "…is one number, $\log_\golden(M_{\mathrm{Pl}}/M)=93.737$ **[N]**, and its equality with the
position of the top is the definition of \S\ref{sec:prediction}…"
**Gate A: ✓** — `test_uv_level` (`test_sections_17_28.py:274-279`) recomputes it from
`ħ, c, G, M` and asserts `≈ 93.737` (abs 5e-4); `test_section_runs.py:45` pins the same line for §24.
**Gate B: (i).**
Action: `…=93.737$ (\testref{test\_uv\_level}) \tier{N}, and…`
`[ ] ✓`

---

#### D37 · L1674 · `σ_obs = 583.88 ± 0.04` and `583.40`
*Claim:* "…$S_{\mathrm{obs}}=3\pi/(\Lambda_{\mathrm{obs}}\ell_P^2)=3.3\times10^{122}$ and the Planck
values of \S\ref{sec:data}, $\sigma_{\mathrm{obs}}=583.88\pm0.04$, and $583.40$ with the local $H_0$ **[N]**."
**Gate A: △ → ✓ for the two values, ✗ for the error bar.** `test_data_readings`
(`test_sections_17_28.py:196-201`) asserts `583.877` and `583.402` — the values — but nothing asserts
`± 0.04` (the Monte-Carlo propagation printed by `sections.py:1061`); `test_monte_carlo_error`
covers §17's `380.315 ± 0.04`, a different quantity.
**Gate B: (i) + a one-line test for the error bar.**
Action: `…and $583.40$ with the local $H_0$ (\testref{test\_data\_readings}) \tier{N}.`
Optional new test `test_observer_level_error_is_point_zero_four`: read
`observer level (…): sigma = … +- …` from §18 and assert `0.03 <= sd <= 0.05`, then cite it too.
`[ ] ✓` *(author: witness the ±0.04, or drop it from the sentence?)*

---

#### D38 · L1715 · `S·T_GH ∝ φ^{3σ/2}`
*Claim:* "$S\tau_F$ is constant, while the entropy times the inverse Gibbons–Hawking temperature
grows as $\golden^{3\sigma/2}$ **[N]**, so it does not by itself fix the level."
**Gate A: △** — grep `Gibbons` in `tests/` returns only `test_sections_29_38.py:265` (the `πφ¹²`
identity), not this growth law. The claim is a two-line consequence of `S ∝ φ^σ` and `T_GH ∝ φ^{-σ/2}`.
**Gate B: (ii)** *(two lines, cheapest honest fix)*; alternative (iii) — write the two exponents in the
sentence and drop the tag.
Proposed test `test_entropy_over_the_gh_temperature_grows_as_phi_to_the_three_sigma_over_two`:
`for s in (0, 12, 24): assert ratio(s+1)/ratio(s) == approx(PHI**1.5, rel=1e-12)` where
`ratio(s) = (math.pi*PHI**s) / (PHI**(-s/2))`.
Action: then `…grows as $\golden^{3\sigma/2}$ (\testref{test\_entropy\_over\_the\_gh\_temperature\_grows\_as\_phi\_to\_the\_three\_sigma\_over\_two}) \tier{N}, so…`
`[ ] ✓`

---

#### D39 · L1746 · `397` Planck units at the observer
*Claim:* "…the canonical distance $\sqrt2\,\sigma\log\golden$ grows without bound along the tower,
$397$ Planck units at the observer **[N]**."
**Gate A: ✓** — `test_canonical_distance_along_the_tower[584-397.4]`
(`test_sections_29_38.py:121-124`) recomputes `√2·584·ln φ = 397.4`.
**Gate B: (i).**
Action: `…$397$ Planck units at the observer (\testref{test\_canonical\_distance\_along\_the\_tower}) \tier{N}.`
`[ ] ✓`

---

#### D40 · L1882 · `3149` modes below 1000 TeV
*Claim:* "…: $3149$ below $1000$~TeV, with no Hagedorn growth **[N]**."
**Gate A: ✓** — `test_graviton_modes_below_1000_tev` (`test_sections_29_38.py:196-203`) counts
`jn_zeros(1,5000)·M·φ¹² < 1e6` and asserts `count == 3149` and the linear estimate `3149.7`.
**Gate B: (i).**
Action: `…with no Hagedorn growth (\testref{test\_graviton\_modes\_below\_1000\_tev}) \tier{N}.`
`[ ] ✓`

---

#### D41 · L1886 · the Regge masses in both units
*Claim:* "…its first state lies at $5.6\times10^{-4}$~GeV, below the first graviton mode, and in the
gravitational unit at $1.05\times10^{18}$~GeV, far above it **[N]**."
**Gate A: ✓** — `test_regge_masses_in_both_units` (`test_sections_29_38.py:185-194`) asserts
`5.616e-4` and `1.048e18` (rel 1e-3) and the `203.56`-level conversion.
**Gate B: (i).**
Action: `…far above it (\testref{test\_regge\_masses\_in\_both\_units}) \tier{N}.`
`[ ] ✓`

---

### 2.2 The 30 that already carry a `\testref` + the 2 fused — Gate A only

Gate A closed on all 30; **four need action** (T4 already listed in §1.5), the rest are `✓ no action`.

| Line | Cited test | Gate A | Action |
|---|---|---|---|
| L428 | `test_shannon_bit_against_the_area_law` | ✓ | none — the test computes `ln2/(A/2)=2.773` and `ln2/A=1.386`, which is the "log2 per area" of the sentence |
| **L682** | `test_entropy_modes_and_bits` | **△ partial** | the sentence also claims **slope 1.001**, which that test does not check (`test_cardy_slope_of_the_count`, `test_sections_09_16.py:341-347`, does). Action: `(\testref{test\_entropy\_modes\_and\_bits}; \testref{test\_cardy\_slope\_of\_the\_count})` `[ ] ✓` |
| L531 | `test_mass_ratios_of_imp_a1` | ✓ | none |
| L750 (fused `WW27`) | `test_theta3_at_tau_i` | ✓ | none — fused form is correct: cite key outside, test inside |
| L775 | `test_w2_integer_dimension` | ✓ | none |
| L987 | `test_the_measure_that_gives_the_spectrum` | ✓ | none |
| L997 | `test_offset_of_j1_zeros_tends_to_one_quarter` | ✓ | none |
| **L1234** | `test_ratio_against_the_bessel_ratio` | **✗ wrong test** | see T4: replace by `(\testref{test\_predictions\_at\_sigma\_12})` — **also add the missing period** (§3 C1). `[x] ✓` |
| **L1262** | `test_vector_ratio_range` | **✗ tautology** | see T1/D25: repair the test, keep the tag. `[x] ✓` |
| L1265 | `test_gluon_background_level` | ✓ | none |
| L1329 (1st) | `test_boundaries_nest` | ✓ | none |
| L1331 (b) | `test_hurwitz_constant_of_phi` | ✓ | none |
| L1331 (c) | `test_the_three_columns_of_irrational_unimodular_pisot` | ✓ | none |
| L1379 | `test_section41_prints_its_conclusions` | ✓ | none — §41 carries its own `assert`s (`sections.py:1826-1869`), the stdout test only pins them |
| L1380 | `test_pairs_that_give_s_on_average` | ✓ | none (same test also cited at L1666 — intentional, two claims of one computation) |
| L1432 | `test_three_gaps_of_the_marks`, `test_discrepancy_stays_below_half_a_percent` | ✓ | none |
| L1480 | `test_rational_step_has_a_kernel` | ✓ | none |
| L1484 | `test_three_golds_with_ratio_phi_squared` | ✓ | none |
| L1527 | `test_icosaedral_contact_spheres_do_not_touch` | ✓ | none |
| L1543 | `test_best_lattice_index` | ✓ | none |
| L1553 | `test_bragg_peaks_of_the_fibonacci_chain`, `test_bragg_random_level` | ✓ | none |
| L1565 | `test_weight_crossing_is_a_quarter_turn` | ✓ | none |
| L1604 | `test_offsets_against_the_printed_column` | ✓ | none |
| L1666 | `test_pairs_that_give_s_on_average` | ✓ | none |
| L1694 | `test_data_readings` | **△ partial** | the values `583.877 / 583.40` are asserted; **"2.2 to 3.1 standard deviations" is not** (`test_the_worst_case_is_deci` pins only `integer 583 at 5.0 sigma`). Action: add the two σ values to `test_data_readings` **or** drop the range from the sentence. `[ ] ✓` |
| L1695 (2 tags) | `test_desi_against_planck`, `test_the_worst_case_is_deci`, `test_three_sigma_criterion` | ✓ | none |
| L1753 | `test_cpl_projection` | ✓ | none |
| L1759 (fused `BV20`) | `test_distance_to_the_measured_lambda` | ✓ | none — fused + testref is the documented pattern |
| L1773 | `test_vector_ratio_depends_only_on_the_depth` | ✓ | none |
| L1873 | `test_higuchi_bound` | ✓ | none |
| L1952 | `test_black_hole_threshold` | ✓ | none |
| L169 | *(legend, exempt)* | — | none — rule 6 exempts the legend; see §3 C8 for the wording consequence |

**Untagged twin (unevenness):** `main.tex:1215-1216` states the *same* look-elsewhere argument as L1016
(`0.08`, `2×10⁵` values, `seed 2`) with **no tag at all**, while L1016 carries `[N]` (D14).
`[ ] ✓` — *either* add `(\testref{test\_probability\_of\_a\_phi\_coincidence}) \tier{N}`-style witness
for the seed-2 variant (needs a test), *or* accept that only one of the two twins is marked.

---

## 3. Logical consistency of the prose (after the removal of `L` and `R`)

21 findings. `main.tex` line numbers refer to HEAD `d68386f`.

### 3.1 Punctuation and grammar induced by `d68386f`

| # | Line | Problem | Exact fix |
|---|---|---|---|
| **C1** | **1234** | **Missing period.** The edit that inserted the testref also dropped the full stop that used to end the sentence: `…(\testref{…}) \tier{N} Fitted to the same two observed candidates…` — run-on. | `…(\testref{test\_ratio\_against\_the\_bessel\_ratio}) \tier{N}. Fitted to the same two observed candidates…` *(and swap the testref per T4)* |
| **C2** | **1262** | **Missing period**, same cause: `…(\testref{test\_vector\_ratio\_range}) \tier{N} Read as a measure of the graviton throat…` | `…\tier{N}. Read as a measure of the graviton throat…` |
| **C3** | **595** | **Orphan tag.** `\tier{N}` sits alone on its own line (it used to be `\tier{N} \tier{L}`); its witness is in the *next* sentence and the class is wrong. | see D03: delete the line, put `\tier{P}` at the end of the Lean sentence |
| **C4** | **1115** | Tag after a full stop, then a capital with no punctuation: `…of second order. \tier{N} The scale is one side of a pair:` | see D19: `…of second order (\testref{…}) \tier{N}. The scale is one side of a pair:` |
| **C5** | **338, 864, 917, 931, 953, 958, 983, 1016, 1022, 1052, 1093, 1115, 1203, 1223, 1238, 1280** (16 sites) | **Two placement conventions.** 16 tags sit *after* the final period (outside the sentence they mark) while 38 sit *before* it. `docs/citations.md` §8.2 rule 3 says the witness lives "in the prose of the same sentence" — the 16 are outside theirs. | Move each tag inside the sentence it marks, before the final punctuation, the way L531, L1432, L1480 already do. One mechanical pass, no wording change. `[x] ✓` |
| **C6** | **1280, 1238, 1674** | Tags that end a paragraph with nothing after them (`1280` is followed by a blank line), so the reader cannot tell which claim they annotate. | covered by C5 + D24/D25/D37 |
| **C7** | **1713** | The `R`-removal introduced `\textemdash{}` **with a space after and none before** (`observe it \textemdash{} a reading…`), while the manuscript's only other em dashes are closed `---` (`main.tex:299-300`). | `…the particles of a level observe it---a reading of the records, not a result about them.` |

### 3.2 Contradictions between the legend, `docs/citations.md` §8 and the body

| # | Where | Problem | Exact fix |
|---|---|---|---|
| **C8** | `main.tex:169` vs 41 tags | The legend promises *"`\tier{N}` verified numerically, **with the name of the test that checks it**"*, but 41 of the 72 free tags carry no test name. The legend is currently false for 57 % of its instances. | Resolved automatically by applying §2.1; if any `✓` lands on (iii)/(iv), re-read the legend once afterwards to make sure it still describes what is left. `[ ] ✓` |
| **C9** | `docs/citations.md:213` | The standard explains **"Why there is no `L`"** but says nothing about **`R`**, which `d68386f` removed at 15 sites (its rationale is only in the commit message). The document and the history disagree about what the alphabet used to be. | Add after §8.3's `L` paragraph: *"**Why there is no `R`.** `R` marked the direction of a reading rather than how a claim is established; eleven of its sites repeated what the prose already said, and a reading is now written as prose (`a reading of the records, not a result about them`), so the class carried no information the sentence does not."* `[x] ✓` |
| **C10** | `main.tex:53-55` vs `docs/citations.md:174` | The preamble comment lists **`a \cite`** among the valid witnesses of a bare tag; §8.2 rule 2 says *"An external source is the citation, not a tag"* and rule 3's witness list is `\testref{}` / `\Lean{}` / `\eqref`/`\ref` / `\witness{}`. The two standards contradict each other. | Rewrite the comment to: `%   \tier{X}        -> [X]      the witness lives in the prose of the same\n%                               sentence (a \Lean name, a \testref, an\n%                               \eqref/\ref or a \witness; a \cite is\n%                               never the witness of a bare tag)` `[x] ✓` |
| **C11** | `main.tex:520,528,554,613,644,652,658,702,707,730,1817` (11 sites) | `\tier{P} in~\cite{…}` — a `P` tag whose witness is a citation, printed as **two brackets** `[P] in [CW6]`. §8.2 rule 5 says a `P` *without* a bracket means "proved here, with no theorem name quoted at that point", and the grammar exists precisely so a fused tag shows one bracket. | Either fuse — `\tier[CW6]{P} in~\cite{…}` becomes `P[n]` with a single bracket — or, if these are meant as "proved here", drop `in~\cite{…}` from the sentence. **Author decision** (they all sit inside `imported` blocks, so the intended reading matters). `[ ] ✓` |

### 3.3 Uneven use of the alphabet

| # | Line(s) | Problem | Exact fix |
|---|---|---|---|
| **C12** | **595, 748, 1026, 1169, 1203, 1585** | `N` (which §8.3 defines as *"verified numerically, with the name of the test"*) is attached to sentences whose only witness is a `\Lean{}` name or a `\witness{P}` block — the definition of `P`. | D03 → `P`, D04 → `P`, D35 → testref or `P`, D16/D21/D22 → reformulate. `[ ] ✓` |
| **C13** | **1016 vs 1215-1216** | Two structurally identical look-elsewhere claims (`P = 0.08`, `2×10⁵` samples): the first carries `[N]`, the second carries nothing. | see §2.2, untagged twin |
| **C14** | **1234, 1238** | Two tags in one paragraph; the second dangles after `\S\ref{sec:data}.` at the paragraph end while the first is mid-sentence. | C5 + D24 |
| **C15** | **1135 vs 1127** | "gives the same value, $11.98$ (\eqref{eq:sigmaIR})" while the referenced equation says `11.97`. | D20 |
| **C16** | **1232-1236** | "the next two" is used twice in one paragraph for two different pairs (`1664/1982`, then `1014/1328`). | `…the two-brane model gives $1014$ and $1328$~GeV for **its** next two modes;` *(one word)* `[x] ✓` |
| **C17** | **893, 1005** | A `\witness{P}{…}` block immediately followed by `\tier{N}`: two statuses for one sentence. | D06, D13 |
| **C18** | **1336, 1363, 1379, 1380** (4 tags in captions) vs **1344-1354, 1357-1364** | Captions are tagged inconsistently: four carry `[N]`, while the `fig:mobius` caption (L1344-1354) and the first half of the `fig:granularity` caption (`three gap lengths, in the ratio φ and φ²`, L1358-1359) state computed numbers with no tag. | Either tag the parallel claims (`(\testref{test\_three\_gaps\_of\_the\_marks}) \tier{N}` also at L1359) or state in §8.2 that *captions carry no tags* and remove the four. **Author decision.** `[ ] ✓` |
| **C19** | **1331** | Four tags in a single paragraph (two already cited, two in D27/D28). Not a rule-1 violation (they are not adjacent) but it is the densest spot in the article. | no action unless C18 decides against caption/body tags |
| **C20** | **864 → 865** | The sentence marked `[N]` is followed by "In $\langle\cdot,\cdot\rangle_\eta$ it is positive for every $a\ge0$" — an *unqualified* universal claim whose support is `Proposition~\ref{prop:metric}` and `Imported statement~\ref{imp:A1}`. Before `d68386f` the surrounding tags bounded the scope; now the claim reads absolute. | Acceptable as written (the witnesses are in the sentence); only worth a re-read after D05 lands. `[ ] ✓` |
| **C21** | **1715-1716** | The `R`-removal left "…so it does not by itself fix the level." directly after a clause that used to be bounded by `[R]`; the paragraph now ends on an absolute negative. | Acceptable; flagged for the author's eye only. `[ ] ✓` |

---

## 4. Effort budget

| Work item | Quantity | Notes |
|---|---|---|
| **New tests** | **10 distinct** | D05 sym-T eigenvalues · D07+D08 Dirichlet `26.4` · D09+D19 grid convergence · D11 `11–12 %` · D15 spacing variance · D20 `11.98` · D21 residues · D24 `1.4 % / 15 GeV` · D38 `φ^{3σ/2}` = **9 runnable** · D23 Coleman–Weinberg `1.07` = **1 blocked on the author** |
| **Extensions / rewrites of existing tests** | **5** | D10 (`test_deep_chain_yields_the_j1_zeros` +1 assert), D17 (`test_scales` +1 param), D25 (`test_vector_ratio_range` — rewrite, fixes T1), D33 (`test_worst_gap_ratio…` +3 asserts), §2.2 L682 / L1694 (small additions) |
| **`\testref{}` insertions** | **21** | 17 in §2.1 + 4 in §2.2 (L682, L1234, L1262, L1694) |
| **Tags deleted** | **5** | D01, D06, D12, D13, D18 |
| **Sentences reformulated** | **4 + 6** | §2.1: D03, D04, D16, D22 · §3: C1, C2, C7, C16, C15, C10 |
| **Tags moved inside their sentence** | **16** | §3 C5 — mechanical, no wording change |
| **New lines in `tests/test_section_census.py:164`** | **≈17** | every *new* testref name must be added to the pinned set; `test_three_gaps_of_the_marks` and `test_data_readings` are already there |
| **`docs/citations.md` edits** | **2** | C9 (`Why there is no R`), C10 is a `main.tex` comment instead |
| **Total estimated size** | ≈ 150 lines of test code · ≈ 40 lines of `main.tex` · 17 lines of census · 1 doc paragraph | one editing pass after the tests are green |

**Sequencing (recommended):** tests first (they are the only thing that can fail) → census → tag
insertions → deletions/reformulations → the 16 tag moves → §3 prose fixes → one `uv run pytest` and
one `pnpm run build`.

### 4.1 Explicitly left to the author

1. **D23 / T3 — `1.07 levels down`**: supply the computation, or delete the number. *Blocked.*
2. **D16 — `2000 spacings checked`**: does such a run exist outside this repo? If not, drop the count.
3. **D20 / T2 — `11.98` vs `11.97`**: keep the number and add the test, or align the sentence with
   `eq:sigmaIR`.
4. **D06, D13 — `\witness{P}` + `[N]`**: delete the `N`, or promote it to `P`.
5. **D35 — `1/√2`**: `N` + testref, or `P` + the Lean name.
6. **C11 — the 11 `\tier{P} in~\cite{…}` sites**: fuse them, or drop the citation from the sentence.
7. **C18 — tags in captions**: tag the parallel claims, or drop tags from captions altogether.
8. **D02/D14/D26… style**: whether a fused `\tier[KEY]{N}` should ever be paired with a `\testref`
   (L1759 does) — §8.2 does not forbid it, but it is not exemplified either.
9. **§1.4 D5/D7 — `0.31384` vs `0.313851`, `1.22089e19` vs `1.2209e19`**: unify behind
   `constants.py` (touching `tests/`), or document the two as intentional (a §4 editing pass).
10. **§1.4 D1 — the seven assertions lost in the §39 rewrite**: restore them, or accept that §41 now
    covers the same ground under a different counting convention (D2).
