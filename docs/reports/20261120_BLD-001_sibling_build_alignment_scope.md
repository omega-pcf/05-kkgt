# Sibling build alignment — scope of the selfcitation propagation and of a generic entrypoint

| Field | Value |
|---|---|
| **id** | `BLD-001` |
| **title** | Sibling build alignment — scope of the selfcitation propagation and of a generic entrypoint |
| **status** | report only — nothing implemented; the decision is the author's |
| **date** | 2026-11-20 |
| **version** | 1.0 |

**Scope.** Read-only inventory of the five family repositories (`01-hilbert-polya`, `02-odd-zeta`,
`03-crystalline-worldsheet`, `04-mersenne-cr`, `05-kk-golden-throat`) at their 2026-11-20 `HEAD`s, plus `05`'s
`SPEC-001`, to bound two work items: (i) propagating the deterministic self-citation mechanism to
`01`/`03`/`04`, and (ii) pairing the figure and verification entrypoints behind a more generic entrypoint.
Evidence is `grep`/`cat`/`git log` output and content hashes (md5, 7–8 hex) of the shared files; no build,
test or generator was executed, and no file outside this report was written. `02` was read only (blocked for
edits).

## 1. Inventory per repo

### 1.1 `package.json` scripts

| script | 01 | 02 | 03 | 04 | 05 |
|---|---|---|---|---|---|
| `type-check` (`tsc --noEmit`) | ✓ | ✓ | ✓ | ✓ | ✓ |
| `generate:figures` | `uv run python scripts/figures/main.py` | same | same | `bash scripts/figures/build.sh` | `uv run python scripts/figures/main.py` |
| `generate:figures:list` | ✓ | ✓ | ✓ | — | ✓ |
| `figures` (alias) | — | — | — | — | ✓ |
| `generate:types` | — | ✓ | ✓ | — | ✓ |
| `verify:py` | `uv run python tests/verify_t_star.py` | `uv run python tests/verify_odd_zeta_pcf_unified.py` | `uv run python -m pytest tests/ -q -m 'not slow'` | **absent** | `uv run pytest tests/ -q -m 'not slow'` |
| `test` | — | — | `pytest -q` | — | `pytest -q` |
| `verify:lean` | `lake build` | `lake build` | `lake build CW6_complete_v2` | `lake build` | `lake build TorreKK_LYR_v35` |
| `selfcitations`, `selfcitations:check` | — | — | — | — | ✓ |
| `validate` | `verify` | `verify` | `verify` | `verify` | `selfcitations:check && verify` |
| `build`, `build:full`, `release`, `release:dry-run` | ✓ | ✓ | ✓ | ✓ | ✓ |

`packageManager` is `pnpm@9.0.0` and `.python-version` is `3.12` in all five; `pnpm-lock.yaml` exists in
`03`/`04`/`05` and is absent in `01`/`02` (SPEC-001 D-7). No repository has `.github/` — there is no CI
anywhere in the family.

### 1.2 Shared pipeline files (md5-8, five repos)

| file | 01 | 02 | 03 | 04 | 05 |
|---|---|---|---|---|---|
| `scripts/build.ts` | `42ed1172` | `42ed1172` | `42ed1172` | `42ed1172` | `9dda7971` |
| `scripts/tasks/compile.ts` | `3bc28956` | `3bc28956` | `3bc28956` | `3bc28956` | `aceed4f8` |
| `scripts/tasks/citation.ts` | `2ad00587` | `19edf85e` | `2ad00587` | `2ad00587` | `7789096f` |
| `scripts/tasks/checksums.ts` | `8ed77fca` | `8ed77fca` | `8ed77fca` | `8ed77fca` | `8ed77fca` |
| `scripts/tasks/cleanup.ts` | `19efaa43` | `19efaa43` | `19efaa43` | `19efaa43` | `19efaa43` |
| `scripts/tasks/selfcitations.ts` | — | — | — | — | 420 lines |
| `scripts/generate_types.ts` | `9b7949e` | `9b7949e` | `9b7949e` | `9b7949e` | `91e1da0` |
| `.release-it.ts` | `a3921c7` | `914f341` | `a3921c7` | `6ef7d3b` | `6ef7d3b` |
| `tsconfig.json` / `.latexmkrc` | identical 5/5 (`59de0d8` / `f6b82a4`) | | | | |

