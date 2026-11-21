# Build and Release Workflow

## Daily Development

**Workflow:** LaTeX Workshop (James Yu) in VS Code
- Automatically compiles to `build/main.pdf`.
- Real-time preview on save.

**Build:**
```bash
pnpm run build
```

## Counts

The numbers the documentation states about the repository — the pytest suite
total and its not-slow total, the census size, the `\testref{...}` anchors,
the Lean source statistics and the figure inventory — are **measured, never
typed** (follow-up of `docs/reports/20261120_CVR-001_build_standardization_coverage_review.md` §5):

```bash
pnpm run counts         # rewrite the marked regions and regenerate docs/counts.md
pnpm run counts:check   # fail, with a diff, when either has drifted
```

`counts:check` runs inside `validate`, after `parity`. The mechanism follows
the `selfcitations` precedent (SPEC-001 §5.2): a region is delimited by
`<!-- counts:begin id="..." -->` … `<!-- counts:end id="..." -->` in prose, and
by `# counts:begin id="..."` … `# counts:end id="..."` on lines of their own
inside a code fence, where an HTML comment would print as text. The manuscript
joins the same mechanism with the third grammar, `% counts:begin id="..."` …
`% counts:end id="..."` on lines of their own in `main.tex` — a `%` comments
out the rest of its line, so the markers own whole lines exactly as the
`selfcite` version markers do. Inside that region the task writes the counts
as `\newcommand{\Count…}{…}` declarations, and the prose quotes the macros
instead of a raw number: a value is therefore typed into the tree only by
`pnpm run counts`, and a hand-typed digit in the prose fails `counts:check`.
`\newcommand` is chosen over `\def` (which would silently shadow an existing
name) and over a generated `\input` file (which would add a second source to
track for six numbers): it refuses to redefine, so a name collision fails the
compile.

`pnpm run build` calls `syncCounts()` next to `syncSelfCitations()`, before
the render, so the PDF can never print a stale count. That makes the suite
counters a per-build cost — three `pytest --collect-only` runs, collection
only, seconds, never a test run — which is recorded in `docs/counts.md`.
`docs/counts.md` is regenerated in full and lists every counter with the
command that measures it and the regions that quote it.

Dated reports (`docs/reports/`) and specs (`docs/specs/`) are snapshots of a
moment: they are corrected by hand with the reason recorded, never rewritten by
the task. Running times quoted in the documentation are machine-dependent
estimates and stay outside the mechanism.

## Shared files

Most of the build pipeline is shared by **byte, not by copy**: the five
repositories of the family (`01-hilbert-polya`, `02-odd-zeta`,
`03-crystalline-worldsheet`, `04-mersenne-cr`, `05-kk-golden-throat`) carry the
same `scripts/tasks/*.ts`, `scripts/types*`, `scripts/schemas/*`,
`scripts/utils/git.ts`, `tsconfig.json`, `.latexmkrc` and the toolchain pins.
What must stay identical is pinned in
[`scripts/shared-files.json`](../scripts/shared-files.json) — one SHA-256 per
file — and verified by `scripts/tasks/manifest.ts`:

```bash
pnpm run manifest         # rewrite the pinned hashes from the working tree
pnpm run manifest:check   # fail, naming the file and both digests, when one drifted
```

`manifest:check` runs inside `validate`, right after `counts:check`. A listed
file is a **family** file: changing it in one repository only fails the gate.
A deliberate change is ported to every repository, `pnpm run manifest`
refreshes the manifest in each one, and the refreshed manifest is committed
together with the change; a file that legitimately stops being shared moves to
the manifest's `excluded` table with its reason, again in all five
repositories, so the manifest itself stays byte-identical family-wide.

The `excluded` table is part of the contract, not a footnote: `package.json`
and `CITATION.cff` are per-repository identity roots (asserted by `parity`),
`pyproject.toml` and `uv.lock` are the per-repository dependency sets,
`scripts/tasks/counts.ts` is a per-repository counter table by design,
`scripts/build.ts` carries the reason recorded in the manifest, and the
manifest never lists itself. Each exclusion names its measured reason where a
file was evaluated and rejected.

The design follows the checksum-manifest pattern (`sha256sum -c` over a
versioned list) and the lockfile philosophy — pin the bytes, fail loudly on
drift, update the pin in the same commit as the change — rather than a runtime
integrity layer: background and sources are recorded in
[`specs/20261120_SPEC-004_family_build_alignment_and_version_scheme.md`](specs/20261120_SPEC-004_family_build_alignment_and_version_scheme.md)
§3.1.

## Commits

