# AUD-001 test gaps closed, tolerances audited, section 47 tested

| Field | Value |
|---|---|
| **id** | `TST-001` |
| **title** | Closing the AUD-001 test gaps under the tolerance rule, and the first tests of the v138 section 47 |
| **status** | applied — `tests/**` only; `main.tex`, `scripts/`, `citation.csl.json`, `lean/` and `images/` untouched |
| **date** | 2026-11-17 |
| **repository** | `05-kk-golden-throat` (public as `omega-pcf/05-kkgt`), base `ea73175` |
| **evidence** | `docs/reports/20261116_AUD-001_claim_test_matrix.md`, the captured stdout of `kkgt.sections` (sections 1, 2, 3, 4, 30, 32, 34, 37, 40, 41, 42), `reproduce_v138.py 47`, and the probes `kkgt_tolerance_probe.py`, `kkgt_section47_probe.py` (session scratch) |

**Rule applied.** (i) every figure `sections.py` prints and no test asserted
gets its assertion; (ii) a tolerance never exceeds **half the last digit of
the figure it guards**. No assertion was relaxed; nothing was invented —
every asserted literal was read out of the source's own stdout or computed
from the closed form the source uses.

---

## 1. The 19 printed figures (policy (i))

Eighteen of the nineteen rows print from `seccion_1`, the nineteenth from
`seccion_30`, so the assertions live in the module that owns that section:
`tests/test_sections_01_08.py` (8 new tests, 18 rows) and
`tests/test_sections_29_38.py` (1 new test, 1 row). Line numbers below are
the AUD-001 audited numbering.

