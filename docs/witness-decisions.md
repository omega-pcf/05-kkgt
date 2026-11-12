# Witness decisions — handoff for the principal author

**Status: applied, pending commit.** Everything marked `[x]` below is already
edited into `main.tex`, `docs/citations.md` and `tests/`. Nothing in this
repository has been committed by this pass.

**Repository:** `05-kk-golden-throat` · **HEAD:** `26808d6` · **scope:** the
witness layer only (`main.tex`, `docs/`, `tests/`). `citation.csl.json`,
`lean/`, `scripts/` and `images/` untouched.

This file replaces the previous 802-line gate document: that one described
the manuscript *before* the v134 merge, and most of its §4.1 "explicitly left
to the author" rows were artefacts of the review process rather than
decisions. The rows below are the **current** state of the document — one row
per site still open, and one short list at the end that is genuinely yours.

---

## 0. How to use this file

1. §0.1 is the executive summary (counters by decision type).
2. §1 lists what this pass applied, with the before/after of the non-trivial
   edits — read it once, it is history you do not have to re-check.
3. §2 lists rows closed without a decision (obsolete, superseded, or already
   on disk before this pass).
4. §3 is the fresh coverage: every witness site of the current manuscript
   that still has an open question, one row each.
5. §4 is work on **our** side — tests still to write. It needs no input from
   you; it is here so nothing is silently forgotten.
6. §5 **Needs the author** — the only list left for you. One `✓` per row.

The three mechanical rules of an editing pass are unchanged: every new
`\testref{…}` joins the pinned set in `tests/test_section_census.py`; the
test is green before the tag that cites it is written; the tag sits **inside**
the sentence it marks, before the final punctuation.

**Gate status**

| Gate | What it asks | State |
|---|---|---|
| **A** — does the evidence say what the claim says? | per site, against the real test/cite/Lean name | **closed for 60 of the 74 tags**; 14 body `N` still carry no test name (§3): 6 need only a test we write (§4), 7 need your call (§5), 1 is already witnessed |
| **B** — which option? | specific test / new test / reformulate / remove | **10 rows open** — all in §5 |
| **C** — is the prose even? | post-`L`/`R` removal, grammar, captions | **all 21 findings of the old document closed or obsolete** (§2); 2 re-read flags left in §5 |

---

### 0.1 Executive summary

| Decision type | Count | Where |
|---|---|---|
| **(i)** cite an existing test — `\testref{…}` inserted | **25 sites** (23 inserts + 2 cite-key migrations), **20 new test ids** | §1.2 |
| **(ii)** write a new test first | **4 tests now + 3 behind a ✓ in §5**, plus **3 extensions** | §4 |
| **(iii)** reformulate the sentence | **4 open** — D03, D04, D16, D22 | §5 |
| **(iv)** drop the tag | **1 applied** (D12), **2 open** — D01, D18 | §1.4, §5 |
| class changed `N` → `P` | **1 applied** — D35, on a Lean proof | §1.3 |
| unsupported numbers removed | **2** — `1.07 levels`, `2000 spacings` | §1.5 |
| caption status tags removed | **3 sites** (the 4th of the old report was already gone) | §1.4 |
| prose/consistency findings closed | **7 applied** (C1, C2, C7, C9, C10, C15, C16) + 12 obsolete | §2 |
| rows closed as obsolete | **11** (D03-orphan, D13, D29, D20, T1, T4, D1, D5, D7, D12-count, D2/T5) | §2 |
| **Needs the author** | **10 rows** | §5 |
| **Blocked on nothing** | the three "no provenance" numbers are gone from the text | §1.5 |

Test suite: **490** tests (was 484), **486** without the slow mark (was 480);
`main.tex` (Code and data) and `tests/README.md` updated.

---

## 1. Applied in this pass `[x]`

### 1.1 Grammar — Option A (author approval 2026-11-11)

The optional argument of `\tier` now means **internal ids only**:

