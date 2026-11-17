# PYT-001 — Numerical and academic testing practices: contrast of the `05-kkgt` suite against authoritative sources

- Report date: 2026-11-17 (fetch date for every source below: 2026-11-17)
- Requested by: the operator, after the section/marker machinery was read as self-built without a standards basis
- Method: `donsetch` `web_search` + `web_fetch` of primary documentation (pytest, NumPy, SymPy, Hypothesis, pytest-regressions, The Turing Way, JOSS); every claim below carries its source; anything that is *our* convention is labelled as such
- Companion documents: `docs/specs/20261117_SPEC-002_sections_co_location.md` (agreed target architecture), `docs/reports/20261117_TST-001_aud001_test_gaps_and_tolerances.md` (the tolerance rule), `docs/reports/20261116_AUD-001_claim_test_matrix.md`

## 1. What was contrasted (inventory, verified against the working tree)

| # | Construct | Where |
|---|---|---|
| C1 | `MARKERS = {n: text}` (section prose index) | `tests/test_section_runs.py:21` |
| C2 | `SECCIONES = []` registry, assembled in `__init__.py` | `tests/src/kkgt/sections/{_rest,s09_16,s17_24}.py`, `__init__.py:25` |
| C3 | `run_section` fixture: captures **stdout** once per section, caches it, every test parses it | `tests/conftest.py:47`, `tests/src/kkgt/harness.py:105` (`SectionRun`) |
| C4 | Census suite (15 test functions → 18 items): order, callable, unique titles, identity body, package location, `\testref` resolves, unique names, **exact pin**, no numbered section, no old entry point, figure files, figure writer, caption cites, slow declared | `tests/test_section_census.py` |
| C5 | Implicit parametrize ids (`@pytest.mark.parametrize("n", _params())`, `"depth,printed"` …) — **no `pytest.param(id=…)` anywhere** | `tests/test_section_runs.py:84` et al. |
| C6 | Tolerance rule *≤ half a unit of the last printed digit*, applied ad hoc per assert (no central helper) | TST-001; asserts across `tests/` |
| C7 | Registered custom markers `slow`, `figure` + `testpaths`/`pythonpath`/`addopts` | `pyproject.toml [tool.pytest.ini_options]` |
| C8 | Golden figures compared byte-wise (md5 + regeneration through our own pipeline) | `tests/`, `scripts/` |
| C9 | Claim-to-test audits (`AUD-001`, `CIT-001/002`) — editorial traceability, not execution | `docs/reports/` |

## 2. Sources (fetch date 2026-11-17; extracts literal)