| # | claim | section | new test | tolerance (half unit of the print) |
|---|---|---|---|---|
| 1 | L805 `313.84` | 1 | `test_the_printed_koide_scale_is_313_84` | `5e-3` (.2f) |
| 2 | L1454 `3.8317` | 1 | `test_the_four_graviton_zeros_are_the_printed_four` | `5e-5` (.4f) |
| 3 | L1454 `3.8319` | 1 | `test_the_ir_level_in_phi_units_is_the_printed_3_8319` | `5e-5` (.4f) |
| 4 | L1464 `313.84` | 1 | `test_the_printed_koide_scale_is_313_84` | `5e-3` |
| 5 | L1475 `8.30` | 1 | `test_the_scale_in_powers_of_two_is_the_printed_8_30` | `5e-3` (the section prints `8.3`; `round(got, 2) == 8.30` ties it to the manuscript) |
| 6 | L1557 `5.03` | 1 | `test_the_log_pi_of_the_scale_is_the_printed_5_03` | `5e-4` (.3f print `5.028`) + `round(got, 2) == 5.03` |
| 7 | L1594 `2.295` | 1 | `test_the_j0_limit_is_the_printed_2_295` | `5e-4` (.3f) |
| 8 | L1601 `2.295` | 1 | idem | `5e-4` |
| 9 | L1610 `37.72` | 1 | `test_the_two_uv_tops_in_levels_are_the_printed_two` | `5e-3` (.2f) |
| 10 | L1610 `39.33` | 1 | idem | `5e-3` |
| 11 | L1610 `90.39` | 1 | idem | `5e-3` |
| 12 | L1612 `3.8317` | 1 | `test_the_four_graviton_zeros_are_the_printed_four` | `5e-5` |
| 13 | L1612 `7.0156` | 1 | idem | `5e-5` |
| 14 | L1613 `10.1735` | 1 | idem | `5e-5` |
| 15 | L1613 `13.3237` | 1 | idem | `5e-5` |
| 16 | L1617 `11.84` | 1 | `test_the_lyr_vector_table_is_the_printed_four` | the LYR figures live in the label `vs LYR 2.45 5.57 8.7 11.84` (the section's own zeros are asserted at `5e-5`) |
| 17 | L1617 `5.57` | 1 | idem | idem |
| 18 | L1618 `5.57` | 1 | idem | idem |
| 19 | L2108 `39.33` | 30 | `test_the_top_of_the_clock_is_the_printed_39_33` | label `(top at Planck: 39.33)`; section 1 computes the same `39.33` at `5e-3` |

**19 of 19 rows asserted.** No figure was missing from the code: all
nineteen were found in `sections/` (as a printed value or inside the `P(...)`
label), so none had to be reported as unassertable.

## 2. The five "only in code" figures

| claim | where the figure lived | what was added |
|---|---|---|
| L877 `4.318` | `test_ring_constant_mode_equals_the_bf_bound_scale` (unasserted) | the assertion `round(-1 / LN_PHI**2, 3) == -4.318` inside that test (section 1 prints `round(..., 3)`), and its tolerance tightened `1e-3 → 5e-5` (the `.4f` figure `-4.3184`) |
| L2028 `583.789` | test code of `test_rational_step_versus_the_contrast` | new `test_the_worst_case_level_is_583_789_plus_or_minus_0_028` (`tests/test_sections_29_38.py`), reading the DESI worst-case row of section 32, which prints `level 583.789 +- 0.028` |
| L2028 `0.028` | idem | idem, `abs=5e-4` (.3f) |
| L2028 `\pm0.028` | idem | idem (the `+-` field of the same row) |
| L2472 `5\times10^{-5}` | `R4` in `test_sections_01_08.py` and the tests that use it | new `test_the_rounding_tolerance_of_a_four_decimal_figure_is_5e_5`, which pins `R4 == 5e-5 == 0.5 * 10**-4` and the property that makes half a unit the right width |

Note: AUD-001 also named `test_free_phase_fit_is_not_better` as a carrier of
`5e-5`; in the current file that test guards a three-decimal figure with
`R3 = 5e-4` and no longer contains `5e-5`, so the assertion went where the
literal lives (`R4`, used by `test_offset_of_j1_zeros_tends_to_one_quarter`).

**5 of 5 rows closed.**

## 3. Tolerance audit (decision (ii))

149 tolerance sites in the nine test modules (111 `abs=`, 14 `rel=`, 24
`tol=`; `tests/src/kkgt/` carries none). Each was read against the figure it
guards; where the tolerance exceeded half that figure's last digit the
**actual gap** was computed first (probe `kkgt_tolerance_probe.py`, plus the
captured stdout) and the tolerance was tightened only when the gap fitted.

### 3.1 Tightened — 29 sites, none relaxed

| site | figure guarded | half unit | before → after | measured gap |
|---|---|---|---|---|
| `01_08` ring constant mode | `-4.3184` (.4f) | `5e-5` | `1e-3 → 5e-5` | 4.53e-5 |
| `01_08` `test_mpcf_framework_unit` | `67.846` (.3f) | `5e-4` | `1e-3 → 5e-4` | 1.89e-4 |
| `01_08` convergence table | `1.2e-4, 2.9e-5, 7.3e-6, 1.8e-6` (`.1e`) | `5e-6, 5e-7 ×3` | `rel=0.05 → per-entry abs` | 0 (the section prints those strings) |
| `01_08` `A(K=20)` | `0.22327442` (.8f) | `5e-9` | `1e-7 → 5e-9` | 0 |
| `01_08` section-2 depth identity | `1.0694864` (.7f) | `5e-8` | `1e-6 → 5e-8` | 4.66e-8 (93 % of budget: the two operands are both rounded prints) |
| `01_08` section-2 depth value | `1.0694864` | `5e-8` | `1e-6 → 5e-8` | 0 |
| `01_08` `test_graviton_zeros_are_the_j1_zeros` | `3.8317 …` (.4f) | `5e-5` | `5e-4 → 5e-5` | 3.19e-5 |
| `01_08` `test_vector_zeros_against_the_lyr_table` | `2.4448, 5.5615, 8.6958` (.4f) | `5e-5` | `5e-4 → 5e-5` | 0 |
| `01_08` `levels × ln φ` | `39.33` (.2f) | `5e-3` | `0.01 → 5e-3` | 4.26e-3 |
| `01_08` `12 + levels` | `93.74` (.2f) | `5e-3` | `0.01 → 5e-3` | 0 |
| `01_08` `sigma_UV` | `93.74` (.2f) | `5e-3` | `0.01 → 5e-3` | 0 |
| `01_08` `sym(T)` eigenvalues | `0.35, -0.06, -2.83` (.2f) | `5e-3` | `0.01 → 5e-3` | 3.0e-3 |
| `09_16` `test_cardy_correction_settles` | `2.7337 … 2.4437` (.4f) | `5e-5` | `5e-4 → 5e-5` | 4.75e-5 |
| `17_28` `test_unit_of_f1` | `4.6258` (.4f) | `5e-5` | `5e-4 → 5e-5` | 4.28e-5 |
| `17_28` `test_koide_scale_and_unit` (unit) | `4.6258` (.4f) | `5e-5` | `5e-4 → 5e-5` | 2.62e-5 |
| `17_28` `test_planck_mass_in_gev` | `1.22089e19` (6 s.f.) | rel `4.1e-6` | `rel=1e-5 → rel=1e-6` | rel 1.05e-7 |
| `17_28` `test_best_lattice_index` | `0.074` (.3f) / `0.74` (.2f) | `5e-4` / `5e-3` | `rel=0.02 → half the last digit of the row's weight` | 2.3e-4 / 3.9e-3 |
| `29_38` `test_required_omega_at_level_584` | `2.68126e-122` (6 s.f.) | `5e-128` | `rel=1e-4 → abs=5e-128` | 2.59e-128 |
| `29_38` `test_scales` (large branch) | `1.048e7` (4 s.f.) | `5e3` | `rel=5e-4 → abs=5e3` | 2363 |
| `29_38` `test_regge_masses_in_both_units` | `5.616e-4` (4 s.f.) | rel `8.9e-5` | `rel=1e-3 → rel=5e-5` | rel 1.61e-5 |
| `29_38` idem | `1.048e18` (4 s.f.) | `5e14` | `rel=1e-3 → abs=5e14` | 9.06e13 |
| `29_38` `test_w2_integer_dimension` | `0.9972` (.4f) | `5e-5` | `tol=5e-4 → 5e-5` | 0 |
| `29_38` `test_cardy_slope_of_the_count` | `1.0010` (.4f) | `5e-5` | `tol=5e-4 → 5e-5` | 0 |
| `29_38` `test_the_measure_that_gives_the_spectrum` | `1.8308 …` (.4f) | `5e-5` | `5e-4 → 5e-5` | 0 |
| `39_43` `test_two_prototiles_keep_their_areas` | `1.483259` (.6f) | `5e-7` | `rel=1e-6 → abs=5e-7` | 1.52e-7 |
| `39_43` idem | `0.916704` (.6f) | `5e-7` | `rel=1e-6 → abs=5e-7` | 3.82e-7 |
| `39_43` `{5,4} with qubits` | `1.4907` (.4f) | `5e-5` | `tol=5e-4 → 5e-5` | 0 |
| `45_46` `test_the_asymptotic_and_today_levels_are_the_printed_two` | `583.877` (.3f) | `5e-4` | `5e-3 → 5e-4` | 5.70e-6 |
| `45_46` idem | `583.090` (.3f) | `5e-4` | `5e-3 → 5e-4` | 4.05e-4 |

### 3.2 Kept, with the reason the source requires (6 sites)

| site | tolerance | why it stays |
|---|---|---|
| `01_08` second-order ratio | `rel=0.3` | the guarded claim is the *rate* ("of second order"), which the manuscript states without a decimal; the ratio of successive discretisation errors is not a printed number (AUD-001 §7 reaches the same reading) |
| `01_08` `x1_vec/x1_grav` | `abs=1e-4` | a quotient of two `.4f` prints compared against a `.4f` print: the two roundings compose to a 6.3e-5 bound, above the 5e-5 of a single figure; the test's own comment records the propagation. Not loosened — it was already `1e-4` |
| `01_08` chain vs J1 zeros | `rel=2e-3` | the gap *is* the discretisation error of the M=32 chain, which the section itself reports (rms 0.54 %); tightening it would assert the chain equals the exact zeros |
| `09_16` `test_gap_structure_at_n1000` | `abs=1e-6` | the operands are a gap ratio of values rounded to 10 decimals and the closed form `φ²`; no printed decimal is involved |
| `17_28` `0.014 × 1028` | `abs=1` | main.tex:1611 says "**about** $15$ GeV": an explicitly approximate integer, so the check pins the integer within 1 GeV instead of half a unit it never claimed |
| `39_43` `test_crofton…` constant | `abs=1e-5` | a numerically found constant against its closed form (`1/√5`); no printed figure |

### 3.3 Already within the rule

The remaining 114 sites are at or below half the last digit of their figure
(`5e-4` on three-decimal figures, `5e-5` on four-decimal ones, `5e-3` on
two-decimal ones, `1e-12`/`rel=1e-9` on identities between computed
quantities). Two comments were corrected rather than the values: the
`R2`/`R3`/`R4` block of `test_sections_01_08.py` claimed `R2 = 5e-4` was "the
rounding tolerance for a value printed with .2f" (a `.2f` width is `5e-3`);
the constants keep their values — they are *tighter* than the rule — and the
comment now says so.

## 4. Section 47 of the v138 round

New file `tests/test_sections_47.py`, `TestSection47ThePentagonalCode` (5
tests), following the module pattern and the "independent" check kind — the
package has no `seccion_47` yet, so nothing here reads its stdout:

| figure the paper will bring | test | how it is grounded |
|---|---|---|
| `a = 1.061275` | `test_the_pentagon_side_is_the_printed_1_061275` | `2 arccosh(cos(π/5)/sin(π/4))`, formatted `.6f` == the original's print; `cosh a = φ`, `sinh a = √φ` |
| `5F₂ₙ₊₁−4 / 5L₂ₙ₊₁` | `test_the_layer_counts_are_five_f_odd_minus_four_and_five_l_odd` | the reflection walk of the original re-derived here: `[1,6,21,61,166,441,1161] = 5F(2n+1)−4`, `[5,20,55,145,380,995,2605] = 5L(2n+1)` |
| `rate → 1/√5` | `test_the_layer_six_rate_tends_to_one_over_root_five` | `0.4457` (`.4f`), limit `0.4472`, the original's own `abs(rate − 1/√5) < 2e-3`, and `φ² = 2.6180` |
| `0.745` | `test_the_chosen_cut_is_the_printed_0_745` | `cro = 10a/π² = 1.0753`, `cro ln2 = 0.745`, `cro ln2 / ½ = 1.49` — each asserted at its own print width |
| `χ(S) = 1.592` | `test_the_chi_that_would_give_s_is_the_printed_1_592` | `exp(0.5/cro)` formatted `.3f` == `1.592` |
| `2000 spacings` | **not written** | no support: the string does not appear in `reproduce_v138.py`, in section 47's stdout, nor anywhere in `tests/` or `tests/src/` — asserting it would mean inventing it → **bring-up** |

Captured stdout of `reproduce_v138.py 47` (2026-11-17) is quoted in each
docstring; it reads `a = 1.061275`, `pentágonos [1, 6, 21, 61, 166, 441,
1161] = 5F(2n+1)-4`, `tasa en la capa 6: 0.4457; límite F/L = 1/sqrt5 =
0.4472`, `Crofton: 1.0753 … con chi=2, 0.745 … chi que daría S: 1.592`.

**Contract tests for section 47 (reading its stdout) were not forced**: they
need `seccion_47` inside `kkgt.sections`, which moves `SECCIONES`,
`test_forty_six_sections_in_order` (1..46), `test_all_sections_covered`
(`range(1, 47)`), `MARKERS[47]` in `test_section_runs.py`, the README map and
the manuscript's own "forty-six sections" sentence — see the bring-up list.

## 5. Easy fixes applied

* `tests/README.md`: suite counters `533/529 → 549/545` (both verified by
  running the commands), the layout tree now lists `test_sections_47.py`, and
  the section→test map was re-derived from `pytest --collect-only -q`
  (stale entries corrected: sections 1, 4, 29, 30, 32, 41) with a line
  stating how the number is produced.
* `R2` comment corrected (see §3.3).
* A stray `fig_tilings_strip.pdf` written into the repository root by a
  manual `python -m kkgt.sections 41` during this pass was removed; the tree
  carries only the test changes.

## 6. Bring-up for the principal author

1. **Port `seccion_47` into `kkgt.sections`** (or decide the paper keeps 46
   sections): it is what the contract tests of §4 need, and it moves the
   registry pins, `MARKERS`, the README map and the manuscript's
   "forty-six sections" claim in one pass. The v138 merge plan already flags
   the 46-vs-47 tension (MRG-001, h77/h78).
2. **`2000 spacings`**: no source anywhere in the repository or the v138
   script — needs the figure from the author or a decision to drop it.
3. **Counters outside `tests/`**: root `README.md:60` and `main.tex:2507`
   still quote `533`/`529`; they are now `549`/`545`. Both are outside this
   worker's file range (the manuscript is another worker's) → recount at the
   next wave that owns them.