* the citation-key branch of the dispatch is **gone** — `\tier[WW27]{N}` and
  `\tier[BV20]{N}` no longer exist; anything that is not a `\testref` in the
  optional argument raises `\PackageError` instead of silently rendering a
  bracket full of a key (the build fails loudly, it never prints a wrong
  bracket);
* the preamble comment (main.tex:53-70) and `docs/citations.md` §8.1, §8.2
  rules 2 and 5, and the §8.3 table were rewritten to match: an external
  source is a real citation **next to** the tag — `[N]~\cite{key}` or
  `[P] in~\cite{key}` — never inside it;
* all forms kept, none reduced: `\tier{X}` (short inline),
  `\tier[ids]{X}` (short inline with internal ids), `\witness{X}{ids}`
  (own line, flush right). Inline and own-line coexist;
* the sites that already carried an internal id keep rendering
  `N[test_name]` exactly as before — only the two that sat in captions were
  removed (§1.4, C18) — and none of them prints a number.

**PDF verification:** every `N[…]`/`P[…]` in the text contains a *name*
(test name or Lean name), **zero contain a number**; `[P] in [68]` appears
**11 times** and reads correctly (one bracket for the tag, one for the
citation); no `[N] [12]` or `[12] [N]` adjacency anywhere.

### 1.2 The 25 sites that now carry their test `[x]`

Each is the fused internal form `\tier[\testref{…}]{N}` → `N[test_name]`.
Every id was checked against `uv run pytest --collect-only -q` before it was
written, and each was added to the pinned set in
`tests/test_section_census.py`.

| Row | Site (current line) | Test now cited |
|---|---|---|
| D02 | L801 Koide reconstruction to `~10⁻⁴` | `test_reconstruction_is_below_one_part_in_ten_thousand` |
| D05 | L1206 the three `sym(T)` eigenvalues | `test_sym_t_eigenvalues_are_the_printed_three` **(new test)** |
| D07 | L1259 Dirichlet ⇒ no zero mode | `test_dirichlet_lowest_eigenvalue_is_positive` **(new test)** |
| D08 | L1273 the Dirichlet value `26.4` | `test_dirichlet_lowest_eigenvalue_is_positive` **(new test)** |
| D09 | L1281 second-order convergence on the golden grid | `test_second_order_convergence_on_the_golden_grid` **(new test)** |
| D10 | L1295 residuals and mass errors | `test_rms_against_the_lyr_table`; `test_error_on_the_ratios` (two ids, one sentence) |
| D11 | L1300 one node per level → `11–12 %` | `test_one_node_per_level_degrades_the_residual` **(new test)** |
| D14 | L1359 probability `0.08` of a φ-coincidence | `test_probability_of_a_phi_coincidence` |
| D17 | L1394 `M φ¹¹ = 62.5 GeV` | `test_m_phi_11_is_62_5_gev` **(new test)** |
| D19 | L1457 the four grid errors | `test_second_order_convergence_on_the_golden_grid` (shared with D09) |
| D25 | L1620 the gluon ratio `2.275` in `2.15–2.39` | `test_vector_ratio_range` |
| D26 | L1669 `0.9757 S` | `test_unweighted_count_tends_to_a_fixed_fraction` |
| D27 | L1671 `115` distinct arc weights | `test_distinct_arc_weights_of_73` |
| D28 | L1671 the shortest geodesic `4 log φ` | `test_trace_three_and_the_shortest_geodesic` |
| D31 | L1721 the ratio list and `0.9998` | `test_ratio_at_sigma_22_is_unity_to_four_decimals` |
| D32 | L1789 the Cardy correction `2.73, 2.50, 2.44` | `test_cardy_correction_settles` |
| D34 | L1880 the threshold window `0.301 … 0.632` | `test_first_active_level_is_two` |
| D36 | L1924 `log_φ(M_Pl/M) = 93.737` | `test_uv_level` |
| D37 | L2007 `σ_obs = 583.88 ± 0.04` and `583.40` | `test_data_readings` |
| D39 | L2079 `397` Planck units at the observer | `test_canonical_distance_along_the_tower` |
| D40 | L2215 `3149` modes below 1000 TeV | `test_graviton_modes_below_1000_tev` |
| D41 | L2219 the Regge masses in both units | `test_regge_masses_in_both_units` |
| new | L1345 the Dirichlet sine band `m_k ∝ sin(πk/16)` | `test_cw6_sine_band_matches_the_eigenvalues` **(new test)** |
| WW27 | L1092 the lemniscatic value `θ₃(e^{-π})` | migrated, see §1.3 |
| BV20 | L2093 the value below the TCC bound | migrated, see §1.3 |

