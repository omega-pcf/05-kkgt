# DEC-002 — the principal author's open decisions, reconciled

| Field | Value |
|---|---|
| **id** | `DEC-002` |
| **title** | Every decision of the principal author still open, reconciled across the reports of 2026-11-15 → 2026-11-17 |
| **status** | report only — this file is the only thing staged; no manuscript, test, script or Lean file touched |
| **date** | 2026-11-17 |
| **version** | 1.0 |
| **repository** | `05-kk-golden-throat` (public as `omega-pcf/05-kkgt`), HEAD `989f2dc`, clean tree |
| **sources** | `DEC-001`, `AUD-001`, `CIT-001`, `CIT-002`, `TST-001`, `MRG-001` (W1/W3/W4/W6), `FIG-001`, `PYT-001`, `PRF-001`, `docs/specs/20261117_SPEC-002_sections_co_location.md`, `docs/witness-contract.md` |
| **method** | each row was re-checked against the working tree with `grep` and `git log` at HEAD `989f2dc`; a decision appears only while its defect is still on disk |

**Scope.** One row per decision only the principal author can take, grouped by theme,
quoted as `id · decision · verified state · source § · suggested action`. Anything a
later commit already closed is not listed; those items are counted in §10. Line numbers
are the current `main.tex`; anchors were verified by literal because the manuscript is
edited concurrently. Counts by theme are in §9.

---

## 1. Witnesses and the alphabet (4)

- **W-01** · Euler characteristic mark (L966) · ours carries a bare `\cite{Ser71}` while theirs tagged `N` · `MRG-001 §W1.7-1` · queue `N[\testref{test_the_chain_of_twelves}]` and its census line in one pass that owns `main.tex` and `tests/`, or leave it bare.
- **W-02** · mark for `$\Gamma\propto x^{3}$` (L1408) · bare `\cite{DHR00}`, the literal W1 rule and §8.3 disagree · `MRG-001 §W1.7-2` · choose `[P] in~\cite{DHR00}`, `[N]~\cite{DHR00}` or the bare citation.
- **W-03** · marks for the section-47 perfect-tensor and Mumford `p=2` sentences · `Mar18` sits in `src/bibliography.bib:1199` and is cited **0** times in `main.tex`; the block was never ported · `MRG-001 §W1.7-3`, `§W3.6-4` · decide *prose, no mark* (the recorded target) when the pentagon block lands.
- **W-04** · ratify the front matter not ported (their legend `P, P*, N, L, R`, one-argument `\tier`, removal of the 99 anchors and 12 labels, their date) · ours stands: legend `main.tex:253-258` defines `P`/`N` only, `\date{261116; last modified \today; v0.1.0}` at `:155`, `\testref{` = 99, `\tier{L}`/`\tier{R}` = 0 · `MRG-001 §W1.8` · confirm ours, or list which of the four to adopt.

## 2. Citations (8)

- **C-01** · `LYR26` version and the sentence at L698 · the quadruplet at `main.tex:690` is unversioned and `\cite{LYR26} quotes no mass errors for the graviton candidates` survives at `:698`, against the source's own `700±20` · `CIT-002 §9-1` · pin `arXiv:2610.31458v1`/`v2`, restate `380, 700, 1000, 1300`, or add a version note — and correct or qualify L698.
- **C-02** · split `PYHP15` · `main.tex:1745` still attaches `1.49 S` to `\cite{PYHP15}`, a figure this repository computes (`1.4907`) · `CIT-002 §9-2` · re-attribute `1.49` to a `\testref` and keep the key for the tiling, or drop `1.49` from the cited claim.
- **C-03** · `CW6` cross-references · `(81)--(82)` (`:880`), `Appendix~A.1, eqs.~(158)--(159)` (`:888`), `(160)` (`:891`), `eq.~(31)` (`:904`), `Proposition~2.24` (`:916`, `:1546`) are all still on disk; no single record version carries them · `CIT-002 §9-3`, `§4` · re-point per the served record (`(81)→(4.26)`, `(31)→(2.21)`, `A.1→A.7`, `Prop. 2.24→Remark 2.24`) or pin the version and accept the labels it breaks.
- **C-04** · source for the Planck masses · `main.tex:1643` still rides `1.2209×10^{19}` and `2.435×10^{18}` on `RS99`; no `PDG` string exists in `main.tex` or `src/bibliography.bib` · `CIT-002 §9-4` · add a PDG key at L1643 and state the reduced value as `M_Pl/√(8π)`.
- **C-05** · `Pol98` (`D=c=26`, §§1.3/7.3) · `pending`: every route of `CIT-002 §6` failed (no preview, no lending copy) · `CIT-002 §9-5` · supply a print/preview copy or accept the documented `pending`.
- **C-06** · `Hux03` wording · `main.tex:1759` still reads `differs from its area by an error of lower order`; the abstract supports the substance, not the words · `CIT-002 §9-7` · keep, reword to the abstract's phrasing, or obtain the article text.
- **C-07** · the ten AUD-001 §3 rows · none retargeted: `test_the_windows_of_the_panel_cast_their_shadows` is cited **0** times in `main.tex` although the caption at `:661` prints `19,61,127` · `CIT-002 §9-6`, `AUD-001 §12-2/3` · per row, assert it, retarget its anchor, or mark the figure external data (row 3 = C-04).
- **C-08** · two housekeeping calls · `_rest.py:200` still prints the stale label `11.835` (print and manuscript say `11.834`), and the last legs/S entry is printed `2.415` as `2.42` · `CIT-002 §9-6` · fix the label, and fix the rounding convention (half-up or half-even) or print `2.415`.

