# Tests for the note (package `kkgt`)

The computation of the note lives in the importable package
`tests/src/kkgt`, in the module `kkgt.sections`: forty-seven numbered
sections registered in `SECCIONES`.  Nothing is a script any more: the
tests import the package, and `main.tex` cites the tests that check its
numbers with `\testref{...}` (a test name of the suite), which
`tests/test_section_census.py` parses to prove that every reference the
manuscript makes exists in the suite, that no numbered `section~N`
citation is left, and that each of the five figures names the test that
writes it.

```bash
uv run pytest tests/ -q                 # whole suite   (550 tests, ~60 s)
uv run pytest tests/ -q -m 'not slow'   # without >10 s (546 tests, ~60 s)
pnpm run test                           # same, through package.json

PYTHONPATH=tests/src uv run python -m kkgt.sections        # the 47 sections
PYTHONPATH=tests/src uv run python -m kkgt.sections 38     # only section 38
```

The pytest configuration lives in `pyproject.toml` under `[tool.pytest.ini_options]`
(`testpaths`, `pythonpath`, `markers`, `addopts`), so a bare `uv run pytest` collects
the same 550 tests as `uv run pytest tests/ -q`.

## Layout (mirrors `03-crystalline-worldsheet/tests/`)

```
tests/
├── conftest.py                # Agg backend, `sections_module`, `sections`, `run_section`
├── src/kkgt/
│   ├── sections/              # the computation: 47 numbered sections (SECCIONES)
│   │   ├── __init__.py        #   assembles SECCIONES in numeric order
│   │   ├── __main__.py        #   `python -m kkgt.sections [N ...]`
│   │   └── _rest.py           #   the sections SEC-001 layer 2 has not moved yet
│   ├── constants.py           # PHI, M_PCF, OBS_G, FIGURES, SLOW_SECTIONS
│   └── harness.py             # SectionRun: run a section, read its stdout
├── test_section_census.py     # \testref{...} <-> main.tex contract (numbers, figures)
├── test_section_runs.py       # all 47 sections run clean and print their number
├── test_sections_01_08.py     # tower, spectra, phase, Bessel chain, look-elsewhere
├── test_sections_09_16.py     # granularity, contact, figures 1-2, gaps, Koide
├── test_sections_17_28.py     # observer level, units, window, nome, Poisson
├── test_sections_29_38.py     # lattice point, quintessence, entropy, area law
├── test_sections_39_43.py     # tilings (figures 4-5), dictionary, three columns
├── test_sections_44.py        # figure 1 (fig_background): the background figure
├── test_sections_45_46.py     # (F10) observer level, Hopf foliation and J
└── test_sections_47.py        # v138 section 47: independent checks of its figures
```

## Section -> test map

