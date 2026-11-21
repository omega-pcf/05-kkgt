# CVR-001 — coverage review of the build standardisation migration

| Field | Value |
|---|---|
| **id** | `CVR-001` |
| **title** | Coverage review of the sibling build standardisation (SPEC-004 and the 30 divergences of BLD-001) against the five repositories |
| **status** | report only — no source, spec or test file modified; one report file and its index row |
| **date** | 2026-11-20 |
| **version** | 1.0 |
| **repository** | `05-kk-golden-throat` (public as `omega-pcf/05-kkgt`) |
| **sources** | `docs/specs/20261120_SPEC-004_family_build_alignment_and_version_scheme.md`, `docs/reports/20261120_BLD-001_sibling_build_alignment_scope.md`, `docs/reports/20261120_PEND-001_status_and_pending.md`, `docs/architecture.md` §Sources of truth, and the five repositories themselves |
| **method** | independent re-measurement: `git`, `grep`, content hashes (md5-8), `pnpm run …`, `uv run pytest …`, `pdftotext`, `pdftohtml -xml`, and destructive probes that were restored and re-verified clean. Prior reports are treated as hypotheses. Measurements were executed in the session opened on 2026-11-20 (CST); the machine clock had advanced to 2026-11-21 by the gate runs, which is why one rendered date line reads November 21. |

## 1. Scope and heads measured

| repository | head read | how |
|---|---|---|
| `01-hilbert-polya` | `e803e0c` (`main`) | checkout |
| `02-odd-zeta` | `c4fdf1d` (`origin/main`) | temporary worktree — the local checkout sits on `scratch/lean-release` and is reported separately where it differs |
| `03-crystalline-worldsheet` | `87a58ca` (`main`) | checkout |
| `04-mersenne-cr` | `1fdbf42` (`main`) | checkout |
| `05-kk-golden-throat` | `dd72b40` (`main`) | checkout |

All five checkouts reported `git status --porcelain` empty at the end of the pass;
every probe was restored and re-checked (§4).

## 2. Matrix — id | state | evidence | note

State vocabulary: **resolved** (measured to hold), **partial** (holds in part,
or holds only under a narrower reading than the source claims), **open** (does
not hold, or nothing implements it).

### A — `package.json` script contract (BLD-001 §2.A, 8 rows)

| id | state | evidence | note |
|---|---|---|---|
| A1 `figures` alias | resolved | `scripts.figures` present 5/5: `pnpm run generate:figures` in 01/03/04/05; in 02 a declaration that exits 0 and prints `figures: no committed figures in this repository (images/ empty); nothing to regenerate` | 02's form is the SPEC-004 §3.1 P6 adapter |
| A2 `selfcitations` / `selfcitations:check` | resolved | both keys 5/5 (02 read at `origin/main`); `scripts/tasks/selfcitations.ts` md5 `a8aed7d8` identical 5/5 | the local `02` checkout (`scratch/lean-release`) still has neither |
| A3 `validate` chain | resolved | literal string `pnpm run selfcitations:check && pnpm exec tsx scripts/tasks/parity.ts && pnpm run verify` in 5/5 | `selfcitations:check` first, as SPEC requires |
| A4 `test` script | open | present only in 03 and 05 (`uv run pytest tests/ -q`); absent in 01/02/04 | outside SPEC-004's six-key contract, so no gate tracks it |
| A5 `generate:types` | open | absent in 01 and 04; present in 02/03/05; `scripts/generate_types.ts` exists in 5/5 | coupled to B4 — see the executed probe there |
| A6 `generate:figures:list` | open | absent in 04; present in 01/02/03/05 | not in the contract |
| A7 `verify:py` absent in 04 | resolved | `04/package.json` `verify` = `verify:lean && type-check`; `tests/` holds `README.md`/`REPORT.md` only | SPEC-004 §3.1 declares this; no suite was invented |
| A8 `verify:py` engine | partial | 01 `uv run python tests/verify_t_star.py`; 02 `uv run python tests/verify_odd_zeta_pcf_unified.py`; 03/05 `pytest … -m 'not slow'` | the contract fixes the key, not the engine; engines still differ |

