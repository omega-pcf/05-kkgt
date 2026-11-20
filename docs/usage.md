# Build and Release Workflow

## Daily Development

**Workflow:** LaTeX Workshop (James Yu) in VS Code
- Automatically compiles to `build/main.pdf`.
- Real-time preview on save.

**Build:**
```bash
pnpm run build
```

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
  the pipeline detail lives in [architecture.md](architecture.md).
- **The paper prints it.** The page-1 footnote of the family is standardised
  as:

  ```latex
  \renewcommand{\datename}{\textbf{Received:}}
  \date{<Month D, YYYY>; \textbf{Last modified:} \today; \textbf{Version:} vX.Y.Z}
  ```

  which renders `Received: <Month D, YYYY>; Last modified: <today>; Version:
  vX.Y.Z.` The first label lives in `\datename` because amsart prefixes the
  footnote with it (its own default would read `Date: Received: …`). Inside
  the `selfcite` markers the `vX.Y.Z` token is owned by `package.json` and
  checked by `pnpm run selfcitations:check`, so the printed version, the
  committed version and the version archived by Zenodo cannot diverge.

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