| Id | Source | Extract |
|---|---|---|
| S1 | pytest, *How to parametrize* — https://docs.pytest.org/en/stable/how-to/parametrize.html | parametrization at several levels; `pytest.param(...)` carries per-set `marks`; ids shown as `test_eval[6*9-42]` (derived from values) |
| S2 | pytest, *Reference: pytest.param* — https://docs.pytest.org/en/stable/reference/reference.html | `param(*values[, id][, marks])` — "**id**: str \| `pytest.HIDDEN_PARAM`": an explicit, caller-chosen test id is part of the API |
| S3 | pytest, *Assertions* — https://docs.pytest.org/en/stable/how-to/assert.html | "Instead of using `assert abs(a - b) < tol` or `numpy.isclose`, you can use `pytest.approx()`"; **"asserts in supporting modules which are not themselves test modules will not be rewritten"** (use `register_assert_rewrite`) |
| S4 | pytest, *Capture stdout/stderr* — https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html | fd-level capture by default; fixtures `capsys`/`capfd` + `readouterr()` are the supported way to assert on **printed** output |
| S5 | NumPy, `numpy.testing.assert_allclose` — https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose.html | defaults `rtol=1e-07, atol=0`; criterion `abs(actual−desired) ≤ atol + rtol·abs(desired)`; "tighter default tolerance values" than `allclose`; see also `assert_array_max_ulp` |
| S6 | NumPy, `assert_array_almost_equal` — https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_array_almost_equal.html | **"It is recommended to use one of `assert_allclose`, `assert_array_almost_equal_nulp` or `assert_array_max_ulp` instead of this function for more consistent floating point comparisons"** |
| S7 | pytest-regressions — https://pytest-regressions.readthedocs.io/en/latest/ | fixtures `data_regression`, `file_regression`, **`num_regression`**, `ndarrays_regression`, `image_regression` — the FOSS standard for golden-value tests, incl. numerical |
| S8 | Hypothesis — https://hypothesis.readthedocs.io/en/latest/ | "**the property-based testing library for Python** … tests which should pass for all inputs in whatever range you describe, and let Hypothesis randomly choose which of those inputs to check — including edge cases you might not have thought about" |
| S9 | SymPy, *Run Tests* — https://docs.sympy.org/dev/modules/testing/runtests.html | goals: "compatible with py.test", "**no magic, just import the test file and execute the test functions**"; `SymPyOutputChecker` "supports **numerical comparison of floats occurring in the output** of the doctest examples" |
| S10 | The Turing Way, *General guidance and good practice* — https://book.the-turing-way.org/reproducible-research/testing/testing-guidance/ | "write some tests"; **run them**; automate + CI; scale test count to runtime; document how to run them; "**pytest (recommended)**" for Python; pitfall: *"the illusion of good coverage"* — sanity-check tests can pass "for the wrong reasons" |
| S11 | The Turing Way, *Challenges and exceptional cases* — https://book.the-turing-way.org/reproducible-research/testing/testing-exceptions/ | *Testing if non-integer numbers are equal*: compare "to within a given tolerance, alternatively termed a threshold or delta"; `pytest.approx`; cross-language equivalents (JUnit `delta`, testthat `tolerance`, Julia `isapprox(atol, rtol)`) |
| S12 | JOSS, *Review criteria* — https://joss.readthedocs.io/en/latest/review_criteria.html | **Tests**: "automated test suite covering the core functionality"; Good = "hooked up to continuous integration"; Bad = "**No way for you, the reviewer, to objectively assess whether the software works**"; Quality assurance = automated tests, CI, documented verification |
| S13 | JOSS, *Review checklist* — https://github.com/openjournals/joss/blob/main/docs/review_checklist.md | "**Automated tests:** Are there automated tests or manual steps described so that the functionality of the software can be verified?" |
| S14 | scientific-python.org discussion, *Remove all uses of the disrecommended numpy.testing assertion functions* — https://discuss.scientific-python.org/t/remove-all-uses-of-the-disrecommended-numpy-testing-assertion-functions/2107 | search-result **snippet only**: `xp_assert_close` vs `assert_allclose` strictness debate (ecosystem actively pruning decimal-style asserts) |

## 3. Verdict table

