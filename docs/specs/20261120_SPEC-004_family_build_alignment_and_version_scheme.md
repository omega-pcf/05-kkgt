# SPEC-004 — family build alignment (option C) and the two-tier version scheme

| Field | Value |
|---|---|
| **id** | `SPEC-004` |
| **title** | Scope agreement for the family-wide build refactor: hybrid contract (option C of `BLD-001`) plus a development version identifier that does not compete with the release tag |
| **status** | **amended 2026-11-22 (D2 wave)** — toolchain-pin amendment (§3): family Lean pin `v4.33.1` → `v4.36.0-rc2` + Mathlib `a8754b18`, reason: the author's pin v168. **amended 2026-11-20 (approved)** — version-token amendment approved by the operator and executed family-wide: the committed token is the clean `vX.Y.Z`, the `-dev@<sha>` form is injected at build time only (§2, AC-12, §3.1). Previously: approved 2026-11-20 — in execution (P0…P7, family-wide, `02` included) |
| **date** | 2026-11-20 |
| **supersedes** | nothing; implements `BLD-001` §4–§5 (option C chosen by the operator 2026-11-20) |
| **repositories** | `01-hilbert-polya`, `03-crystalline-worldsheet`, `04-mersenne-cr`, `05-kk-golden-throat` — **family-wide in one pass**, `05-granularity` excluded (draft), `02-odd-zeta` read-only until the author's version lands |
| **sources** | `docs/reports/20261120_BLD-001_sibling_build_alignment_scope.md` (30 divergences, options A/B/C,8 phases), `05/.release-it.ts`, `05/scripts/tasks/selfcitations.ts`, `docs/specs/20261116_SPEC-001_deterministic_self_citations.md` |

## 1. Decisions taken by the operator

1. **Option C — hybrid**: an identical script *contract* per repo (same entrypoint
   names, same task semantics), local adapters where a repo's content differs, and a
   **parity gate** that fails when a repo drifts from the contract. Option B (shared
   pnpm package) stays blocked until a family scaffold repository exists.
2. **Family-wide, not05-first**: the refactor lands across all siblings in the same
   effort (01/03/04/05), so working between repositories is standardised in one go.
3. **The version identifier is expanded** (§2): development builds must print an
   intermediate identifier that cannot be mistaken for a release tag.

## 2. The two-tier version scheme (proposal)

### Tier 1 — release identifier: `vX.Y.Z`, clean

- The **only** string that becomes a git tag, a GitHub release and a Zenodo version.
- `package.json` `version` stays a clean `X.Y.Z` at release time — never suffixed.
- **Guardrails:**
  a. in `.release-it.ts`, a `hooks['before:init']` step asserts
     `^\d+\.\d+\.\d+$` on `package.json.version` (a suffixed version fails the
     release before anything is written);
  b. the release path already passes the post-bump version explicitly:
     `after:bump` runs `pnpm exec tsx scripts/build.ts ${version}`, so the printed
     token inside the `selfcite` region is exactly `vX.Y.Z` — tag, CFF, `.zenodo.json`
     and PDF share one string (the chain `BLD-001` §3 documents).

### Tier 2 — development identifier: `vX.Y.Z-dev@<shortsha>` (+`-dirty`)

- **Every build that is not the release path** prints
  `Version: v0.1.0-dev@a1b2c3d` (and `…-a1b2c3d-dirty` when the worktree has
  uncommitted changes). Derived at build time, never written by hand:
  `git rev-parse --short HEAD` + `git status --porcelain`.
- **Typeset in monospace (2026-11-20).** The page-1 line sets only the
  identifier in `\texttt`; the labels stay `\textbf` and `Version: ` itself
  is not typed:

  ```latex
  \date{<Month D, YYYY>; \textbf{Last modified:} \today; \textbf{Version:} \texttt{vX.Y.Z}}
  ```

  Both tiers print inside that wrapper — `injectDevVersion()` replaces only
  the token between the braces, so the `-dev@<sha>` form is monospaced as
  well — and `selfcitations --check` together with `parity` fail when a
  committed token sits outside `\texttt{…}` (the sync wraps it back).