| section | run test | deep tests |
|---|---|---|
| 1  | `test_section_runs.py::test_section_runs_and_prints_its_number[section-01]` | `TestSection1Numbers` (41) |
| 2  | `...[section-02]` | `TestSection2Casimir` (3) |
| 3  | `...[section-03]` | `TestSection3TwoBraneSpectra` (7) |
| 4  | `...[section-04]` | `TestSection4MetricPositivity` (5) |
| 5  | `...[section-05]` | `TestSection5QuarterPhase` (2) |
| 6  | `...[section-06]` | `TestSection6BesselChain` (5) |
| 7  | `...[section-07]` | `TestSection7Prediction` (4) |
| 8  | `...[section-08]` | `TestSection8LookElsewhere` (12) |
| 9  | `...[section-09]` | `TestSection9GapRatios` (7) |
| 10 | `...[section-10]` | `TestSection10Granularity` (12) |
| 11 | `...[section-11]` | `TestSection11ContactConfigurations` (5) |
| 12 | `...[section-12]` | `TestSection12FigureOneStatements` (21) -- checks only: figure 1 moved to section 44 |
| 13 | `...[section-13]` | `TestSection13FigureTwoReciprocity` (11) |
| 14 | `...[section-14]` | `TestSection14RingGaps` (12) |
| 15 | `...[section-15]` | `TestSection15StateCount` (6) |
| 16 | `...[section-16]` | `TestSection16KoideFromM` (4) |
| 17 | `...[section-17]` | `TestSection17ObserverLevelFromLambda` (3) |
| 18 | `...[section-18]` | `TestSection18TwoReadingsOfTheSameCurvature` (3) |
| 19 | `...[section-19]` | `TestSection19TowerOffset` (9) |
| 20 | `...[section-20]` | `TestSection20TwoCandidates` (6) |
| 21 | `...[section-21]` | `TestSection21TwoBraneRival` (2) |
| 22 | `...[section-22]` | `TestSection22CurvatureUnit` (6) |
| 23 | `...[section-23]` | `TestSection23LatticeOfUnits` (10) |
| 24 | `...[section-24]` | `TestSection24ScaleAndTop` (4) |
| 25 | `...[section-25]` | `TestSection25AutodualWindow` (11) |
| 26 | `...[section-26]` | `TestSection26WindowEdge` (6) |
| 27 | `...[section-27]` | `TestSection27WindowAsNome` (6) |
| 28 | `...[section-28]` | `TestSection28PoissonTheta` (4) |
| 29 | `...[section-29]` | `TestSection29LatticePointFromOmegaLambda` (8) |
| 30 | `...[section-30]` | `TestSection30SymmetricThroat` (5) |
| 31 | `...[section-31]` | `TestSection31ModuliMetric` (11) |
| 32 | `...[section-32]` | `TestSection32LevelVersusGridShape` (7) |
| 33 | `...[section-33]` | `TestSection33ColourHole` (8) |
| 34 | `...[section-34]` | `TestSection34Quintessence` (4) |
| 35 | `...[section-35]` | `TestSection35HalfThreshold` (8) |
| 36 | `...[section-36]` | `TestSection36BlackHoleWhereNeeded` (7) |
| 37 | `...[section-37]` | `TestSection37Consistency` (13) |
| 38 | `...[section-38]` | `TestSection38AreaLawHalf` (4) |
| 39 | `...[section-39]` | `TestSection39FibonacciTiling` (28) |
| 40 | `...[section-40]` | `TestSection40DictionaryAgainstTheCusp` (27) |
| 41 | `...[section-41]` | `TestSection41FiveRegularTilings` (18) |
| 42 | `...[section-42]` | `TestSection42TwoCoordinatesAndTheStep` (33) |
| 43 | `...[section-43]` | `TestSection43ThreeColumns` (12) |
| 44 | `...[section-44]` | `TestSection44BackgroundFigure` (31) |
| 45 | `...[section-45]` | `TestSection45ObserverLevel` (15) |
| 46 | `...[section-46]` | `TestSection46HopfFoliation` (13) |
| 47 | `...[section-47]` | `TestSection47ThePentagonalCode` (5) |

The number in parentheses is the count of collected items of that class
(`uv run pytest tests/ --collect-only -q | grep -c <ClassName>`), so it
moves whenever a test is added.  Every section therefore has at least two
tests: one that *runs* it (so the author's own `assert`s execute) and one or
more that recompute its numbers.  Section 47 of the v138 round (the triad
and the pentagonal code) is in `SECCIONES` since the W4 port:
`test_sections_47.py` (`TestSection47ThePentagonalCode`, 5) checks its
figures from the closed forms, independently of the section's own run.

## Two kinds of check

* **independent** -- the quantity is recomputed in the test from the closed
  form (Bessel zeros, Fibonacci words, lattice counts, weighted fits) and
  compared with an explicit tolerance.  This is the regression net: it does
  not depend on the section being right.
* **contract** -- the number is read from the section's stdout with an
  explicit tolerance, for quantities whose computation lives only inside the
  section (discretised chains, the 50 340-pair search of section 40, the
  seeded Monte-Carlo errors).

Tolerances are never loosened to make a test pass.  Rounding tolerances are
the width of the printed precision (`.4f` -> `5e-5`); everything else is
stated in the test with a comment saying where the number comes from.

## Slow tests

`@pytest.mark.slow` marks what takes more than 10 s on this machine:

* section 41 (figure 5) -- 33 s; four tests carry the mark;
* everything else runs under 10 s: section 40 takes 9.2 s, section 44
  (figure 1) 2.2 s and section 12 (checks only, it no longer draws) 0.8 s.

Figure 1 is `fig_background.pdf`, written by section 44 since the v134:
section 12 keeps the checks of the statements its panels used to draw.

Sections run inside a temporary directory, so the five `fig_*.pdf` files and
the `kk_vs_cw6_out.txt` dump never touch the repository, and the matplotlib
backend is forced to `Agg` in `conftest.py`.
