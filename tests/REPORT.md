# Report: the numbered sections → pytest suite

## (a) Tree of files created / modified

```
pyproject.toml                 M  [dependency-groups] dev = ["pytest>=8.0"]
                                       + [tool.pytest.ini_options] (testpaths,
                                         pythonpath, addopts, markers)
uv.lock                        M  + pytest 9.2.0, colorama, iniconfig, pluggy, pygments
package.json                   M  scripts: "test", "test:fast"  (scripts block only)
tests/src/kkgt/sections.py      M  the computation, moved here from the
                                      repository root (no entry point left)
tests/                         N
├── README.md                  N  structure, tolerance policy, section→test map
├── REPORT.md                  N  this report
├── conftest.py                N  Agg backend, fixtures sections_module/sections/run_section
├── src/kkgt/__init__.py       N
├── src/kkgt/constants.py      N  PHI, LN_PHI, M_PCF, EPS0, OBS_G, FIGURES, SLOW_SECTIONS
├── src/kkgt/harness.py        N  SectionRun: runs one section, reads its stdout
├── test_section_census.py     N  contract registry ↔ main.tex (numbers and figures)
├── test_section_runs.py       N  the 43 sections run and print their number
├── test_sections_01_08.py     N  sections 1-8
├── test_sections_09_16.py     N  sections 9-16
├── test_sections_17_28.py     N  sections 17-28
├── test_sections_29_38.py     N  sections 29-38
└── test_sections_39_43.py     N  sections 39-43
```

`main.tex`, `citation.csl.json`, `scripts/`, `build/` and `lean/` were not
touched; there are no commits nor pushes.

## (b) Commands, literal output, runtime and counts

```
$ cd /mnt/media/dev/05-kk-golden-throat && uv run pytest tests/ -q
........................................................................ [ 80%]
........................................................................ [ 96%]
...............                                                          [100%]
447 passed in 69.24s (0:01:09)

real    1m10.910s     exit 0
```

```
$ uv run pytest tests/ -q -m "not slow"
........................................................................ [ 81%]
........................................................................ [ 98%]
........                                                                 [100%]
440 passed, 7 deselected in 56.32s

real    0m57.956s     exit 0
```

```
$ pnpm run test
447 passed in 68.15s (0:01:08)      exit 0
```

`uv lock` regenerated `uv.lock` (pytest 9.2.0) and the sections run with
`PYTHONPATH=tests/src uv run python -m kkgt.sections 38`
still runs exactly as before.

## (c) Map section → test