`scripts/utils/git.ts` and `scripts/types.ts` (73 416 bytes) are identical 5/5.

### 1.3 Figures

| | 01 | 02 | 03 | 04 | 05 |
|---|---|---|---|---|---|
| mechanism | `main.py` + `generators/` (28 generator modules + `registry.py`) | same shell, `generators/` empty | `main.py` delegating to `CW3_all_figures.py` + `CW3_gue_figures.py`, explicit `GENERATORS` list | `build.sh` running `pdflatex` in Docker over `scripts/figures/*.tex` | `main.py` + `generators/` (`rc.py`, `registry.py`, `v134.py`) + `figuras_v134.py` |
| committed artifacts | 28 PDF + 27 SVG + 1 PNG | **0** (`images/` empty) | 8 PDF | 1 PDF | 5 PDF |
| `SOURCE_DATE_EPOCH` | `scripts/figures/utils/__init__.py` | none | default `1794274263` in `main.py` | default in `build.sh` | `generators/rc.py` |
| byte pin of artifacts | — | — | — | — | `FIGURE_MD5` in `tests/src/kkgt/constants.py` + `harness.py` + census test |
| figure docs | `docs/figures.md`, `scripts/figures/README.md` | only `scripts/figures/README.md` | both | only `docs/figures.md` | only `docs/figures.md` |
| figures regenerated at release | ✓ (`after:bump`) | **—** | ✓ | ✓ | ✓ |

### 1.4 Verification

