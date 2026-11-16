# docs/reports/ — specific reports

Reports are the *specific* material of the documentation: per-site
inventories, decision logs and verdict tables tied to one repository state.
The generic, portable documents live one level up in `docs/`
(`README.md`, `architecture.md`, `citations.md`, `figures.md`,
`installation.md`, `usage.md`, `witness-rationale.md`); a report is what a
generic rule *refers to* for its concrete instances.

Naming: `YYYYMMDD_<ID>_<slug>.md` (ISO date of the report, stable id, slug).

| id | title | status | date | file |
|---|---|---|---|---|
| `DEC-001` | Witness decisions — per-site decision log, counters and pending work | applied and committed | 2026-11-15 | [20261115_DEC-001_witness_decisions.md](20261115_DEC-001_witness_decisions.md) |
| `WIT-001` | Criterion sites — the applied inline/own-line inventory | applied (2026-11-15 pass); snapshot | 2026-11-15 | [20261115_WIT-001_criterion_sites.md](20261115_WIT-001_criterion_sites.md) |
| `WIT-002` | u/p verdicts — the two heuristics applied to `main.tex` | proposed — awaiting application | 2026-11-16 | [20261116_WIT-002_u_p_verdicts.md](20261116_WIT-002_u_p_verdicts.md) |

Reports are snapshots: their line numbers refer to the manuscript as written
and move with concurrent editing; the sentence tail (or the id) identifies
each site.