Every section `N` has **at least two tests**: one that *runs* it (id
`section-NN`, with the script's internal `assert`s) and a deep class
`TestSectionNN…` that recomputes its numbers. Full detail in
`tests/README.md`; summary (deep class → number of tests):

| § | class | n | § | class | n | § | class | n |
|---|---|---|---|---|---|---|---|---|
| 1 | TestSection1Numbers | 19 | 16 | TestSection16KoideFromM | 4 | 31 | TestSection31ModuliMetric | 11 |
| 2 | TestSection2Casimir | 3 | 17 | TestSection17ObserverLevelFromLambda | 3 | 32 | TestSection32LevelVersusGridShape | 6 |
| 3 | TestSection3TwoBraneSpectra | 7 | 18 | TestSection18TwoReadingsOfTheSameCurvature | 3 | 33 | TestSection33ColourHole | 8 |
| 4 | TestSection4MetricPositivity | 4 | 19 | TestSection19TowerOffset | 9 | 34 | TestSection34Quintessence | 4 |
| 5 | TestSection5QuarterPhase | 2 | 20 | TestSection20TwoCandidates | 6 | 35 | TestSection35HalfThreshold | 8 |
| 6 | TestSection6BesselChain | 5 | 21 | TestSection21TwoBraneRival | 1 | 36 | TestSection36BlackHoleWhereNeeded | 6 |
| 7 | TestSection7Prediction | 4 | 22 | TestSection22CurvatureUnit | 6 | 37 | TestSection37Consistency | 13 |
| 8 | TestSection8LookElsewhere | 11 | 23 | TestSection23LatticeOfUnits | 10 | 38 | TestSection38AreaLawHalf | 4 |
| 9 | TestSection9GapRatios | 7 | 24 | TestSection24ScaleAndTop | 4 | 39 | TestSection39FibonacciTiling | 28 |
| 10 | TestSection10Granularity | 12 | 25 | TestSection25AutodualWindow | 11 | 40 | TestSection40DictionaryAgainstTheCusp | 27 |
| 11 | TestSection11ContactConfigurations | 5 | 26 | TestSection26WindowEdge | 6 | 41 | TestSection41FiveRegularTilings | 17 |
| 12 | TestSection12FigureOneStatements | 21 | 27 | TestSection27WindowAsNome | 6 | 42 | TestSection42TwoCoordinatesAndTheStep | 33 |
| 13 | TestSection13FigureTwoReciprocity | 11 | 28 | TestSection28PoissonTheta | 3 | 43 | TestSection43ThreeColumns | 12 |
| 14 | TestSection14RingGaps | 12 | 29 | TestSection29LatticePointFromOmegaLambda | 7 | | | |
| 15 | TestSection15StateCount | 6 | 30 | TestSection30SymmetricThroat | 4 | | | |

On top of that `tests/test_section_census.py` (10 tests) pins the numbering: it parses
`main.tex` and requires the cited `sections~N` = {2,10,12,13,29,36,37,38,39,40,41,42,43}
⊆ registry, the 43 sections to be 1..43 contiguous, every `seccion_N` to
carry a `# N.` banner in the source, and the five figures included by the tex
(`fig_granularity`, `fig_one_structure`, `fig_mobius_throat`, `fig_throat_tiling`,
`fig_tilings_strip`) to be written by their own section.

Total: **447 tests** = 43 execution + 394 deep + 10 census.

## (d) Inherited tolerances vs the standard of sibling 03

**Inherited from the script** (the internal `assert`s, now exercised by the run
tests): `1e-12` (ε₀M=π, ring ratio, norms, matrix identities),
`1e-15` (half turn of the fibre), `1e-9` (closure per level, z·τ, τ(12)),
`1e-6·φ^{2s}` (phase on the cell), `atol=1e-9` (Clifford torus),
`1e-9` relative (S = π(A/φ²+B/φ³)), `Decimal 10^-45` (§40, 60 digits),
`1e-6` (Binet deviation, §43), `1e-3` (Hurwitz <0.36, growths),
`5e-4` (W2 slope = 0.9972), `Decimal 1e-9` (non-integrality), `0.05`
(tiling growths), and the ad-hoc windows `1.3<min<1.5`,
`1.7<max<1.9` (§29).

**Standard of sibling 03**: fixtures `np_1e12`/`np_1e9`, `mp25`/`mp40`,
`tol = 10^{-(dps-6)}`, `tol_eig = 10^{-(dps//2)}` and pointwise comparisons
`mpf('1e-20')`.

**What I use here** (same spirit, no mpmath fixtures because almost everything
is float64): exact identities with `1e-12`/`1e-9` (the same ones as the
script); rounding tolerances = the width of the printed precision (`.4f` →
`5e-5`, `.3f`/`.2f` → `5e-4`); exceptions **documented in the docstring**:

* `2e-3` for the M=32 chain of §6 against the J1 zeros (discretisation
  error: the script itself reports rms 0.54 %; the 4th ratio differs by
  1.5e-3);
* `1e-4` for `x1_vec/x1_grav = 0.6381` of §3 (quotient of two zeros
  printed to 4 decimals: 2.4448/3.831706 = 0.63804, the rounding
  propagation is ~1e-4);
* `1e-5`/`5e-5` for the Hurwitz constants of §41, with the window of
  `n` in the docstring (n=15..25 for φ, n=5..15 for √2): below that the
  convergent has not converged, above it the subtraction collapses in float64 (n=40 → 0);
* `rel=1e-3` for the Regge masses of §33 (printed to 3 digits).

No tolerance was widened to make a failing check pass: out of the 38 failures
of the first run, all were my own regex/parameter/expectation mistakes (e.g.
`sigma\[[0,6]\]` with double brackets, `assert run.has(...)` over a function
that returned nothing, shifted indices); the tests were fixed, not the
thresholds. The four exceptions above were already justified when written.

## (e) Checks that fail or stay marked

* **Failures: 0** (`447 passed`) after the first round of fixes.
* **`xfail`/`skip`: none.** No section of the script fails: its 64 internal
  `assert`s all pass (§11, 12, 13, 29, 37, 39, 40, 41, 42, 43).
* **Note on `chk`**: it does not exist (`grep -c chk tests/src/kkgt/sections.py` → 0). The
  "ad-hoc checks" are 64 message-less `assert`s; when run inside
  pytest they fail with the section number and the full stdout
  (`SectionRun.match/has` include them in the message).
* **`@pytest.mark.slow` (7 tests)**, by the 10 s rule:
  * §12 (figure 1, 12.3 s): `test_section_writes_its_figure[section-12]`,
    `test_section_runs_and_prints_its_number[section-12]`,
    `TestSection12FigureOneStatements::test_section12_runs_all_of_its_checks`
  * §41 (figure 5, 35.7 s): `test_section_writes_its_figure[section-41]`,
    `test_section_runs_and_prints_its_number[section-41]`,
    `TestSection41FiveRegularTilings::test_section41_prints_its_conclusions`,
    `::test_qubit_bond_dimension_of_54`
  * §40 measured 9.5 s → left **un**marked (below the threshold).
* The backend is `Agg` and every section runs in a temporary directory: the
  five `fig_*.pdf` and `kk_vs_cw6_out.txt` are not written into the repo.

## (f) "Witness" / tier labels

**`main.tex` (not renamed here; census taken before the witness standardisation):**

> After this report the witness system of `main.tex` was
> standardised (colour by class, `\witness{P}{…}` on its own line, labels
> `W1[CLPW]`, migration of 16 marks `P*`→`P` with verification of the 33
> names against `lean/TorreKK_LYR_v33.lean`). Current state: 114 `\tier`
> (P 12, P* 5, N 74, L 8, R 15) + 16 `\witness{P}` = 130 marks, 12
> `\wtag`, and "not yet compiled" = 0. The table below documents the state
> at which the script was audited.

| label | occurrences |
|---|---|
| `\tier{N}` | 74 |
| `\tier{P*}` | 21 |
| `\tier{R}` | 15 |
| `\tier{P}` | 12 |
| `\tier{L}` | 8 |

Witness items: `W1 (CLPW)`, `W2 (W01)`, `W3 (W01)`, `W4 (W01)`, `W5 (W01)`,
`W6 (W01)`, `W7 (W01)`, `W8 (W01)`, `W9 (GH)`, `W10 (W01)`, `W11 (CLPW)`,
`W12 (CLPW)`. Formula labels: `F1`…`F9`, `B1`…`B4`; statement labels: `I12`.

**`tests/src/kkgt/sections.py` (same names as the tex):**

| label | where (line) | text |
|---|---|---|
| `W2` | 1467 (comment), 1476 (§37) | `W2: integer dimension (states with L0 <= N/2): sigma=3,4,5 -> 1654, …` |
| `W4`, `W8` | 1048, 1051, 1058 (§18); 1131, 1132 (§22) | `observer level (W4 = W8 in the gravitational unit l = sqrt2 l_P)`, `W8 in unit l: 583.877; W4: 583.877`, `= W4 + log_phi 2` |
| `(F1)` | 1003, 1007, 1014, 1017, 1023, 1031, 1042, 1059 (§16-18, §24) | `The scale M of (F1)…`, `M = 313.84 # MeV, (F1)`, `unit of (F1): 4.6258 MeV` |
| `(F9)` | 1017, 1034 (§17) | `The observer level from the value of Lambda, below (F9)…` |
| `(B1)` | 1498, 1507 (§38) | `The 1/2 of (B1): area quantum, Fisher unit and Shannon bit` |
| `I9` | 253 (§1) | `SL2(Z) facts of Imported statement I9` |
| `I12` | 812 (§12, figure header), 1130 (§22) | `I12: $|\Omega|_\sigma=1/2$…`, `l = l_P/sqrt(G_N) = … (I12, tau = i)` |
| `I15` | 827 (§12) | `I15: $z=\varphi y$ carries the triangle onto Z[i]…` |
| `[R]` | 692 (§11) | `the twelve of the icosahedron and that of the background are proved separately (reading [R])` |
| `I1`…`I7` | §42 (prints `I1:`…`I7:`) | the block of section 42 |

The computation does **not** contain the macro `\tier{}` (grep `tier` → 0). The
overlaps `W2/W4/W8/F1/F9/B1/I9/I12/I15/[R]` are the ones to standardise later;
nothing was renamed here.

## (g) Deviations from the standard of 03 and why

1. **The computation stayed in one file** (it was not split into modules).
   Reason: the 43 sections *are* the code of the note, they live in their
   own namespace and are importable as they are; splitting 1990 lines would
   add structure without gaining coverage.  The file did move: it is now
   `tests/src/kkgt/sections.py`, the module `kkgt.sections`, and no entry
   point is left at the root of the repository.  `kkgt.harness.run_section`
   remains the only place that knows how to invoke a section.
2. **pytest in `[dependency-groups] dev`** instead of
   `[project.optional-dependencies] test` as in 03 (what the brief asks for).
3. **`addopts = "--tb=short -p no:cacheprovider"`** without `-v` (03 uses
   `-v --tb=short …`), so that the command line (`-q`) controls the
   verbosity.
4. **Markers**: `slow`, `section`, `figure` (03 uses
   `slow/symbolic/numerical/gauge/gravity/places`): there is no sympy nor
   gauge sectors here, but there is section identity and figures.
5. **No `hypothesis` nor `rich`** (03 declares them as test extras): they do
   not contribute to closed numerical checks.
6. **Runs cached per session in a temporary directory**: the
   sections print and write files (03 `cw6` is pure), so
   `run_section` runs them once per session and shares the stdout; the
   slow tests depend on that cache and are therefore marked `slow` too.
7. **`tests/src/kkgt`** holds the computation, the test constants and the
   harness, because the package *is* the library of the note
   (`pythonpath = ["tests/src"]`; nothing is imported from the root).

## (h) Reconciliation: the computation is a package, the tex cites tests

One pass after this report, with the manuscript, the suite and the
computation brought to the same contract:

* **The computation moved** from the root of the repository to
  `tests/src/kkgt/sections.py`, the module `kkgt.sections`; it is the only
  place where the 43 sections live. One section still runs on its own with
  `PYTHONPATH=tests/src uv run python -m kkgt.sections 38`.
* **No test imports a script**: the harness returns the package module
  (`kkgt.load_sections()`), and `conftest.py` exposes the `sections_module`,
  `sections` and `run_section` fixtures. `pyproject.toml` now sets
  `pythonpath = ["tests/src"]` only.
* **`main.tex` cites tests**: the 26 numbered citations were replaced by 28
  `\testref{<test name>}` references. The five figure captions cite
  `test_section_writes_its_figure[section-NN]` (the test that runs the
  section and requires the figure file), and every number cites the test
  that recomputes it from its closed form or reads it from the stdout of
  its section. The `Code and data` section now describes the package, the
  suite (451 tests), `uv run pytest tests/ -q` and the tolerance policy.
* **`tests/test_section_census.py` is the new contract**: every `\testref`
  of the manuscript must resolve to a collected node id, no test name may
  be defined twice, the cited set is pinned, no numbered `section~N`
  citation may remain, the manuscript may not carry the word the old entry
  point is named with, and each of the five captions must name its test.
  The registry checks (43 sections in order, banners, the five figure
  files, the slow marks) are unchanged.
* **Counts**: `451 passed` (was 447: four census checks added, none
  removed) and `444 passed, 7 deselected` with `-m 'not slow'` (was 440).
  Two test functions were renamed (`...yields_the_j1_zeros`,
  `...give_s_on_average`) to keep the word out of `tests/`; no assertion
  changed.