**§2.2 of the old report (the tags that already had a test):**

* **L1024** — the sentence claims both `log2 = 0.693` *and* slope `1.001`;
  `test_cardy_slope_of_the_count` was added beside
  `test_entropy_modes_and_bits` in the same tag `[x]`.
* **L1575 / L1603** (old C1/C2/T4/T1) — periods restored and the wrong test
  swapped for `test_predictions_at_sigma_12` **before** this pass `[x]`.
* **L2027** (old L1694) — the values `583.877 / 583.40` are asserted, the
  `2.2 to 3.1 σ` range is not → §5.

### 1.3 The two cite-key migrations and the class of D35 `[x]`

**WW27 (L1092) — chose (i) `N`.**
*Evidence:* `test_theta3_at_tau_i` recomputes `Σ e^{-πk²}` and asserts it
equals `π^{1/4}/Γ(3/4)` to `1e-10`; `lean/TorreKK_LYR_v33.lean` has **no**
theorem about `θ₃` (grep `theta3|vartheta|lemnisc` → 0 hits); the phrase is
the identity itself, and WW27 (Whittaker & Watson, *A Course of Modern
Analysis*, 1927) is the provenance of the value, not its witness.
*Before:* `\tier[WW27]{N} (\testref{test\_theta3\_at\_tau\_i}).`
*After:* `the lemniscatic value~\cite{WW27}
\tier[\testref{test\_theta3\_at\_tau\_i}]{N}.`

**BV20 (L2093) — chose (i) `N`.**
*Evidence:* `test_distance_to_the_measured_lambda` asserts
`(√(2/3) − 0.698)/0.173 = 0.68`, i.e. the TCC bound sits 0.68 σ **above**
the measured central value — exactly the sentence's claim. Lean proves
`moduli_slope_below_tcc : 1/√2 < √(2/3)`, but that is the *model slope*,
already cited with `\cite{BV20} \Lean{moduli_slope_below_tcc}` at L2077; the
claim here is about the data, which no Lean statement touches.
*Before:* `\tier[BV20]{N} (\testref{test\_distance\_to\_the\_measured\_lambda}).`
*After:* `of trans-Planckian censorship~\cite{BV20}
\tier[\testref{test\_distance\_to\_the\_measured\_lambda}]{N}.`

**C11 — the 11 `\tier{P} in~\cite{…}` sites.** Under Option A this is the
*standard* external form, not a defect: the tag carries one bracket and the
citation its own, each printed by its own macro. The ten sites that already
read `[P] in~\cite{…}` were left **unchanged**; the eleventh had been fused
during the earlier migration and was put back:

*Before:* `\tier{P} for the identity, \tier[CW6]{P} for the weld;`
*After:* `\tier{P} for the identity, \tier{P} in~\cite{CW6} for the weld;`

**D35 (L1918) — chose `P`, not `N`.**
*Evidence:* `lean/TorreKK_LYR_v33.lean:1201` proves
`theorem moduli_slope (L : ℝ) (hL : 0 < L) : L / (Real.sqrt 2 * L) = 1 / Real.sqrt 2`
— the exact identity the sentence states (instantiate `L = log φ`). The
numerical test `test_canonical_slope` only confirms the float `≈ 0.7071`.
A machine-checked exact proof outranks a float check, and the Lean name was
already in the sentence, so the class that fits is `P`.
*Before:* `=1/\sqrt2$ \Lean{moduli\_slope} \tier{N}, under the`
*After:* `=1/\sqrt2$ \Lean{moduli\_slope} \tier{P}, under the`