| | 01 | 02 | 03 | 04 | 05 |
|---|---|---|---|---|---|
| `verify:py` shape | one script | one script | pytest, `-m 'not slow'` | absent (`verify` = Lean only) | pytest, `-m 'not slow'` |
| `[tool.pytest.ini_options]` | — | — | `testpaths`, `pythonpath`, 6 markers, `addopts = "-v --tb=short -p no:cacheprovider"` | — | `testpaths`, `pythonpath`, 3 markers, `addopts = "--tb=short -p no:cacheprovider"` |
| suite | 0 `test_*` (1 script) | 0 (1 script) | 13 files / 262 `def test_*` (README: 570 tests, ~25 s) | empty (`tests/README.md` only) | 9 files / 255 `def test_*` (README: 499 tests, ~35 s) |
| tests touching `images/` | — | — | — | — | ✓ (census + harness pins) |
| `verify:lean` scope | all libs in `lakefile.toml` (`pcf`, `PCF_Complete_v11_Unified`, `PCF_OperatorConvergence`) | all 11 libs (incl. a copy of `03`'s `CW6_complete_v2`) | one named target | all libs (`mersenne-cr`, `golden_mersenne`) | one named target |
| `type-check` | identical 5/5 | | | | |

## 2. Concrete divergences (30 rows: A 8, B 5, C 6, D 5, E 6)

**A — `package.json` script contract (8).** A1 `figures` alias (05 only) · A2
`selfcitations`/`selfcitations:check` (05 only) · A3 `validate` chain (05 runs the check first) · A4 `test`
(03, 05) · A5 `generate:types` (02, 03, 05; the file exists in all five) · A6 `generate:figures:list` (missing
in 04) · A7 `verify:py` (missing in 04) · A8 `verify:py` command (standalone script vs `pytest -m 'not slow'`
vs absent).

**B — shared pipeline files (5).** B1 `build.ts`: `05` adds the `syncSelfCitations` import, the call between
`syncCitationMetadata` and `compilePDF`, and one log line (10 diff lines vs the byte-identical 01–04 copy). B2
`compile.ts`: `05` passes `TZ=CST6`, the others `TZ=UTC`, so `\today` resolves differently for the same commit
(`SOURCE_DATE_EPOCH` is honoured everywhere). B3 `citation.ts`: three variants — `01/03/04` (positional key
rewrite + UTC `date-released`), `02` (pre-`1e7b085` naive global key replace, i.e. the duplicate-key bug is
still present), `05` (positional rewrite + `TZ=CST6` date). B4 `generate_types.ts`: only `05` re-emits the
hand-written `ReleaseConfig` tail that `build.ts`/`compile.ts`/`checksums.ts` import from `scripts/types.ts`;
running `generate:types` in `01`–`04` as written would drop that interface (read from code, not executed). B5
`.release-it.ts`: `02` lacks the `after:bump → generate:figures` hook and the `pyproject.toml` version bump;
`01/03` vs `04/05` differ only in comments. Controls: `checksums.ts`, `cleanup.ts`, `tsconfig.json`,
`.latexmkrc` are identical 5/5.

**C — figures (6).** C1 four distinct mechanisms (registry modules / vestigial registry / single-file
matplotlib / Docker pdfTeX). C2 inventory 28 · 0 · 8 · 1 · 5 figures, mixed PDF+SVG vs PDF only. C3
determinism pin lives in four different places, and `02` pins nothing (it renders nothing). C4 artifact
byte-pinning exists only in `05` (`FIGURE_MD5`); `01`/`03`/`04` tests never mention `images/`. C5 figure docs
are split (`docs/figures.md` missing in `02`; `scripts/figures/README.md` missing in `04`/`05`). C6 output
contract differs: `03` `chdir`s into `images/` and writes relative to the CWD, `01`/`05` resolve
`<root>/images` explicitly, `04` uses `-output-directory` inside Docker.

**D — verification (5).** D1 pytest configuration exists only in `03`/`05` and their `addopts` differ. D2
suite scale and markers differ (1 script · 1 script · 262/570 · none · 255/499; markers 0/0/6/0/3). D3
`verify:lean` scope differs (build-everything vs one named target); `02`'s `lakefile.toml` lists eleven
libraries including a copy of `03`'s. D4 only `05` verifies the committed figure bytes from the suite. D5 no
CI in any repo, so nothing enforces family parity automatically (the `type-check` contract is the one
verification control that already holds 5/5).

**E — selfcitations (6).** E1 `scripts/tasks/selfcitations.ts` exists only in `05`. E2 README marker pairs
(`id="badge"`, `id="citation"`) exist only in `05` (`grep -c 'selfcite:begin' README.md` = 2 there, 0
elsewhere). E3 the `main.tex` pair `id="version"` exists only in `05` (added 2026-11-16 by `2488097`); the
printed token is present in `01` (`v2.5.4`, line 112), `03` (`v1.2.1`, line 194), `04` (`v0.3.20`, line 108),
`05` (`v0.1.0`, line 156) and **absent in `02`** (its `\date` at line 113 prints only received/last-modified).
E4 `metadata.citationKey` (required input of `loadData()`, `selfcitations.ts:98`) exists only in `05`
(`Gonzalez2026KKGoldenThroat`). E5 `SPEC-001` lives only under `05/docs/specs/`. E6 the derived-files table of
`docs/citations.md` (line 27) does not list `README.md` in **any** repo — SPEC-001 AC-10 is unmet even in `05`
(its `docs/README.md` index of `specs/` is the satisfied half).

## 3. Scope of the selfcitation propagation

What `05` has (phase 0 of SPEC-001, plus one extension): the 420-line task rendering the README
`badge`/`citation` regions from `CITATION.cff` + `metadata.citationKey` (no citation.js, no lockfile
dependency), a `main.tex` region that keeps the printed `vX.Y.Z` equal to `package.json`, rewrite and
`--check` modes, the `build.ts` hook, the two `package.json` scripts, and the `validate` chain. The `main.tex`
region is **not** in SPEC-001 (§8 puts `main.tex` bylines out of scope): it is a post-spec extension that must
be consciously accepted or dropped per repo.

| SPEC-001 phase | repo | state at 2026-11-20 | remaining work |
|---|---|---|---|
| 0 | `05` | script + README markers + hook + gate + `docs/README.md` index done | AC-10 half: add the `README.md` row to `docs/citations.md` derived table |
| 1 | `03` | not started (0 markers) | `citationKey: CW6`; copy task; 2 scripts; `validate`; `build.ts` hook; 2 README pairs (block then regenerates `Zenodo.`→`Preprint.`, `journal={Zenodo}`→`{Preprint}`, key `CW6` unchanged); 2 `main.tex` lines around `\date` (token `v1.2.1` exists); docs row |
| 2 | `02` | not started; **read-only / blocked** | as above with `citationKey: Gonzalez2026OddZeta`; regenerating fixes D-4 (`L. M}`); **decision needed**: no version token in `main.tex` at all — add one, or exempt `02` from the `id="version"` region |
| 3 | `01` | not started | as above with `citationKey: Gonzalez2026HilbertPolya`; regeneration fixes D-2 (LaTeX `--`/`$\mathbb{F}_1$` leaking into prose, since the block re-renders the identity title); token `v2.5.4` exists |
| 4 | `04` | not started; DOI prerequisite **already satisfied** | as above with `citationKey: Gonzalez2026MersenneCR`; SPEC-001's D-1 is stale — `a0454a6` (2026-11-16) left one concept DOI `10.5281/zenodo.21681394` in README, `CITATION.cff`, `package.json` and `main.tex` (measured), so AC-5 now passes in all four DOI repos |
| 5 | scaffold | not started; no family-level scaffold repository exists on this disk | new repos born with task + markers + scripts + hook + gate |

Gates per phase (SPEC-001 §7, verbatim commands): AC-1 idempotence, AC-2 check catches hand edits, AC-3 build
does not churn `README.md`, AC-4 cross-sibling hash of the block modulo four variable strings, AC-5 single DOI
per repo, AC-6 marker count = 2, AC-7 `type-check`, AC-8 no clock in regions, AC-9 DOI-less branch, AC-10
docs; plus `pnpm run validate` and `git diff --exit-code -- images/` to prove the figure artifacts were not
touched. Estimated files per sibling: 7 (`scripts/tasks/selfcitations.ts`, `package.json`, `README.md`,
`main.tex`, `scripts/build.ts`, `docs/citations.md`, optional `docs/specs/` copy or a link to `05`'s
SPEC-001).

## 4. Options for a generic entrypoint

**Option A — identical contract per repo + parity gate.** Every repo exposes the same script names and the
same task set (`build`, `verify`, `validate`, `figures`, `selfcitations*`), configuration stays local, and a
parity check (a small `scripts/tasks/parity.ts` plus a pinned manifest of md5s for the files that must be
byte-identical: `build.ts`, `checksums.ts`, `cleanup.ts`, `tsconfig.json`, `.latexmkrc`) fails `validate` when
a repo drifts. + Lowest risk: no cross-repo plumbing, every repo keeps its own lockfile and release, drift
becomes loud instead of silent. − Manifest updates are manual; it detects divergence but does not remove it,
and it does not by itself unify figure or verification semantics.

**Option B — shared package (pnpm workspace / common folder) with adapters.** One implementation of the tasks,
imported by each repo through a thin adapter. + Single source of truth; a fix lands once. − The five repos are
independent git repositories with independent releases and no common root exists on this disk, so the
workspace would have to be a sixth repository or a vendored copy; `01`/`02` have no `pnpm-lock.yaml` (D-7), so
a shared dependency would make their builds less reproducible, not more; a shared-code change can alter the
rendered PDFs and the byte-stable figures of published repos at once; it breaks the `git archive`
sibling-scaffold flow SPEC-001 §6.2 relies on.

**Option C — hybrid: contract + local adapters (recommended, non-binding).** Option A's contract and parity
gate, plus an explicit *interface* each adapter must satisfy rather than a shared implementation:
`generate:figures` must exist, be deterministic (explicit `SOURCE_DATE_EPOCH` default) and leave `images/`
unchanged when re-run; `verify` must exist and exit 0 with a documented command recorded in `tests/README.md`;
`selfcitations:check` must be in `validate`; figure byte-pins are required only where `images/` is non-empty.
+ Fixes the semantics Víctor named (one command meaning the same thing everywhere) while keeping per-repo
engines (matplotlib vs pdfTeX vs none) and per-repo test stacks (script vs pytest); every step is reversible
per repo. − Two artefacts to maintain (manifest + interface doc); does not deduplicate code, so `02`'s stale
`citation.ts` and `04`'s absent `verify:py` still need their own small fixes.

**What must not change under any option:** rendered PDFs and their `SOURCE_DATE_EPOCH` handling; committed
figure bytes (`images/`, pins `1794274263` where set); the citation regions' variable strings (title, authors,
DOI/URL, key — `03` keeps `CW6`); per-repo citation keys and DOIs; the region-scoped write discipline (outside
the markers is untouched by construction); the family rule of one conventional commit per repo with no
tag/release during rollout.

