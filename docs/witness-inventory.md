# Witness inventory — 05-kk-golden-throat

> **GENERATED** — `pnpm run witness:inventory` (`scripts/tasks/witness-inventory.ts`) rewrites
> this file from the working tree; `pnpm run inventory:check` (inside `validate`) fails with
> a diff when it drifts. Do not edit by hand.

Measured over the tracked manuscript sources (`main.tex` and `src/**/*.tex`) — 1 files. TeX comments (a line whose first non-space character is `%`) and the lines that *define* a counted macro are excluded; nothing here is copied from an older document. The form taxonomy is the one of `docs/witness-contract.md` §6.1.

## Marks

| form | count |
|---|--:|
| own-line `\witness[ids]{P}` | 26 |
| own-line `\witness[ids]{N}` | 12 |
| own-line `\witness{P}` (bare) | 0 |
| own-line `\witness{N}` (bare) | 0 |
| inline `\witness[ids]{P}` | 147 |
| inline `\witness[ids]{N}` | 53 |
| inline `\witness{P}` (bare) | 6 |
| inline `\witness{N}` (bare) | 3 |
| `\witness[\testref{…}]{N}` marks | 65 |

Ids carried by `N` marks: **79 ids over 72 distinct**.

## Decoration and accounting macros

| macro | occurrences in the manuscript |
|---|--:|
| `\LeanInline` | 0 |
| `\LeanStar` | 0 |
| `\LeanTally` | 0 |
| `\LeanCW` | 0 |
| `\leanline` | 0 |
| `\code` | 40 |
| `\testref` | 95 |
| `\witness` | 251 |

## Gates measured here

| gate | result |
|---|---|
| citation-key lint (no key, no `\cite` inside a tag) | **0 failures** |
| stars (`\LeanStar` body uses) | **0** |
| `Tier` column in a table | **0** |
| `pending(D7)` markers | **0** |
| `\witness[…]` id parts that are neither a `\testref`, a snake_case id nor a qualified declaration | **30** |
| open sites (`(open;`) | **0** |

`\witness[…]` ids that are neither a `\testref`, a snake_case id nor a namespace-qualified declaration (30 occurrences, 17 distinct):

- `bessel\_J1\_zeros` ×5
- `S\_acts\_as\_mirror` ×3
- `dS\_entropy\_law` ×3
- `eta\_T` ×3
- `dedekindEta` ×2
- `pairing\_FP\_modulus\_half` ×2
- `theta\_S\_law` ×2
- `D\_conjugated\_hop\_is\_one` ×1
- `D\_conjugated\_hops\_equal` ×1
- `D\_sq\_eq\_eta` ×1
- `J\_four` ×1
- `J\_lifts\_W10` ×1
- `J\_sq` ×1
- `J\_swaps\_moduli` ×1
- `eta\_eq\_exp\_fourA` ×1
- `eta\_power\_T\_phase` ×1
- `partition\_T\_invariant` ×1

## Per-file marks

| file | `\witness` marks |
|---|--:|
| `main.tex` | 247 |

Re-generate with `pnpm run witness:inventory`; a hand-edited figure is a defect.