4. **The other ten AUD-001 rows of §3** (of the 29 with no assertion) that
   this pass did not close because `sections.py` carries no literal for them:
   L647 `61,127` (retarget, not add), L804 `67.846` (docstring/comment only),
   L1609 `1.2209×10^{19}`, L1609 `2.435×10^{18}` (numeric `2.435e18` only),
   L1615 `11.834`, L1788 `46.25`, L1789 `56.37`, L2005 `2.42`, L2005
   `2.75`, L2005 `3.40` — each needs the same decision the audit states:
   compute and assert, or mark the manuscript figure as external data.
5. **Class `c` (10 figures) and the 61 `mover` retargets** were not touched,
   per the policy of this wave (reclassification lives in `main.tex`).
6. **Citation pins**: the new tests are not cited by the manuscript. Adding a
   `\testref{...}` for any of them must land together with its line in
   `test_testref_set_is_pinned`, which asserts exact set equality.
7. **`about 15 GeV`** (`main.tex:1611`, `abs=1` in `17_28`): if the author
   wants the sentence pinned to a decimal, the sentence has to quote one
   first.

Already closed elsewhere and verified here: the `m_τ` divergence of AUD-001
§9 — `constants.py` now single-sources `M_TAU_MEV = 1776.86`, and
`test_koide_scale_and_unit` imports it, so the suite no longer asserts two
Koide scales.

## 7. Gates

```
$ uv run pytest tests/ -q
549 passed in 59.67s

$ uv run pytest tests/ -q -m 'not slow'
545 passed, 4 deselected in 60.50s

$ pnpm run type-check
> tsc --noEmit
(exit 0, no output)

$ git diff | grep '^-.*def test_'
(no output — no test renamed or removed)
```

`build` was not run: this pass does not touch `.tex`.

## 8. Gaps

* The `L###` line numbers are the AUD-001 audited numbering;
  `main.tex` is being edited in parallel by another worker, so the anchors
  were verified by literal, not by line.
* The tolerance audit classified every site by the figure it guards, but the
  *gap* was computed only where the tolerance exceeded the rule (29 sites,
  §3.1) and at the six justified sites; the 114 within-rule sites rest on
  the classification, not on a per-site probe.
* No assertion was relaxed anywhere in this pass; no figure was asserted
  that the source does not print or compute.
