# Sections migration ledger — the SEC-001 record for `tests/src/kkgt/sections.py`

| Field | Value |
|---|---|
| **id** | `SEC-001` |
| **title** | Migration ledger for the forty-six `seccion_N` functions of `tests/src/kkgt/sections.py` |
| **status** | layer 0 (this ledger) and layer 1 (shared primitives) applied; layer 2 (moving the section bodies) started: lot 0 (the package shell), lot 1 (17–24) and lot 2 (9–16) applied — 16 of 46 rows ticked; lots 3–7 pending |
| **date** | 2026-11-16 |
| **version** | 1.0 |
| **repository** | `05-kk-golden-throat` (public as `omega-pcf/05-kkgt`), written from HEAD `ce7ff48` |
| **evidence** | `docs/reports/20261116_AUD-001_claim_test_matrix.md` (AUD-001), `CLAIMS_FINAL.json` (350 claims), an AST parse of the nine `tests/test_*.py` files plus `tests/conftest.py`, and `uv run pytest tests/ -q` |
| **scope** | `tests/**` and this file only; `main.tex`, `scripts/`, `lean/` and the other reports were not touched |

**Why this file exists.** The manuscript's computation lives in one 2 176-line
module with 46 `seccion_N` functions; as long as it stays whole but
un-migrated the suite reads as half-finished. The migration was requested
*by layers*, so that no intermediate state goes red: layer 0 fixes the plan as
one row per section, layer 1 removes the primitives that are defined twice,
layer 2 moves the bodies lot by lot. This file is both the plan and the
checkbox ledger that each layer-2 commit ticks.

## 1. Method

* **Sections.** The 46 `seccion_N` functions and their `SECCIONES.append(...)`
  titles were read out of `tests/src/kkgt/sections.py` (46 functions, 46
  appends; the file is 2 176 lines / 132 796 bytes after layer 1).
* **Dependent tests.** Each test function of the suite was parsed with `ast`;
  a test is *sections-dependent* when its signature takes the `run_section`,
  `sections` or `sections_module` fixture, or when its body imports
  `kkgt.sections`. Sections called by `run_section(<literal>)` were read
  literally; the two parametrized users were resolved from their
  `@pytest.mark.parametrize` data (`test_section_runs_and_prints_its_number`
  runs `n = 1..46`, `test_section_writes_its_figure` runs the five
  `FIGURES` sections 10, 13, 39, 41, 44).
* **Dependent claims.** For every claim of `CLAIMS_FINAL.json` that carries at
  least one `\testref`, the cited test was bound to the section(s) it runs;
  a claim is listed on every row whose section it rests on.
* **Class-c column.** The six claims AUD-001 §10 records as existing *only*
  in `sections.py` (`L703 0.0036 / 0.3027 / 68.17 / \pm0.0036`,
  `L2460 1.18`, `L2460 3.13`) are not among the 133 — no test asserts them —
  but they disappear with their section, so each is pinned to the row that
  holds its literal.

## 2. Dependencies in numbers

| Quantity | Count | Note |
|---|---:|---|
| `seccion_N` functions | 46 | `seccion_1` … `seccion_46`, one `SECCIONES` append each |
| Sections-dependent test functions | **70** of 243 | 65 take `run_section`, 4 take `sections`/`sections_module`, 1 (`test_the_sections_live_in_the_package`) imports the module and asserts its path |
| — per file | — | `01_08` 30, `29_38` 14, `39_43` 10, `census` 6, `09_16` 3, `17_28` 3, `44` 1, `45_46` 2, `runs` 1 |
| Cited claims resting on a sections-driven test | **133** of 232 | via the 20 cited tests that run a section (class `b` 59, `a` 54, `a~` 14, `a?` 6) — AUD-001 §10 |
| … plus the three claims citing the figure test | **136** | `L647 61,127` and `L647 \pm1` (section 44), `L1702 0.9757` (section 39); AUD-001 excluded `test_section_writes_its_figure[section-N]` from its 20, this ledger keeps it because the test does run a section |
| Class-c claims that exist only in `sections.py` | 6 | AUD-001 §10; attributed on 9 rows because two literals occur in two sections |
| Distinct dependent tests named in the rows | 65 | the 65 `run_section` users; + 5 registry-level tests (below) = 70 |
| Sum of the claim cells / distinct claims | 172 / 136 | 36 claims cite tests of two sections and therefore appear on two rows; totals never double count |
| Rows carrying at least one dependent claim | 11 of 46 | sections 1, 4, 6, 7, 29, 32, 34, 37, 39, 40, 44 |
| Rows whose only test is the marker test | 18 of 46 | sections 9, 11, 14, 15, 19–22, 24–28, 30, 31, 33, 35, 42 — no test binds a claim to them |