### B — shared pipeline files (BLD-001 §2.B, 5 + controls)

| id | state | evidence | note |
|---|---|---|---|
| B1 `build.ts` | partial | md5 `1cc0c2ab` in 01/02/03/04; `c54ab24b` in 05; full diff = 16 lines (comment wording, `releaseVersion` vs `process.argv[2]`) | `syncSelfCitations` + `injectDevVersion` wiring present 5/5 (`scripts/build.ts:4` and `:56`/`:50`) |
| B2 `compile.ts` zone | resolved | `'-e', 'TZ=CST6'` at `scripts/tasks/compile.ts:55` in 5/5 | the zone divergence of BLD-001 B2 is closed in all five, `02 origin/main` included |
| B3 `citation.ts` variants | resolved | md5 `7789096f` identical 5/5; `process.env.TZ = 'CST6'` line 42, `todayInProjectZone()` line 45 | 02's pre-`1e7b085` duplicate-key variant is gone on `origin/main` |
| B4 `generate_types.ts` ReleaseConfig tail | open | 05 `91e1da01` vs 01/02/03/04 `9b7949e6`; **probe executed**: `pnpm run generate:types` in an `origin/main` worktree → `git diff` `1 insertion, 11 deletions` in `scripts/types.ts` → `pnpm run type-check` → three `error TS2305: Module "./types.js" has no exported member 'ReleaseConfig'` (`ELIFECYCLE … exit code 2`); file restored | BLD-001 read this from source only; it is now measured, and it bites 02 and 03 (both expose the script) |
| B5 `.release-it.ts` | partial | 01/03 `9b3320d1`; 04 `9bd9bfa0` (diff vs 01 = comments only); 02 `469764be` (no `after:bump → generate:figures`, no `pyproject.toml` bumper row); 05 `6ef7d3b5` = 04 minus the `before:init` block | see CT-7 |
| B6 controls `checksums.ts`, `cleanup.ts`, `tsconfig.json` | resolved | md5 `8ed77fca`, `19efaa43`, `59de0d80` identical 5/5 | |
| B7 `.latexmkrc` control | open | 01/03/04/05 `f6b82a4b`; 02 `origin/main` `25e4160c` — `$bibtex_use = 1;` and no `$biber` line, against the family's `$biber = 'biber %O %S'; $bibtex_use = 2;` | BLD-001 §1.2 claimed "identical 5/5"; that measurement came from 02's `scratch/lean-release` checkout, not from `origin/main` |
| B8 `scripts/utils/git.ts` | open (new) | 01/03/04/05 `39595046`; 02 `origin/main` `231207ad`, which wraps `git log -1 --pretty=%ct` in a `try` with a `Date.now()` fallback | not listed in BLD-001; outside git the fallback silently replaces `SOURCE_DATE_EPOCH` with the wall clock |

### C — figures (BLD-001 §2.C, 6 rows + AC-14)

| id | state | evidence | note |
|---|---|---|---|
| C1 mechanisms | open (accepted) | 01 `main.py` + `generators/`; 02 vestigial registry + declaration; 03 `main.py` delegating to `CW3_all_figures.py` / `CW3_gue_figures.py`; 04 Docker pdfTeX `scripts/figures/build.sh`; 05 `main.py` + `generators/` | SPEC-004 keeps per-repo engines by design |
| C2 inventory | resolved | `ls images` → 01: 56 files (28 pdf, 27 svg, 1 png); 02: 0; 03: 8 pdf; 04: 1 pdf; 05: 5 pdf | matches both prior reports and row 7 of every `docs/architecture.md` |
| C3 determinism pins | partial | `SOURCE_DATE_EPOCH` sources: 01 `scripts/figures/utils/__init__.py`; 03 default inside `main.py`; 04 default inside `build.sh`; 05 `generators/rc.py`; 02 none (renders nothing) | four locations remain |
| C4 byte pin from the suite | open | `grep -l 'images/' tests/*.py` → 01: 0, 03: 0, 04: 0, 05: 2; `tests/test_section_census.py:313` asserts `set(FIGURE_MD5) == set(FIGURES.values())` | BLD-001 gap 7 unchanged |
| C5 figure docs split | open | `docs/figures.md` absent in 02; `scripts/figures/README.md` absent in 04 and 05 (present in 01, 02, 03) | |
| C6 output contract | open | 03 `os.chdir(args.output_dir)` (`scripts/figures/main.py:90`); 01 `--output` default `images` (`main.py:68`); 04 `-output-directory=$OUTDIR` (`build.sh:29`); 05 resolves the root explicitly | |
| C7 AC-14 byte stability | resolved | `pnpm run figures` → `RUN_EXIT=0` and `git diff --exit-code -- images/` → `DIFF_EXIT=0`, `DIRTY_COUNT=0` in 01, 03, 04 and 05; 02 printed its declaration and exited 0 | measured, not quoted |

