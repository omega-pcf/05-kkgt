# Fundamento de la marca de testigo

**Documento:** justificación de la convención de testigos (`\tier`, `\witness`,
`\wtag`) del manuscrito `05-kk-golden-throat`, escrita para que la convención
tenga cabida en un artículo de matemáticas puras.

**Registro:** tercera persona, español; los identificadores, las macros y los
nombres de archivo se escriben en inglés y en monoespaciado.

**Relación con el resto de la documentación.** Este documento **argumenta**; la
regla **operativa** vive en `docs/citations.md` §8 (gramática, reglas de
redacción, alfabeto, convenciones y, en §8.5, el criterio cuantificado de
inline frente a línea propia). Las decisiones por sitio —qué testigo sostiene
cada claim, qué se reescribe y qué se elimina— viven en
`docs/witness-decisions.md`. Nada de lo que se afirma aquí cambia el contrato
de `docs/citations.md`: si ambos documentos llegaran a discrepar, manda
`docs/citations.md`, porque es el que el build y la revisión de textos usan.

**Estado:** vigente con el manuscrito en HEAD `7ce658c`. Las cifras de §4.4 y
de §4.5 corresponden al estado del manuscrito al escribir este documento y se
identifican por la cola de la oración, no sólo por el número de línea, porque
el manuscrito se edita de forma concurrente.

---

## 1. Qué se justifica aquí

El manuscrito marca, junto a cada claim, cómo se estableció: `P` cuando la
afirmación está probada y comprobada por máquina en Lean, `N` cuando está
verificada numéricamente con el nombre de la prueba que la comprueba. La marca
es un corchete pequeño, inmutable y de color propio (`\tier{P}`, `\tier{N}`,
`\tier[ids]{X}`), o una línea propia alineada a la derecha cuando el claim
arrastra varios testigos (`\witness{X}{ids}`). La primera página lleva una
leyenda que define las clases y nada más.

Ese dispositivo no es una moda tipográfica ni un adorno: es la respuesta a un
problema real de lectura y de atribución, y su forma —inline o línea propia—
se decide con un criterio cuantificado. Lo que este documento sostiene es
precisamente eso: que la convención es **legítima** (resuelve algo que la
cita bibliográfica no resuelve), **coherente** con la práctica
contemporánea de verificación, **usable** (no cuesta legibilidad ni espacio
imprimible de más) y **honestamente declarada** (no se presenta como una
norma de AMS o de Chicago, y advierte de su novedad).

Lo que este documento **no** hace: no fija reglas de edición. Las reglas están
en `docs/citations.md`; aquí se da la razón de ser de cada una de ellas.

---

## 2. Por qué una marca de testigo en un artículo de matemáticas puras

### 2.1 El problema que resuelve

Una referencia bibliográfica responde a *dónde se ha publicado* una afirmación.
No responde a *cómo se estableció* la afirmación que el lector tiene delante.
En un artículo que mezcla tres tipos de afirmación —identidades probadas con
Lean, números calculados y contrastados contra una suite, y resultados leídos
en fuentes externas—, esa omisión tiene tres consecuencias concretas:

1. **La dirección de la referencia queda ambigua.** Un `\cite` al final de un
   claim dice que hay una fuente; no dice si la fuente *prueba* el claim, si
   sólo *reporta* el número, o si es el origen de una hipótesis que el artículo
   toma prestada. El lector de matemáticas está habituado a leer la
   bibliografía como procedencia del enunciado, no como verificación de él.
   La marca separa los dos planos: la cita queda junto al claim con su forma
   propia (`[N]~\cite{key}` para un valor leído en una fuente,
   `[P] in~\cite{key}` para un resultado probado en ella), y la marca lleva
   el testigo interno, por identificador.

2. **El referente no es único.** Cuando un claim se apoya en tres
   demostraciones de `lean/TorreKK_LYR_v34.lean` y en dos pruebas de la suite,
   citar "la demostración" en singular obliga a elegir una y a esconder las
   demás, o a escribir una enumeración en prosa que rompe la oración. La
   gramática del dispositivo —un claim, una marca; el listado de identificadores
   dentro del corchete o en su propia línea— da al lector el referente completo
   y verificable: cada identificador es un nombre que se puede buscar en el
   archivo de Lean o en la suite.

