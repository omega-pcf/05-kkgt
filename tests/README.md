# Tests for the note (package `kkgt`)

The suite lives in `tests/`; its support code lives in the importable
package `tests/src/kkgt` — `kkgt.constants` (closed forms and the numbers
the tests assert) and `kkgt.harness` (the repository root, the committed
figure artifacts and their byte pin, the Planck-Λ formula). There is no
computation module any more: each claim test owns the code that produces
its numbers and asserts them directly (SPEC-002). `main.tex` cites the
tests that check its numbers with `\testref{...}` (a test name of the
suite), which `tests/test_section_census.py` parses to prove that every
reference the manuscript makes exists in the suite, and that no numbered
`section~N` citation is left. The same file holds the no-import contract: an AST
sweep of `tests/` and `scripts/` that fails on any `import`/`from`
resolving to the deleted `kkgt.sections` package or to a `seccion_*`
function, so the artifact cannot return (SPEC-002 §3).

```bash
# counts:begin id="commands"
uv run pytest tests/ -q                 # whole suite   (498 tests)
uv run pytest tests/ -q -m 'not slow'   # without >10 s (495 tests)
# counts:end id="commands"
pnpm run test                           # same, through package.json
```

The pytest configuration lives in `pyproject.toml` under `[tool.pytest.ini_options]`
(`testpaths`, `pythonpath`, `markers`, `addopts`), so a bare `uv run pytest` collects
the same <!-- counts:begin id="suite-total" -->498<!-- counts:end id="suite-total" --> tests as `uv run pytest tests/ -q`.

## Layout (mirrors `03-crystalline-worldsheet/tests/`)

```
tests/
├── conftest.py                # Agg backend, tests/src on sys.path (no fixtures)
├── src/kkgt/
│   ├── __init__.py            # re-exports of constants and REPO_ROOT
│   ├── constants.py           # PHI, M_PCF, OBS_G, FIGURES, FIGURE_MD5, SLOW_SECTIONS
│   └── harness.py             # figure artifacts + md5 pin, lam_planck, REPO_ROOT
├── test_section_census.py     # \testref{...} <-> main.tex contract, figures, no-import AST sweep
├── test_sections_01_08.py     # tower, spectra, phase, Bessel chain, look-elsewhere
├── test_sections_09_16.py     # granularity, contact, figures 1-2, gaps, Koide
├── test_sections_17_28.py     # observer level, units, window, nome, Poisson
├── test_sections_29_38.py     # lattice point, quintessence, entropy, area law
├── test_sections_39_43.py     # tilings (figures 4-5), dictionary, three columns
├── test_sections_44.py        # figure 1 (fig_background): the background figure
├── test_sections_45_46.py     # (F10) observer level, Hopf foliation and J
└── test_sections_47.py        # v138 section 47: independent checks of its figures
```

Deleted by SPEC-002 (units 3–4): `src/kkgt/sections/` (the computation
package), `test_section_runs.py` (the marker driver) and the
`sections_module` / `sections` / `run_section` fixtures of `conftest.py`.
`tests/REPORT.md` is the dated report of the earlier survey and is kept
as it was written.

## Section -> test map