### D — verification (BLD-001 §2.D, 5 rows)

| id | state | evidence | note |
|---|---|---|---|
| D1 pytest configuration | partial | `addopts` now identical in 03 and 05 (`--tb=short -p no:cacheprovider`); marker sets are **not** aligned — 03 declares seven (`slow, figure, symbolic, numerical, gauge, gravity, places`) against 05's three (`slow, figure, section`), and `slow` reads `>5s` in 03 versus `>10 s` in 05 | SPEC-004 §3.1 ("the shared `slow`/`figure` markers are aligned") holds for `addopts` and for the names only |
| D2 suite scale | partial | 03: `571 passed in 24.12s` (full) and `543 passed, 28 deselected in 15.49s` (`-m 'not slow'`); 05: `498 passed in 33.91s` and `495 passed, 3 deselected in 26.82s`; `def test_` totals 262/13 files (03) and 254/9 files (05); 01 and 02 single scripts; 04 none | `03/tests/README.md` still says 570 / 542 — stale by one |
| D3 `verify:lean` scope | partial | forms standardised: 01 `cd lean && lake build`, 02 same, 03 `lake build CW6_complete_v2`, 04 `lake build`, 05 `lake build TorreKK_LYR_v35`; 02 `origin/main` `lean/lakefile.toml` declares **one** `[[lean_lib]]` (`odd_zeta_pcf_v1`) | SPEC-004 §3.1's "`02` all eleven libraries" is false at `origin/main` — the eleven-library lakefile sits on `scratch/lean-release`, although the spec instructs the reader to take 02's contract from `origin/main` |
| D4 figure bytes verified from the suite | open | only 05 (C4) | |
| D5 CI / parity automation | open | `.github/` absent in 5/5; `pnpm-lock.yaml` absent in 01/02, present in 03/04/05 | the parity gate only runs when someone runs `validate` |

### E — selfcitations (BLD-001 §2.E, 6 rows)

| id | state | evidence | note |
|---|---|---|---|
| E1 task file | resolved | `scripts/tasks/selfcitations.ts` md5 `a8aed7d8`, 5/5 | |
| E2 README marker pairs | resolved | `grep -c 'selfcite:begin' README.md` = 2 in 5/5 | |
| E3 `main.tex` version pair | resolved | exactly one pair each: 01 lines 112/114, 02 120/122, 03 194/196, 04 108/110, 05 155/157; printed tokens `v2.5.4`, `v1.7.2`, `v1.2.1`, `v0.3.20`, `v0.1.0`, each inside `\texttt{…}` | the local 02 checkout still has 0 markers and prints `Date: Received: …` with no `Version:` |
| E4 `metadata.citationKey` | resolved | `Gonzalez2026HilbertPolya` (01), `Gonzalez2026OddZeta` (02), `CW6` (03), `Gonzalez2026MersenneCR` (04), `Gonzalez2026KKGoldenThroat` (05) | |
| E5 `SPEC-001` location | open (accepted) | `docs/specs/` exists only in 05 (`SPEC-001`, `SPEC-002`, `SPEC-004`); 01/03/04 and `02 origin/main` have no `docs/specs/` | siblings run the mechanism without carrying the spec |
| E6 `README.md` in the derived-files table (AC-10) | open | `05/docs/citations.md:29-36` lists `src/bibliography.bib`, `CITATION.cff`, `.zenodo.json`, `build/document-vX.Y.Z.pdf` only; the same four rows in 01/03/04; `02 origin/main` has no `docs/citations.md` at all | SPEC-001 AC-10 unmet in 5/5 |

