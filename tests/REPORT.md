# Reporte: `reproduce_v108.py` → suite pytest

## (a) Árbol de archivos creado / modificado

```
pyproject.toml                 M  [dependency-groups] dev = ["pytest>=8.0"]
                                       + [tool.pytest.ini_options] (testpaths,
                                         pythonpath, addopts, markers)
uv.lock                        M  + pytest 9.2.0, colorama, iniconfig, pluggy, pygments
package.json                   M  scripts: "test", "test:fast"  (bloque scripts sólo)
reproduce_v108.py              –  SIN CAMBIOS (entry point citado por el tex)
tests/                         N
├── README.md                  N  estructura, política de tolerancias, mapa sección→test
├── REPORT.md                  N  este informe
├── conftest.py                N  backend Agg, fixtures repro/sections/run_section
├── src/kkgt/__init__.py       N
├── src/kkgt/constants.py      N  PHI, LN_PHI, M_PCF, EPS0, OBS_G, FIGURES, SLOW_SECTIONS
├── src/kkgt/harness.py        N  SectionRun: ejecuta una sección, lee su stdout
├── test_section_census.py     N  contrato registro ↔ main.tex (números y figuras)
├── test_section_runs.py       N  las 43 secciones corren e imprimen su número
├── test_sections_01_08.py     N  secciones 1-8
├── test_sections_09_16.py     N  secciones 9-16
├── test_sections_17_28.py     N  secciones 17-28
├── test_sections_29_38.py     N  secciones 29-38
└── test_sections_39_43.py     N  secciones 39-43
```

No se tocaron `main.tex`, `citation.csl.json`, `scripts/`, `build/`, `lean/`; no
hay commits ni push.

## (b) Comandos, salida literal, runtime y conteos

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

`uv lock` regeneró `uv.lock` (pytest 9.2.0) y `uv run python reproduce_v108.py 38`
sigue funcionando igual que antes.

## (c) Mapa sección → test

Cada sección `N` tiene **como mínimo dos tests**: uno que la *ejecuta* (id
`section-NN`, con los `assert` internos del script) y una clase profunda
`TestSectionNN…` que recalcula sus números.  Detalle completo en
`tests/README.md`; resumen (clase profunda → nº de tests):

| § | clase | n | § | clase | n | § | clase | n |
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

Además `tests/test_section_census.py` (10 tests) fija la numeración: parsea
`main.tex` y exige que `sections~N` citadas = {2,10,12,13,29,36,37,38,39,40,41,42,43}
⊆ registro, que las 43 secciones son 1..43 contiguas, que cada `seccion_N`
tiene banner `# N.` en el fuente, y que las cinco figuras incluidas por el tex
(`fig_granularity`, `fig_one_structure`, `fig_mobius_throat`, `fig_throat_tiling`,
`fig_tilings_strip`) las escribe su sección.

Total: **447 tests** = 43 de ejecución + 394 profundos + 10 de censo.

## (d) Tolerancias heredadas vs estándar del hermano 03

**Heredadas del script** (los `assert` internos, ahora ejecutados por los run
tests): `1e-12` (ε₀M=π, razón de anillos, normas, identidades de matriz),
`1e-15` (media vuelta de la fibra), `1e-9` (cierre por nivel, z·τ, τ(12)),
`1e-6·φ^{2s}` (fase sobre la celda), `atol=1e-9` (toro de Clifford),
`1e-9` relativo (S = π(A/φ²+B/φ³)), `Decimal 10^-45` (§40, 60 dígitos),
`1e-6` (desviación de Binet, §43), `1e-3` (Hurwitz <0.36, crecimientos),
`5e-4` (pendiente W2 = 0.9972), `Decimal 1e-9` (no-enteralidad), `0.05`
(crecimientos de teselados), y las ventanas ad-hoc `1.3<min<1.5`,
`1.7<max<1.9` (§29).

**Estándar del hermano 03**: fixtures `np_1e12`/`np_1e9`, `mp25`/`mp40`,
`tol = 10^{-(dps-6)}`, `tol_eig = 10^{-(dps//2)}` y comparaciones puntuales
`mpf('1e-20')`.