3. **El coste tipográfico importa.** Un claim con un solo testigo cabe en la
   oración; un claim con cinco nombres de cuarenta caracteres no. Sin una regla
   de forma, el texto acumula corchetes largos en mitad de la frase y el lector
   pierde el hilo de la oración que los contiene. De ahí que la distinción
   inline / línea propia no sea estética: es la condición de que el dispositivo
   sea legible.

### 2.2 Qué gana el lector

- **Comprueba la afirmación sin salir del texto.** El identificador está en la
  página; el archivo de Lean y la suite están en el repositorio. Un número
  marcado `N[test_rms_against_the_lyr_table]` puede reproducirse con una
  orden; una identidad marcada `P[moduli_slope]` localiza el teorema.
- **Distingue de un vistazo la naturaleza de la evidencia**, sin leer la
  bibliografía: la letra carga el significado, el color sólo lo repite (§4.2).
- **Sabe qué no está marcado.** La ausencia de marca es información: un claim
  sin testigo es un claim que el artículo no verifica en el sitio donde se
  afirma. Esa asimetría es útil sólo si la marca es sistemática, y la
  sistematicidad exige una regla de forma explícita.

---

## 3. El argumento post-2025

Víctor sostiene que, **a partir de 2025 y con el estado del arte de la
inteligencia artificial, la tendencia a la verificación exhaustiva numérica y
mediante Lean y otros asistentes de pruebas llegó para quedarse** en las
matemáticas formales, en la física y en otras disciplinas. El argumento se
descompone en tres pasos.

1. **La verificación dejó de ser excepcional.** La generación y la revisión de
   pruebas por modelos de lenguaje, junto con la madurez de ecosistemas como
   Lean y Mathlib, han abaratado el coste de comprobar una identidad o de
   reconstruir un cálculo hasta el punto de que *no verificar* empieza a ser
   la opción que exige justificación. Lo que antes era el privilegio de unos
   pocos desarrollos —un teorema formalizado a mano durante años— es hoy una
   expectativa razonable de lector para las afirmaciones numéricas y para las
   identidades de cálculo.

2. **La consecuencia editorial es una nueva clase de evidencia.** Si una parte
   creciente de las afirmaciones de un artículo se establece por ejecución o
   por comprobación de máquina, el artículo necesita decirlo *en el lugar
   donde afirma*, y no sólo en una sección de "métodos" o en un apéndice
   descriptivo. La referencia bibliográfica no puede hacer ese trabajo: no
   distingue entre "probado en una fuente", "calculado aquí" y "supuesto por
   hipótesis". Una convención que **marca la naturaleza de la evidencia junto
   al claim obedece a esa realidad**: describe el estado real de cómo se
   establece cada afirmación, con el mismo criterio en toda la disciplina.

3. **La disciplina ya se mueve en esa dirección.** Los precedentes cercanos —
   planos de trabajo con estado por enunciado (`leanblueprint`), tablas de
   estado por resultado y sellos o insignias de artefacto que certifican qué
   parte de un artículo está comprobada— existen precisamente porque la
   verificación formal y numérica se ha vuelto un dato estructural del
   resultado, no un detalle de implementación. La marca del manuscrito toma
   ese principio y lo baja al nivel del claim, que es la unidad en que un
   lector de matemáticas lee y juzga.

De ahí que el dispositivo no se presente como un gusto de los autores: se
presenta como la respuesta editorial a un cambio en la práctica de la
disciplina. Eso no convierte a la marca en una norma de sociedad erudita; ver
§6, donde se declara exactamente lo que la convención es y lo que no.

---

## 4. Usabilidad y compactness

El criterio de usabilidad y el de *compactness* —cuánto cuesta la marca en
espacio y en atención— ya estaban parcialmente definidos en la documentación
de la familia. Esta sección los recoge y los enriquece con el factor
sintáctico en prosa pedido para §8.5 de `docs/citations.md`.

### 4.1 Herencia de la notación secundaria de la ingeniería de software

El dispositivo no nace de la tipografía matemática, sino de una práctica
consolidada en la ingeniería de software y en el diseño de interfaces:

- **Tipado semántico:** los nombres dicen qué son. Un identificador
  `test_second_order_convergence_on_the_golden_grid` no necesita glosa; el
  lector que busque la comprobación la encuentra. El corchete del testigo
  hereda esa disciplina: sólo admite identificadores internos, nunca claves de
  bibliografía ni números impresos, de modo que su contenido es siempre un
  nombre buscable.