### SPEC-004 contract and acceptance criteria

| id | state | evidence | note |
|---|---|---|---|
| CT-1 six contract script keys | resolved | `scripts/tasks/parity.ts` md5 `3abf0a41` 5/5; check (a) green in 5/5 (`parity ✓ SPEC-004 contract holds…`) | |
| CT-2 `verify` composition | resolved | 01/02/03/05 `verify:py && verify:lean && type-check`; 04 `verify:lean && type-check` | matches SPEC-004 §3.1 exactly |
| CT-3 parity wired into `validate` | resolved | `grep '"validate"' package.json` contains `tsx scripts/tasks/parity.ts` in 5/5 | 05 landed it inside `b2da631`, not in a dedicated `test(build)` commit as in 01–04 |
| CT-4 clean token, one pair, `\texttt{…}` | resolved | parity check (c) green 5/5; `pdftohtml -xml` page 1 of 05: token in `fontspec size="13" family="…+SFTT0900"` (typewriter), `Version:` in `size="13" …SFBX0900` (bold roman) | the wrapper contract holds where it is checked |
| CT-5 `validate` runs `selfcitations:check` | resolved | parity check (d) green 5/5 | |
| CT-6 family manifest in 05 | open | `find` over a repository for `*manifest*` returns only `lean/lake-manifest.json`; `parity.ts` hardcodes `REQUIRED_SCRIPTS` per repository | SPEC-004 §3 / §4 P5's "family manifest in 05" does not exist; neither does BLD-001 option A's pinned md5 manifest, so shared-file drift (B7, B8) is invisible to every gate |
| CT-7 `before:init` guardrail (AC-13) | partial | block present at `.release-it.ts:27-31` in 01, 02, 03, 04; `diff 04 .release-it.ts 05 .release-it.ts` = that block alone; 05 has no `before:init` hook anywhere in the repository; probe with the literal hook text: clean `X.Y.Z` → exit 0, `1.7.2-dev@a64ad10` → `before:init: package.json.version must be a clean X.Y.Z` exit 1 | `05/docs/usage.md:77` states that `.release-it.ts` guards the release side with that check — untrue for this repository's own file |
| AC-11 dev/release display | partial | every committed PDF page 1 prints `Version: vX.Y.Z-dev@<sha>[-dirty]` (01 `v2.5.4-dev@c89c673-dirty`, 02 `v1.7.2-dev@a64ad10-dirty`, 03 `v1.2.1-dev@43d8db0-dirty`, 04 `v0.3.20-dev@12dcc29-dirty`, 05 `v0.1.0-dev@ffea84d-dirty`); `computeDisplayVersion()` at `selfcitations.ts:300` selects the tier | the dev half is measured; the release invocation (`tsx scripts/build.ts <version>`) was not executed — the release path is on hold, so the clean half rests on the code |
| AC-12 negative behaviour | resolved | probes in an `origin/main` worktree: committed token `v9.9.9` → `selfcitations:check` exit 1 (`expected the clean v1.7.2`); `v1.7.2-dev@a64ad10` → exit 1; token outside `\texttt{…}` → exit 1 (`carries the version token "v1.7.2" outside \texttt{…}`); `pnpm run selfcitations` → `✓ main.tex version token wrapped in \texttt{…}` then check exit 0 | caveat: a brace imbalance introduced by the probe itself still passed the check — the check reads the token and its wrapper, not the surrounding brace balance |
| AC-13 guard probe | partial | see CT-7: probe passes where the hook exists (01/02/03/04), cannot be run in 05 because the hook is absent | |
| AC-14 figures | resolved | see C7 | |
| AC-15 parity probe | partial | passes in 5/5; removal probe (deleting `scripts.figures` from a scratch copy) → `parity ✗ (a) package.json scripts.figures is missing or empty` exit 1, restored → exit 0; probes recorded in the commit messages of 01 (`c61a4b8`), 02 (`b59d3ff`), 03 (`f40a3ae`), 04 (`3523d82`) | 05's wiring commit `b2da631` records no removal probe |

