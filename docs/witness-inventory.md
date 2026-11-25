# Witness inventory — 05-kk-golden-throat

Generated 2026-11-25 from the working tree at `e3ada7a` (`git rev-parse --short HEAD`), over `main.tex` and `src/**/*.tex` — 1 files. Every number below is read from those files at run time; nothing here is copied from an older document. The form taxonomy comes from FTI-001 §2, F8-001 §1, WIT-RECON-001 and INV-WIT-001 §A, which this file supersedes (`superseded-by: docs/witness-inventory.md`).

## Marks

| form | count |
|---|--:|
| `\tier[ids]{P}` | 145 |
| `\tier[ids]{N}` | 53 |
| `\tier{P}` (bare) | 6 |
| `\tier{N}` (bare) | 3 |
| own-line `\witness{P}{…}` | 31 |
| own-line `\witness{N}{…}` | 12 |
| `\tier[\testref{…}]{N}` marks | 53 |

Ids carried by `N` tags: **56 citations over 51 distinct ids**.

## Decoration and accounting macros

| macro | occurrences in the manuscript |
|---|--:|
| `\LeanInline` | 0 |
| `\LeanStar` | 0 |
| `\LeanTally` | 0 |
| `\LeanCW` | 0 |
| `\leanline` | 0 |
| `\code` | 40 |
| `\testref` | 94 |
| `\witness` | 43 |

## Gates measured here

| gate | result |
|---|---|
| citation-key lint (no key, no `\cite` inside a tag) | **0 failures** |
| stars (`\LeanStar` body uses) | **0** |
| `Tier` column in a table | **0** |
| `pending(D7)` markers | **0** |
| `\tier[…]` id parts that are neither a `\testref`, a snake_case id nor a qualified declaration | **23** |
| open sites (`(open;`) | **0** |

`\tier[…]` ids that are neither a `\testref`, a snake_case id nor a namespace-qualified declaration (23 occurrences, 14 distinct):

- `dS\_entropy\_law` ×3
- `S\_acts\_as\_mirror` ×3
- `bessel\_J1\_zeros` ×3
- `theta\_S\_law` ×2
- `pairing\_FP\_modulus\_half` ×2
- `eta\_T` ×2
- `D\_conjugated\_hop\_is\_one` ×1
- `eta\_power\_T\_phase` ×1
- `partition\_T\_invariant` ×1
- `J\_sq` ×1
- `J\_four` ×1
- `J\_lifts\_W10` ×1
- `J\_swaps\_moduli` ×1
- `dedekindEta` ×1

## Per-file marks

| file | `\tier[…]` + `\tier{…}` marks |
|---|--:|
| `main.tex` | 207 |

Re-generate with the measurement of the wave that owns this file; a hand-edited figure is a defect.