**Working recommendation (non-binding):** Option C, adopting Option A's identical files + parity manifest
first, because it is the only option that can be landed repo-by-repo without touching published artifacts;
Option B should be reconsidered only if a family-level repository is created.

## 5. Estimated phasing

| phase | content | files | commits | gates |
|---|---|---|---|---|
| P0 | contract + parity manifest piloted in `05` (script, manifest, `validate` wiring, contract section in `docs/` or a spec) | 3–4 in `05` | 1 | `type-check`, `validate`, `selfcitations:check` |
| P1 | selfcitations → `03` (SPEC-001 phase 1) | 7 | 1 | AC-1…AC-10, `validate`, `git diff --exit-code -- images/` |
| P2 | selfcitations → `02` (phase 2; **blocked** until the repo is unblocked; needs the Version-token decision) | 7 | 1 | same |
| P3 | selfcitations → `01` (phase 3) | 7 | 1 | same |
| P4 | selfcitations → `04` (phase 4; DOI prerequisite already met) | 7 | 1 | same |
| P5 | parity manifest + contract conformance in `01`–`04` (script names, shared-file hashes, `validate` chain) | 2–3 per repo | 4 | `validate` fails on a deliberately perturbed file, then passes |
| P6 | figures alignment where adopted (alias, output contract, hash pins, docs rows) | 1–3 per repo | 0–4 (optional) | figure regeneration leaves `images/` byte-identical |
| P7 | verification alignment where adopted (`verify:py` for `04`, pytest config or documented script contract, `verify:lean` target scope) | 1–3 per repo | 0–3 (optional) | `verify`, `test` where present |