### Dates, titles, documentation

| id | state | evidence | note |
|---|---|---|---|
| DAT-1 `compile.ts` zone | resolved | `compile.ts:55` `-e TZ=CST6` in 5/5 | |
| DAT-2 `citation.ts` zone | resolved | `citation.ts:42` `process.env.TZ = 'CST6'`, `:45` `todayInProjectZone()`, `:184` `cff['date-released'] = todayInProjectZone()` in 5/5 | |
| DAT-3 rendered date line | resolved | `pdftotext -f 1 -l 1`: 01 `Received: November 15, 2025; Last modified: November 20, 2026; Version: v2.5.4-dev@c89c673-dirty.`; 02 (`origin/main` build) `… November 20, 2026; … v1.7.2-dev@a64ad10-dirty.`; 03 `… v1.2.1-dev@43d8db0-dirty.`; 04 `… v0.3.20-dev@12dcc29-dirty.`; 05 `… November 21, 2026; … v0.1.0-dev@ffea84d-dirty.` | 02's local checkout still renders `Date: Received: April 10, 2026; …` with no `Version:` |
| DAT-4 artifact token freshness | open (new) | the printed sha equals the parent of the commit that carries the PDF only in 05 (`d4d4dfc^ = ffea84d`); 01 `58c7c77^ = 08269a3` vs printed `c89c673`, 02 `ee6d9c2^ = ee54a80` vs `a64ad10`, 03 `98b6070^ = 324fbe9` vs `43d8db0`, 04 `f0b3b48^ = 79568a5` vs `12dcc29`; all five print `-dirty` | display-only by design, but no gate notices that a committed artifact identifies an older tree built with uncommitted changes |
| TYP-1 canonical title | resolved | `grep -n 'Hilbert-Polya\|Hilbert--P\|F_1\|mathbb{F}'` over `CITATION.cff`, `citation.csl.json`, `README.md`, `package.json` → 0 hits in 5/5; en-dash `Hilbert–Pólya` and `𝔽₁` present wherever they belong | the "0 ASCII leftovers" reading is confirmed |
| TYP-1b README `H1` identity | partial (new) | 03 `README.md:1` prints `$\mathbb{F}_1$` where `package.json:4` and `CITATION.cff:3` carry `𝔽₁`; 04 `README.md:1` is title case while `package.json:4`, `CITATION.cff` and `main.tex:93` are sentence case | no gate reads the README heading |
| TYP-2 monospace version token | resolved | `pdftohtml -xml` page 1 of 05: `Version:` in `SFBX0900` size 13, token `v0.1.0-dev@ffea84d-dirty` in `SFTT0900` size 13, dates in `SFRM0900` size 13 | label bold roman, identifier typewriter, as specified |
| TYP-3 `cff.title ← package.json description` | resolved | `docs/architecture.md` row 2 carries the same sentence in 5/5 (`if (pkg.description) cff.title = pkg.description`), and `description` equals the CFF `title` (whitespace-normalised) in 5/5 | |
| TYP-4 witness mark sizes | partial | 05 `pdftohtml -xml` page 19: `W1` in `SFBX0900` size **13**; its monospace content `[CLPW]` in `SFTT1000` size **15**; surrounding prose `SFRM1095` size **16** | the previous `13/15` reading is confirmed for mark vs monospace content; if "content" meant the surrounding prose, that size is 16, not 15 |
| DOC-1 §Sources of truth | resolved | `docs/architecture.md:69` `## Sources of truth` in 5/5, seven rows each; row 7 matches the measured `images/` inventory (C2) and the measured command (C7) in 5/5 | |
| DOC-2 §Commits / §Versioning | resolved | `docs/usage.md` carries `## Commits` and `## Versioning` in 5/5 (01 14/52, 02 14/33, 03 14/52, 04 14/52, 05 14/51) | |
| DOC-3 `### Manual build` heading | partial | `README.md:93` (05), `README.md:124` (01), `README.md:113` (04); absent in 02 and 03, which use `## Build and Compilation` | |
| DOC-4 cross-links | resolved | 163 internal markdown links checked (01 27, 02 4, 03 38, 04 23, 05 71): 0 broken inside `docs/` and `README.md`; the two `04` hits live under `.hermes/desktop-attachments/` (outside the documentation set), the three `05` hits are `…` and `<repository-code>` placeholders inside SPEC-001 prose | |
| DOC-5 generic docs set | open (new) | `02 origin/main` `docs/` = `README.md architecture.md installation.md usage.md` — no `citations.md`, `figures.md`, `style-guide.md`, `witness-contract.md`, `reports/`, `style/`, all of which 01/03/04/05 carry | no prior report measured the documentation set |
| DOC-6 spec index | partial | `05/docs/README.md:20,54` indexes `SPEC-001` only; `SPEC-002` and `SPEC-004` are unindexed | BLD-001 gap 3, still open and wider |