- **Color como marcador de *UX*, redundante con la etiqueta:** en las
  interfaces serias el color acelera la lectura, pero la etiqueta sigue
  portando el significado; el color nunca es la única vía. Aplicado al
  manuscrito: azul `P`, verde `N`, ocre `P*`, turquesa `W` — y la letra, no el
  tono, es lo que el lector en blanco y negro, con baja visión o con
  deficiencia de color percibe.
- **Marca de estado junto al objeto, no en una lista aparte:** como un
  indicador de *build* verde al lado del commit, la marca vive al lado del
  claim. Moverla a una tabla al final del artículo la haría más barata y menos
  útil, a cambio de ahorrar unos caracteres.

La pasada de investigación previa sobre la convención —su alcance y su método
están descritos en el *skill* de la familia `omega-pcf-paper-repos`, archivo
`references/decision-gates.md`, sección *"When the convention itself is
questioned"*— recorrió esa literatura con un propósito declarado: separar qué
es estándar de la disciplina, qué es dispositivo propio del proyecto y cuál es
el precedente real más cercano. El resultado destilado quedó en
`docs/citations.md` §8.4: los precedentes reales son el estado por enunciado
de `leanblueprint`, las tablas de estado y los sellos de artefacto; el resto —
la marca en línea, la gramática de una sola macro, la regla de color— es
dispositivo propio y se declara como tal.

### 4.2 La regla WCAG 1.4.1: el color nunca carga significado solo

`docs/citations.md` §8.4 fija ya esta regla: **el color es redundante con la
letra (WCAG 1.4.1)**; la marca se lee igual en escala de grises y la letra
basta para portar el significado. La regla se sostiene aquí por tres razones:

1. **Impresión.** El artículo se lee en papel y en PDF a color reducido; el
   PDF se archiva y se cita en formatos que pierden color.
2. **Accesibilidad.** El 1.4.1 es la condición de que un lector con
   deficiencia de color distinga `P` de `N` sin ayuda cromática.
3. **Consistencia del sistema.** Si el color portara significado propio, la
   paleta sería una segunda gramática que habría que mantener sincronizada con
   el alfabeto; al ser redundante, añadir una clase exige una letra, no un
   matiz.

Ninguna de las tres razones es decorativa: las tres son condiciones de
usabilidad del dispositivo en su medio de circulación.

### 4.3 El contraste con la numeración alfabética de AMS y Chicago

La tentación natural, ante un enunciado con varias partes, es numerarlas —
`(a)`, `(b)`, `(c)` o `(i)`, `(ii)`, `(iii)`—, que es la práctica que AMS y
Chicago emplean para desglosar un enunciado y que todo lector de matemáticas
conoce. Esa numeración **ordena**, y por eso no sirve aquí:

- **No certifica.** La letra `(a)` dice que hay una parte primera; no dice que
  esté probada ni por qué. La marca dice exactamente eso: cómo se estableció.
- **No es portable entre claims.** La numeración alfabética se reinicia en
  cada enunciado y es local al enunciado; el testigo es un identificador
  global, buscable en `lean/TorreKK_LYR_v34.lean` o en la suite.
- **No distingue fuentes.** Numerar partes no separa "probado aquí" de "leído
  en una fuente"; el dispositivo sí, con formas distintas para cada caso.
- **Coste comparado.** Una enumeración alfabética añade un nivel de estructura
  al enunciado; la marca añade un corchete. En un claim de una línea, la
  enumeración es más cara que la marca.

La convención, por tanto, **no compite** con la numeración alfabética: la usa
para lo que ella sirve (desglosar) y deja el estatus a la marca. Del mismo
modo, la marca no sustituye a la bibliografía: la numeración alfabética de la
bibliografía del artículo (`sorting=nyt`, la convención AMS que el proyecto ya
sigue, `docs/citations.md` §7) sigue ordenando las referencias por autor; la
marca no entra en esa capa.

### 4.4 El criterio cuantificado: usabilidad, compactness y sintaxis

La forma de cada marca se decide con cinco cantidades leídas directamente de
`main.tex`, sin juicio de gusto. Se resumen aquí porque son el núcleo del
enriquecimiento pedido; la definición exacta, los cuatro umbrales y la tabla de
sitios están en `docs/citations.md` §8.5.