**Registry-level dependencies (they apply to every row and are therefore not
repeated in the table).** Five of the 70 depend on the whole registry rather
than on one section: `test_forty_six_sections_in_order`,
`test_every_section_is_callable`, `test_titles_are_unique`,
`test_section_function_body_has_an_identity` (the `sections` /
`sections_module` fixtures) and `test_the_sections_live_in_the_package`
(asserts `module.__name__ == "kkgt.sections"` and the file path). None of the
five is cited by `main.tex`. The sixth registry-wide test,
`test_section_runs_and_prints_its_number[section-NN]`, *is* listed in every
row because it is parametrized per section (it asserts the `MARKERS[NN]`
stdout line; it is not cited either).

## 3. The ledger — one row per section

| § | function | dependent tests (of the 70) | dependent claims (of the 133) | class-c claims that exist only here (AUD-001 §10) | target module (layer 2) | done |
|---:|---|---|---|---|---|:---:|
| 1 | `seccion_1` | `test_section_runs_and_prints_its_number[section-01]`, `test_section1_stdout_blocks`, `test_alternatives_for_the_bottom_level`, `test_mpcf_framework_unit`, `test_dirichlet_lowest_eigenvalue_is_positive`, `test_second_order_convergence_on_the_golden_grid`, `test_one_node_per_level_degrades_the_residual`, `test_m_phi_11_is_62_5_gev`, `test_cw6_sine_band_matches_the_eigenvalues`, `test_the_three_spacings_have_the_variance_of_the_ensemble` | 25 claims · L1268, L1274, L1300, L1363, L1364, L1395, L1454, L1455, L1456, L1464, L1469, L1471, L1472, L1475, L1477 | L2460 `1.18`, L2460 `3.13` (seccion_1 docstring: "Python 3.13 … SciPy 1.18.1") | `kkgt/sections/s01_08.py` | [ ] |
| 2 | `seccion_2` | `test_section_runs_and_prints_its_number[section-02]`, `test_a_converges_with_the_number_of_exact_zeros`, `test_b_is_positive`, `test_depth_is_minus_log_s_over_log_phi` | — (0 claims) | — | `kkgt/sections/s01_08.py` | [ ] |
| 3 | `seccion_3` | `test_section_runs_and_prints_its_number[section-03]`, `test_vector_ratio_grows_with_the_depth`, `test_graviton_zeros_are_the_j1_zeros`, `test_vector_zeros_against_the_lyr_table`, `test_uv_depth_in_levels` | — (0 claims) | — | `kkgt/sections/s01_08.py` | [ ] |
| 4 | `seccion_4` | `test_section_runs_and_prints_its_number[section-04]`, `test_standard_product_is_not_positive`, `test_sym_t_eigenvalues_are_the_printed_three`, `test_eta_weighted_product_is_positive`, `test_eta_is_the_sqrt_minus_g_of_the_metric`, `test_K_is_self_adjoint_in_the_eta_product_only` | 5 claims · L1207 | — | `kkgt/sections/s01_08.py` | [ ] |
| 5 | `seccion_5` | `test_section_runs_and_prints_its_number[section-05]`, `test_measured_phase_in_d4_is_a_quarter`, `test_free_phase_fit_is_not_better` | — (0 claims) | — | `kkgt/sections/s01_08.py` | [ ] |
| 6 | `seccion_6` | `test_section_runs_and_prints_its_number[section-06]`, `test_rms_against_the_lyr_table`, `test_deep_chain_yields_the_j1_zeros`, `test_without_the_weight_the_chain_degrades` | 17 claims · L1289, L1290, L1292, L1294, L1295, L1296 | — | `kkgt/sections/s01_08.py` | [ ] |
| 7 | `seccion_7` | `test_section_runs_and_prints_its_number[section-07]`, `test_error_on_the_ratios`, `test_gluon_scale_needs_three_levels` | 17 claims · L1289, L1290, L1292, L1294, L1295, L1296 | — | `kkgt/sections/s01_08.py` | [ ] |
| 8 | `seccion_8` | `test_section_runs_and_prints_its_number[section-08]`, `test_rs_fit_beats_the_golden_fit`, `test_discrete_kk_operator_matches_its_closed_form` | — (0 claims) | — | `kkgt/sections/s01_08.py` | [ ] |
| 9 | `seccion_9` | `test_section_runs_and_prints_its_number[section-09]` | — (0 claims) | — | `kkgt/sections/s09_16.py` | [x] |
| 10 | `seccion_10` | `test_section_writes_its_figure[section-10]`, `test_section_runs_and_prints_its_number[section-10]` | — (0 claims) | — | `kkgt/sections/s09_16.py` | [x] |
| 11 | `seccion_11` | `test_section_runs_and_prints_its_number[section-11]` | — (0 claims) | — | `kkgt/sections/s09_16.py` | [x] |
| 12 | `seccion_12` | `test_section_runs_and_prints_its_number[section-12]`, `test_section12_runs_all_of_its_checks` | — (0 claims) | — | `kkgt/sections/s09_16.py` | [x] |
| 13 | `seccion_13` | `test_section_writes_its_figure[section-13]`, `test_section_runs_and_prints_its_number[section-13]`, `test_section13_draws_figure_two` | — (0 claims) | — | `kkgt/sections/s09_16.py` | [x] |
| 14 | `seccion_14` | `test_section_runs_and_prints_its_number[section-14]` | — (0 claims) | — | `kkgt/sections/s09_16.py` | [x] |
| 15 | `seccion_15` | `test_section_runs_and_prints_its_number[section-15]` | — (0 claims) | — | `kkgt/sections/s09_16.py` | [x] |
| 16 | `seccion_16` | `test_section_runs_and_prints_its_number[section-16]`, `test_printed_values` | — (0 claims) | — | `kkgt/sections/s09_16.py` | [x] |
| 17 | `seccion_17` | `test_section_runs_and_prints_its_number[section-17]`, `test_monte_carlo_error` | — (0 claims) | — | `kkgt/sections/s17_24.py` | [x] |
| 18 | `seccion_18` | `test_section_runs_and_prints_its_number[section-18]`, `test_lambda_times_s_is_six_pi` | — (0 claims) | — | `kkgt/sections/s17_24.py` | [x] |
| 19 | `seccion_19` | `test_section_runs_and_prints_its_number[section-19]` | — (0 claims) | — | `kkgt/sections/s17_24.py` | [x] |
| 20 | `seccion_20` | `test_section_runs_and_prints_its_number[section-20]` | — (0 claims) | — | `kkgt/sections/s17_24.py` | [x] |
| 21 | `seccion_21` | `test_section_runs_and_prints_its_number[section-21]` | — (0 claims) | — | `kkgt/sections/s17_24.py` | [x] |
| 22 | `seccion_22` | `test_section_runs_and_prints_its_number[section-22]` | — (0 claims) | — | `kkgt/sections/s17_24.py` | [x] |
| 23 | `seccion_23` | `test_section_runs_and_prints_its_number[section-23]`, `test_the_background_level_is_twelve` | — (0 claims) | — | `kkgt/sections/s17_24.py` | [x] |
| 24 | `seccion_24` | `test_section_runs_and_prints_its_number[section-24]` | — (0 claims) | — | `kkgt/sections/s17_24.py` | [x] |
| 25 | `seccion_25` | `test_section_runs_and_prints_its_number[section-25]` | — (0 claims) | — | `kkgt/sections/s25_32.py` | [ ] |
| 26 | `seccion_26` | `test_section_runs_and_prints_its_number[section-26]` | — (0 claims) | — | `kkgt/sections/s25_32.py` | [ ] |
| 27 | `seccion_27` | `test_section_runs_and_prints_its_number[section-27]` | — (0 claims) | — | `kkgt/sections/s25_32.py` | [ ] |
| 28 | `seccion_28` | `test_section_runs_and_prints_its_number[section-28]` | — (0 claims) | — | `kkgt/sections/s25_32.py` | [ ] |
| 29 | `seccion_29` | `test_section_runs_and_prints_its_number[section-29]`, `test_the_planck_level_is_2_2_to_3_1_sigma_from_584`, `test_the_script_asserts_the_window_it_quotes` | 19 claims · L2026, L2027, L2028, L2029, L2030, L2031, L2033, L2035 | L703 `0.0036`, L703 `0.3027`, L703 `\pm0.0036` (line 1117 data tuple) | `kkgt/sections/s25_32.py` | [ ] |
| 30 | `seccion_30` | `test_section_runs_and_prints_its_number[section-30]` | — (0 claims) | — | `kkgt/sections/s25_32.py` | [ ] |
| 31 | `seccion_31` | `test_section_runs_and_prints_its_number[section-31]` | — (0 claims) | — | `kkgt/sections/s25_32.py` | [ ] |
| 32 | `seccion_32` | `test_section_runs_and_prints_its_number[section-32]`, `test_the_worst_case_is_deci`, `test_the_criterion` | 19 claims · L2026, L2027, L2028, L2029, L2030, L2031, L2033, L2035 | L703 `0.0036`, L703 `0.3027`, L703 `68.17`, L703 `\pm0.0036` (the DESI table of lines 1182-1184) | `kkgt/sections/s25_32.py` | [ ] |
| 33 | `seccion_33` | `test_section_runs_and_prints_its_number[section-33]` | — (0 claims) | — | `kkgt/sections/s33_40.py` | [ ] |
| 34 | `seccion_34` | `test_section_runs_and_prints_its_number[section-34]`, `test_cpl_projection` | 2 claims · L2091, L2093 | — | `kkgt/sections/s33_40.py` | [ ] |
| 35 | `seccion_35` | `test_section_runs_and_prints_its_number[section-35]` | — (0 claims) | — | `kkgt/sections/s33_40.py` | [ ] |
| 36 | `seccion_36` | `test_section_runs_and_prints_its_number[section-36]`, `test_correlation_converges_only_for_the_irrational_step` | — (0 claims) | — | `kkgt/sections/s33_40.py` | [ ] |
| 37 | `seccion_37` | `test_section_runs_and_prints_its_number[section-37]`, `test_vector_ratio_range`, `test_vector_ratio_depends_only_on_the_depth`, `test_first_gluon_at_the_background`, `test_w2_integer_dimension`, `test_cardy_slope_of_the_count`, `test_e_to_the_s_is_never_an_integer`, `test_the_measure_that_gives_the_spectrum` | 51 claims · L1006, L1025, L1026, L1119, L1582, L1589, L1590, L1591, L1592, L1593, L1594, L1599, L1601, L1609, L1610, L1612, L1613, L1615, L1617, L1618, L1619, L2108, L2111, L2112 | — | `kkgt/sections/s33_40.py` | [ ] |
| 38 | `seccion_38` | `test_section_runs_and_prints_its_number[section-38]`, `test_section38_stdout` | — (0 claims) | — | `kkgt/sections/s33_40.py` | [ ] |
| 39 | `seccion_39` | `test_section_writes_its_figure[section-39]`, `test_section_runs_and_prints_its_number[section-39]`, `test_section39_draws_figure_four` | 1 claims · L1702 | — | `kkgt/sections/s33_40.py` | [ ] |
| 40 | `seccion_40` | `test_section_runs_and_prints_its_number[section-40]`, `test_open_legs_of_73`, `test_crofton_constant`, `test_pairs_that_give_s_on_average`, `test_distinct_arc_weights_of_73` | 14 claims · L1670, L1711, L2005, L2006 | — | `kkgt/sections/s33_40.py` | [ ] |
| 41 | `seccion_41` | `test_section_writes_its_figure[section-41]`, `test_section_runs_and_prints_its_number[section-41]`, `test_layer_growth`, `test_tiles_inside_the_disc`, `test_section41_prints_its_conclusions`, `test_qubit_bond_dimension_of_54` | — (0 claims) | — | `kkgt/sections/s41_46.py` | [ ] |
| 42 | `seccion_42` | `test_section_runs_and_prints_its_number[section-42]` | — (0 claims) | — | `kkgt/sections/s41_46.py` | [ ] |
| 43 | `seccion_43` | `test_section_runs_and_prints_its_number[section-43]`, `test_section43_stdout` | — (0 claims) | — | `kkgt/sections/s41_46.py` | [ ] |
| 44 | `seccion_44` | `test_section_writes_its_figure[section-44]`, `test_section_runs_and_prints_its_number[section-44]`, `test_section44_draws_the_background_figure` | 2 claims · L647 | — | `kkgt/sections/s41_46.py` | [ ] |
| 45 | `seccion_45` | `test_section_runs_and_prints_its_number[section-45]`, `test_section45_prints_the_planck_levels` | — (0 claims) | — | `kkgt/sections/s41_46.py` | [ ] |
| 46 | `seccion_46` | `test_section_runs_and_prints_its_number[section-46]`, `test_section46_prints_the_window_tori` | — (0 claims) | — | `kkgt/sections/s41_46.py` | [ ] |