### Gates actually executed (literal numbers)

| id | state | evidence | note |
|---|---|---|---|
| G1 `pnpm run validate` | resolved | exit 0 in 5/5; `selfcitations:check ✓` and `parity ✓` printed in 5/5; `Build completed successfully (3009 jobs)` (01), `(3008 jobs)` (02 `origin/main`), `(8707 jobs)` (03, 04, 05); `pnpm run type-check` ran to completion in each | |
| G2 suites | resolved | 03 `571 passed in 24.12s` full / `543 passed, 28 deselected in 15.49s`; 05 `498 passed in 33.91s` / `495 passed, 3 deselected in 26.82s`; 01 `verify:py` exit 0 with `Zeros verified: 39`, `Global bound M: < 0.017 (observed: 0.01681)`; 02 `verify:py` `219 [PASS]`, `RESULT: ALL CHECKS PASSED`; 04 none by design | |
| G3 census | resolved (count) | `uv run pytest tests/test_section_census.py -q` → `13 passed in 1.21s` (9 `def test_`, one parametrized over five ids) | PEND-001's "census 14" is stale — the caption guard was deleted in `cebd4f5` |
| G4 `\testref{` count | resolved | `grep -o '\testref{' main.tex \| wc -l` → **94**; distinct ids **84**; pinned set **84**; `test_testref_set_is_pinned` green | PEND-001's "99" is stale; `SPEC-002:19` records the 99 → 94 drop |
| G5 `Generated by` | resolved | 0 occurrences in `main.tex`, `README.md`, `docs/` (a dated `DEC-001` snapshot still quotes the retired phrasing) and 0 in the built PDF | |
| G6 manuscript sanity | resolved | `pdfinfo` → `Pages: 63`; `grep -c '^!'` → 0; `undefined` → 0 | matches PEND-001 §2 |
| G7 witness sizes | partial | see TYP-4 | mark and monospace content measured; the surrounding prose reads 16 |

**Tally: 35 resolved · 16 partial · 17 open (68 rows).**

## 3. Claims of the prior reports that did not survive