| Símbolo | Cantidad | Papel en el criterio |
|---|---|---|
| `k` | número de identificadores del claim | `k ≥ 2` es la condición de partida: un identificador nunca gana una línea propia |
| `L` | longitud del listado, en caracteres | mide el peso visual del corchete; `L ≥ 35` es el umbral, calibrado con la lista más corta que ya se imprime como bloque |
| `r` | **residuo de la oración**: palabras de la misma oración que siguen a la marca | `r = 0` exige que la marca *cierre* la oración; `r ≥ 1` mantiene la marca en línea, sin excepción |
| `d` | distancia en palabras al bloque más cercano del mismo párrafo | ritmo de la prosa: `d ≥ 75` evita dos bloques seguidos |
| `i` | 1 si la marca cierra un `\item` de una enumeración | posición sintáctica: dentro de una lista el bloque rompería el ítem |

En una frase operativa: **un listado de dos identificadores o más y de treinta
y cinco caracteres o más pasa a línea propia sólo si la marca cierra su
oración, no cierra un elemento de lista y está a setenta y cinco palabras o
más del bloque anterior.** Todo lo demás queda en línea.

Las cuatro condiciones responden a las cuatro exigencias de usabilidad:

- `k` y `L` al **coste**: el bloque paga un salto de párrafo, así que sólo se
  pide a listados que de verdad necesitan la línea.
- `r` a la **lectura**: como `\witness` emite `\par` antes y después, la
  oración que la sigue empezaría un párrafo nuevo; un residuo de una sola
  palabra (un paréntesis de referencia, un `\testref` final) ya rompería la
  oración. El residuo se cuenta, no se estima.
- `d` al **ritmo**: si el párrafo ya lleva un bloque a menos de setenta y
  cinco palabras, el segundo bloque es monotonía; el propio manuscrito marca
  el suelo empírico, que es la pareja de bloques más apretada que ya acepta.
- `i` a la **posición**: un bloque dentro de una enumeración separaría el
  testigo del resto del ítem; ninguno de los bloques del manuscrito está
  dentro de uno.

El criterio es reproducible por cualquier persona que abra `main.tex`, y
reproduce el estado aplicado sin una sola excepción: los dieciocho bloques del
manuscrito cumplen las cinco condiciones. De las marcas en línea con dos
identificadores o más —treinta y cuatro, treinta y uno `P` y tres `N`—,
trece cierran su oración; el criterio señala nueve de ellas para pasar a
bloque y deja cuatro en línea con una razón numérica (el listado más corto
de todos, dos elementos de lista, un bloque vecino a setenta palabras). La
tabla completa, con la cola de la oración que cada marca cierra, está en
`docs/citations.md` §8.5.

**Revisión.** La convención se revisa con una pasada de lectura sobre la
tabla de `docs/citations.md` §8.5: una pregunta por fila, *¿sigue alguna
palabra de la oración a la marca?* No se escribe una prueba de CI para esto:
un test que volviera a derivar lo que esa sección ya garantiza se probaría
contra sí mismo; el censo (`tests/test_section_census.py`) custodia lo de lo
que el build depende —los identificadores de prueba que el manuscrito cita— y
esto no lo es.

### 4.5 Compactness: el coste medido del dispositivo

El *compactness* no es una intuición aquí: se puede contar. Con el manuscrito
en el estado de este documento, el aparato completo ocupa:

- **240 marcas en línea** — 18 sin argumento (una de ellas la leyenda de la
  primera página) y 222 con identificadores (167 `P` y 55 `N`)—, todas
  compuestas en `\footnotesize` dentro de la oración que marcan: cuestan los
  caracteres del corchete, no una línea;
- **18 bloques** — 9 `P` y 9 `N`—, cada uno con una línea propia y dos saltos
  de párrafo (`\par` antes y después de `\witness`);
- **12 etiquetas** `\wtag` de la lista de testigos y **98 apariciones** de
  `\testref`.

De ahí salen dos consecuencias que justifican los umbrales de §4.4:

1. **El bloque es caro, así que se pide a cambio.** Cuesta una línea y rompe
   el párrafo; sólo se le pide a un listado de 35 caracteres o más, que es
   exactamente la lista más corta que el manuscrito ya imprime como bloque.
   Sin ese umbral, el listado `pisano_orders, modular_orders` —29
   caracteres— ganaría una línea entera por veintinueve caracteres, y el
   coste no tendría contrapartida.
2. **El corchete en línea es barato pero no gratis.** El argumento opcional
   de `\tier` imprime nombres, nunca números: el coste del corchete no crece
   con la numeración de referencias, y los identificadores se rompen en
   línea gracias a los guiones bajos permitidos (`\brk@us`). El límite real
   no es el ancho, es la oración: por eso manda `r`, no `L`.