**Lo que uso aquí** (mismo espíritu, sin fixtures de mpmath porque casi todo
es float64): identidades exactas con `1e-12`/`1e-9` (las mismas que el
script); tolerancias de redondeo = ancho de la precisión impresa (`.4f` →
`5e-5`, `.3f`/`.2f` → `5e-4`); excepciones **documentadas en el docstring**:

* `2e-3` para la cadena M=32 de §6 frente a los ceros de J1 (error de
  discretización: el propio script reporta rms 0.54 %; el 4.º ratio difiere
  en 1.5e-3);
* `1e-4` para `x1_vec/x1_grav = 0.6381` de §3 (cuociente de dos ceros
  impresos a 4 decimales: 2.4448/3.831706 = 0.63804, la propagación del
  redondeo es ~1e-4);
* `1e-5`/`5e-5` para las constantes de Hurwitz de §41, con la ventana de
  `n` en el docstring (n=15..25 para φ, n=5..15 para √2): por debajo no
  converge el convergente, por encima colapsa la resta en float64 (n=40 → 0);
* `rel=1e-3` para las masas de Regge de §33 (impresas a 3 cifras).

Ninguna tolerancia se amplió para hacer pasar una comprobación que fallaba:
de las 38 fallas de la primera ejecución, todas eran errores míos de
regex/parámetro/expectativa (p. ej. `sigma\[[0,6]\]` con corchetes dobles,
`assert run.has(...)` sobre una función que no devolvía nada, índices
desplazados); se corrigieron los tests, no los umbrales.  Las cuatro
excepciones de arriba ya estaban motivadas al escribirlas.

## (e) Comprobaciones que fallan o que quedan marcadas

* **Fallas: 0** (`447 passed`) tras la primera ronda de corrección.
* **`xfail`/`skip`: ninguno.** Ninguna sección del script falla: sus 64
  `assert` internos pasan todos (§11, 12, 13, 29, 37, 39, 40, 41, 42, 43).
* **Nota sobre `chk`**: no existe (`grep -c chk reproduce_v108.py` → 0).  Las
  "comprobaciones ad-hoc" son 64 `assert` sin mensaje; al correr dentro de
  pytest fallan con el número de sección y el stdout completo
  (`SectionRun.match/has` los incluyen en el mensaje).
* **`@pytest.mark.slow` (7 tests)**, por la regla de los 10 s:
  * §12 (figura 1, 12.3 s): `test_section_writes_its_figure[section-12]`,
    `test_section_runs_and_prints_its_number[section-12]`,
    `TestSection12FigureOneStatements::test_section12_runs_all_of_its_checks`
  * §41 (figura 5, 35.7 s): `test_section_writes_its_figure[section-41]`,
    `test_section_runs_and_prints_its_number[section-41]`,
    `TestSection41FiveRegularTilings::test_section41_prints_its_conclusions`,
    `::test_qubit_bond_dimension_of_54`
  * §40 se midió en 9.5 s → queda **sin** marcar (bajo el umbral).
* El backend es `Agg` y cada sección corre en un directorio temporal: los
  cinco `fig_*.pdf` y `kk_vs_cw6_out.txt` no se escriben en el repo.

## (f) Etiquetas de "testigo" / tier

**`main.tex` (no renombradas aquí):**

| etiqueta | apariciones |
|---|---|
| `\tier{N}` | 74 |
| `\tier{P*}` | 21 |
| `\tier{R}` | 15 |
| `\tier{P}` | 12 |
| `\tier{L}` | 8 |

Ítems testigo: `W1 (CLPW)`, `W2 (W01)`, `W3 (W01)`, `W4 (W01)`, `W5 (W01)`,
`W6 (W01)`, `W7 (W01)`, `W8 (W01)`, `W9 (GH)`, `W10 (W01)`, `W11 (CLPW)`,
`W12 (CLPW)`.  Etiquetas de fórmula: `F1`…`F9`, `B1`…`B4`; de enunciado: `I12`.