| # | claim | source | measurement |
|---|---|---|---|
| F1 | suite is "499 tests (496 not-slow, 3 slow)" | PEND-001 §2 | `498 passed` / `495 passed, 3 deselected`; `05/tests/README.md` already says 498/495, and `SPEC-002:28` agrees |
| F2 | "`\testref` anchors **99**" | PEND-001 §2 | **94** occurrences, 84 distinct ids (the 99 → 94 drop is recorded in `SPEC-002:19`) |
| F3 | "census **14**" | PEND-001 §2 | census file collects **13** |
| F4 | "`02` excluded, waiting on the author" among the standardised siblings | PEND-001 §2 | `02 origin/main` carries the whole port (`a72df89`, `b59d3ff`, `753f772`, `5197f1c`, `952a969`, `a64ad10`, `d25ee93`, `63da17e`, `ee54a80`, `ee6d9c2`, `c4fdf1d`) and its `validate` exits 0 |
| F5 | "`tsconfig.json` / `.latexmkrc` identical 5/5" | BLD-001 §1.2 | `.latexmkrc` differs at `02 origin/main` (`25e4160c` vs `f6b82a4b`); `tsconfig.json` is indeed identical |
| F6 | "`01`, `03`, `04` show dozens of modified tracked files" | BLD-001 §6 | all five checkouts report `git status --porcelain` empty |
| F7 | "this report does not appear in the `docs/reports/README.md` index" | BLD-001 §7.4 | `BLD-001` and `PEND-001` are both indexed (`README.md:113-114`) |
| F8 | "`03`'s README quote of 570 tests was not reconciled with the 262 `def test_*` found" | BLD-001 §7.6 | reconciled now, and it does not hold: the suite collects **571**; the README's 570/542 are stale by one |
| F9 | "`02` all eleven libraries" | SPEC-004 §3.1 | `02 origin/main` `lean/lakefile.toml` declares one `[[lean_lib]]` |
| F10 | "the shared `slow`/`figure` markers are aligned" | SPEC-004 §3.1 | only `addopts` and the marker names align; `03` declares seven markers, `05` three, and `slow` is `>5s` vs `>10 s` |
| F11 | "plus a family manifest in 05" (§3, §4 P5) | SPEC-004 | no manifest file exists in any repository; `parity.ts` hardcodes the contract per repo |
| F12 | "`.release-it.ts` guards the release side with a `before:init` check" | `05/docs/usage.md:77` | 05's own `.release-it.ts` has no `before:init` hook; the four siblings do |

## 4. New gaps — things no prior report records

1. **`05` is the one repository without the AC-13 guardrail**, while its own `docs/usage.md` claims the guard exists (F12). The sibling ports added it; the repository that wrote the spec did not receive it.
2. **The family manifest of SPEC-004 §3/§4 P5 does not exist** (CT-6). Consequences measured here: `.latexmkrc` (B7) and `scripts/utils/git.ts` (B8) drifted and no gate noticed, and BLD-001 option A's pinned-hash manifest was never built either.
3. **`generate:types` is a live type-check bomb in 02 and 03** (B4, executed): regenerating types removes `ReleaseConfig` and three files fail `tsc`. BLD-001 read it from source; it is now a probe, and the two repositories that expose the script are one command away from a red tree.
4. **`02 origin/main` carries three shared-file divergences absent from BLD-001's table**: missing `latexmk`-exit and empty-`.bbl` guards in `compile.ts`, a different `.latexmkrc` biber configuration, and a wall-clock fallback in `scripts/utils/git.ts`. BLD-001 measured `02`'s checkout, not `origin/main`, for its control hashes.
5. **The generic documentation set is not uniform**: `02 origin/main` ships four of the eight generic documents (no `citations.md`, `figures.md`, `style-guide.md`, `witness-contract.md`, no `reports/`, no `style/`).
6. **Every committed PDF identifies an older tree**: the printed `-dev@<sha>` matches the parent of the carrying commit only in 05, and all five print `-dirty` (DAT-4). No gate reads the printed identity.
7. **README headings are outside every identity gate** (TYP-1b): 03's heading uses `$\mathbb{F}_1$` against the canonical `𝔽₁`, 04's is title case against the sentence-case identity title.
8. **Unregulated script divergences survive the contract**: `test` (03, 05), `generate:types` (01 absent, 04 absent), `generate:figures:list` (04 absent) — BLD-001 A4/A5/A6, none of them in SPEC-004's six keys.
9. **The named waves carry no ids inside the repositories, and their landing is uneven**: no file in the five repositories and no card on the PCF board contains `FU-1`…`FU-4`, a "tipografía A/B" label, or a documental `D1`…`D4` — the waves survive only as commit subjects, which were reconstructed and checked. Follow-ups: FU-1 `fix(citation): stamp dates in the project timezone` (01 `f59dc23`, 02 `d25ee93`, 03 `9f960f6`, 04 `707f3b4`; 05 is the source of the zone rule and carries no such commit), FU-2 `docs: show the monospace version token in the versioning example` (01 `e8d875a`, 02 `63da17e`, 03 `eee3fc7`, 04 `79568a5`, 05 as `eee2d30 … in the documented examples`), FU-3 `fix(citation): use the canonical en-dash title in cross-references` (01 `08269a3`, 02 `ee54a80`, 03 `324fbe9`, 05 `0fd41bd` — not applicable to 04, whose bibliography carries no `Hilbert–Pólya` record: 0 hits), FU-4 `docs(spec): extend AC-12 with the monospace wrapper` (05 `fdf7385`, spec-only by construction). Typography pair: CFF-title typography (`c89c673` 01, `43d8db0` 03, absent in 04 for the same reason as FU-3) and monospace token (`3474cea` 01, `a64ad10` 02, `f737739` 03, `12dcc29` 04, `82a7bef` 05). Documental quartet `docs: document the commit and version conventions` / `docs: propagate the family witness…` / `docs: document the sources of truth and the generation chains` / `docs: rename the manual build section`: 4/4 in 01 (`209d04a`, `2560318`, `94109dd`, `e803e0c`) and 04 (`28867ce`, `f7092f3`, `bdf35f1`, `1fdbf42`), 3/4 in 03 (no rename commit — DOC-3), 3/4 in 05 (`a05c0a2`, `8fb1765`, `86aa8a5`; it is the source of the witness documents), and 1/4 in 02 `origin/main` (only `c4fdf1d`; the conventions arrived as `c189af3 docs: add standardized build pipeline docs`, and neither a witness document nor a manual-build heading exists there — DOC-3, DOC-5). MRG-001's `D1`–`D3` conflict classes are unrelated to that quartet.
10. **`05`'s parity wiring rode into `fix(build) b2da631`** without a recorded removal probe, where 01–04 each landed a `test(build)` commit carrying theirs (CT-3, AC-15).