| section | deep tests |
|---|---|
| 1  | `TestSection1Numbers` (41) |
| 2  | `TestSection2Casimir` (3) |
| 3  | `TestSection3TwoBraneSpectra` (7) |
| 4  | `TestSection4MetricPositivity` (5) |
| 5  | `TestSection5QuarterPhase` (2) |
| 6  | `TestSection6BesselChain` (5) |
| 7  | `TestSection7Prediction` (4) |
| 8  | `TestSection8LookElsewhere` (12) |
| 9  | `TestSection9GapRatios` (7) |
| 10 | `TestSection10Granularity` (12) |
| 11 | `TestSection11ContactConfigurations` (5) |
| 12 | `TestSection12FigureOneStatements` (21) -- checks only: figure 1 moved to section 44 |
| 13 | `TestSection13FigureTwoReciprocity` (11) |
| 14 | `TestSection14RingGaps` (12) |
| 15 | `TestSection15StateCount` (6) |
| 16 | `TestSection16KoideFromM` (4) |
| 17 | `TestSection17ObserverLevelFromLambda` (3) |
| 18 | `TestSection18TwoReadingsOfTheSameCurvature` (3) |
| 19 | `TestSection19TowerOffset` (9) |
| 20 | `TestSection20TwoCandidates` (6) |
| 21 | `TestSection21TwoBraneRival` (2) |
| 22 | `TestSection22CurvatureUnit` (6) |
| 23 | `TestSection23LatticeOfUnits` (10) |
| 24 | `TestSection24ScaleAndTop` (4) |
| 25 | `TestSection25AutodualWindow` (11) |
| 26 | `TestSection26WindowEdge` (6) |
| 27 | `TestSection27WindowAsNome` (6) |
| 28 | `TestSection28PoissonTheta` (4) |
| 29 | `TestSection29LatticePointFromOmegaLambda` (8) |
| 30 | `TestSection30SymmetricThroat` (5) |
| 31 | `TestSection31ModuliMetric` (11) |
| 32 | `TestSection32LevelVersusGridShape` (7) |
| 33 | `TestSection33ColourHole` (8) |
| 34 | `TestSection34Quintessence` (4) |
| 35 | `TestSection35HalfThreshold` (8) |
| 36 | `TestSection36BlackHoleWhereNeeded` (7) |
| 37 | `TestSection37Consistency` (13) |
| 38 | `TestSection38AreaLawHalf` (4) |
| 39 | `TestSection39FibonacciTiling` (28) |
| 40 | `TestSection40DictionaryAgainstTheCusp` (27) |
| 41 | `TestSection41FiveRegularTilings` (18) |
| 42 | `TestSection42TwoCoordinatesAndTheStep` (33) |
| 43 | `TestSection43ThreeColumns` (12) |
| 44 | `TestSection44BackgroundFigure` (31) |
| 45 | `TestSection45ObserverLevel` (15) |
| 46 | `TestSection46HopfFoliation` (13) |
| 47 | `TestSection47ThePentagonalCode` (6) |

The number in parentheses is the count of collected items of that class
(`uv run pytest tests/ --collect-only -q | grep -c <ClassName>`), so it
moves whenever a test is added. Every section is covered by one or more
deep tests that recompute its numbers; the five figure tests
(`test_section_writes_its_figure[section-10|13|39|41|44]`) verify the
committed artifacts instead of writing anything. The manuscript no longer
cites them: since the witness labels left the captions, only the artifact
is pinned here, never the attribution.

## Two kinds of check

* **independent** -- the quantity is recomputed in the test from the closed
  form (Bessel zeros, Fibonacci words, lattice counts, weighted fits) and
  compared with an explicit tolerance.  This is the regression net: it does
  not depend on anything else being right.
* **migrated** -- the computation itself lives in the test module
  (SPEC-002 §1): the body of the section these tests consume was moved out
  of the deleted package into the test file, and every number the file used
  to read back from a section's stdout is asserted on its value, at the
  section's own print precision and with the section's own tolerance.

No test parses a section's stdout any more: there are no sections to run.

Tolerances are never loosened to make a test pass.  Rounding tolerances are
the width of the printed precision (`.4f` -> `5e-5`); everything else is
stated in the test with a comment saying where the number comes from.

## Slow tests

`@pytest.mark.slow` marks what takes more than 10 s on this machine
(three tests, all of section 41):

* `test_section_writes_its_figure[section-41]` (the artifact of figure 5);
* `test_section41_prints_its_conclusions` and
  `test_qubit_bond_dimension_of_54` (the section's own checks).

Everything else runs under 10 s: section 40 takes 9.2 s and section 44
(figure 1) 2.2 s. The census test `test_slow_figure_sections_are_declared`
pins `SLOW_SECTIONS ∩ FIGURES = {41}`.

Figures are never written by a test: the five `fig_*.pdf` files belong to
the generators of `scripts/figures` (`pnpm run figures`), and the tests
only verify that the committed bytes of `images/` still match
`FIGURE_MD5`.
