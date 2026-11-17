# Rationale applied state and pending work — 05-kk-golden-throat

| Field | Value |
|---|---|
| **id** | `WIT-003` |
| **title** | Rationale applied state and pending work |
| **status** | snapshot — the pending rows are the author's and are **not** closed by this move |
| **date** | 2026-11-17 |
| **version** | 1.0 |

**Scope.** This report holds the repository-specific material that
`docs/witness-rationale.md` carried until 2026-11-17, when the rationale
was split: the generic argument now lives in
[`docs/witness-contract.md`](../witness-contract.md) (portable across the
family) and the operational rule in [`docs/citations.md`](../citations.md)
§8; the counters, the verdicts and the pending work of *this* manuscript
are kept here, where the directory doctrine of [`docs/README.md`](../README.md)
places anything tied to one repository state.

**Repository:** `05-kk-golden-throat`. Line numbers are those of the
manuscript when the text was written and move with concurrent editing; the
sentence tail (or the id) identifies each site. Statuses below are the
author's and are reproduced unchanged — nothing here closes an open row.

---

## 1. Applied state of the criterion (§4.4 of the old rationale)

The criterion reproduces the applied state of this manuscript without a
single exception: the manuscript's **twenty-seven blocks** meet the five
conditions — twenty-six outright, and one (`pisano_orders, modular_orders`,
29 characters) because `p` lifts gate 2 at the paragraph close. Of the
inline marks with two identifiers or more — **twenty-five today**,
twenty-three `P` and two `N`, from the thirty-four counted at the pass —
**thirteen** closed their sentence; the criterion flagged **nine** of them
to become a block, all nine have since been applied, and **four** remain
inline with a numerical reason (the shortest list of all, two list items,
a neighbouring block at seventy words).

The complete table, with the tail of the sentence each mark closes, is
[`20261115_WIT-001_criterion_sites.md`](20261115_WIT-001_criterion_sites.md).

## 2. Compactness census (§4.5 of the old rationale)

Measured with `grep` on `main.tex`, the whole apparatus occupies:

- **230 inline marks** — 16 without argument (two of them the
  *Evidence tags* gloss) and 214 with identifiers (159 `P` and 55 `N`) —
  all set in `\footnotesize` inside the sentence they mark: they cost the
  characters of the bracket, not a line;
- **27 blocks** — 17 `P` and 10 `N` — each with a line of its own and two
  paragraph breaks (`\par` before and after `\witness`);
- **12** `\wtag` **labels** of the witness list and **99 occurrences** of
  `\testref`.

Consequences argued against those numbers (thresholds themselves are
`docs/citations.md` §8.5):

1. The block costs a line and breaks the paragraph, so it is only asked of
   a list of 35 characters or more — exactly the shortest list this
   manuscript already printed as a block. Without the threshold,
   `pisano_orders, modular_orders` — 29 characters — would earn a whole
   line for twenty-nine characters; it prints on a line of its own today
   only because `p`, the paragraph-close heuristic, lifts gate 2 for that
   site.
2. Inline marks fell from 231 to 230 with the `u`/`p` pass
   ([`20261116_WIT-002_u_p_verdicts.md`](20261116_WIT-002_u_p_verdicts.md)).

## 3. The eliminated class `R` — its sites

`R` marked the direction of a reading rather than how a claim is
established; **eleven of its sites** repeated what the prose already said,
and the only one that worked was written as prose (`a reading of the
records, not a result about them`). The eleventh had been fused with the
claim it annotated — see
[`20261115_DEC-001_witness_decisions.md`](20261115_DEC-001_witness_decisions.md).

## 4. Internal references of the old §7, in this repository

| File | What it provides |
|---|---|
| `docs/reports/20261115_DEC-001_witness_decisions.md` | per-site decisions, counters of the harmonisation pass and the author's pending-work list |
| `main.tex` — preamble (witness system, `\tier` dispatch, definition of `\witness` and `\wtag`) and the *Evidence tags* gloss | the implementation and what the reader sees at the first mark of the body |
| `lean/TorreKK_LYR_v34.lean` | the `P` identifiers the mark can print |
| `tests/` and `tests/test_section_census.py` | the numerical suite and the census that fixes the test identifiers the manuscript cites |
| `tests/REPORT.md` | historical census of the witness apparatus, explicitly marked as prior to standardisation; kept as history, not as state |
| `omega-pcf-paper-repos` → `references/witness-system.md` | grammar of the family witness system and the state of propagation to the sibling repositories (05-kk-golden-throat and 03-crystalline-worldsheet render marks) |

## 5. Limits and pending work — reproduced unchanged (§8 of the old rationale)

These rows are open. Nothing in this report or in the split of
`witness-rationale.md` closes, supersedes or re-decides them; they remain
the principal author's.

1. **Application of the flagged rows.** `docs/citations.md` §8.5 flagged
   nine inline sites that the quantified criterion takes to a block; all
   nine have been applied — the last of them by
   `docs/reports/20261116_WIT-002_u_p_verdicts.md` — and the counters of
   the pass live in `docs/reports/`.
2. **Gloss and coverage.** The gloss promises `N` = "checked numerically,
   with the test that checks it named where the check is ours"; the pending
   work of `docs/reports/20261115_DEC-001_witness_decisions.md` §3.1 and §4
   consists of each body claim `N` carrying that name. Two body claims `N`
   print with no test in the tag: `main.tex:1869` (`…for the full list of
   distances`) names its test in the prose of the same sentence, as rule 4
   of `docs/citations.md` §8.2 allows, while `main.tex:1368` (`…The two
   are degrees of one property.`) names none at all; the gloss itself
   is exempt by rule 6. While there are `N` without a named witness, the
   gloss describes the intention of the system and not all its sites.
3. **Preamble comments.** The header comment of `main.tex` describes the
   shape of the apparatus as "a mark with ids stays inline `\tier[ids]{X}`
   and moves to a line of its own in list form … when the gates of
   `docs/citations.md` section 8.5 hold", and follows it with the four
   thresholds and the two heuristics. It is a summary of the criterion,
   not the criterion; the rule lives in `docs/citations.md` §8.5.
4. **Propagation to the family.** Only `05-kk-golden-throat` and
   `03-crystalline-worldsheet` render marks; the adoption of the criterion
   in the remaining repositories is an editorial decision, never a
   mechanical one.
5. **No external guarantee.** While there is no published norm that
   describes the claim-by-claim mark, the convention rests on this
   documentation and on its review; that is declared in §6 of
   `docs/witness-contract.md` and must not be presented otherwise.

---

## Related documents

- [`docs/witness-contract.md`](../witness-contract.md) — the portable
  rationale (why the marks exist, what they do not assert).
- [`docs/citations.md`](../citations.md) §8 — the contract and the
  quantified criterion.
- [`20261115_WIT-001_criterion_sites.md`](20261115_WIT-001_criterion_sites.md)
  — site table and threshold calibrations.
- [`20261116_WIT-002_u_p_verdicts.md`](20261116_WIT-002_u_p_verdicts.md)
  — verdicts of the two heuristics (pending application).
- [`20261115_DEC-001_witness_decisions.md`](20261115_DEC-001_witness_decisions.md)
  — the decision log behind the tiers.