### 1.4 Deletions `[x]`

* **D06 (old L893)** — the `\tier{N}` that followed a `\witness{P}` block is
  gone (D13's had already been removed by commit `81b9814`; only one site
  remained). The trailing fragment was folded into the sentence so the block
  stays the last thing in its paragraph:
  *Before:* `…is therefore open.\n\witness{P}{…, ring\_mode\_below\_BF} \tier{N} for the complex spectrum.`
  *After:* `…is therefore open for the complex spectrum.\n\witness{P}{…, ring\_mode\_below\_BF}.`
* **D12 (old L983)** — `d=4 is fixed by the arity, through (F2), rather than
  assumed \tier{N}` → the tag promised a numerical verification that exists
  nowhere (the report's own option (iv)); the sentence keeps its content:
  `…rather than assumed.`
* **C18 — status tags in captions.** Three sites removed: the `\tier{N}` of
  the `fig:granularity` caption and the two fused tags of the
  `fig:tilingstrip` caption (the fourth of the old report, the cube-diagonal
  one, disappeared with the v134 rewrite). Each caption still names its test
  — `Generated by \testref{test_section_writes_its_figure[…]}` plus the test
  of the claim itself — so the status is covered. The rule is now written in
  `docs/citations.md` §8.2 **rule 8: “No status tags in captions.”**
  No caption was found whose claim fails to name a test.

### 1.5 The two numbers with no provenance `[x]`

**D23 / T3 — `1.07 levels down`.** The number exists in no file (grep
`1.07` in `main.tex`, `tests/`, `sections.py` → only this sentence; the one
`1.07` hit in `sections.py` is an unrelated plot coordinate), and the
displayed formula `V(s) ∝ s⁴ Σ j_k⁴ log(s²j_k²)` is implemented nowhere.
The whole unsupported clause went, together with the tag that could not be
witnessed:

*Before:*
`And the depth is not fixed by a Coleman--Weinberg stabilisation of the tower: the extremum of its regularised vacuum energy lies $1.07$ levels down for renormalisation scale $1/\ell$ and moves with that scale; here $V(s)\propto s^4\sum_k j_k^4\log(s^2j_k^2)$ with $m_k=s\,j_k$, regularised with the exact zeros of $J_1$ for $k\le60$ and McMahon's expansion summed by Hurwitz $\zeta$ beyond \tier{N}.`

*After:*
`And the depth is not fixed by a Coleman--Weinberg stabilisation of the tower: here $V(s)\propto s^4\sum_k j_k^4\log(s^2j_k^2)$ with $m_k=s\,j_k$, regularised with the exact zeros of $J_1$ for $k\le60$ and McMahon's expansion summed by Hurwitz $\zeta$ beyond.`

(The tag had to go with the number: after the removal the sentence carries no
test, no Lean name and no reference, and a bare `\tier{N}` with nothing to
point at is the defect the whole system exists to prevent.)

**D16 — `2000 spacings checked`.** No file counts 2000 spacings (grep
`2000 spacings` / `spacings checked` → only this sentence and the archived
round). The count was removed, the claim kept:

*Before:* `\Lean{bessel\_J1\_zeros} \tier{N} for the $2000$ spacings checked.`
*After:* `\Lean{bessel\_J1\_zeros} \tier{N} for the spacings checked.`

**D20 / T2 — `11.98` vs `11.97`** was already on disk (the sentence reads
`$11.97$ (\eqref{eq:sigmaIR})`, matching the equation) `[x]`.

### 1.6 The duplicated constants — one source `[x]`

Both pairs are now unified behind `tests/src/kkgt/constants.py`, which
`sections.py` imports for the first time:

* `M_GEV = M_KOIDE_MEV / 1000` (= 0.31384 GeV, the value (F1) states and
  main.tex quotes at L799/L887/L1464) replaces **every** literal, including
  the two sections and four tests that carried `0.313851`;
* `M_PLANCK_GEV = 1.22089e19` replaces every `1.2209e19`. Section 24
  *computes* the Planck mass from `ħ, c, G` and prints `1.22089e+19`, so
  `1.22089e19` is the value, and `1.2209e19` was the rounded copy;
* the MeV/eV forms (`313.84`, `313.84e6`, `1.220890e28`) now read
  `M_KOIDE_MEV`, `M_KOIDE_MEV * 1e6`, `M_PLANCK_GEV * 1e9` — verified
  bit-identical to the old literals before the change.

**Printed numbers affected: none in the manuscript.** Every number main.tex
quotes is unchanged at its printed precision: `39.33`, `81.74`, `93.74`,
`37.72`, `90.39`, `203.56`, `387`, `101.06`, `1.048×10¹⁸`, `3149` (checked
by recomputing both constant variants side by side).

**One number in the suite moved:** section 33's *linear estimate* of the
graviton-mode count, `1e6/(π M φ¹²)`, printed `3149.7` with `M = 0.313851`
and prints **`3149.9`** with the canonical `M = 0.31384`. The matching
assertion was updated (`tests/test_sections_29_38.py`, `round(estimate, 1)
== 3149.9`). The count itself, `3149`, is unchanged and is the number the
manuscript quotes.

### 1.7 Counters `[x]`

`main.tex` (Code and data): “runs all **$490$** tests … the **$486$** that
each take under ten seconds” (was 484/480). `tests/README.md` lines 14-15
updated to match. Six tests were added (§1.2), none marked slow.

---

## 2. Rows closed without a decision

Deleted from the previous document because they no longer describe anything:

| Old row | Why it is gone |
|---|---|
| **D03** (orphan `\tier{N}` on its own line) | removed by commit `81b9814`; the tag now sits in the sentence about the Pisano periods — that residue is a live row, §3 |
| **D13** (`\witness{P}` + `[N]`) | removed by commit `81b9814`; only D06 remained and was removed here (§1.4) |
| **D29** (cube-diagonal projections `8,27,125,343,729 → 7,19,61,127,217`) | the v134 rewrite deleted those numbers from the manuscript; the claim now carries `(\testref{test\_cube\_diagonal\_projection})` in prose and no tag. Grep confirms `729`, `217`, `125`, `343`, `3L²`, `1008`, `385` all have **0** occurrences in `main.tex` |
| **D20** (`11.98` vs `11.97`) | applied before this pass `[x]` |
| **T1** (`test_vector_ratio_range` a tautology) | already rewritten on disk: it now reads the vector zeros from §3, computes `5.5615/2.4448`, asserts `≈ 2.275` and membership in `2.15–2.39`, and runs §37 for the symmetric window |
| **T4** (wrong test at old L1234) | swapped for `test_predictions_at_sigma_12` and the period restored, before this pass `[x]` |
| **§1.4 D1** (the seven assertions lost in the §39 rewrite) | **closed as not necessary**: the manuscript no longer asserts those counts — `729`, `217`, `125`, `343`, `3L²` → 0 occurrences (see D29 above). Section 41 asserts its own conclusions and `test_section41_prints_its_conclusions` pins them |
| **§1.4 D5 / D7** (the two values of each constant) | unified behind `constants.py`, §1.6 — the choice was unambiguous (the manuscript states `M = 313.84 MeV`, and §24 computes `M_Pl` from `ħ,c,G`) |
| **§1.4 D6** (dead constants) | `M_PLANCK_GEV` now imported by `sections.py`; `U_MEV` and `EPS0` are documentation of numbers main.tex quotes (`4.626 MeV`, `ε₀M = π`), not dead weight |
| **§1.4 D8** (no tolerance policy) | the policy is now stated in the manuscript itself (Code and data: “a rounding tolerance is the width of the printed precision … no tolerance is widened to make a test pass”) |
| **§1.4 D10, D11, D12** (the archived `tmp/reproduce_v93.py`) | the script is no longer in the tree; §1 of the old document was a comparison against a file that cannot be read any more — kept only as history |
| **C1, C2** (missing periods), **C7** (the lone `\textemdash{}`), **C9** (no “Why there is no `R`”), **C10** (preamble comment contradicting §8), **C15** (`11.98`), **C16** (“the next two” twice) | all applied — C1/C2/C7 in commit `ff27eaf`, C9/C10 in `923358d`, C15 before this pass, C16 marked `[x]` in the old file and present on disk. C10's comment was rewritten again here for Option A (§1.1) |
| **C5** (16 tags after the full stop) | commit `923358d` moved them; a grep now finds **no** tag preceded by a full stop except sentence-starting marks whose own sentence carries the witness |
| **C17** (block + tag) | D06/D13, §1.4 |
| **C18** (tags in captions) | §1.4 |
| **C3, C4, C6, C13, C14, C19** | superseded: their sites were either rewritten by v134 or are covered by the rows in §3 |
| **§4.1 items 1–10** of the old document | all ten dispositioned by the author and executed here — no longer a list |

---

## 3. Fresh coverage of the current manuscript — open rows

Inventory of the current `main.tex`: **83 inline tags** (14 body `\tier{N}` +
1 legend `\tier{N}` + 16 `\tier{P}` + 52 `\tier[\testref{…}]{N}`), **16
`\witness{P}{…}` blocks**, **12 `\wtag` labels**, **11 `[P] in~\cite{…}`**.
No tag sits on its own line, no two tags are adjacent, no tag is preceded by
a full stop without carrying its own witness, and every caption is tag-free.

### 3.1 The 14 body `\tier{N}` that still carry no test name

| # | Line | Claim | Witness in the sentence now | What is missing | Next step |
|---|---|---|---|---|---|
| 1 | L444 | Background: the golden step, “among the irrational steps checked, spread most evenly” | `\cite{Sos58,vRa88}` | the comparison itself: `test_worst_gap_ratio_over_the_first_5000_levels` asserts only `φ → 2.618` | §4.1 (shared with row 12) |
| 2 | L680 | the assumed `±20/±30/±40 GeV` error bars | `\cite{LYR26}` | nothing — these are *assumptions*, not computed values | **§5.1** |
| 3 | L935 | “The orders are Pisano periods, computed here” | `\cite{Wall60}` (the `\Lean{pisano_orders, modular_orders}` names are in the **next** sentence) | a witness in this sentence | **§5.2** |
| 4 | L1090 | the heat kernel whose modes are the left side | `\Lean{theta\_S\_law}` | class: `N` over a Lean name | **§5.3** |
| 5 | L1365 | the zeros of `ζ` follow the statistics of that ensemble | `\cite{Mon73,Odl87}` (tag *after* the cite) | `test_the_three_spacings_have_the_variance_of_the_ensemble`, and the tag moved into the variance sentence | §4.2 |
| 6 | L1369 | “for the spacings checked” | `\Lean{bessel\_J1\_zeros}` | class: `N` over a Lean name | **§5.4** |
| 7 | L1435 | roots bracketed on 6000 points, refined by Brent | `\eqref{eq:sl}`, `\eqref{eq:vector}` | a test of the continuum match, or no tag | **§5.5** |
| 8 | L1511 | “`[N]` for the residues” | `\Lean{half\_turn\_of\_clock24, …}` (witnesses the *half-turn*, not the residues) | `test_the_residues_of_phi_to_the_twelve` | §4.3 |
| 9 | L1545 | “the transformation laws, checked to `10⁻¹⁶`” | `\Lean{…}`, `\cite{PRV19}`, `\ref{sec:inputs}` | the `10⁻¹⁶` check exists in no file | **§5.6** |
| 10 | L1577 | `1.4 %` and `15 GeV` between the two models | `\ref{sec:data}` | `test_the_two_models_differ_by_one_point_four_percent` | §4.4 |
| 11 | L1822 | worst gap ratios `3.414 / 9.52 / 293.6` | `\cite{vRa88}`, `\ref{imp:polar}` | the three comparison values asserted nowhere | §4.1 (shared with row 1) |
| 12 | L1860 | the full list of icosahedral distances | `(\testref{test\_icosaedral\_contact\_spheres\_do\_not\_touch})` | — | **none** |
| 13 | L2048 | `S·T_GH ∝ φ^{3σ/2}` | `\cite{CW6}`, `\ref{imp:units}` | `test_entropy_over_the_gh_temperature_grows_as_phi_to_the_three_sigma_over_two` | §4.5 |
| 14 | L1295 | D10 residuals: the `0.011 (0.6 %)` parenthesis | two testrefs now (§1.2) | neither test asserts `0.011` | **§5.7** |

(For orientation: the other open sites of the old report are closed — D02,
D05, D07–D09, D11, D14, D17, D19, D25–D28, D31, D32, D34, D36, D37,
D39–D41 in §1.2; D06, D12, D16, D23, D35, C11, C18 in §1.3–§1.5.)

### 3.2 Other open sites

| Site | State |
|---|---|
| **L1558** (the untagged twin of D14) | the same look-elsewhere argument with `seed 2` carries **no** tag while the `seed 1` twin at L1359 carries `N[…]`. Add a tag + test, or accept one twin marked → **§5.8** |
| **L2023** (old L1694) | `583.877`, `583.40` and `5.0 σ` are asserted by `test_data_readings`; **“2.2 to 3.1 standard deviations” is not** → **§5.9** |
| **L2149** | `\tier{P} for the identity` — the sentence has no witness in it for that first tag (the fused `\cite` covers only “for the weld”) → **§5.10** |
| **L1477** (D20) | `11.97 (\eqref{eq:sigmaIR}) [N]` `[x]`. Optional: fold `test_alternatives_for_the_bottom_level` into the tag — it asserts `11.97` |
| **P sites** | 16 bare `\tier{P}`, 11 `[P] in~\cite{…}`, 16 witness blocks, 12 `\wtag`: all grammatical, no action |

---

## 4. Open work on our side — no decision needed

These are the old report's Gate B (ii) rows that are still ours to write.
Each was already recommended in the report; they are listed so they are not
lost, and each lands as `§4.x` only after the row it belongs to is settled.

1. **D33 + Background L444** — three lines in
   `test_worst_gap_ratio_over_the_first_5000_levels`: the worst gap ratio of
   `√2`, `e`, `π` over `N = 10…5000` (`3.414`, `9.52`, `293.6`), then one
   `\testref` each at L1822 and L444. *Caveat to check first:* the star
   discrepancy of `e` is **lower** than `φ` at `n = 1000` and `n = 10000`
   (`test_star_discrepancy`), so the claim must stay in the gap-ratio sense
   the sentence already uses.
2. **D15** — `test_the_three_spacings_have_the_variance_of_the_ensemble`:
   recompute the three spacings of `eq:data`, assert `round(var, 3) == 0.001`
   and `round(3π/8−1, 3) == 0.178`; move the tag into that sentence and drop
   it from after the `\cite`.
3. **D21** — `test_the_residues_of_phi_to_the_twelve`:
   `round(φ¹²) % 16 == 1`, `% 9 == 8`, and the order of `φ` mod `5` is `20`.
4. **D24** — `test_the_two_models_differ_by_one_point_four_percent`:
   `round(100·|g−t|/g, 1) == 1.4` for `1028/1014` and `1346/1328`, and
   `0.014·1028 ≈ 15` GeV.
5. **D38** — `test_entropy_over_the_gh_temperature_grows_as_phi_to_the_three_sigma_over_two`:
   `ratio(s) = π φˢ / φ^{−s/2}`, assert the step is `φ^{3/2}` at `s = 0,12,24`.
6. **L935 (if you choose `N`)** — a Pisano test: the period of the Fibonacci
   sequence mod `n` is `24` for `n = 16, 9, 12, 24, 48, 72`, `20` for `5`,
   `60` for `10`.
7. **L1435 (if you keep the tag)** — `test_the_vector_ratio_matches_the_continuum_roots`:
   the discretised `m₂/m₁` against the root ratio of `J₀/Y₀` to `1e-4` at
   depths `24` and `81.74`.
8. **Tests behind a `✓` in §5** — one extra assert in
   `test_deep_chain_yields_the_j1_zeros` (row §5.7), the two σ values in
   `test_data_readings` (§5.9), a seed-2 twin test (§5.8).

Nothing in §4 needs you; §5 does.

---

## 5. Needs the author

Ten rows. One `✓` per row; the recommended option is marked **[rec]**.
Everything else in this file is already applied or already ours.

1. **D01 · L680 · the assumed error bars.** `[N]` sits on a sentence whose
   own words are “we assume `±20` … `±40`”: an assumption is not a computed
   value, and the sentence's only source is its `\cite`.
   **[rec] drop the tag** (`\cite{LYR26}` already carries the claim) — or
   keep it and we look for a test that recomputes the error propagation the
   assumption feeds.
   `[ ] ✓`

2. **D03 · L935 · the Pisano periods.** The tag says “computed here `[N]`”
   while the names that do the computing are in the next sentence.
   **[rec] move the tag to that sentence as `\Lean{pisano\_orders,
   modular\_orders} \tier{P}`** (machine-checked → `P`) — or keep `[N]` here
   and we write the Pisano test (§4.6).
   `[ ] ✓`

3. **D04 · L1090 · the heat kernel.** `[N]` on a sentence whose only witness
   is `\Lean{theta\_S\_law}`, and L1939 already calls the same name
   machine-checked. **[rec] `\tier{P}`** in place of `\tier{N}`.
   `[ ] ✓`

4. **D16 · L1369 · “for the spacings checked”.** Same shape: `[N]` over
   `\Lean{bessel\_J1\_zeros}`. **[rec] `\tier{P}`** — or keep `N` and we
   name the spacing test (needs a new test first).
   `[ ] ✓`

5. **D18 · L1435 · the Brent bracketing window.** The sentence describes how
   the roots are found, not a result; no test reads `6000`, `[0.5,15]` or
   Brent. **[rec] drop the tag** (the sentence keeps its content) — or say
   the continuum match is load-bearing and we write §4.7.
   `[ ] ✓`

6. **D22 · L1545 · “checked to `10⁻¹⁶`”.** No file mentions `1e-16` or a
   transformation-law check. **[rec] drop the precision** — “…both are the
   fixed point of an involution (`\S\ref{sec:inputs}`); the transformation
   laws follow from them.” — or tell us where the check runs and we name it.
   `[ ] ✓`

7. **D10 · L1295 · the `0.011 (0.6 %)` parenthesis.** The two tests now cited
   cover `1.0 %` and `±0.11/0.16/0.21`; neither asserts `0.011`.
   **[rec] keep the parenthesis** and we add one assert to
   `test_deep_chain_yields_the_j1_zeros` — or delete the parenthesis.
   `[ ] ✓`

8. **L2023 · “2.2 to 3.1 standard deviations”.** `test_data_readings`
   asserts the values and the `5.0 σ`, not this range.
   **[rec] keep the range** and we add the two σ values to the test — or
   drop the range from the sentence.
   `[ ] ✓`

9. **L1558 · the `seed 2` twin.** The same argument with a different seed
   carries no tag while L1359 does. **[rec] add the tag with its test** (we
   write it, §4.8) — or accept that only one of the two twins is marked.
   `[ ] ✓`

10. **L2149 · `\tier{P} for the identity`.** Which identity? Name it (we add
    the reference) or **[rec] drop that first tag** and keep
    `\tier{P} in~\cite{CW6} for the weld`, which is witnessed.
    `[ ] ✓`

**One re-read when the above land (no tick needed):** the first-page legend
promises `N` = “verified numerically, **with the name of the test that checks
it**”; 14 body tags still carry no test name (§3.1). Once rows 1–6 and §4
have landed, read the legend once and confirm it still describes what is
left — that was C8 of the old document, and it is the only consistency finding
that cannot be closed from here.