## 4. Layer 1 — shared primitives (applied in this pass)

Nothing inside a `seccion_N` body was moved; only definitions that existed
twice were given one origin.

1. **`m_τ` is single-sourced as `kkgt.constants.M_TAU_MEV = 1776.86`** (the
   value that reproduces the manuscript's `M = 313.84` MeV; AUD-001 §9). The
   six live literals became imports/references:
   `sections.py` lines that held `1776.86` (sections 1 and 16) and
   `1776.93` (section 24), `test_sections_09_16.py` (`OBS["tau"]`), and the
   three sites of `test_sections_17_28.py`. `grep -c '1776.93' tests/` now
   returns **0**.
   * `test_koide_scale_and_unit` — the assertion that reproduced the wrong
     scale: **before** `assert m * 1e3 == pytest.approx(313.851, abs=5e-4)`
     (computed 313.8509 from `m_τ = 1776.93`, i.e. the number the manuscript
     does not print, at 19.6× the tolerance of its own divergence);
     **after** `assert m * 1e3 == pytest.approx(313.841, abs=5e-4)` (computed
     313.8411 from `M_TAU_MEV`, diff `1.3e-5`). The tolerance is unchanged;
     `round(313.8411, 2) == 313.84` is the figure of `main.tex` 805/896/1484.
   * The same test's unit: **before** `approx(4.6259, abs=5e-4)` → **after**
     `approx(4.6258, abs=5e-4)` (computed 4.6257738, diff `2.6e-5`);
     `4.6258` is `kkgt.constants.U_MEV` and what section 24 now prints for
     `u`, and it still rounds to the cited `4.626` (AUD-001 `L810`, `L896`).
   * `test_the_grid_does_not_fix_the_top` keeps `203.562` (`abs=5e-4`):
     the value moves 203.56193 → 203.56206, diff `5.9e-5`.
   * `test_uv_level` keeps `93.737` (`abs=5e-4`), which is the cited claim
     `L1933` (class `a`): the value moves 93.73738 → 93.73744, diff
     `4.4e-4 < 5e-4`, still printing `93.737` (`MARKERS[24]`).
   * Section 24's stdout changes `M = 313.851` → `M = 313.841` and
     `u = 4.6259` → `u = 4.6258`; no test asserts those two strings, and the
     section's marker line (`sigma_UV = … 93.737`) and `203.562` are
     unchanged, so `test_section_runs_and_prints_its_number[section-24]`
     stays green.
2. **The CODATA constants are single-sourced as
   `kkgt.constants.HBAR / C_LIGHT / G_NEWTON / MPC_M`.** They were defined in
   `test_sections_17_28.py`, again in `test_sections_29_38.py` and again as
   `sections.py`'s module-level `_C`; `_C` and both test files now import
   them (same literals, no numeric change).
3. **The Planck-Λ formula is single-sourced as
   `kkgt.harness.lam_planck(h0, omega_l)`.** It existed as
   `sections.py::_LamP` (module level) and as a local `lam_planck` in
   `test_sections_17_28.py`; `_LamP` is now an alias of the harness function
   and the test imports it.
4. **`PHI_BAR`** is no longer re-declared as a class attribute of
   `TestSection25AutodualWindow`; the class uses `kkgt.constants.PHI_BAR`.
5. **No test id was renamed.** Every `\testref` target and every
   parametrized `[…]` node id keeps its exact name — the census pin
   (`test_testref_set_is_pinned`) and the manuscript's citations depend on
   them.

*Left for layer 2 (blocked by the "do not touch a section body" rule):* the
inline `phi = (1 + 5**0.5) / 2` recomputed inside 38 section bodies, and the
`HBAR_EVS` / `MPC_KM` / `LP_M` literals that the tests still hold locally
because the same literals sit inside section bodies.

## 5. Layer 2 — plan by lots (lots 0–2 applied; lots 3–7 pending)

`kkgt/sections.py` and a `kkgt/sections/` package cannot coexist, so the
first lot is structural and the last lot deletes the façade.

**Lot 0 — structure.** Create `tests/src/kkgt/sections/`, move the current
content of `sections.py` verbatim into `kkgt/sections/_rest.py`, add
`kkgt/sections/__init__.py` that assembles `SECCIONES` (numeric order) from
`_rest` plus whatever parts are already migrated, and delete
`tests/src/kkgt/sections.py`. Update, in the same commit,
`test_the_sections_live_in_the_package`'s path assertion (it is not cited)
and the docstrings that quote the old file. `kkgt.harness.load_sections()`
keeps returning a module named `kkgt.sections`, so `conftest.py` and the
census fixtures do not move yet.

**Lots 1–6 — the bodies.** Each lot cuts its `seccion_N` functions (and only
those) out of `_rest.py` into the module below, keeps every
`SECCIONES.append(...)` in the registry, runs the gates, and ticks the
lot's rows in §3.

| lot | sections | module | dependent tests | dependent claims |
|---:|---|---|---:|---:|
| 0 | — (shell) | `kkgt/sections/__init__.py` + `_rest.py` | 70 (all) | 136 (all) |
| 1 | 17–24 | `kkgt/sections/s17_24.py` | 4 | 0 |
| 2 | 9–16 | `kkgt/sections/s09_16.py` | 5 | 0 |
| 3 | 25–32 | `kkgt/sections/s25_32.py` | 5 | 19 |
| 4 | 41–46 | `kkgt/sections/s41_46.py` | 10 | 2 |
| 5 | 33–40 | `kkgt/sections/s33_40.py` | 17 | 68 |
| 6 | 1–8 | `kkgt/sections/s01_08.py` | 31 | 47 |
| 7 | — (close) | `_rest.py` deleted, registry complete | 70 | 136 |

The order above is by ascending risk (fewest dependent tests first); the
sequential order 1–8, 9–16, … is equally valid if reading order is preferred —
the ledger's target column is the same either way. If a lot goes red and the
cause is not obvious, split it in two at a section boundary and re-run the
gates; a lot is never "done" with a failing suite.

**Done — every one of these must hold when the migration closes:**

1. `find tests/src -name 'sections.py'` returns nothing: the file is deleted.
2. `grep -rn 'def seccion_' tests/src/kkgt/` matches only
   `kkgt/sections/*.py`; all 46 bodies are inside the six modules, and
   `SECCIONES` still yields 46 entries in numeric order
   (`test_forty_six_sections_in_order` green).
3. `tests/conftest.py` carries no branch that loads a module file:
   `grep -n 'load_sections\|sections.py' tests/conftest.py` returns nothing;
   the `sections_module` / `sections` / `run_section` fixtures import the
   `kkgt.sections` package directly. The only tests allowed to be edited for
   this are the uncited census ones
   (`test_the_sections_live_in_the_package` and, if the helper is dropped,
   `test_section_function_body_has_an_identity`).
4. This ledger shows **46 of 46** boxes ticked, one per lot commit.
5. Gates green: `uv run pytest tests/ -q` (533), `pnpm run type-check`,
   `grep -c '1776.93' tests/` → 0, `pnpm run build` never run (no `.tex`
   touched by this work).

Commit plan: one conventional commit per lot, in English, no push —
`refactor(tests): create the kkgt.sections package shell`,
`refactor(tests): move sections 17-24 into the sections package`, … ,
`refactor(tests): delete the sections module façade`.

## 6. Gaps

* **18 sections carry no test beyond the marker test**, so their rows show
  "0 claims": no `\testref` evidence would break if they moved, but nothing
  checks their numbers either (an AUD-001 finding, not something this
  migration changes).
* **36 claims appear on two rows** because the manuscript cites tests of two
  different sections in one sentence (e.g. `L1290` cites a section-6 and a
  section-7 test). The row cells are per-section; the totals in §2 are
  de-duplicated.
* **133 vs 136.** AUD-001 §10 counts 133 dependent cited claims via 20 tests;
  this ledger reaches the same 133 and adds the 3 claims that cite
  `test_section_writes_its_figure[section-39|44]`, which AUD-001 excluded
  from its 20 although the fixture runs those sections. Both numbers are
  stated so that neither is mistaken for the other.
* **`L2460 1.18` / `L2460 3.13`** are the software-version figures of the
  manuscript's environment note (current `main.tex` L2480: "Python 3.13 …
  SciPy 1.18.1"), pinned to `seccion_1`'s docstring because that is where the
  literals sit; they are not computed values.
* **Lots 0–2 are applied**: `tests/src/kkgt/sections.py` is gone, its content
  lives verbatim in `kkgt/sections/`; sections 9–16 are in `s09_16.py` and
  sections 17–24 in `s17_24.py`, and `kkgt/sections/__init__.py` assembles
  `SECCIONES` in numeric order. The other 30 functions are still in
  `_rest.py` (1 738 lines at lot 2).