Con eso, el presupuesto del dispositivo es previsible: en un manuscrito de
este porte, unas veinte líneas propias y un corchete por claim. Es un precio
que la información que compra —cómo se estableció cada afirmación— justifica,
y es también la razón por la que la regla de forma existe: sin ella, el
presupuesto crecería con la prosa y el aparato empezaría a leerse como
ruido.

---

## 5. Qué es y qué no es

**No es una clase de revisión por pares.** La marca `P` dice que una
demostración está formalizada y comprobada por una máquina en el archivo del
proyecto; `N` dice que un número se recalcula en la suite y se contrasta con
una tolerancia declarada. Ninguna de las dos dice que un tercero haya leído el
artículo, ni que la demostración haya sido revisada por un humano, ni que el
resultado esté publicado. Confundir verificación de máquina con revisión por
pares sería el error más grave que este dispositivo podría inducir, y por eso
la leyenda de la primera página define las clases y nada más: la explicación
del aparato vive en esta documentación, no en la página 1.

**No sustituye a la cita.** La fuente externa es y sigue siendo el `\cite`, con
su forma propia junto al claim: `[N]~\cite{key}` y `[P] in~\cite{key}`. El
argumento opcional de `\tier` admite **sólo** identificadores internos —un
`\testref` o el nombre crudo de una declaración de nuestro archivo de Lean— y
el preámbulo levanta un `\PackageError` ante cualquier otra cosa, de modo que
un corchete de marca nunca imprime un número de referencia. Un bracket que
dijera "está citado" sería redundante con la cita que ya está ahí.

**Un claim, una marca.** No hay dos marcas contiguas, ni una marca y un
`\cite` diciendo lo mismo, ni marcas en los pies de figura (la regla 8 de
`docs/citations.md` §8.2). La leyenda es exempta de la regla de testigo
obligatorio porque define, no afirma.

**`P*` es interno.** La clase existe y funciona en el preámbulo (despacho
`\@namedef{tiercol@P*}`, color ocre) para marcar entre compilaciones una
afirmación escrita pero aún no nombrada; el texto impreso nunca la invoca, la
leyenda no la menciona y la prosa no habla de ella. Es una herramienta de
trabajo, no una clase del alfabeto publicado.

**`L` y `R` se eliminaron, y por qué.** Ambas cargaban información que el
texto ya daba:

- `L` significaba "está citado", que es exactamente lo que dice la cita
  numérica, repetida según la norma AMS cada vez que se cita de nuevo (las
  matemáticas no tienen forma de segunda mención; `op. cit.` e `ibid.` son de
  la nota bibliográfica de Chicago). La clase no añadía información y era la
  única que a veces se sostenía sin ninguna referencia junto a ella. Su
  contenido se absorbió en prosa: cada claim conserva su cita al lado.
- `R` marcaba la dirección de la lectura —un "esto se lee como"—, no cómo se
  establece el claim, de modo que no pertenecía a un alfabeto de testigos.
  Once de sus sitios repetían lo que la prosa ya decía; el único que
  funcionaba se escribió como prosa (`a reading of the records, not a result
  about them`), y dos sitios añadidos en una ronda contradecían la sección
  "probado aquí" en la que estaban.

Ambas eliminaciones están documentadas en `docs/citations.md` §8.3 y aplicadas
en el manuscrito: el alfabeto publicado es `P` y `N`.

---

## 6. Honestidad: la novedad declarada

Este documento no presenta la convención como algo consagrado. La afirmación
verificable es la inversa: **ninguna publicación previa marca la verificación
claim por claim en línea, en el punto exacto donde se afirma**, y el proyecto
lo dice como tal.

- `docs/citations.md` §8.4 declara sin rodeos que el estado en línea es
  "una convención de este proyecto y no una de AMS o de Chicago", y señala los
  precedentes reales —`leanblueprint` con estado por enunciado, tablas de
  estado, sellos de artefacto— como lo más cercano que existe.
- La familia omega-pcf es, en ese sentido, **pionera**: adopta el principio de
  esos precedentes y lo baja al claim, que es un nivel de granularidad que los
  precedentes no cubren. Ser pionera tiene un coste declarado: no hay una norma
  externa a la que apelarse si alguien pregunta "¿dónde está esto
  especificado?", y la respuesta es este archivo y `docs/citations.md` §8.
