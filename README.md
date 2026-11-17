# One object instead of a choice of vacuum to put the observer in de Sitter space: From wormholes, black holes and baby universes to the criteria for an observer in de Sitter, contrasted with the Kaluza–Klein graviton candidates and with the cosmological constant

<!-- selfcite:begin id="badge" -->
<!-- selfcite:end id="badge" -->

[![Project Page](https://img.shields.io/badge/Project%20Page-omega--pcf.com-blue)](https://omega-pcf.com/kkgt)

## Authors

**Jorge Armando González García**¹, **Víctor Manuel González García**¹, **Itzel Marion Dressler Pérez**², **Luz María García Ordóñez**¹

¹ *TTAMAYO PUNTO COM, S.A.P.I. de C.V., Research & Development Division, Mexico*
² *Independent Researcher*

---

## Abstract

In de Sitter space an observer must be inside the universe it observes, and in string theory placing it has become a choice: of a vacuum among some 10^500. The same choice returns where wormholes, black holes and baby universes meet. The baby universes that branch off through wormholes carry parameters that fix the constants of nature, the cosmological constant among them, and the same parameters label the boundary theories over which the gravity of a black-hole throat is averaged; in both the question is which value, and the answer is sought in what a throat contains. The programme to which this note belongs, written within critical realism, reads the difficulty as one of representation rather than of selection: what is missing is one object that meets the criteria Witten and Chandrasekaran, Longo, Penington and Witten set for an observer in de Sitter, not a choice among values. This note does not test that claim itself; it tests two of its consequences where data can reach them, on the particles of one throat and on the cosmological constant. The object, in the framework of the programme, is a microstate whose levels form a tower built from two numbers, π and the golden ratio φ; read as a warped extra dimension it is a throat, the golden throat, whose Kaluza–Klein modes are its particles. The question becomes whether the tower fixes what a throat model otherwise chooses. The two-brane model of Randall and Sundrum assumes the dimension and chooses the infrared scale and the depth. The golden throat has the same equations, so the same mass ratios, and four independent conditions of the tower, reflection positivity, four-dimensional gravity, the arity of the framework and the clock of φ, fix its spectrum with no free parameter, to leading order π(k+1/4) times Mφ^12 in the unit M of the framework. The arity gives the dimension that the two-brane model assumes; with M identified with the scale of the charged leptons and the level 12 with the bottom of the throat, the spectrum fixes the infrared scale that it chooses. Identified with the graviton candidates reported at 380 and 700 GeV, they place the bottom of the throat at 11.97±0.05, 0.6 standard deviations from 12, and give the next modes at 1028 and 1346 GeV, against 1014 and 1328 GeV for the two-brane model fitted to the same candidates. Only the depth, the position of the top, stays free, and the ratio of the vector modes can decide it if they share the throat. The same tower carries the observer of de Sitter space. In the gravitational unit of the framework the observed cosmological constant gives the observer's level, 583.79±0.03: the level is read from the data, not chosen, and the hypothesis that it sits at an integer level is excluded within ΛCDM at 7.6 standard deviations. What the note leaves open is one number, the ratio of the lepton scale to the Planck scale.

**Keywords:** de Sitter space, wormholes, Kaluza–Klein gravitons, golden ratio, Randall–Sundrum model, cosmological constant, formal verification, Lean 4.

<!-- selfcite:begin id="citation" -->
## Citation

González García, J. A., González García, V. M., Dressler Pérez, I. M., & García Ordóñez, L. M. (2026). *One object instead of a choice of vacuum to put the observer in de Sitter space: From wormholes, black holes and baby universes to the criteria for an observer in de Sitter, contrasted with the Kaluza–Klein graviton candidates and with the cosmological constant*. Preprint. Repository: [omega-pcf/05-kkgt](https://github.com/omega-pcf/05-kkgt).

```bibtex
@article{Gonzalez2026KKGoldenThroat,
  author  = {González García, J. A. and González García, V. M. and Dressler Pérez, I. M. and García Ordóñez, L. M.},
  title   = {One object instead of a choice of vacuum to put the observer in de Sitter space: From wormholes, black holes and baby universes to the criteria for an observer in de Sitter, contrasted with the Kaluza–Klein graviton candidates and with the cosmological constant},
  journal = {Preprint},
  year    = {2026},
  url     = {https://github.com/omega-pcf/05-kkgt}
}
```
<!-- selfcite:end id="citation" -->

## Repository Structure

### Manuscript

- **`main.tex`**: the manuscript (single-file article, `amsart`, biblatex bibliography).
- **`src/bibliography.bib`**: references — auto-generated from `citation.csl.json` on every build; never edit by hand.

### Citations

- **`citation.csl.json`**: CSL JSON array — the single source of truth for every reference. See [`docs/citations.md`](docs/citations.md).
- **Witness conventions**: see [`docs/citations.md`](docs/citations.md#8-witnesses-tiers), section *Witnesses (tiers)*.

### Formal Verification (`lean/`)

- **`lean/TorreKK_LYR_v34.lean`**: the entire development in one file (163 theorems, 6 axioms, no `sorry`).
- **`lean/lakefile.toml`**: lake build configuration with the Mathlib dependency (`v4.33.1`).
- **`lean/lean-toolchain`**: `leanprover/lean4:v4.33.1`.

### Numerical checks

- **`tests/src/kkgt/sections/`** (module `kkgt.sections`): every number and every figure of the note, in forty-seven sections that run together or one at a time (`PYTHONPATH=tests/src uv run python -m kkgt.sections`).
- **`tests/`**: the suite that checks them, `uv run pytest tests/ -q` (550 tests; 546 with `-m 'not slow'`); `main.tex` cites the test behind each number with `\testref{...}`.

### Figures (`images/`)

- `images/fig_*.pdf`: the five vector figures of the manuscript, generated by `pnpm run generate:figures` (`scripts/figures/main.py` + the author's `figuras_v134.py`). The run is deterministic — two consecutive runs are byte-identical — and every PDF carries `/ToUnicode`, so `pdftotext` reads the math glyphs back. How and why: [`docs/figures.md`](docs/figures.md).

## Verification Execution

```bash
pnpm run validate     # = pnpm run verify = verify:py (pytest) + verify:lean (lake)
pnpm run verify:lean  # cd lean && lake build TorreKK_LYR_v34
```

## Build and Compilation

```bash
pnpm install           # once
pnpm run type-check    # tsc --noEmit
pnpm run build         # citation sync + Docker latexmk + checksums
pnpm run build:full    # generate:figures first (idempotent — see docs/figures.md)
```

> [!IMPORTANT]
> - **Metadata flow**: `citation.csl.json` → `src/bibliography.bib`, `CITATION.cff`, `.zenodo.json`, all regenerated by `pnpm run build`.
> - **Verification**: `build` produces the PDF only; proof verification runs through `pnpm run verify`.

## Release

```bash
pnpm run release
```

Releases, tags and GitHub publication are handled by `release-it` and are **not** executed in this repository without an explicit instruction from the author.

### Traditional Manual Build

For local environments with a full TeX Live distribution:

```bash
pdflatex main
biber main
pdflatex main
pdflatex main
```

## License

See [LICENSE](LICENSE) for details.
