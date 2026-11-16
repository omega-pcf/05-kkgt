# Project Documentation

This directory contains technical documentation for the shared build and release pipeline.

## Structure

```
docs/
├── README.md          # This file
├── architecture.md    # Release system architecture
├── citations.md       # CSL single-source citation pipeline + witness (tier) contract
├── figures.md         # Deterministic figure pipeline (the five PDFs)
├── installation.md    # Prerequisites and setup
├── usage.md           # Build and release commands
├── witness-rationale.md  # Why the marks exist (convention rationale, EN)
└── reports/           # Specific, repository-tied reports (dated, id'd)
    ├── README.md      # Index of the reports (id · title · status · date)
    ├── 20261115_DEC-001_witness_decisions.md
    ├── 20261115_WIT-001_criterion_sites.md
    └── 20261116_WIT-002_u_p_verdicts.md
```

`docs/` itself stays generic (rules and rationale, portable across the
sibling repositories); anything tied to one repository state — per-site
inventories, decision logs, verdict tables — goes to `docs/reports/`.

## Contents

- **architecture.md**: Tech stack, execution flow, reproducibility measures, scripts structure.
- **citations.md**: How `citation.csl.json` drives the bibliography, CITATION.cff and .zenodo.json; §8 is the witness (tier) contract, §8.5 the quantified inline / line-of-its-own criterion.
- **figures.md**: What `pnpm run generate:figures` guarantees and why (byte-stable, text-extractable PDFs).
- **installation.md**: Prerequisites and setup instructions.
- **usage.md**: Daily workflow, conventional commits, build and release commands.
- **witness-rationale.md**: The rationale of the witness marks: evidence classes, usability, succinctness.
- **reports/**: Specific reports — the witness decision log (DEC-001), the criterion site inventory (WIT-001) and the `u`/`p` verdict table (WIT-002); index in `reports/README.md`.

## Conventions

All commits follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <description>
```

**Common types:** `feat`, `fix`, `docs`, `refactor`, `chore`.