| Construct | Verdict | Basis / migration note |
|---|---|---|
| pytest + `approx` + registered markers (C7) | **keep** | S3, S10: this is the standard stack; `pythonpath`/`markers` are documented practice |
| Tolerance rule "half a unit of the last digit" (C6) | **adapt** | Legitimate *display-precision* convention (S11 accepts tolerance/delta), but must be **stated in standard form**: `pytest.approx(expected, rel=…, abs=0.5·10⁻ᵈ)` in one helper, not ad hoc; S6 warns off decimal-style asserts (`assert_array_almost_equal`) in favour of rtol/atol/ULP |
| Node-ids cited by the paper (C5) | **adapt (highest priority)** | S2: `pytest.param(id=…)` is the documented mechanism for **stable, caller-chosen ids**; our cited ids currently derive from parameter **reprs** — a refactor of values would silently break `\testref`. Freeze them explicitly |
| `MARKERS` prose dict (C1) | **eliminate** | Standing instruction: migrate out of the provenance file. Narrative belongs in the claim tests' docstrings (S9's "no magic"); its assertions migrate with them (SPEC-002) |
| `SECCIONES` registry + `seccion_N` modules (C2) | **eliminate** | No imports from the package anywhere (operator's requirement): computations move into the tests that assert them; **0 of the 99 cited anchors live in the driver test**, so the registry and its driver can be deleted without touching the paper's anchors (verified 2026-11-17) |
| Stdout contract (C3) | **eliminate with co-location** | Once a computation lives inside its test, the test asserts the **value** (S3's introspection model, S10's "isolate smaller chunks"): no stdout to parse, and assertion rewriting applies (S3). `capsys` (S4) remains the tool only if a test must ever assert *printed* output — none needs to after migration |
| Census suite (C4) | **keep, re-labelled** | Not a testing standard — it encodes **paper↔repo invariants** (editorial contract). Honest label: "contract tests" (S12's *documented verification processes*); document them in `tests/README` so they read as verification, not folklore |
| Golden figures (C8) | **adapt** | Equivalent in kind to S7's `file_regression`/`image_regression`; adopting the fixture would replace bespoke md5/regeneration plumbing with the FOSS tool |
| Claim audits (C9) | **keep** | Traceability artefacts; outside pytest scope, consistent with S12 "documented verification" |
| Property-based tests | **add (phase 3, optional)** | S8: after phase 2 (returned data), identities in C-suite are natural `@given` properties; not before, because stdout is not property-friendly |
| CI | **gap → add** | S10, S12, S13: the single largest deviation — gates run only by hand today |
| Coverage measurement | **gap → measure** | S10: aspire to coverage; and beware the *illusion* (our claim-based audits already counteract it) |

## 4. Findings (the uncomfortable ones)

1. **The section/marker machinery is a provenance artifact, not a project convention** (C1–C4): it is the original `reproduce_vNNN.py` pytest copied verbatim, and the operator's standing instruction — repeated across sessions — was to **migrate out of it entirely** into the project's own test structure, reconciling each test against the manuscript. An earlier draft of this report framed these constructs as "unlabelled conventions"; that framing was wrong and is corrected here: the file is undesirable *by instruction*, and the correct verdict is **eliminate**, not adapt (rows C1–C3 of §3). What the standard-contrast contributes is the supporting evidence: nothing in S1–S14 prescribes a prose-marker dict, a mutable module-level registry with `append`, or stdout parsing — and the migration path out is the standard one (tests own their computations, §5).
2. **The paper's `\testref` anchors ride on implicit ids** (C5) — the suite's most cited surface is protected by an *exact-equality test*, but the ids themselves are generated from parameter values. `pytest.param(id=…)` (S2) converts luck into API.
3. **Assertion introspection stops at the package boundary** (C3 + S3): the layer that holds every numerical helper does not get pytest's failure diffs. Either `register_assert_rewrite("kkgt")` now, or remove the intermediate layer in phase 2 (SPEC-002 §3).
4. **The tolerance rule is sound but unstated in standard terms** (C6): NumPy's documented criterion (`atol + rtol·|desired|`, S5) is the lingua franca; our last-digit rule is a special case with `abs=0.5·10⁻ᵈ` and should be written once, centrally.
5. **No CI, no coverage** (S10–S13): for a paper whose Code-and-data section invites reproduction, the review-standard expectation is an automated suite hooked to CI; today's green gates are local events.

## 5. Order of changes (aligned with SPEC-002 phases; no new phases created)

- **Phase 1 (structure, current):** co-location per SPEC-002; `MARKERS` → docstrings/index; registry → index; **freeze every cited node-id with `pytest.param(id=…)`**; add `register_assert_rewrite("kkgt")` (one line) while the stdout layer still exists.
- **Phase 2 (contract, next):** stdout → returned data; single tolerance helper in standard `rel/atol` form; consider `pytest-regressions` (`num_regression`/`file_regression`) for golden numerics/figures.
- **Phase 3 (optional):** `pytest-cov` measurement, CI workflow (JOSS S12/S13), `hypothesis` for identities.

## 6. Research gaps

- scipy's developer testing guide URL not resolved (404 on the attempted path); SciPy therefore absent from S-list — NumPy + SymPy + pytest cover the numerical-assertion ground.
- mpmath's own test suite not fetched; SymPy (S9) stands in for the computer-algebra practice.
- S14 is a search-result snippet, not a fetched page; treated as context, not as a load-bearing citation.
- The pytest `ids`-customisation prose section was not re-fetched in full; S2 (reference page) carries the API claim.