Totals: **8 phases, 9 commits mandatory (P0–P5), up to 16 with optional P6/P7 adoption.** SPEC-001 phase 5
(scaffold) is excluded: no scaffold repository exists on this disk.

## 6. Risks and invariants

- **Byte stability first.** Any edit to `compile.ts`, `citation.ts` or `generate_types.ts` while aligning them can move printed dates (`TZ=CST6` vs `TZ=UTC`), `date-released` or the generated `.bib` keys → re-rendered PDFs; align those three files only with an explicit decision on which variant wins.
- **`generate:types` hazard (B4):** in `01`–`04` it would strip `ReleaseConfig` and break `type-check`; porting `05`'s tail is a one-file fix but changes a shared file hash in the manifest.
- **`02` is blocked and behind:** on branch `scratch/lean-release`, dirty, with the pre-fix `citation.ts`; propagation there waits for the author.
- **Dirty trees:** `01`, `03`, `04` show dozens of modified tracked files at `HEAD` (cause not investigated); `05` shows two (`.zenodo.json`, `CITATION.cff`). Propagation commits must stage only their own files.
- **No CI:** the parity gate only runs when someone runs `validate`.
- **Not touched under any phase:** PDFs, figure artifacts, citation-region variable strings, DOIs/keys, `SOURCE_DATE_EPOCH` values, release/tag policy, `02`.

## 7. Gaps

1. SPEC-001's defect list is partly stale (D-1 fixed by `a0454a6`); its phase table and AC-5 need re-validation before phases 1–4 are executed.
2. The `main.tex` version region is an undocumented extension of SPEC-001; whether to port it — and what `02` does without a version token — is an open decision.
3. AC-10 is unmet even in `05` (`docs/citations.md` derived table lacks `README.md`); `SPEC-002` is also not indexed in `docs/README.md`.
4. This report does not appear in the `docs/reports/README.md` index (write scope was limited to this file; that index has not listed anything after `SEC-001` since 2026-11-16).
5. No family-level/scaffold repository was found on this disk, so Option B and SPEC-001 phase 5 have no host today.
6. Nothing was executed: `generate:types` behaviour (B4), suite counts and AC-1…AC-10 are read from source and documentation, not from a run; `03`'s README quote of 570 tests was not reconciled with the 262 `def test_*` found.
7. Whether figure byte-pins (`FIGURE_MD5`) should become a family requirement for `01` (28 figures) and `03` (8) is left open — it changes their test suites.
