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
├── style-guide.md     # Family style guide v2.2: editorial (§1–§12), code quality D1–D7 (§13), tex/proofreading (§14)
├── style/             # Portable extracts of the style guide
│   └── grammar.md     # Grammar and usage rules of human language (ES/EN/FR/IT examples)
├── usage.md           # Build and release commands
├── witness-rationale.md  # Why the marks exist (convention rationale, EN)
├── specs/            # Design specifications (dated, id'd, ISO header)
│   └── 20261116_SPEC-001_deterministic_self_citations.md
└── reports/           # Specific, repository-tied reports (dated, id'd)
    ├── README.md      # Index of the reports (id · title · status · date)
    ├── 20261115_DEC-001_witness_decisions.md
    ├── 20261115_WIT-001_criterion_sites.md
    ├── 20261116_WIT-002_u_p_verdicts.md
    └── 20261116_FIG-001_figure_1_deembed.md
```

`docs/` itself stays generic (rules and rationale, portable across the
sibling repositories); anything tied to one repository state — per-site
inventories, decision logs, verdict tables — goes to `docs/reports/`.

## Contents

- **architecture.md**: Tech stack, execution flow, reproducibility measures, scripts structure.
- **citations.md**: How `citation.csl.json` drives the bibliography, CITATION.cff and .zenodo.json; §8 is the witness (tier) contract, §8.5 the quantified inline / line-of-its-own criterion.
- **figures.md**: What `pnpm run generate:figures` guarantees and why (byte-stable, text-extractable PDFs); the concrete figure-1 incident is [FIG-001](reports/20261116_FIG-001_figure_1_deembed.md).
- **installation.md**: Prerequisites and setup instructions.
- **style-guide.md**: The family style guide (v2.2): editorial rules (§1–§12), including the rigorous IMRAD structure of §7 (section roles, antecedent before use, discourse thread, and the principal author's exclusive decision on moving content between sections), the software-quality doctrine D1–D7 (§13) and the tex/proofreading pipeline with its cited sources (§14). Generic across the family: this repository's own conventions are linked, never copied — witness contract in `citations.md` §8, rationale in `witness-rationale.md`, grammar rules in `style/grammar.md`.
- **style/grammar.md**: The grammar and usage rules extracted from `style-guide.md` §1.5 — language-neutral (complete structure, agreement, clear reference, voice, punctuation, economy), worked in Spanish, English, French and Italian, with the RAE-checked Spanish `se` verbs and their sources.
- **usage.md**: Daily workflow, conventional commits, build and release commands.
- **witness-rationale.md**: The rationale of the witness marks: evidence classes, usability, succinctness.
- **specs/**: Design specifications — proposals that change the pipeline or a
  shared artifact, with purpose, evidence, acceptance criteria and open
  questions; first entry
  [SPEC-001](specs/20261116_SPEC-001_deterministic_self_citations.md)
  (deterministic self-citation blocks in the READMEs).
- **reports/**: Specific reports — the witness decision log (DEC-001), the criterion site inventory (WIT-001), the `u`/`p` verdict table (WIT-002) and the figure-1 prose de-embed (FIG-001); index in `reports/README.md`.

## Conventions

Commits follow [Conventional Commits](https://www.conventionalcommits.org/);
format, common types, examples and the English-subject rule:
[usage.md](usage.md) §Commits.