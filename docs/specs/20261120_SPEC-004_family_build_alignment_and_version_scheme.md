# SPEC-004 — family build alignment (option C) and the two-tier version scheme

| Field | Value |
|---|---|
| **id** | `SPEC-004` |
| **title** | Scope agreement for the family-wide build refactor: hybrid contract (option C of `BLD-001`) plus a development version identifier that does not compete with the release tag |
| **status** | proposed — for the operator's approval before execution |
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

### Tier 2 — development identifier: `vX.Y.Z@<shortsha>` (+`-dirty`)

- **Every build that is not the release path** prints
  `Version: v0.1.0@a1b2c3d` (and `…-a1b2c3d-dirty` when the worktree has
  uncommitted changes). Derived at build time, never written by hand:
  `git rev-parse --short HEAD` + `git status --porcelain`.
- **It cannot compete with the release tag** by construction: it is a *display*
  string in the PDF only — it never enters `package.json`, `CITATION.cff`,
  `.zenodo.json`, the changelog, or any tag; `selfcitations --check` validates it
  against the same derivation, so a stale line fails `validate`.
- **Precedent:** the operator reports the same idea in use at ttamayo (the
  WordPress-plugins entrypoint project, extracted with bash). The exact script was
  not located in this pass (`~/Documents/DevelopmentV2/tt-wordpress-automation`
  exists but no matching extraction was found under `*.sh`); to be consulted at
  execution — the semantics above stand without it.
- **Rejected alternatives (recorded so they are not re-litigated):**
  - `git describe` form `vX.Y.Z-4-gabc1234` — conventional, but `05` has **no tags**
    yet (release on hold), so it degrades to `gabc1234` with no version base;
  - strict semver prerelease `vX.Y.Z-dev.<sha>` — semver-pure, but the operator's
    `@sha` form is the one already recognised across ttamayo; `package.json` remains
    the only semver-parsed artefact, so the display string needs no semver rank.

### Where it lives (one mechanism, family-wide)

- `selfcitations.ts` gains `computeDisplayVersion()`:
  release context (explicit version argument from `build.ts ${version}`, or the
  release-it environment) → `v${version}`; otherwise → `v${pkg.version}@${sha}`.
- `VERSION_TOKEN` widens to
  `/v\d+\.\d+\.\d+(?:@[0-9a-f]{7,}(?:-dirty)?)?/`, still applied **only inside**
  the `% selfcite:begin/end id="version"` region (exactly-one-marker rule intact).
- The token is written by the same rewrite pass as today (`pnpm run selfcitations`,
  hooked in `build.ts`), checked by `--check` inside `validate`.
- **Non-goal:** the README badge keeps the clean `package.json` version; only the
  page-1 line carries the development suffix.

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
above (script keys exist, version region present and exactly one pair, token
matches `computeDisplayVersion()`), plus a family manifest in05 listing the
expected contract — a repo that drifts fails its own `validate`.

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
- AC-11: `pnpm run build` in any repo prints `Version: vX.Y.Z@<sha>`; the same
  build invoked as `tsx scripts/build.ts <version>` prints `Version: vX.Y.Z`.
- AC-12: a deliberately stale token fails `pnpm run selfcitations:check` in every repo.
- AC-13: the `before:init` guard fails a suffixed `package.json.version` (probe
  recorded in the commit message).
- AC-14: `git diff --exit-code -- images/` is clean after `pnpm run figures` in
  every repo that has figures.
- AC-15: the parity gate passes in `01`/`03`/`04`/`05` and fails when a contract
  key is removed (probe recorded).

## 6. Open points for the operator

1. Confirm `vX.Y.Z@<shortsha>` as the printed form (vs `git describe` / semver
   prerelease — both recorded as rejected in §2).
2. `02-odd-zeta`: gets the same treatment read-only note only until the author's
   version lands — or is it patched now? (It currently prints **no** version at all.)
3. P6/P7 (figures, verification): separate GO as phased, or folded into this effort?
