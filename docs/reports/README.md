# docs/reports/ — specific reports

| Field | Value |
|---|---|
| **Document** | `docs/reports/README.md` |
| **Status** | In force |
| **Version** | 1.0 (generic template + local index) |
| **Date** | 2026-11-17 |
| **Scope** | The reports convention of the family: what a report is, how it is named and headed, and the index of the reports of *this* repository |

Reports are the *specific* material of the documentation: per-site
inventories, decision logs, verdict tables, audits and incident records
tied to one repository state. The generic, portable documents live one
level up in `docs/` (`README.md`, `architecture.md`, `citations.md`,
`figures.md`, `installation.md`, `style-guide.md`, `usage.md`,
`witness-contract.md`, `style/grammar.md`); a report is what a generic
rule *refers to* for its concrete instances. Anything tied to one
repository state goes here — never to a document at the `docs/` root: the
applied inventory of the placement criterion, the counters, the verdicts
and the pending rows are archived here, and the documents at the `docs/`
root are rules and rationale only.

## Naming

`YYYYMMDD_<ID>_<slug>.md` — ISO date of the report, stable id, slug in
kebab-case. The id is `<AREA>-<NNN>` with a sequence number that never
reuses a retired number; the area names the concern, e.g. `DEC`
(decisions), `WIT` (witness), `FIG` (figures), `AUD` (audits), `CIT`
(citations), `MRG` (merges), `SEC` (sections). A proposal that changes
the pipeline or a shared artifact is not a report: it is a specification
under `docs/specs/`, same naming, `SPEC-NNN` id.

## Report header

Every report opens with its title and an ISO field table:

```markdown
# <Title>

| Field | Value |
|---|---|
| **id** | `AREA-001` |
| **title** | <full title> |
| **status** | <applied / report only / snapshot / pending — the honest state> |
| **date** | YYYY-MM-DD |
| **version** | 1.0 |
```

A scope paragraph follows, naming the repository and, where relevant, the
commit the report was written from. Statuses are never optimistic: a
report that changed nothing says `report only`, and a row left to the
author says so.

## Index

The index of the reports of this repository is the table at the end of
this file, under *Reports of this repository*. Its columns are
`id · title · status · date · file`, one row per report, ordered by date.

## Snapshots

Reports are snapshots: their line numbers refer to the manuscript as
written and move with concurrent editing; the sentence tail (or the id)
identifies each site. A report is never edited to follow the manuscript —
a later state is a later report.

---

## Template for a new report

```markdown
# <Title>

| Field | Value |
|---|---|
| **id** | `AREA-001` |
| **title** | <full title> |
| **status** | <honest state> |
| **date** | YYYY-MM-DD |
| **version** | 1.0 |

**Scope.** <what this report holds, which repository, which commit if it
matters, and what it deliberately does not touch.>

<Body: the inventory, the table, the verdicts, the incident — with the
evidence and the method.>

---

## Related documents

- `docs/witness-contract.md` §6 — the generic rule this report instantiates (`docs/citations.md` §8 is only its index).
- `docs/witness-contract.md` — why the device exists.
```

---

## Reports of this repository