## 3. Numbers and retargets (8)

- **N-01** · split the 45 rows sitting on 12 anchors · only four retargets landed (`7a0eb17`); `\testref{` is still **99**, so one anchor cannot name two tests · `MRG-001 §W4.4(a)`, `AUD-001 §12-7` · authorise the pinned set to move, then split the ties.
- **N-02** · the trade of §W4.3 (four claims moved `a → d`) · the four anchors were substituted and `~10^{-4}`, `0.997`, `1.4 %`/`15 GeV`, `2.73, 2.50, 2.44` now carry no `\testref` · `MRG-001 §W4.3` · confirm the de-citing or restore one anchor each (splitting, again N-01).
- **N-03** · six rows whose destination does not assert the line's figure (`4.3`, `±1` ×3, `1.9`, `3.5`) · no commit since W4 changed them · `MRG-001 §W4.4(c)` · pick a test that really asserts the figure or reword the sentence.
- **N-04** · publish class `d` (94 rows: asserted, never cited) · untouched since the audit · `AUD-001 §12-6` · move each `\testref` to the asserting test with its census pin in the same pass.
- **N-05** · class `c` (24 rows, 13 marked `NO`) · untouched; `TST-001 §6-5` records it as open · `AUD-001 §12-5` · assert each figure or mark it cited external data.
- **N-06** · tolerance policy in standard form, and `about 15 GeV` · no central helper exists (`PYT-001` C6); `main.tex:1611` still says `about $15$~GeV` guarded by `abs=1` · `PYT-001 §3/§5`, `TST-001 §6-7` · write one `pytest.approx(rel, abs=0.5·10⁻ᵈ)` helper; pin a decimal in the sentence or keep `abs=1`.
- **N-07** · `11.97` vs `11.98` · ours stands on disk (`$11.97$ (\eqref{eq:sigmaIR})`, six tests at `abs=5e-3`) · `MRG-001 §W3.6-1` · accept ours, or run the four-step rework the plan spells out.
- **N-08** · three non-ported numerals — `2000 spacings`, `1.07 levels down`, the `T0` paragraph · none of the three strings occurs in `main.tex`; the paragraph carries our `1.00000` at `:1704` · `MRG-001 §W3.6-2/3/5`, `TST-001 §6-2` · supply the source for each or accept our text permanently.

## 4. Figures (3)

- **F-01** · the two caption-anchored rows (`±1` at L647, `0.9757` at L1702) · `main.tex:661` still cites only `test_section_writes_its_figure[section-44]`; the census guard `test_every_figure_caption_cites_the_test_that_writes_it` is green and forbids the substitution · `MRG-001 §W4.4(b)` · split the citation inside the caption or leave both rows where they are.
- **F-02** · golden-figure tooling · figures are compared by bespoke md5/regeneration plumbing; `pytest-regressions` `file_regression`/`image_regression` is the FOSS equivalent · `PYT-001 §3 (C8)` · adopt the fixture at phase 2 or keep the bespoke pipeline.
- **F-03** · continuous supervision of figures and suite · gates run only by hand; byte-stability of the five PDFs is a local event · `PYT-001 §3/§5 (CI gap)` · add a workflow that runs `generate:figures` twice plus `pytest`, or accept the manual gate.

## 5. Censos and guards (4)

- **G-01** · the `reproduce` word ban versus the author's verb · `main.tex` carries **0** occurrences of `reproduce`, i.e. his terminology stayed out; seven sites are queued behind the call · `MRG-001 §W3.5/§W3.6-7` · relax the census rule for the verb or keep the ban.
- **G-02** · citation pins for the new tests · the suite is 550/546 while the newest tests are cited by nobody, and `test_testref_set_is_pinned` asserts exact equality · `TST-001 §6-6` · add each `\testref` together with its pin line, or leave the tests uncited.
- **G-03** · the census rewrite of SPEC-002 · five policing tests are to be replaced by one AST no-import contract test, which changes the declared gate count · `SPEC-002 §3` · sign off the count change declared in the same commit.
- **G-04** · the counting slip in `TST-001 §6-4` · the file still reads "the other nineteen AUD-001 rows" while enumerating ten · `CIT-002 §9-8` · correct the word to *ten*.

## 6. Lean (4)

