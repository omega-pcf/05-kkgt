# SPEC-002 — Target architecture for the test suite: eliminate the sections package

- Status: **Revised 2026-11-17** after operator clarification (supersedes the co-location draft of the same date, which wrongly kept `SECCIONES`/`run_section` alive as an index).
- Decided by: the operator. The standing instruction, repeated across sessions, was to **migrate out of `sections.py` entirely** — the provenance pytest copied verbatim from `reproduce_vNNN.py` — into the project's own test structure, reconciling each test against the manuscript.
- Companion: `docs/reports/20261117_PYT-001_numerical_testing_contrast.md` (rows C1–C3 = *eliminate*), `docs/reports/20261116_AUD-001_claim_test_matrix.md` (claim → test map), `docs/reports/20261116_SEC-001_sections_migration.md` (superseded lotes plan).

## 1. Requirement (the whole point, stated once)

**No module may import anything from `kkgt.sections` (any file of the package) or from any `seccion_*` function.** The package, the registry, the marker driver and the stdout fixture are eliminated, not reorganised.

1. **Computations move into the tests that assert them** — with one carve-out decided by the operator: **figure generation is not a test concern**. Code that *writes* a figure lives in the figure generators (`scripts/figures`, entry point `pnpm run figures`); tests only *verify* artifacts (file present, bytes/hash stable, caption cites it). Tests and generators are disconnected structures — a test never produces a figure. For everything else, each claim test owns the code that produces its numbers and asserts those values directly — no stdout to parse, no shared runner (this dissolves the stdout contract test-by-test; `capsys` stays available only for tests that must assert *printed* output, which after migration is none).
2. **The provenance surface dies with the package**: `MARKERS` dict, `test_section_runs` driver, `SECCIONES` registry with `SECCIONES.append(...)`, `run_section` fixture, `__main__` entry point, module-level mutable lists. Their assertions migrate into the claim tests (or into bring-up entries where no assertion exists yet — AUD-001's19 unasserted figures).
3. **Shared code that survives** lives only in neutral helpers: `constants.py` (single origin for numbers) and `harness.py` (generic utilities) — both must shed every import of the sections package.
4. **Code style of migrated code** (standing conventions, applied as each block moves): **English identifiers** (`SECCIONES`, `seccion_*` die with the package), type annotations on every function signature, imports at module level only (no in-function imports), no duplicated literals outside `constants.py`.

## 2. Facts that make the migration safe (verified 2026-11-17)

- **0 of the 99 `\testref` anchors** cite the marker driver (`grep 'testref{test_section_runs' = 0`): the driver and registry can be deleted without touching the paper's anchors.
- **5 cited anchors** live in the figure census: `test_section_writes_its_figure[section-10|13|39|41|44]` — these ids are frozen: the test keeps its name and its `[section-NN]` ids (explicit `pytest.param(id=…)`). Their **bodies change** from "run the section and observe a file appear" to **artifact verification only** (existence/hash/caption), because generation moves to `scripts/figures` (§1.1).
- **19 files** currently reference the package (conftest, `constants`, `harness`, `kkgt/__init__`, the package itself, census, driver, and all8 claim-test files): each is a migration unit.
- Cited claim tests are **named functions** (`test_koide_scale_and_unit`, …): their names never move; only their bodies grow to own their computations.

## 3. Guards

- `\testref` set stays **99**; the exact-equality pin stays (any change to the set requires the author's decision, as before).
- **No assertion is relaxed, no figure invented.** A computation that cannot yet be located for a test goes to **bring-up** with the reason — never back into a shared file.
- **Census is rewritten with the structure**: tests that police the package (`…_sections_in_order`, `…_live_in_the_package`, `…_body_has_an_identity`, `…_is_callable`, `titles_are_unique`) are replaced by a **no-import contract test** (AST scan: no `import`/`from` may resolve to `kkgt.sections`) so the artifact cannot return; the figure ids above keep their names. Gate count may change; the change is declared in the same commit.
- Gates per commit: `uv run pytest tests/ -q` (550+), `pnpm run type-check`0, `build` at wave close; no `lake` inside this work.

## 4. Execution order (reconciliation is per test, not per file)

1. **Figure cluster** (5 cited ids): move each figure-writing computation from `seccion_N` into the **generators** (`scripts/figures`); the cited tests become artifact verifiers (ids frozen); regeneration stays byte-stable through `pnpm run figures`.
2. **Claim clusters** in AUD-001 order of risk: the8 `test_sections_*` files, one module at a time — each module ends with *zero* imports of the package, its assertions on values (not stdout), and a green `pytest` run.
3. **Delete** the package, driver, fixture, `MARKERS`; rewrite census; add the no-import contract test.
4. **Close** SEC-001 ledger with a pointer here; regenerate `tests/README` map (no `sections/` rows).

## 5. Done

- [ ] `tests/src/kkgt/sections/` does not exist; `grep -rn 'kkgt.sections\|seccion_' tests/` returns only the no-import contract test's own literals.
- [ ] No test parses section stdout; no module-level mutable registries; no `SECCIONES.append`.
- [ ] Every migrated function: English name, annotated signature, module-level imports.
- [ ] All47 sections' outputs are either asserted by a named claim test or listed as bring-up in AUD-001/TST-001.
- [ ] Census green (declared count), `\testref`=99, gates green, `tests/README` regenerated.