## 5. Verdict

The migration is real and substantially landed: the contract of SPEC-004 §3
holds in all five repositories under every key the parity gate checks, the three
negative probes of AC-12 behave as specified, AC-14 is byte-verified in the four
repositories that have figures, and `validate` exits 0 in all five. What the
prior reports overstate is coverage: the family-level deliverables (the
manifest), the guardrail in `05`, and the shared-file controls were declared,
not measured — and three of them are measurably absent.

Priorities, not executed here:

1. **Add the missing `before:init` guardrail to `05`'s `.release-it.ts` and the removal probe to its parity record** (CT-7, AC-13, F12) — one block copied from `04`, plus a correction of `docs/usage.md` if the guard is instead rejected for `05`; either way the documentation and the file must agree.
2. **Build the family manifest SPEC-004 §3 promises and point the parity gate at it** (CT-6): the six script keys as today plus a pinned hash list for `build.ts`, `compile.ts`, `citation.ts`, `checksums.ts`, `cleanup.ts`, `tsconfig.json`, `.latexmkrc`, `scripts/utils/git.ts`. It would have caught B7 and B8 automatically, and it is the only mechanism that makes drift loud without CI.
3. **Close the `generate:types` hazard** (B4) by porting `05`'s `ReleaseConfig` tail to 01–04, or by removing the script from `02`/`03` until it is ported; the current state is one command away from a red `type-check`.
4. **Decide the `02 origin/main` shared-file divergences as one decision** (B7, B8, the `compile.ts` guards): either the family adopts 02's variants or 02 adopts the family's — but the decision must be taken on `origin/main`, not on the `scratch/lean-release` checkout the previous inventory read.
5. **Record the stale numbers where they are read** (F1–F3, F8): `PEND-001` §2 and `03/tests/README.md` quote counts the suite no longer reports, and `SPEC-004` §3.1 quotes 02's lakefile scope from the wrong branch.

Deferred, explicitly: C3/C4/C5/C6 (figure-engine and byte-pin alignment),
A4/A5/A6 (unregulated script keys), DOC-3 (the `Manual build` heading in 02 and
03) and DOC-5 (the missing generic documents in 02) all touch published
artifacts or the author's documentation and need an operator decision before
any work starts.