- **L-01** · ratify the two `set_option` deviations from the author's §4 · `longLine false` at `v35:31` and `maxRecDepth 100000` at `v35:528` are both in the green build; dropping them means 17 long-line warnings and a red `pisano_orders` · `MRG-001 §W6.6` · keep both (recommended) or reopen them.
- **L-02** · Spanish docstrings in `v35` against the English prose of the repository · the file header and 173 doc blocks are Spanish, by the author's own §4 instruction · `MRG-001 §W6.6` · keep the author's language or translate in a later pass.
- **L-03** · `pentagon_side_golden` uncited · the declaration exists (164 theorems) and `main.tex` cites it **0** times · `MRG-001 §W6.6`, `§W1.7-4` · cite it with the pentagon block (W-03), which is no longer blocked.
- **L-04** · the mechanical performance pass · `import Mathlib` is still one line (`v35:28`) and 23 bare `simp` remain; all `.lean` edits await his word, and `native_decide`, `decide +native` and a bare `maxHeartbeats` raise stay red lines · `PRF-001 §5.1/§6` · give (or withhold) the go-ahead for M21 + M1–M20; D1–D2 only if a fresh profile shows a slow declaration.

## 7. Release (2)

- **R-01** · cut `v0.1.0` (or hold) · the date line claims `v0.1.0`, the repository has **no** git tag, and `README.md` states that releases, tags and GitHub publication are never executed without an explicit instruction · `README.md` §Release, `main.tex:155` · instruct `pnpm run release`, or move the version out of the date line until he does.
- **R-02** · propagate the witness convention to the sibling repositories · this repository renders `P`/`N`; propagation is declared an editorial decision of each repository's author · `docs/witness-contract.md §8.2` · decide which siblings adopt the marks and the §8.5 criterion.

## 8. SPEC-002 — what needs a decision between units (3)

- **S-01** · freeze the cited node-ids · **0** occurrences of `pytest.param(id=` in `tests/`; the 99 `\testref` ids derive from parameter reprs, so a refactor silently breaks the paper · `PYT-001 §3 (C5), §5 phase 1` · freeze every cited id before the migration starts.
- **S-02** · assertion rewriting across the package boundary · `register_assert_rewrite` appears **0** times, so `tests/src/kkgt/` gets no pytest failure diffs · `PYT-001 §4-3, §5` · register `kkgt` now (one line) or drop the layer at phase 2 — one of the two, not neither.
- **S-03** · migration units and their guards · 19 files import the package; the plan fixes the order (figure cluster → claim clusters → delete) and keeps `\testref` = 99 unless he decides otherwise · `SPEC-002 §1-§4` · confirm the order and the rule that any change to the anchor set is his decision alone.

## 9. Counts by theme

| Theme | Open rows |
|---|---|
| Witnesses and the alphabet | 4 |
| Citations | 8 |
| Numbers and retargets | 8 |
| Figures | 3 |
| Censos and guards | 4 |
| Lean | 4 |
| Release | 2 |
| SPEC-002 | 3 |
| **total** | **36** |

The three most delicate: **N-01** (splitting the ties moves the pinned anchor set, so
`main.tex`, the census and the suite must change in one pass), **C-03** (no single
`CW6` record version carries the note's cross-references, so every option rewrites
scholarship rather than text), **C-01** (the sentence at L698 asserts the opposite of
what the cited source prints).

## 10. Closed since the sources were written — discarded (12)

Verified in git, not taken from the reports' prose: W6 and its three gaps (v35 in the
toolchain, 0 errors, 6 axioms — `3b42e98`, `989f2dc`); SPEC-002 unit 1, figures moved
to `scripts/figures` (`567bb40`, `61cae24`, `8672074`); the release-date zone of
`citation.ts` (`f480e80`); the CIT-002 record itself (`9a987f3`); the `binEntropy_half`
rename (`9f79ae5`); `TST-001 §6-1` port of `seccion_47` and `§6-3` counters, now
`550/546` at `main.tex:2507` and `README.md:60` (`1bd9c9f`, `c32b70f`); all ten
`DEC-001 §5` rows (e.g. `test_the_planck_level_is_2_2_to_3_1_sigma_from_584` cited at
`main.tex:2068`); `CIT-001`'s two pendings and three snippet verdicts (`Bha75`, `Wat44`,
`GW99`, `Hux03` upgraded in CIT-002); the elimination of `L` and `R` and the retirement
of `\Lean{}` (0 occurrences of each); the stale README path (`32da3f1`, `README.md:59`);
the `m_τ` divergence and the five missing asserts (`AUD-001 §12-4/8`, closed by
`TST-001 §1-§2`).

## 11. Gaps of this report

Row-by-row class tables of `AUD-001` (classes `c`/`d`) are counted, not re-enumerated;
`L###` line numbers of the sources belong to the audited snapshot `8e101f5` and were
re-anchored by literal; no suite, build or `lake` run is claimed — verification was
`grep` and `git log` only; and the two style-guide commits named in the brief
(`ba04148`, `2560318`) do not exist in this repository (`git show` → unknown
revision), so no row rests on them.
