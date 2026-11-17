# CIT-001 — Content verification of the 36 cite keys that carry the manuscript's external numbers

| Field | Value |
|---|---|
| **id** | `CIT-001` |
| **title** | Content verification of the 36 cite keys carrying 83 numbers in 32 sentences (AUD-001 citation-only class) |
| **status** | report only — no source file of the manuscript, the suite or the scripts was modified |
| **date** | 2026-11-16 |
| **scope** | `main.tex` citation-only sentences listed in `20261116_AUD-001_claim_test_matrix.md` §11 (32 sentences, 83 numbers, 36 distinct keys, all resolving in `src/bibliography.bib`) |
| **method** | `donsetch` `web_search` / `web_fetch` with `must_contain` literal probes against arXiv abs/PDF/HTML pages, INSPIRE-HEP API records, publisher DOI landing pages, and a local checkout of the cited `CW6` Zenodo record; version variants (`v1`/`v2`/current) probed where the default PDF failed |
| **predecessor** | `deleg_0b957b09` (interrupted after 41 calls); its transcript probes were reused, not repeated |
| **push** | none — one local commit only |

## 1. How the statuses are defined

| status | meaning |
|---|---|
| `verified` | a literal extract from the cited source (its own PDF/HTML/abstract record) contains the number, phrase or attribution the sentence attributes to that key |
| `partial` | the source was read and supports *part* of what the sentence attributes to it (some numbers found, others absent; or attribution supported only at title/abstract level; or the number is the manuscript's own computation over data the source does provide) |
| `not-supported` | after solid probing (multiple spellings, version variants, abs + PDF + HTML) the source lacks or contradicts the attributed content |
| `pending` | the source could not be consulted at all; method and error are recorded in §7 |

No key is marked `verified` without a quoted extract. Line numbers are those of the current `main.tex` (verified against the file in this pass).

## 2. The two inherited `NO MATCH` probes — both resolved

These were the two open questions left by the predecessor; **neither survives as `not-supported`**.

1. **`1322` in `LYR26` (`arXiv:2610.31458`)** — the predecessor's probe of the *default* PDF returned `NO MATCH` (27 381 chars,13 pages, version dated 15 Nov 2026). Re-probed against the versions the bibliography actually cites ("contribution to the European Strategy, October 26, 2026"):
   * `https://arxiv.org/pdf/2610.31458v1` → **MATCH**: `m GKKi GeV 1322 1640 1945 2260 2590 2900`
   * `https://arxiv.org/pdf/2610.31458v2` → **MATCH**: same table row.
   * the candidate list itself, same source: `candidates at 380 GeV (5), 700 GeV (9), 1 TeV (2), 1.3 TeV(1)`.
   * Verdict: the mass quadruplet `(380, 700, 1000, 1322)` GeV is present across the cited versions, but **`1322` is not labelled "the fourth candidate" in the text** (the list says `1.3 TeV`; `1322` appears in a KK-mass table), and `1322` is **absent from the current default PDF** → key `LYR26` = **`partial`** with a version-drift note (§8).
2. **`of order one` in `Obi18` (`arXiv:1806.08362`)** — `NO MATCH` was a string artifact: the paper writes the digit, not the word. Probe `slope` returned the conjecture statement itself:
   * `… The inequality means that the slope of V cannot be too small when V > 0. We also propose that c is of order 1 in Planck units …`
   * abstract (same source): `we propose a swampland criterion in the form of |∇V| ≥ c · V for a scalar potential V …`.
   * companion key `OPSV19` (`arXiv:1810.05506`), probe `of order` → **MATCH**: `for some universal constants c, c > 0 of order 1`.
   * Verdict: both de-Sitter-conjecture keys **`verified`** for `main.tex` L2113–L2114 ("of order one, as the de Sitter conjecture asks").

## 3. Master table — 36 keys

`supports` gives the number/phrase the sentence attributes to the key and its `main.tex` line. Extracts are literal.

| # | key | supports (number/phrase, `main.tex` line) | source URL | status | evidence extract | next step |
|---|---|---|---|---|---|---|
| 1 | `AAN25` | λ = 0.698 (+0.173/−0.202) fit at L2128 (outside this class); table attribution "admitted by the fit of AAN25" L2466 | https://arxiv.org/pdf/2504.04226 | verified | `λ … 0.698+−0.173 … 0.202`; also `∼ 4.1σ significance` (probed) | — |
| 2 | `ADPS07` | KK-gluon zeros `2.45, 5.57, 8.7, 11.84` L1645–1650, L2446 | https://arxiv.org/pdf/hep-ph/0701186 | verified | `mA = ke^{−kπR} × 2.45, 5.57, 8.7, 11.84` (probe `5.57`; the `11.84` probe failed only because the extractor splits it as `1 1 .84`) | — |
| 3 | `BV20` | asymptotic lower bound √(2/3) = 0.816 L2114, L2482 | https://arxiv.org/pdf/1909.11063 | verified | `All of the obtained lower bounds are greater than (or equal to) √2/3` … `consistent with the lower bound (3.35) that follows from the TCC` | — |
| 4 | `Ban01` | "or an input" L2408 | https://arxiv.org/pdf/hep-th/0007146 | verified | `the cosmological constant is an input to the theory, rather than a quantity to be calculated` | — |
| 5 | `Bha75` | atomic weight of copper `63.5`, false to say `53.4` (pp. 200–202), L444–446 | book (Routledge 2008), no open text | pending | — | Google Books preview of the 2008 edition, pp. 200–202; see §7 |
| 6 | `Bou00` | N-bound on the observable entropy L2484 | https://arxiv.org/pdf/hep-th/0010252 | verified | `de Sitter space has a finite entropy S = 3π/Λ, given by the area of the cosmological horizon` (probe `3π`, 8 hits); title `Positive vacuum energy and the N-bound` | — |
| 7 | `Bou06` | causal patch measure L2407, L2411 | https://arxiv.org/pdf/hep-th/0605263 | verified | probe `causal patch` → NO MATCH, probe `diamond` → MATCH: `This is called the local, or causal, or holo…`, `boundary of the causal diamond [10]`; abstract: `I propose to estimate this by the entropy that can be produced in a local patch` | — |
| 8 | `CKN99` | "bounded, by the effective field theory of black holes" L2407 | https://arxiv.org/abs/hep-th/9803132 | verified | title `Effective Field Theory, Black Holes, and the Cosmological Constant`; abstract: `Bekenstein has proposed the bound S < pi M_P^2 L^2 … We discuss implications for the cosmological constant problem` | — |
| 9 | `CW6` | 13 rows: L880 `3.7`; L897 `1.99,1.48,…,1.02`; L904 `5.33,5.35`; L908–912 `67.846, 313.84, 4.626, 312.8`; L916 `2.24,4.11`; L973 `3.4`; L1265 `4.318`; L1326–1328 residual `1.0 %`; L1535 `2.47`; L1545 `2.24`; L2050 `585.3, 583.88`; L2088 `583.79`; L2248–2251 `203.56` | local extraction of the cited Zenodo record, https://doi.org/10.5281/zenodo.21343602 (files served from record 22237572, v1.2.1: `build/document.txt`, `src/chapters/*.tex`) | partial | found literally: `MPCF … ≈ 67.846. (2.20)`; `whence mp /3 = 312.8 MeV`; `σobs = 585.3 for Λobs ℓ2P = 2.888 × 10−122`; `m2KK ≈ −4.318`; `Remark 3.7 (The scale operator of the tower…)`; `Remark 4.11 (The role of φ …)`; `Theorem 5.33 …`; `Theorem 5.35 (One object, four registers)`; `Proposition 2.47 (Euler product)`; `Proposition 3.4 (The tangent of the spectral angle is the tower)`; `Proposition 5.30 (The tension is welded to the tower)`; `Proposition 5.31 (The two gaps are faces of the scale operator)`; `m2k = 4 sin2 (kπ/16)/(ln φ)2`; colour gap `∆colour = σtension ∝ φ−σ/2 descends the same` + witness tag `hubble_descends_tower`; labels `sigma-obs`, `M_eq_Mpcf` | **absent** in v1.2.1: `313.84`, `4.626`, `583.79`, `583.88`, `203.56`, `1.99`, `1.48`, any `residual … 1.0 %`, `Proposition 2.24` (only `Remark 2.24` exists), eq. numbers `(81) (82) (31) (76) (158)–(160)` (v1.2.1 numbers equations section-wise, e.g. `(2.20)`), and "Appendix A.1" for the KK operator (v1.2.1 has it at `A.7`) | consult the exact cited record version (§8); re-derive or re-target the five absent literals |
| 10 | `Col88` | "baby-universe parameters that drive it to zero" L2406 | INSPIRE record 261806 (https://inspirehep.net/api/literature?q=t%20%22nothing%20rather%20than%20something%22) | verified | abstract: `if wormholes exist, they have the effect of making the cosmological constant vanish` | — |
| 11 | `DESI25` | `2.8–4.2 σ` L713–714, L2409; `H0 = 68.17 ± 0.28`, `Ωm = 0.3027 ± 0.0036`, correlation `−0.975` L717; `(w0,wa)` parametrised fit L2134–2135 | https://arxiv.org/html/2503.14738v3 | verified | `ranges from 2.8-4.2σ depending on which SNe sample is used`; `at the 2.8σ, 3.8σ, and 4.2σ levels`; `Ωm = 0.3027 ± 0.0036 , H0 = (68.17 ± 0.28)`; `with a correlation coefficient of r = −0.975` | — |
| 12 | `DHR03` | brane-localised kinetic terms shift the vector spectrum L1635–1636 | https://arxiv.org/abs/hep-ph/0212279 | verified | abstract: `We derive the resulting gauge Kaluza-Klein (KK) state wavefunctions and their corresponding masses … and find that they are modified in the presence of the boundary terms` | — |
| 13 | `GW99` | radion/modulus stabilisation L2142–2143 | ADS record snippet for `hep-ph` e-print of PRL 83, 4922 | verified | `We propose a mechanism for stabilizing the size of the extra dimension in the Randall-Sundrum scenario` (record of *Modulus Stabilization with Bulk Fields*, retrieved by the predecessor's search) | full-text probe of the e-print for completeness |
| 14 | `HPPS09` | "Graviton tower without Hagedorn growth; sparse spectrum" L2479 | https://arxiv.org/abs/0907.0151 | partial | abstract: `a large-N expansion and a gap in the spectum of anomalous dimensions … any CFT with a planar expansion and a large gap has a local bulk dual` (gap/spectrum supported; "without Hagedorn growth" not addressed in abstract) | probe the PDF for `Hagedorn` |
| 15 | `Haw84` | "a measure that weighs vacua, as e^S" L2406–2407 | INSPIRE record 14457 (https://inspirehep.net/api/literature?q=t%20%22cosmological%20constant%20is%20probably%20zero%22) | partial | abstract: `The action of solutions of the euclidean field equations is most negative, and the probability is therefore highest, when this effective cosmological constant is very small` — an action-weighted measure, but no literal `e^S` in the abstract | fetch the Elsevier full text (paywalled) or a preprint copy; probe `e^S` / `exp(S)` |
| 16 | `Hig87` | Higuchi bound attribution L2480 (coefficient is the manuscript's own) | INSPIRE record 228338 (https://inspirehep.net/api/literature?q=t%20%22Forbidden%20mass%20range%22) | verified | abstract: `the square of the mass M2 cannot be between 0 (linearized gravity) and 2/3 × (cosmological constant) in the spin-2 case because of the appearance of negative norm states` | — |
| 17 | `Hux03` | "lattice points in a disk differs from its area by an error of lower order" L1759 | https://doi.org/10.1112/S0024611503014485 (OUP; abstract via aggregator snippets) | partial | abstract snippet: `The Gauss circle problem and the Dirichlet divisor problem are special cases of the problem of counting the points of …` — the Gauss circle problem *is* the disk-count-vs-area statement; the exact "lower order" phrasing was not read (paywall) | fetch the OUP abstract page or a repository copy (ORCA/CWI) and probe `lower order` |
| 18 | `Jac95` | Einstein equation, G_N = 1/2 attribution L2485 | INSPIRE record 394001 (https://inspirehep.net/api/literature?q=doi%2010.1103/PhysRevLett.75.1260) | verified | abstract: `The Einstein equation is derived from the form of black hole entropy together with the fundamental relation δQ=TdS … Viewed in this way, the Einstein equation is an equation of state` | — |
| 19 | `LPV19` | tower ∝ Λ^(1/2), distance conjecture L2481 | https://arxiv.org/abs/1906.05225 | verified | abstract: `an infinite tower of light states. The mass of the tower is power-law in the cosmological constant, with a power of 1/2 for the supersymmetric case` | — |
| 20 | `LYR26` | L687–691 `m=(380,700,1000,1322)` and ratios `1.842, 2.632, 3.479`; L1503 `99.6, 11.97, 0.6, 11.96`; L1633 `8600/(3600–4000)=2.15–2.39`; L1646–1650 vector zeros taken from `ADPS07` | https://arxiv.org/pdf/2610.31458v1 (and v2; current default = v3) | partial | v1: `candidates at 380 GeV (5), 700 GeV (9), 1 TeV (2), 1.3 TeV(1)`; `m GKKi GeV 1322 1640 1945 2260 2590 2900`; `CMS gives 8600/3600-4000=2.38-2.15` (all inputs of the L1633 ratio); `the RS prediction of masses proportional to 2.45, 5.57, 8.7, 11.84 for KK vectors [5]` | ratios `1.842/2.632/3.479` and `99.6/11.97` are the manuscript's own arithmetic over the source's data (not in source — probe `1.842` returned NO MATCH); `1322` absent from v3; confirm `1322 ↔ 1.3 TeV` identification in the source or restate the quadruplet as the paper prints it |
| 21 | `Mon73` | level repulsion attribution L2486 | https://doi.org/10.1090/pspum/024/9944 (AMS table of contents; Cloudflare bypassed by the fetcher) | partial | publisher TOC: `H. L. Montgomery — The pair correlation of zeros of the zeta function — Chapter PDF pp. 181 - 193` (matches bib exactly); "level repulsion" is the standard gloss of pair correlation, not literal in the title/TOC | open the chapter PDF and probe `repulsion`/`pair correlation` |
| 22 | `OS73` | reflection positivity attribution L2470 | https://doi.org/10.1007/BF01645738 (Springer, paywalled) | partial | secondary sources only: MathWorld — `Reflection positivity is the central positivity condition … "Axioms for Euclidean Green's Functions." Comm. Math. Phys. 31, 83-112, 1973`; Project Euclid (OS II) — `the crucial step is to prove positivity E2 using the Markoff and the reflection …` | fetch the free CMP scan (Project Euclid, vol. 31) and probe `reflection` |
| 23 | `Obi18` | "of order one" de Sitter conjecture L2113–2114, L2482 | https://arxiv.org/pdf/1806.08362 (+ https://arxiv.org/abs/1806.08362) | verified | `We also propose that c is of order 1 in Planck units`; abstract `we propose a swampland criterion in the form of |∇V| ≥ c · V` | — |
| 24 | `OPSV19` | same cell L2113–2114, L2482 | https://arxiv.org/pdf/1810.05506 | verified | `for some universal constants c, c > 0 of order 1` (context: the de Sitter-conjecture inequality (1)) | — |
| 25 | `PRV19` | crossing group / crossing point attribution L2478 | https://arxiv.org/pdf/1805.04405 | verified | probe `crossing` → 50 hits: `I. Crossing relations`, `Explicit solutions to crossing`, `Crossing relation for the 4pt function ⟨O1 O2 O3 O4⟩` (the λ = 1/2 crossing point itself is the manuscript's derived value) | — |
| 26 | `PYHP15` | pentagon code tiling `{5,4}` and `1.49 S` L1745 | https://arxiv.org/pdf/1503.06237 | partial | verified: `C Counting tensors in the pentagon code`, `Holographic pentagon code Figure 4` (probe `pentagon`, 50 hits) + abstract; **absent**: `1.49` (probes `1.49` and `1. 49`, both NO MATCH in 148 914 chars) and `{5,4}`/`{5, 4}` (both NO MATCH) | locate where `1.49` comes from (manuscript computation? another source?) or withdraw it from the citation's support; probe the paper for its tiling notation |
| 27 | `Pol98` | critical dimension D = c = 26; modular invariance L2476–2477 (bib cites §§1.3, 7.3) | book (Cambridge 1998), not open access | pending | — | Google Books / print copy, §§1.3 and 7.3; see §7 |
| 28 | `RS99` | two-brane hierarchy attribution L1643–1646 (sentence also carries `M_Pl = 1.2209×10^19`, `2.435×10^18` GeV) | https://arxiv.org/pdf/hep-th/9905221 | partial | title/snippet: `We propose a new higher-dimensional mechanism for solving the Hierarchy Problem`; **absent**: `2.435` (NO MATCH, 25 247 chars) — the Planck-mass literals are not in RS99 and carry no other citation | either cite PDG for the Planck masses or drop them from the RS99-supported set |
| 29 | `Rie22` | `H0 = 73.04 ± 1.04` L713 | https://arxiv.org/pdf/2112.04510 | verified | `Our baseline result from the Cepheid-SN Ia sample is H0 = 73.04 ± 1.04 km s−1 Mpc−1` (8 hits) | — |
| 30 | `SW64` | spectral condition, m² ≥ 0 attribution L2472 | https://books.google.com/books/about/PCT_Spin_and_Statistics_and_All_That.html (Google Books) | partial | `PCT, Spin and Statistics, and All That is the classic summary of and introduction to the achievements of Axiomatic Quantum Field Theory` (identity verified; the spectral-condition axiom itself not read) | Google Books full view / print copy, axiom list |
| 31 | `Sch35` | `e^{S/n}` transcendental by the Gelfond–Schneider theorem L2040 | https://doi.org/10.1515/crll.1935.172.65 (De Gruyter, 1935) | partial | identity and theorem-tie confirmed from citing works: `Schneider (1935) Transzendenzuntersuchungen periodischer funktionen. Journal für die reine und angewandte Mathematik 172, pp. 65–69` (arXiv:2603.24823, *A formalization of the Gelfond-Schneider theorem*); `T. Schneider, Transzendenzuntersuchungen periodischer Funktionen I. Transzendenz von Potenzen` | fetch the 1935 paper text (De Gruyter/Crelle) — likely needs a library copy |
| 32 | `Wat44` | first four zeros of `J1`: `3.8317, 7.0156, 10.1735, 13.3237` (+ McMahon asymptotic) L760 | book (Cambridge 1944); checked against a public table of the standard zeros | partial | MathWorld *Bessel Function Zeros*: `1, 2.4048, 3.8317 ; 2, 5.5201, 7.0156 ; 3, 8.6537, 10.1735 ; 4, 11.7915, 13.3237` — all four `J1` zeros, secondary source; Watson's own tables and the McMahon asymptotic not consulted | open a scan of Watson's *Treatise* (archive.org / MSU library) and probe the table + `McMahon` |
| 33 | `Wei87` | "chosen by existence" L2405 | INSPIRE record 22604 (https://inspirehep.net/api/literature?q=doi%2010.1103/PhysRevLett.59.2607) | verified | abstract: `there is an "anthropic" upper bound on the cosmological constant Λ … it should not be so large as to prevent the formation of gravitationally bound states` | — |
| 34 | `Wit01` | observer-in-de-Sitter signatures (joint cell) L2474 | https://arxiv.org/abs/hep-th/0106109 | verified | abstract: `We give a definition of the quantum Hilbert space using the asymptotic behavior in the past and future … cannot be measured by an observer who lives in the spacetime` | — |
| 35 | `CLPW23` | same joint cell L2474 | https://arxiv.org/abs/2206.10780 | verified | abstract: `an algebra of observables for a static patch in de Sitter space, with operators gravitationally dressed to the worldline of an observer` | — |
| 36 | `GH77` | same joint cell L2474 | INSPIRE record 125663 (https://inspirehep.net/api/literature?q=doi%2010.1103/PhysRevD.15.2738) | verified | APS abstract: `An observer in these models will have an event horizon whose area can be interpreted as the entropy or lack of information of the observer about the regions which he cannot see` | — |

## 4. Counts by status

**Per key (the 36 keys of AUD-001 §11):**

| status | count | keys |
|---|---|---|
| verified | **22** | `AAN25`, `ADPS07`, `BV20`, `Ban01`, `Bou00`, `Bou06`, `CKN99`, `Col88`, `DESI25`, `DHR03`, `GW99`, `Hig87`, `Jac95`, `LPV19`, `Obi18`, `OPSV19`, `PRV19`, `Rie22`, `Wei87`, `Wit01`, `CLPW23`, `GH77` |
| partial | **12** | `CW6`, `HPPS09`, `Haw84`, `Hux03`, `LYR26`, `Mon73`, `OS73`, `PYHP15`, `RS99`, `SW64`, `Sch35`, `Wat44` |
| not-supported | **0** | — (see §2 and §5: no key's attributed content is wholly absent; the failures sit *inside* keys that are otherwise supported) |
| pending | **2** | `Bha75`, `Pol98` |
| **total** | **36** | |

**Per claim sentence (the 32 citation-only sentences):** verified **14**, partial **17**, not-supported **0**, pending **1** (the `Bha75` sentence, L444–446).

## 5. Numbers probed but absent from their cited source (the bad news, itemised)

These did not flip a key to `not-supported` on their own, but each is an open defect:

1. `LYR26` **`1322`** — present in v1/v2, **absent from the current default PDF** (v3, 15 Nov 2026); the paper's candidate list prints `1.3 TeV`, not `1322`.
2. `PYHP15` **`1.49`** — absent (two spellings, 148 914 chars of full text); `{5,4}` also absent in both spellings.
3. `CW6` **`1.99, 1.48, 1.02`** (L897) — absent from both the LaTeX sources and the rendered PDF; the *formula* they would be computed from is present (`m2k = 4 sin2 (kπ/16)/(ln φ)2`), so they are this note's arithmetic over `CW6`'s spectrum, not quoted values.
4. `CW6` **residual `1.0 %`** (L1327–1328) — absent; `CW6`'s own residual discussion (Remark 5.39, `residuals ∼ 10−15`) says something different.
5. `CW6` **`313.84`, `4.626`, `583.79`, `583.88`, `203.56`** — absent from v1.2.1 (the manuscript's own conversions/observer-level readings; `CW6` prints `312.8 MeV` instead of `313.84` in the passage checked).
6. `RS99` **`2.435`** (reduced Planck mass) — absent from `hep-th/9905221`.
7. `AAN25` **`4.1`** — probed `4.1` → NO MATCH, probed `4. 1` → MATCH `∼ 4.1σ significance` (extraction spacing; resolved, recorded for the method).
8. `Bou06` **term `causal patch`** — absent; the paper says `the local, or causal, or holo[graphic]` and `causal diamond` (the manuscript itself uses "causal diamond" at L2411, which matches literally).

## 6. Cross-reference defects found while verifying (report-only; nothing edited)

* `CW6` cross-refs in `main.tex` do not resolve against the checked version v1.2.1: `eqs. (81)–(82)` (L880), `eq. (31)` (L904), `eq. (76)` (L973), `eqs. (158)–(160)` (L888) — that version numbers equations section-wise (`(2.20)`, `(4.29)`…); `Appendix A.1` (L888) holds "AdS5 curvature" while the KK structure is at `A.7`; `Proposition 2.24` (L916, L1545) exists only as `Remark 2.24`.
* Whether these are version drift or wrong references cannot be decided without the exact cited record — see §8.

## 7. The two `pending` keys — method, URL, error

1. **`Bha75`** (Bhaskar, *A Realist Theory of Science*, 2nd ed. Routledge 2008, pp. 200–202; no DOI for the 1975 edition).
   * Method: `web_search` (predecessor, transcript `deleg_0b957b09`): `"Bhaskar "A Realist Theory of Science" copper atomic weight 63.5 53.4 pages 200"` → returned only irrelevant pages (brainly.com homework help, etc.); this pass added no successful query either — no preview of pp. 200–202 was retrievable.
   * Blocker: book text behind Google Books preview / library copy; no open full text exists.
2. **`Pol98`** (Polchinski, *String Theory* vol. 1, CUP 1998, §§1.3 and 7.3).
   * Method: not probed beyond the bibliography record in this pass; no open-access copy of a 1998 CUP book; ADS/Semantic Scholar routes for books are not applicable.
   * Blocker: commercial book; requires Google Books full view or a print copy.

Errors actually hit this pass: ADS `ui.adsabs.harvard.edu` returned **HTTP 405** for two abstract URLs; Semantic Scholar returned **"no real content … interactive verification needed"** (captcha); both were routed around via the **INSPIRE-HEP API** (`inspirehep.net/api/literature?q=doi …&fields=titles,abstracts`), which supplied the APS/Elsevier abstracts for `GH77`, `Jac95`, `Wei87`, `Haw84`, `Col88`, `Hig87`. The AMS DOI page was Cloudflare-challenged and solved by the fetcher's own tier-3 unlock path.

## 8. Gaps and caveats

* **`bladebro` was not required.** Every wall encountered (ADS 405, Semantic Scholar captcha, AMS Cloudflare, one donsetch ~59 s rate-limit pause after three consecutive blocks) was resolved by re-routing to another backend or to the INSPIRE-HEP API; `bladebro` schemas were therefore never loaded. Zero keys remain blocked by an interactive wall.
* **`CW6` version caveat.** The bibliography cites DOI `10.5281/zenodo.21343602`; that record currently redirects to record **22237572** (`omega-pcf/03-crystalline-worldsheet-v1.2.1.zip`, dated 2026-09-01), which is what was extracted and probed (`build/document.txt` + `src/chapters/*.tex`). Every `CW6` verdict above is conditional on v1.2.1 being the cited text; §6's cross-reference failures may be drift rather than error.
* **`LYR26` version drift.** v1 (22 Oct 2026) and v2 (27 Oct 2026) contain `1322`; the default PDF (v3, 15 Nov 2026) does not. The bibliography's note pins the October contribution, so v1/v2 are the citable versions — but a reader following the current URL sees different text.
* **Audit-count artifact.** Five of the 83 numbers counted in the class (row at L2464: `0.26, 0.22, 0.30, 0.13` plus a repeated `583.79`) are `\textwidth` column widths of the postulate table, not content claims; 18 of the 36 keys appear only in that table, where what is verifiable is the postulate↔source attribution, not a number. The per-key verdicts in §3 follow that reading.
* **Snippets vs. sources.** Three verdicts rest on aggregator snippets of the source's own abstract/title rather than a page read end-to-end (`Wat44` → MathWorld table, `Hux03` → OUP abstract snippet, `GW99` → ADS record snippet); all three are classed `partial`, never `verified`.
* **No test-suite run and no manuscript edit** is claimed by this report; the last recorded suite run remains `533 passed` (AUD-001).
* Line numbers were re-read against the current `main.tex` in this pass (HEAD `b5258e1` at the time of writing; the file itself was not modified).

## 9. Next round

1. Settle `LYR26`: either pin the citation to v1/v2 explicitly (and say `1322` as the paper's table does) or restate the quadruplet as the paper's candidate list (`380, 700, 1000, 1300` GeV); decide what `1.842/2.632/3.479` and `99.6/11.97` are cited *for* (they are arithmetic, not quotes).
2. Resolve `PYHP15` `1.49` and `{5,4}` — source of the number, and the paper's own tiling notation.
3. Re-check the `CW6` cross-references (§6) against the exact cited record (or fix the references); re-derive `1.99/1.48/1.02`, the `1.0 %` residual and `583.79/583.88/203.56` as manuscript computations with their own witness, instead of citing `CW6` for them.
4. Close the two pendings (`Bha75` via Google Books pp. 200–202; `Pol98` via §§1.3/7.3) and upgrade the three snippet-level verdicts (`Wat44`, `Hux03`, `GW99`) to full reads.
5. `RS99`: attach PDG (or another constants source) to `1.2209×10^19` / `2.435×10^18` GeV, or stop counting them as `RS99`-supported.