- **It cannot compete with the release tag** by construction: it is a *display*
  string in the PDF only — it never enters `package.json`, `CITATION.cff`,
  `.zenodo.json`, the changelog, or any tag, **nor `main.tex` in git**
  *(amended 2026-11-20)*.  The token committed in the paper's
  `selfcite id="version"` region is always the clean `vX.Y.Z` of
  `package.json`, so `selfcitations --check` and `parity` are green on a
  committed tree by construction; `--check` fails when the committed token is
  not that clean form — a wrong base such as `v9.9.9`, or any `-dev@<sha>`
  suffix.
- **Precedent (verified 2026-11-20, in the ttamayo WordPress-plugin project the
  operator named — path withheld as local environment):** the release path there is
  **release-it** (`.release-it.json`: `tagName v${version}`, `before:init` build,
  `after:bump` changelog + version injection), while **staging deploys** inject the
  development suffix with bash: `TAG=$(git describe --tags --abbrev=0 || 0.0.0)`,
  `COMMIT_HASH=$(git rev-parse --short HEAD)`, and **only when
  `git describe --tags --exact-match` fails** — i.e. off-tag builds get
  `${TAG#v}-dev@${COMMIT_HASH}` into the plugin header, and the file is restored
  with `git checkout --` afterwards, so **the suffix never enters the repository**.
  Two facts follow: (i) the `…-dev@<sha>` shape is the established ttamayo form
  (adopted here, with the family's `v` prefix); (ii) the release path must print the
  clean version — matching Tier 1. The project's CI (CircleCI) carries the same
  split: deploy jobs run the suffix logic, releases stay release-it.
- **Rejected alternatives (recorded so they are not re-litigated):**
  - bare `vX.Y.Z@<sha>` (the operator's first sketch) — kept as the same idea minus
    the explicit `dev` marker the precedent carries;
  - `git describe` form `vX.Y.Z-4-gabc1234` as the *whole* display — conventional,
    but `05` has **no tags** yet (release on hold), so it degrades to `gabc1234`
    with no version base; the base here is `package.json`, not the last tag;
  - strict semver prerelease `vX.Y.Z-dev.<sha>` — semver-pure, but the display
    string is never semver-parsed (`package.json` is the only semver artefact), so
    the ttamayo shape wins on familiarity.

### Where it lives (one mechanism, family-wide)

- `selfcitations.ts` exposes `computeDisplayVersion()`:
  release context (explicit version argument from `build.ts ${version}`, or the
  release-it environment) → `v${version}`; otherwise → `v${pkg.version}-dev@${sha}`.
- `VERSION_TOKEN` widens to
  `/v\d+\.\d+\.\d+(?:-dev@[0-9a-f]{7,}(?:-dirty)?)?/`, still applied **only inside**
  the `% selfcite:begin/end id="version"` region (exactly-one-marker rule intact).
- The token **written to `main.tex`** by the same rewrite pass as today
  (`pnpm run selfcitations`, hooked in `build.ts`) is the clean `vX.Y.Z` of
  `package.json` *(amended 2026-11-20)*; `--check` inside `validate` compares
  the committed token against exactly that form.
- The development form reaches the page only through `injectDevVersion()`,
  called by `build.ts` around the compilation *(amended 2026-11-20)*.
- **Non-goal:** the README badge keeps the clean `package.json` version; only the
  page-1 line carries the development suffix.

**Amendment (approved 2026-11-20).** The original mechanism had the rewrite
pass stamp the *derived* token into `main.tex`, so every commit moved HEAD and
left the committed token stale: `selfcitations:check`/`validate` were red on a
committed tree by construction — structurally incompatible with a tree that
must stay green.  The approved mechanism keeps the precedent's shape
(`inject → render → restore`, the ttamayo `git checkout --` pattern replaced
by an in-memory restore that never depends on git):

1. the sync always writes the clean `vX.Y.Z` (= `package.json`, the release
   form) into the region — never a sha;
2. `--check` validates (i) exactly one marker pair, (ii) the README regions up
   to date, (iii) the committed token equals that clean `vX.Y.Z`
   (`^\d+\.\d+\.\d+$` inside the `v`, no suffix) → **green at rest after every
   commit**;
3. `scripts/build.ts` reads the original `.tex`, injects the display token
   (dev or release according to its argument), renders, and restores the
   original bytes from memory in a `finally` — the committed PDF carries the
   `-dev@<sha>` form while the committed `.tex` stays clean;
4. `parity.ts` check (c) asserts the same clean committed token against
   `package.json`, so `01`–`05` share one rule.

## 3. The contract (option C) — what "identical" means

Every repository exposes the same `package.json` scripts with the same semantics:

| script | contract |
|---|---|
| `build` | `tsx scripts/build.ts [version?]` — with an argument = release build (clean token); without = development build (`@sha` token) |
| `verify` | composition of `verify:py` (when the repo has Python tests), `verify:lean` (when it has a `lean/`), `type-check` |
| `figures` | regenerate the repo's figures through its own mechanism, byte-stable (`git diff --exit-code -- images/` afterwards) |
| `selfcitations` / `selfcitations:check` | rewrite / verify the citation regions **and** the version token (ported from05) |
| `validate` | `selfcitations:check && verify` |

**Parity gate (P5):** a small test or script per repo that asserts the contract
above (script keys exist, version region present and exactly one pair, the
committed token is the clean `vX.Y.Z` of `package.json` and never a
`-dev@<sha>` suffix — *amended 2026-11-20*), plus a family manifest in05
listing the expected contract — a repo that drifts fails its own `validate`.
*(Amended 2026-11-21: the manifest now exists — `scripts/shared-files.json`
pinned with one SHA-256 per shared file, verified by
`scripts/tasks/manifest.ts` and wired into every `validate` as
`manifest:check`.  See §3.1, note "Shared-file manifest".)*

### 3.1 Family manifest (P5 landed 2026-11-20; `figures` and `verify` amended by P6/P7, 2026-11-20)

The expected contract per repository as P1–P7 landed it.  The columns are
exactly what `scripts/tasks/parity.ts` asserts in `01`–`05`: the six script
keys (`build`, `verify`, `figures`, `selfcitations`, `selfcitations:check`,
`validate`), one non-inverted `selfcite id="version"` pair in `main.tex`, the
committed token equal to `package.json`'s clean `vX.Y.Z` — never a
`-dev@<sha>` suffix *(amended 2026-11-20)* — and `validate` running
`selfcitations:check`.

| repository | `build` | `verify` | `figures` | `selfcitations` | `selfcitations:check` | `validate` | `scripts/tasks/parity.ts` | `main.tex` version region |
|---|---|---|---|---|---|---|---|---|
| `01-hilbert-polya` | ✓ | `verify:py && verify:lean && type-check` | ✓ → `generate:figures` | ✓ | ✓ | `selfcitations:check && parity && counts:check && manifest:check && verify` | ✓ | exactly one pair |
| `02-odd-zeta` | ✓ | `verify:py && verify:lean && type-check` | ✓ → declares no committed figures | ✓ | ✓ | `selfcitations:check && parity && counts:check && manifest:check && verify` | ✓ | exactly one pair |
| `03-crystalline-worldsheet` | ✓ | `verify:py && verify:lean && type-check` | ✓ → `generate:figures` | ✓ | ✓ | `selfcitations:check && parity && counts:check && manifest:check && verify` | ✓ | exactly one pair |
| `04-mersenne-cr` | ✓ | `verify:lean && type-check` (no Python suite) | ✓ → `generate:figures` | ✓ | ✓ | `selfcitations:check && parity && counts:check && manifest:check && verify` | ✓ | exactly one pair |
| `05-kk-golden-throat` | ✓ | `verify:py && verify:lean && type-check` | ✓ → `generate:figures` | ✓ | ✓ | `selfcitations:check && parity && counts:check && manifest:check && verify` | ✓ (wired by the 2026-11-20 amendment) | exactly one pair |

Notes:

- `selfcitations:check` runs **first** in `validate` in all five; the parity
  script joins the chain in `01`–`04` (P5) and, since the 2026-11-20
  amendment, in `05` as well — so `05` carries the parity gate like its
  siblings (`validate = selfcitations:check && parity && counts:check && manifest:check && verify`),
  which closes AC-15's "…/`05`" open point.
- **counts** *(added 2026-11-21, follow-up of `CVR-001` §5)*: every repository
  also runs `counts:check` inside `validate`, right after `parity` (the table
  above carries the composed string). `scripts/tasks/counts.ts` measures the
  counts the living documents state — the suite totals from
  `pytest --collect-only`, the census size, the `\testref{...}` anchors, the
  Lean source statistics with comments stripped, the numbered sections of the
  package (`TestSection<N>` classes), the `images/` inventory — rewrites the
  marked regions (`<!-- counts:begin id="..." -->` in prose,
  `# counts:begin id="..."` on a line of its own inside a code fence, and the
  LaTeX grammar `05` uses for the manuscript — `% counts:begin id="..."` on
  lines of its own in `main.tex`, around the `\newcommand{\Count…}{…}`
  declarations that the prose quotes instead of a raw number) and regenerates
  `docs/counts.md`; `scripts/build.ts` calls `syncCounts()` beside
  `syncSelfCitations()` before the render, so the PDF prints the measured
  value; a stale number then fails `validate` with a diff instead of surviving
  as a report's footnote. The `counts` and `counts:check` keys are
  deliberately **outside** the six-key parity contract above (parity's list is
  unchanged), so the gate travels with the `validate` wiring of each
  repository.
- **Shared-file manifest** *(added 2026-11-21, closing `CVR-001` CT-6 and §5.2
  priority 2 — the pinned hash list `BLD-001` §4 Option A described but never
  built, whose absence let `.latexmkrc` and `scripts/utils/git.ts` drift
  undetected)*: `scripts/shared-files.json` pins one SHA-256 for every file the
  five repositories must carry **byte-identically** —
  `scripts/tasks/{citation,checksums,cleanup,compile,manifest,parity,selfcitations}.ts`,
  `scripts/build.ts`, `scripts/generate_types.ts`, `scripts/types.ts`, `scripts/types/global.d.ts`,
  `scripts/schemas/cff-schema.json`, `scripts/schemas/zenodo-schema.json`,
  `scripts/utils/git.ts`, `tsconfig.json`, `.latexmkrc`, `.npmrc`, `.nvmrc`,
  `.python-version`, `LICENSE` — and `scripts/tasks/manifest.ts` verifies them:
  `pnpm run manifest` rewrites the pins from the working tree,
  `pnpm run manifest:check` runs inside `validate` right after `counts:check`
  and fails with the file's name plus both digests.  Everything measured and
  deliberately NOT pinned sits in the manifest's `excluded` table with its
  reason in the same JSON (so that file stays byte-identical too):
  `package.json`/`CITATION.cff`/`.zenodo.json` (per-repository identity and
  generated metadata), `pyproject.toml`/`uv.lock` (per-repository
  dependencies), `scripts/tasks/counts.ts` (per-repository counter table by
  design), `.release-it.ts`/`.gitignore`/`.chktexrc` (per-repository), and the
  manifest itself (a file cannot hold its own digest).
  **Amendment (2026-11-21, follow-up (a)):** `scripts/build.ts` — the one file
  of `CVR-001` §5.2's list that stayed unpinned — now sits in `files`, not in
  `excluded`: `01`/`02`/`03`/`04` ported `syncCounts()` from `05` (their
  `counts.ts` gained the `syncCounts()` export, the `kind: 'tex'` marker
  grammar and the `invokedDirectly` guard, and their `build.ts` calls it
  beside `syncSelfCitations()`), so the entry point is byte-identical across
  the five repositories — md5 `caf90950388f81a4d2a5f14ff3ed5575` (05's entry point, adopted verbatim; the siblings' `releaseVersion` const is `process.argv[2]` under another name, so the behaviour is unchanged) — and the
  manifest pins its 20 files with that one change.  The manifest's `excluded`
  table is down to ten entries; `pnpm run manifest:check` reports
  `manifest ✓ 20 shared files` in every repository.
  Design sources (researched 2026-11-21): the checksum-manifest pattern — one
  versioned list of digest + filename, verified as a batch
  (https://www.sysax.com/topics/file-integrity-verification/checksum-files-and-manifests/);
  the lockfile philosophy — pin the exact versions *and hashes* so the
  installed tree cannot silently drift
  (https://safeguard.sh/resources/blog/what-is-a-lockfile);
  integrity versus authenticity — a checksum proves the bytes did not shift,
  not who produced them, so the manifest guards drift, not malice
  (https://docs.gradle.org/current/userguide/securing_dependencies.html);
  and the reproducible-builds timestamp rule this build already follows
  (`SOURCE_DATE_EPOCH`, https://reproducible-builds.org/specs/source-date-epoch/).
  Like a lockfile the manifest records a state: it makes divergence loud, it
  does not remove it — the remedy for a failure is always a family-wide port
  plus a refreshed pin committed with the change.
- **Witness-contract pin (amendment 2026-11-24, wave W01):** `docs/witness-contract.md`
  joined `files` in `scripts/shared-files.json` as the manifest's 22nd entry —
  the `chore(manifest): pin the witness contract` commit of 2026-11-24 in each
  of the five repositories — so `pnpm run manifest:check` reports
  `manifest ✓ 22 shared files` (9 documented exclusions) instead of the 20
  quoted in the 2026-11-21 amendment above (the 21st entry, `.release-it.ts`,
  was pinned on 2026-11-21).  The manifest is byte-identical in all five
  repositories: md5 `641993135ec680e5f8cce3375bae0cac` over
  `scripts/shared-files.json`.
- `figures` (**P6**): every repository exposes the key and parity asserts it
  from P6 on; behind the alias the mechanism stays local — `01`/`03`/`05`
  `uv run python scripts/figures/main.py`, `04` `bash scripts/figures/build.sh`
  (Docker pdfTeX), `02` a declaration that the repository commits no figures
  (`images/` empty) which exits 0 and starts failing the moment a figure is
  committed.  The gate is AC-14: after `pnpm run figures`,
  `git diff --exit-code -- <images dir>` must report no content change;
  measured byte-stable (identical sha256 over `images/*`) in all four
  repositories that have figures.
- `verify` compositions stay local: the contract key is `verify`, what it
  composes is each repository's own.  From **P7** the composition also carries
  `type-check` wherever TypeScript exists (all five), `verify:lean` wherever
  `lean/` exists (all five) and `verify:py` only where Python tests exist —
  `04` has none, so its composition does not include it and no suite was
  invented for it.
- `verify:lean` (**P7**): the form is standardised (`cd lean && lake
  build [target]`) and the scope is declared here, without changing what any
  repository compiles — `01` every library in `lakefile.toml` (`pcf`,
  `PCF_Complete_v11_Unified`, `PCF_OperatorConvergence`), `02` the one
  library its `lakefile.toml` declares (`odd_zeta_pcf_v1`; *corrected
  2026-11-21, `CVR-001` F9 — the eleven-library lakefile of the earlier
  inventories lives on the local `scratch/lean-release` branch, not on
  `origin/main`*), `03` the named target `CW6_complete_v2`, `04` every library
  (`mersenne-cr`, `golden_mersenne`), `05` the named target
  `TorreKK_LYR_v35`.  No `lakefile.toml`, `lake-manifest.json` or mathlib pin
  was touched in any repository *by P7* — the 2026-11-22 toolchain-pin
  amendment below is the recorded exception.
- **Toolchain pin (amendment 2026-11-22)** *(D2 wave, authorized
  2026-11-21; reason: the author's pin v168)*: family-wide, `lean/lean-toolchain`
  `leanprover/lean4:v4.33.1` → `leanprover/lean4:v4.36.0-rc2` and the
  `lean/lakefile.toml` Mathlib `rev` `v4.33.1` →
  `a8754b1890a7f7f1c859d48281cb84a1fce64139` (commit `a8754b18` of
  mathlib4, 2026-11-16) in all five repositories, with `lake-manifest.json`
  regenerated by `lake update` (authorized for this wave alone, superseding
  the standing no-`lake-update` rule) and the Mathlib oleans fetched from the
  release cache — never built from source.  The Lean files are deliberately
  absent from `scripts/shared-files.json`, so `manifest:check` carries no
  hash for them; the pin pair itself is the shared state, quoted here.
- pytest configuration (**P7**) exists only in `03` and `05`; their `addopts`
  (`--tb=short -p no:cacheprovider`) and the shared `slow`/`figure` markers are
  aligned, with test counts and assertions untouched.  `01`, `02` and `04` have
  no pytest configuration and were left without one.
- `02-odd-zeta` was ported **on `main`** through a temporary worktree — the
  local checkout sits on `scratch/lean-release` (the author's pending line)
  and predates this manifest, so read `02`'s contract from `origin/main`.
- **Version token (amendment approved 2026-11-20).**  Every *rendered* build
  shows `vX.Y.Z-dev@<shortsha>[-dirty]`, derived from `git rev-parse --short
  HEAD` + `git status --porcelain` at build time; the token **committed** in
  `main.tex` is always the clean `vX.Y.Z` of `package.json`.  The dev form
  exists only in the PDF — `build.ts` injects it, renders and restores the
  original bytes from memory — so `pnpm run selfcitations:check` and
  `pnpm run validate` stay green at rest after every commit instead of going
  stale against the new HEAD.

## 4. Phasing (family-wide, one effort)

| phase | content | commits |
|---|---|---|
| **P0** | this spec + the contract text in `05/docs/usage.md` (amend §Commits/§Versioning with the two-tier scheme) | 1 (05) |
| **P1–P4** | per repo `03`, `02`(read-only note), `01`, `04`: port `selfcitations.ts` (regions + version token + display derivation), add the `selfcite` markers to `main.tex`, wire scripts, `before:init` guard in `.release-it.ts`, build + `pdftotext` proof of the line | 1 per repo (4) |
| **P5** | parity gate in `01`–`04` + the family manifest in `05` | 1 per repo (4) |
| **P6** (phase 2, separate GO) | figures mechanisms aligned (byte-stability gate) | per repo |
| **P7** (phase 2, separate GO) | verification aligned (`verify:py` in04, pytest config parity, lean scope) | per repo |

Mandatory total: **9 commits**; P6/P7 deferred to their own approval (they touch
generated artefacts, unlike P0–P5 which are tooling and docs).

**Invariants for every phase:** rendered PDFs keep their content (only the version
token changes), figure bytes and `SOURCE_DATE_EPOCH` untouched, citation-region
strings unchanged (`03` keeps its `CW6`), DOIs/keys untouched, one commit per repo,
**no tags, no releases** (the release path stays on hold with the author's v165).

## 5. Acceptance criteria

- AC-1 … AC-10 of `SPEC-001` remain the base for the selfcitations port.
- AC-11: `pnpm run build` in any repo prints `Version: vX.Y.Z-dev@<sha>` in the
  rendered PDF; the same build invoked as `tsx scripts/build.ts <version>`
  prints `Version: vX.Y.Z`.  Either way the committed `main.tex` keeps the
  clean token (the suffix is injected and restored around the render).
- AC-12 *(rewritten by the 2026-11-20 amendment, extended the same day)*: a
  deliberately wrong base (`v9.9.9`) in the committed token fails
  `pnpm run selfcitations:check` in every repo, and so does any `-dev@<sha>`
  suffix in git — the committed token never carries a sha, so the check can no
  longer go red because HEAD moved. Beyond a clean base the committed token
  must also be typeset inside `\texttt{…}`: `selfcitations:check` and
  `parity` fail when the token sits outside the monospace wrapper, and
  `pnpm run selfcitations` wraps it back.
- AC-13: the `before:init` guard fails a suffixed `package.json.version` (probe
  recorded in the commit message).
- AC-14: `git diff --exit-code -- images/` is clean after `pnpm run figures` in
  every repo that has figures.
- AC-15: the parity gate passes in `01`/`03`/`04`/`05` and fails when a contract
  key is removed (probe recorded).

## 6. Open points for the operator

1. ~~Confirm the printed form~~ — **decided 2026-11-20**: `vX.Y.Z-dev@<shortsha>`
   as written in §2, matching the verified ttamayo precedent (`…-dev@${COMMIT_HASH}`).
2. ~~`02-odd-zeta`~~ — **decided 2026-11-20**: include it in the refactor (the
   author's content freeze does not cover tooling; it currently prints no version at
   all, so it gains the markers and the token like the others).
3. ~~P6/P7~~ — **decided 2026-11-20**: included in this effort, with the figures and
   verification adapters decoupled so both entrypoints end up generic, well-made and
   standardised across the family.

**Status update:** all three points decided; the operator gave the go-ahead on
2026-11-20 — execution starts with P0 (this amendment) and proceeds P1→P7 family-wide.