| id | title | status | date | file |
|---|---|---|---|---|
| `DEC-001` | Witness decisions — per-site decision log, counters and pending work | applied and committed | 2026-11-15 | [20261115_DEC-001_witness_decisions.md](20261115_DEC-001_witness_decisions.md) |
| `WIT-001` | Criterion sites — the applied inline/own-line inventory | applied (2026-11-15 pass); snapshot | 2026-11-15 | [20261115_WIT-001_criterion_sites.md](20261115_WIT-001_criterion_sites.md) |
| `WIT-002` | u/p verdicts — the two heuristics applied to `main.tex` | proposed — awaiting application | 2026-11-16 | [20261116_WIT-002_u_p_verdicts.md](20261116_WIT-002_u_p_verdicts.md) |
| `WIT-003` | Rationale applied state and pending work — the counters, verdicts and open rows behind `witness-contract.md` | snapshot; open rows are the author's | 2026-11-17 | [20261117_WIT-003_rationale_applied_state.md](20261117_WIT-003_rationale_applied_state.md) |
| `AUD-001` | Claim ↔ test ↔ original-code matrix — audit of every numeric claim in `main.tex` | report only — no source file modified | 2026-11-16 | [20261116_AUD-001_claim_test_matrix.md](20261116_AUD-001_claim_test_matrix.md) |
| `CIT-001` | Content verification of the 36 cite keys carrying the manuscript's external numbers | report only — no source file modified | 2026-11-16 | [20261116_CIT-001_citation_verification.md](20261116_CIT-001_citation_verification.md) |
| `FIG-001` | Figure 1 (`seccion_44`) — the prose moved to the caption | applied and committed (`ff44a61`); snapshot | 2026-11-16 | [20261116_FIG-001_figure_1_deembed.md](20261116_FIG-001_figure_1_deembed.md) |
| `MRG-001` | The v138 provenance — zone diffs, conflict table and merge plan | report only — nothing of v138 integrated | 2026-11-16 | [20261116_MRG-001_v138_diff_merge_plan.md](20261116_MRG-001_v138_diff_merge_plan.md) |
| `SEC-001` | Migration ledger for the forty-six `seccion_N` functions of `tests/src/kkgt/sections.py` | closed — superseded by `SPEC-002` (ledger §7); the package is deleted | 2026-11-16 | [20261116_SEC-001_sections_migration.md](20261116_SEC-001_sections_migration.md) |
| `CIT-002` | Citation round 2 — remaining keys, cross-references and pending sources | report only — two pendings with the author | 2026-11-17 | [20261117_CIT-002_citation_round2.md](20261117_CIT-002_citation_round2.md) |
| `DEC-002` | The principal author's open decisions, reconciled — 36 rows | evidence index — superseded as live list by `PEND-001` | 2026-11-17 | [20261117_DEC-002_open_author_decisions.md](20261117_DEC-002_open_author_decisions.md) |
| `PRF-001` | Lean build performance — profile and recommendations | report only — recommendations applied in W6 | 2026-11-17 | [20261117_PRF-001_lean_build_performance.md](20261117_PRF-001_lean_build_performance.md) |
| `PYT-001` | Numerical testing practices — the suite contrasted with fourteen sources | report only — rows acted through `SPEC-002` | 2026-11-17 | [20261117_PYT-001_numerical_testing_contrast.md](20261117_PYT-001_numerical_testing_contrast.md) |
| `TST-001` | AUD-001 test gaps and tolerances — criteria, counts and the five code-only figures | applied — §6 rows triaged in `PEND-001` | 2026-11-17 | [20261117_TST-001_aud001_test_gaps_and_tolerances.md](20261117_TST-001_aud001_test_gaps_and_tolerances.md) |
| `BLD-001` | Sibling build alignment — inventory, 30 divergences, options A/B/C, eight phases | report only — awaiting the operator's choice | 2026-11-20 | [20261120_BLD-001_sibling_build_alignment_scope.md](20261120_BLD-001_sibling_build_alignment_scope.md) |
| `PEND-001` | Status and pendings under the v165 wait — `DEC-002` triaged (8 closed / 21 deferred / 7 open) | live list | 2026-11-20 | [20261120_PEND-001_status_and_pending.md](20261120_PEND-001_status_and_pending.md) |
| `CVR-001` | Build standardisation coverage review — SPEC-004 and the 30 divergences of `BLD-001` re-measured against the five repositories (68 matrix rows, gates run, 12 prior claims refuted) | report only — no source, spec or test file modified | 2026-11-20 | [20261120_CVR-001_build_standardization_coverage_review.md](20261120_CVR-001_build_standardization_coverage_review.md) |
| `MRG-002` | The v197 provenance — zone diffs, conflict census and merge plan | report only — nothing of v197 integrated | 2026-11-27 | [20261127_MRG-002_v197_diff_merge_plan.md](20261127_MRG-002_v197_diff_merge_plan.md) |