**`reproduce_v108.py` (mismos nombres que el tex):**

| etiqueta | dónde (línea) | texto |
|---|---|---|
| `W2` | 1467 (comentario), 1476 (§37) | `W2: dimension entera (estados con L0 <= N/2): sigma=3,4,5 -> 1654, …` |
| `W4`, `W8` | 1048, 1051, 1058 (§18); 1131, 1132 (§22) | `nivel del observador (W4 = W8 en la unidad gravitacional l = sqrt2 l_P)`, `W8 en unidad l: 583.877; W4: 583.877`, `= W4 + log_phi 2` |
| `(F1)` | 1003, 1007, 1014, 1017, 1023, 1031, 1042, 1059 (§16-18, §24) | `La escala M de (F1)…`, `M = 313.84 # MeV, (F1)`, `unidad de (F1): 4.6258 MeV` |
| `(F9)` | 1017, 1034 (§17) | `El nivel del observador por el valor de Lambda, bajo (F9)…` |
| `(B1)` | 1498, 1507 (§38) | `El 1/2 de (B1): cuanto de area, unidad de Fisher y bit de Shannon` |
| `I9` | 253 (§1) | `SL2(Z) facts of Imported statement I9` |
| `I12` | 812 (§12, cabecera de figura), 1130 (§22) | `I12: $|\Omega|_\sigma=1/2$…`, `l = l_P/sqrt(G_N) = … (I12, tau = i)` |
| `I15` | 827 (§12) | `I15: $z=\varphi y$ carries the triangle onto Z[i]…` |
| `[R]` | 692 (§11) | `el doce del icosaedro y el del fondo se prueban por separado (lectura [R])` |
| `I1`…`I7` | §42 (impresiones `I1:`…`I7:`) | bloque de la sección 42 |

El script **no** contiene la macro `\tier{}` (grep `tier` → 0).  Los solapes
`W2/W4/W8/F1/F9/B1/I9/I12/I15/[R]` son los que hay que estandarizar después;
aquí no se renombró nada.

## (g) Desviaciones del estándar de 03 y por qué

1. **`reproduce_v108.py` queda intacto** (no se convirtió en runner delgado
   sobre un paquete reestructurado).  Motivo: las 43 secciones *son* el
   código citado por el tex (`section~N of reproduce_v108.py`), están en su
   propio espacio de nombres y son importables tal cual; mover 1990 líneas a
   `tests/src/` arriesgaba romper el artefacto citado sin ganar cobertura —
   los tests importan el módulo y lo ejecutan.  Si se quiere la reestructura
   en módulos, el punto de partida ya está: `kkgt.harness.run_section` es el
   único lugar que sabe cómo invocar una sección.
2. **pytest en `[dependency-groups] dev`** en lugar de
   `[project.optional-dependencies] test` como en 03 (lo pide la consigna).
3. **`addopts = "--tb=short -p no:cacheprovider"`** sin `-v` (03 usa
   `-v --tb=short …`), para que la línea de comando (`-q`) controle la
   verbosidad.
4. **Markers**: `slow`, `section`, `figure` (03 usa
   `slow/symbolic/numerical/gauge/gravity/places`): aquí no hay sympy ni
   sectores gauge, pero sí identidad de sección y figuras.
5. **Sin `hypothesis` ni `rich`** (03 los declara como extras de test): no
   aportan a comprobaciones numéricas cerradas.
6. **Ejecuciones cacheadas por sesión en un directorio temporal**: las
   secciones imprimen y escriben archivos (03 `cw6` es puro), así que
   `run_section` las ejecuta una vez por sesión y comparte el stdout; los
   tests lentos dependen de esa caché y por eso se marcan `slow` también.
7. **`tests/src/kkgt`** contiene constantes de test + harness en vez de la
   biblioteca del proyecto, porque la biblioteca *es* `reproduce_v108.py`
   (importado con `pythonpath = [".", "tests/src"]`).
