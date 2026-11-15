# Project Documentation

This directory contains technical documentation for the shared build and release pipeline.

## Structure

```
docs/
├── README.md          # This file
├── architecture.md    # Release system architecture
├── citations.md       # CSL single-source citation pipeline
├── figures.md         # Deterministic figure pipeline (the five PDFs)
├── installation.md    # Prerequisites and setup
├── usage.md           # Build and release commands
└── witness-decisions.md # The witness/tier decision log
```

## Contents

- **architecture.md**: Tech stack, execution flow, reproducibility measures, scripts structure.
- **citations.md**: How `citation.csl.json` drives the bibliography, CITATION.cff and .zenodo.json.
- **figures.md**: What `pnpm run generate:figures` guarantees and why (byte-stable, text-extractable PDFs).
- **installation.md**: Prerequisites and setup instructions.
- **usage.md**: Daily workflow, conventional commits, build and release commands.
- **witness-decisions.md**: Every decision behind the witness tiers and the open/closed gates.

## Conventions

All commits follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>
```

**Common types:** `feat`, `fix`, `docs`, `refactor`, `chore`.
