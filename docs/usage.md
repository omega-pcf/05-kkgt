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

All commits follow [Conventional Commits](https://www.conventionalcommits.org/),
with **English subject lines** (the documentation language rule is
`docs/citations.md` §6):

```
<type>(<scope>): <description>
```

**Common types:** `feat`, `fix`, `docs`, `refactor`, `chore`.

**Examples:**
```bash
git commit -m "fix(build): resolve Docker bind-mount race condition"
git commit -m "feat(citation): add ORCID support"
git commit -m "docs: update architecture guide"
```

**Automatic Changelog:** The `@release-it/conventional-changelog` plugin generates `CHANGELOG.md` from conventional commits on each release.

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