- La pasada de investigación sobre la convención se comprometió a reportar el
  reparto con honestidad —qué parte es estándar de la disciplina, qué parte es
  dispositivo propio y cuál es el precedente más cercano— y así quedó
  registrado. Nada de lo que este documento afirma se presenta como norma
  publicada cuando no lo es.

La novedad declarada es, además, el mejor argumento a favor de la convención:
si el estado de la evidencia es hoy un dato estructural del resultado (§3),
decirlo en el punto de afirmación es más honesto que silenciarlo, y hacerlo
con un criterio cuantificado y reproducible (§4.4) es lo que separa una
convención de un capricho.

---

## 7. Referencias internas

Todas las fuentes de este documento son archivos del repositorio o del entorno
de trabajo de la familia; no se invoca ninguna URL externa.

| Archivo | Qué aporta |
|---|---|
| `docs/citations.md` §8 (§8.1 gramática, §8.2 reglas de redacción, §8.3 alfabeto y por qué no hay `L` ni `R`, §8.4 convención y regla WCAG 1.4.1, §8.5 criterio inline / línea propio cuantificado) | el contrato del dispositivo; la regla operativa que este documento justifica |
| `docs/citations.md` §5, §6, §7 | higiene de datos, convención de documentación y decisiones de estilo ya fijadas (bibliografía alfabética AMS, iniciales) |
| `docs/witness-decisions.md` | decisiones por sitio, contadores del pase de armonización y la lista de trabajo pendiente del autor |
| `README.md` | enlace a la sección de testigos de `docs/citations.md`; `docs/README.md` es el índice del directorio y todavía no lista este archivo |
| `main.tex` — preámbulo (sistema de testigos, despacho de `\tier`, definición de `\witness` y `\wtag`) y leyenda de la primera página | la implementación y lo que el lector ve en la página 1 |
| `lean/TorreKK_LYR_v34.lean` | los identificadores `P` que la marca puede imprimir |
| `tests/` y `tests/test_section_census.py` | la suite numérica y el censo que fija los identificadores de prueba que el manuscrito cita |
| `tests/REPORT.md` | censo histórico del aparato de testigos, marcado explícitamente como anterior a la estandarización; se conserva como historia, no como estado |
| `citation.csl.json`, `CITATION.cff` | la capa bibliográfica con la que la marca **no** se mezcla: la fuente externa es un `\cite`, nunca un identificador de marca |
| `omega-pcf-paper-repos` → `references/decision-gates.md` | el método de la pasada de investigación de la convención (separar estándar de disciplina, dispositivo propio y precedente real) y la regla de no escribir pruebas de CI para convenciones editoriales |
| `omega-pcf-paper-repos` → `references/witness-system.md` | la gramática del sistema de testigos a nivel de familia, sus defectos conocidos (herencia de cursiva en entornos de teorema, marcas en línea dentro de alineados) y el estado de propagación a los repositorios hermanos |

---

## 8. Límites y trabajo pendiente

1. **Aplicación de las filas señaladas.** `docs/citations.md` §8.5 marca
   nueve sitios en línea que el criterio cuantificado lleva a bloque; su
   aplicación corresponde a un pase de edición que no es este documento y que
   actualizará los contadores de §8.5.
2. **Leyenda y cobertura.** La leyenda promete `N` = "verificado
   numéricamente, con el nombre de la prueba que lo comprueba"; el trabajo
   pendiente de `docs/witness-decisions.md` §3.1 y §4 consiste en que cada
   claim `N` cuerpo lleve ese nombre. Mientras haya `N` sin testigo nombrado,
   la leyenda describe la intención del sistema y no todos sus sitios.
3. **Comentarios del preámbulo.** El comentario de cabecera de `main.tex`
   describe la forma del aparato en una frase ("una marca desnuda queda en
   línea; un testigo con nombres gana una línea propia") que es más gruesa que
   el criterio de `docs/citations.md` §8.5: hay marcas con nombres que quedan
   en línea por los cuatro umbrales. La frase debe leerse como resumen, no
   como regla; la regla vive en `docs/citations.md`.
4. **Propagación a la familia.** Sólo `05-kk-golden-throat` y
   `03-crystalline-worldsheet` renderizan marcas; la adopción del criterio en
   los demás repositorios es decisión editorial, nunca mecánica.
5. **Ninguna garantía externa.** Mientras no exista una norma publicada que
   describa la marca por claim, la convención descansa en esta documentación y
   en su revisión; eso está declarado en §6 y no debe presentarse de otro modo.