Every repository of the family follows [Conventional Commits](https://www.conventionalcommits.org/)
with **English subject lines** (the documentation-language rule is
`docs/citations.md` §6):

```
<type>(<scope>): <description>
```

**Types used in the family:**

| type | meaning | example from this repository |
|---|---|---|
| `feat` | new content or capability | `feat(paper): integrate the Background section of the v134 provenance` |
| `fix` | a defect: manuscript markup, frontmatter, scripts, figures | `fix(frontmatter): label the version in the date line` |
| `docs` | documentation only — reports, specs, guides | `docs(reports): record the CIT-002 citation round 2 verification` |
| `test` | the suite: tests and their fixtures | `test(sections): sections 45 and 46 state their numbers in the tests` |
| `refactor` | structure changes with no behaviour change | `refactor(figures): english generate_fig_* entry points, module-level imports` |
| `style` | formatting that changes no rendered meaning | — |
| `chore` | tooling, metadata, dependencies | `chore(repo): metadata parity with the family` |
| `revert` | reverts | — |

**Scopes** name the surface that changed: `paper` (the manuscript body),
`frontmatter` (title block, dates, authors), `tests`, `figures`, `citation`,
`lean`, `build`, `reports`, `spec`. The type must match the content: `docs`
never carries a manuscript edit, `fix` never carries new content — a wrong
type is a defect of the record, not a style preference.

**Rules:** subject in English, imperative, no trailing period; the body
explains *why*; `!` after the type or scope marks a breaking change
(`feat(api)!: …`); one concern per commit, with the gates green at every
commit.

**Changelog:** `@release-it/conventional-changelog` renders `CHANGELOG.md`
from these subjects at each release.

## Versioning

- **Standard:** [Semantic Versioning](https://semver.org) — `vX.Y.Z`
  (major.minor.patch), where `feat` → minor, `fix` → patch,
  `BREAKING CHANGE`/`!` → major, as declared in the commit subjects above.
- **Single source:** the `version` field of `package.json`.
- **Synchronization chain:** `release-it` bumps `package.json` →
  `@release-it/bumper` writes the same value into `CITATION.cff` →
  `citation.ts` regenerates `.zenodo.json` from the CFF → the GitHub release
  carries the tag → **Zenodo archives exactly this version** under the
  repository's Concept DOI (one DOI per version, one Concept DOI for all of
  them). Zenodo therefore consumes the same string the repository declares;
  the pipeline detail lives in [architecture.md](architecture.md), and the
  row-by-row chain (source → generator → derived file) in
  [architecture.md §Sources of truth](architecture.md#sources-of-truth).
- **Two printed forms (SPEC-004, amended 2026-11-20).** The page-1 line prints
  the *release* identifier `vX.Y.Z` on the release path and a *development*
  identifier `vX.Y.Z-dev@<shortsha>` (`…-dirty` with uncommitted changes) on
  every other build. The development string is derived at build time from
  `git rev-parse --short HEAD` + `git status --porcelain`, is display-only —
  it never enters `package.json`, `CITATION.cff`, `.zenodo.json`, the
  changelog, any tag, **nor `main.tex` in git**: `scripts/build.ts` injects it
  for the render and restores the original bytes, so the committed token is
  always the clean `vX.Y.Z` of `package.json`. `selfcitations:check` fails
  when the committed token is not that clean form (a wrong base such as
  `v9.9.9`, or any `-dev@<sha>` suffix in git), so a committed tree stays
  green at rest. `.release-it.ts` guards the release side with a `before:init`
  check that `package.json.version` is a clean `X.Y.Z`.
- **The paper prints it.** The page-1 footnote of the family is standardised
  as:

  ```latex
  \renewcommand{\datename}{\textbf{Received:}}
  \date{<Month D, YYYY>; \textbf{Last modified:} \today; \textbf{Version:} \texttt{vX.Y.Z}}
  ```

  which renders `Received: <Month D, YYYY>; Last modified: <today>; Version:
  vX.Y.Z.` — with only the identifier in monospace: the labels stay
  `\textbf`, `Version: ` itself is not typed, and the token sits inside
  `\texttt{…}`. The first label lives in `\datename` because amsart prefixes
  the footnote with it (its own default would read `Date: Received: …`).
  Inside the `selfcite` markers the `vX.Y.Z` token is owned by
  `package.json` and checked by `pnpm run selfcitations:check`, so the
  printed version, the committed version and the version archived by Zenodo
  cannot diverge; that check (and `parity`) also fails when the token sits
  outside `\texttt{…}`, and `pnpm run selfcitations` wraps it back.

## Release

```bash
pnpm run release         # Full release: bump → build → tag → GitHub → Zenodo
pnpm run release:dry-run # Preview only: rebuilds the artifacts, then walks the release without tagging or pushing (requires a git remote)
```

## Installation

```bash
pnpm install
```

Prerequisites, requirements and setup have a single home:
[installation.md](installation.md).
