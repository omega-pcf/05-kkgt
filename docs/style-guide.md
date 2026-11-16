# GUÍA DE ESTILO — Coherencia formal interna y calidad de código

| Campo | Valor |
|---|---|
| **Documento** | `docs/style-guide.md` |
| **Estado** | Vigente |
| **Versión** | 2.1 (port genérico de familia) |
| **Fecha** | 2026-11-16 |
| **Ámbito** | Estilo editorial (§1–§12) · Calidad de software y código (§13) · Pipeline tex y proofreading (§14) — genérico de familia: sin convenciones propias de un repositorio concreto |

**Objetivo**: Establecer coherencia interna en lenguaje formal, notación, estructura. NO es imitar Elsevier. Es ser **extremadamente serio** sin forzar en caja artificial.

**Marco (propósito)**:
- **Meta del documento**: maximizar **auditabilidad, best practices y correctness**.
- **Estilo buscado**: elegante y **sucinto**; la succinctness es un objetivo explícito, no una preferencia estética.
- **Sin justificaciones tontas**: toda prescripción se justifica en un frente concreto —matemático, de convención, de agudeza/characterización, de claridad lingüística—; la creatividad argumentativa queda siempre subordinada al correctness.

**PRINCIPIO EDITORIAL FUNDAMENTAL**: Este guide es **editorial**, no **autoril** —en cuanto al texto (§1–§12); la calidad del código que lo sostiene se prescribe en §13. Su función es:
- ✅ Prescribir **estilo, formato, coherencia de notación, estructura de presentación**
- ✅ Asegurar **claridad, rigor formal, consistencia** en la escritura
- ❌ **NO** prescribir contenido matemático específico (conceptos, teoremas, construcciones)
- ❌ **NO** agregar conceptos que no estén en el texto original sin verificación explícita
- ❌ **NO** hacer afirmaciones matemáticas que requieran justificación técnica

**Cuando se encuentre una sugerencia de contenido matemático**: Verificar primero contra el documento fuente original del repositorio. Si no está fundamentado, mantener fidelidad al original y solo mejorar la presentación formal.

**Naturaleza**: documento vivo; evoluciona con cada revisión (§10.3).

**Procedencia**: port de `01-primitive-complex-field-dup/docs/style/STYLE_GUIDE.md` v2.1
(2026-11-16), la guía de la familia. El port retira lo propio de ese repositorio (sus
macros, su documento fuente, sus sitios de manuscrito, sus comandos verificados) y en su
lugar enlaza; el criterio de retención es el de §13.7: ninguna regla que un modelo más
grande deduzca del resto.

**Documentos enlazados — las convenciones propias de cada repositorio no se copian aquí:**

| Convención propia del repositorio | Hogar |
|---|---|
| Testigos (`\tier`, `\witness`, `\testref`): gramática, reglas de escritura, alfabeto, criterio cuantificado inline / línea propia, y el censo de los tests citados | [`docs/citations.md`](citations.md) §8 |
| Justificación de los testigos: por qué existen y qué no afirman | [`docs/witness-rationale.md`](witness-rationale.md) |
| Pipeline de figuras determinista y byte-estable (`pnpm run generate:figures`) | [`docs/figures.md`](figures.md) |
| Pipeline de citas (`citation.csl.json` → `src/bibliography.bib`, `CITATION.cff`, `.zenodo.json`) | [`docs/citations.md`](citations.md) §1–§7 |
| Comandos de build, release y convención de commits | [`docs/usage.md`](usage.md) |
| Requisitos e instalación | [`docs/installation.md`](installation.md) |
| Informes concretos de este repo (inventarios, decisiones, veredictos, incidentes) | [`docs/reports/`](reports/README.md) |

---

## 1. VOZ Y TONO

### 1.1 Principio
- **Formal**: Sin casualidad. Académico riguroso.
- **Directo**: Explicar una cosa una sola vez, bien. Sin repetición.
- **Intelectualmente honesto**: Si contradice ortodoxia, decirlo explícitamente (no escondido).
- **No apologético**: Esto es lo que es. Si es inusual, es porque la estructura lo requiere.

### 1.2 Audiencia
- **Público científico experto**: El paper está dirigido a científicos con formación avanzada en matemáticas, pero su alcance multi-dominio requiere familiaridad con teoría de números, análisis complejo, operadores hermíticos, física cuántica, geometría, y verificación computacional. La separación artificial de las matemáticas en "departamentos" no refleja la naturaleza interdisciplinaria de los problemas abordados.
- **No sacrificar legibilidad de forma "tonta"**: No usar palabras menos claras o concisas solo para que el texto suene menos denso o especializado. La audiencia experta espera y aprecia precisión técnica y terminología apropiada. Evitar perífrasis que busquen "suavizar" el contenido a costa de claridad.
- **Claridad sobre simplicidad artificial**: Preferir términos técnicos precisos y concisos sobre perífrasis innecesarias. La legibilidad viene de la estructura, la coherencia y la precisión, no de evitar terminología especializada. El paper aborda problemas matemáticos profundos que requieren un acercamiento multi-dominio; la escritura debe reflejar esta complejidad sin artificialidad.

### 1.3 Estructura de párrafos
- **Tema + justificación + consecuencia**
- No: "Esto es A, que es importante porque B, además es C, y también D, finalmente E"
- Sí: "Esto es A. Por [razón técnica], esto implica B y C. Esto se diferencia de [ortodoxia] porque [explicación geométrica/estructural]."

### 1.4 Evitar
- Enumeraciones mecánicas innecesarias y listas bullet con amplificación posterior repetitiva → ver **§6, patrones 1–2** (ambas son patrones AI)
- "Observar que", "Es importante notar que", "Cabe mencionar que" → ver **§6, patrón 3**
- Parentéticas excesivas → ver **§6, patrón 4**
- Repetición de la misma idea con distinta notación

(Las enumeraciones y listas bullet son válidas cuando mejoran claridad o estructura; se evaluán caso por caso, no se eliminan sistemáticamente.)

### 1.5 Gramática y puntuación en español

**Principio fundamental**: La escritura matemática rigurosa no justifica el descuido de la gramática, la puntuación ni las convenciones literarias del español. La abstracción matemática y la elegancia lingüística son complementarias, no antagónicas.

**Problema común**: Existe una tendencia artificial en la escritura matemática de omitir preposiciones, conjunciones y elementos gramaticales necesarios bajo la falsa premisa de que la "concisión matemática" requiere sacrificar la corrección gramatical. Esta práctica genera ambigüedad, dificulta la lectura y contradice el objetivo de claridad y precisión.

**Reglas de oro**:

1. **Completar frases**: Toda oración debe tener estructura gramatical completa. No omitir preposiciones, conjunciones o artículos necesarios.
   - ❌ "corresponde a rotación hiperbólica" (después de una ecuación, falta conexión)
   - ✅ "y que corresponde a rotación hiperbólica" (conjunción que conecta con la frase anterior)

2. **Preposiciones necesarias**: Usar preposiciones correctamente para establecer relaciones claras entre conceptos.
   - ❌ "El mapa preserva estructura algebraica mediante isomorfismo grupo de Lorentz"
   - ✅ "El mapa preserva la estructura algebraica mediante isomorfismo entre el grupo de Lorentz y..."

3. **Puntuación para claridad**: Las comas, puntos y comas, y dos puntos deben usarse según las reglas del español para evitar ambigüedades y facilitar la lectura.
   - Usar comas para separar elementos en enumeraciones
   - Usar punto y coma para separar cláusulas relacionadas pero independientes
   - Usar dos puntos antes de enumeraciones o explicaciones

4. **Conjunciones de conexión**: Cuando se presentan múltiples conceptos o resultados relacionados, usar conjunciones apropiadas ("y", "que", "donde", "mediante", etc.) para establecer relaciones claras.

5. **Artículos definidos**: No omitir artículos cuando son gramaticalmente necesarios para la claridad y corrección del español.

6. **Voz pasiva refleja y verbos reflexivos**: Cuando un objeto matemático (representación, función, transformación, definición, construcción, operador, matriz, espacio, métrica, estructura, sistema, operación, método, procedimiento, algoritmo, teorema, proposición, lema, corolario) realiza una acción sobre sí mismo o tiene una propiedad inherente, se debe usar la construcción reflexiva "se + verbo" (voz pasiva refleja).
   - ❌ "La representación algebraica escribe $\mathbb{C} = ...$" (incorrecto: sugiere que la representación "escribe" activamente)
   - ✅ "La representación algebraica se escribe como $\mathbb{C} = ...$" (correcto: indica cómo se expresa la representación)
   - ❌ "La representación polar descompone $\mathbb{C} \cong ...$" (incorrecto: sugiere acción activa)
   - ✅ "La representación polar se descompone como $\mathbb{C} \cong ...$" (correcto: indica cómo se estructura la representación)
   - ❌ "La representación euclidiana identifica $\mathbb{C} \cong ...$" (incorrecto: la representación no es un agente que "identifica")
   - ✅ "En la representación euclidiana, $\mathbb{C}$ se identifica con ..." (correcto: indica cómo se establece la identificación)
   - ❌ "La función define..." (cuando la función es el objeto definido)
   - ✅ "La función se define como..." (cuando se está definiendo la función)
   - ❌ "La transformación preserva..." (puede ser correcto si la transformación es el sujeto activo)
   - ✅ "La transformación se preserva bajo..." (cuando se habla de una propiedad que se mantiene)

   **Regla práctica**: Si el objeto matemático es el **sujeto de la oración** y la acción describe **cómo se expresa, estructura, define o caracteriza** ese objeto, usar "se + verbo". Si el objeto es el **agente activo** que realiza una acción sobre otro objeto, usar el verbo sin "se".

   **Evitar construcciones donde objetos matemáticos son sujetos de verbos transitivos que sugieren acción activa**: Cuando un objeto matemático no puede ser un agente activo (como "representación", "definición", "construcción"), evitar usarlo como sujeto de verbos transitivos como "identifica", "define", "construye", etc. En su lugar, usar construcciones como "En X, Y se identifica con...", "Mediante X, Y se define como...", o "X establece la identificación/definición de...".

   **Verbos comunes que requieren "se" en contexto matemático**:
   - `se escribe`, `se define`, `se descompone`, `se caracteriza`, `se parametriza`, `se clasifica`, `se identifica`, `se representa`, `se expresa`, `se formula`, `se construye`, `se establece`, `se determina`, `se calcula`, `se evalúa`, `se resuelve`, `se aplica`, `se utiliza`, `se emplea`, `se preserva` (cuando es propiedad), `se mantiene`, `se conserva`, `se genera`, `se produce`, `se obtiene`, `se resulta`, `se aparece`, `se surge`, `se emerge`, `se muestra`, `se revela`, `se establece`

**Justificación**: La precisión matemática y la corrección gramatical se refuerzan mutuamente: una frase gramaticalmente correcta elimina ambigüedades de interpretación, y la voz pasiva refleja es necesaria en español para expresar propiedades inherentes y estructuras matemáticas; su omisión genera construcciones agramaticales.

**Ejemplo de mejora**:
- ❌ "La transformación preserva estructura, métrica, simetrías mediante isomorfismo grupo Lorentz corresponde rotación hiperbólica"
- ✅ "La transformación preserva la estructura, la métrica y las simetrías mediante un isomorfismo entre el grupo de Lorentz y las transformaciones conformes, y que corresponde a una rotación hiperbólica"

---

## 2. NOTACIÓN UNIFICADA

### 2.1 Macros de Notación (declaradas en el preámbulo de cada repo)

**Principio**: Solo usar macros para notación específica del documento que:
- Se repite frecuentemente
- Es compleja o larga de escribir
- Podría cambiar o necesitar ajustes globales

**Macros disponibles**: las que declare el preámbulo del propio repositorio. Este
documento no las lista —son notación de ese documento, no de familia—; la fuente es su
`.tex` raíz y su preámbulo.

**Notación estándar (NO usar macros):**
- ✅ Usar directamente `\mathbb{C}`, `\mathbb{R}`, `\mathbb{Z}`, `\mathbb{Q}`, `\mathbb{N}` (estándar, bien conocida)
- ✅ Usar directamente `\varphi` para la razón áurea (estándar)
- ✅ Usar directamente `\mathcal{C}`, `\mathcal{H}`, etc. (estándar)

**Razón**: Los macros para notación estándar agregan complejidad innecesaria sin beneficio real. Solo tienen sentido para notación específica del documento que se repite mucho.

### 2.2 Macros de Referencias Cruzadas (declarados en el preámbulo de cada repo)

Para referencias consistentes a construcciones matemáticas, cada repo declara **un macro
por tipo de construcción** —`\tref` → "Teorema X.Y.Z", `\dref` → "Definición X.Y.Z",
`\pref` → "Proposición X.Y.Z", `\lref`, `\cref`, `\oref`, `\corref`, `\conjref`
análogos— **o** carga el paquete `cleveref`, que los cubre con `\cref`, `\autoref` y
`\eqref`. La lista concreta de un repo es suya; aquí sólo se prescribe el uso.

**Trampa**: si el preámbulo define sus propias macros de referencia con los nombres de
`cleveref` (`\cref` entre ellos), no cargar `cleveref` —ni copiar código que lo use—
sin renombrar antes esas macros: el paquete y la macro propia colisionan en el mismo
nombre.

**Uso recomendado:**
- ✅ Usar estos macros en lugar de escribir manualmente "Teorema~\ref{...}"
- ✅ Ejemplo: `Como se muestra en \pref{prop:<etiqueta>}...` en lugar de `Como se muestra en Proposición~\ref{prop:<etiqueta>}...`
- ✅ Esto asegura formato consistente y facilita cambios globales

### 2.3 Complejos
- **Módulo**: siempre `|z|` en contexto algebraico, "magnitud" en contexto geométrico
- **Variable compleja**: `z = x + iy` en primera definición, luego solo `z`
- **Euler**: `e^{i\theta}` (no `e^{i\theta}` variaciones)

### 2.4 Espacios
- **Plano complejo**: `ℂ` (usar `\mathbb{C}`)
- **Números reales**: `ℝ` (usar `\mathbb{R}`)
- **Enteros**: `ℤ` (usar `\mathbb{Z}`)
- **Hilbert**: `ℋ` o `H` (ELEGIR UNO por sección y mantener)
- **Espacios de Sobolev/L²**: `L²(domain)` - ser explícito sobre dominio

### 2.5 Operadores
- **Operador propio del documento**: si se repite mucho y su nombre es largo, declararle macro en el preámbulo y usarla siempre; un operador estándar nunca lleva macro (§2.1)
- **Fourier**: `ℱ` (usar `\mathcal{F}`)
- **Integral**: siempre `∫_X f(x) dx` con limites claros

### 2.6 Razón áurea
- **Símbolo**: φ (usar `\varphi`, no variaciones)
- **Valor**: φ ≈ 1.618... (si se necesita numérico) o solo φ (algebraico)
- **Potencias**: `φ^σ` o `φ^n` - ser consistente con índice

### 2.7 Conjuntos/Indexación
- **Índices discretos**: `k, n, m ∈ ℤ` o `σ ∈ ℤ`
- **Parámetros continuos**: `t ∈ ℝ`, `θ ∈ [0, 2π)`
- **Secuencias**: `{a_n}_{n∈ℕ}` o solo `{a_n}` si contexto es claro

---

## 3. ESTRUCTURA DE DEFINICIONES

### 3.1 Formato estándar
```
\begin{definition}[Nombre descriptivo]
[ENUNCIADO CONCISO EN UNA FRASE]

Para [elementos en juego], [propiedad fundamental]:
\[
[fórmula principal]
\]

[CONTEXTO/SIGNIFICADO: 1-2 párrafos máximo explicando qué significa, por qué importa, cómo se relaciona con lo anterior]
\end{definition}
```

### 3.2 Ejemplo BUENO
```
\begin{definition}[Módulo en el plano complejo]
Para $z = x + iy \in \mathbb{C}$ con $x, y \in \mathbb{R}$, el módulo es la norma euclidiana:
\[
|z| := \sqrt{x^2 + y^2}
\]
Geométricamente, $|z|$ es la distancia del punto $z$ al origen. Esta magnitud hereda las propiedades de la norma euclidiana en $\mathbb{R}^2$, incluyendo la desigualdad triangular: $|z_1 + z_2| \leq |z_1| + |z_2|$.
\end{definition}
```

### 3.3 Ejemplo MALO
```
\begin{definition}[Módulo]
Se define el módulo como...
\textbf{Propiedades:}
\begin{itemize}
\item Es siempre positivo
\item Satisface la desigualdad triangular
\item Es invariante bajo rotación
\item Etc.
\end{itemize}
[Explicación adicional que repite propiedades]
\end{definition}
```

**Por qué**: El malo tiene 3 problemas:
1. Repite contenido ("Es positivo" → "propiedades" → explicación)
2. No explica SIGNIFICADO de módulo, solo lista atributos sin contexto
3. La enumeración no añade claridad porque solo repite lo mismo que la explicación posterior

**Nota**: Una enumeración sería válida si organizara información técnica de forma clara y añadiera valor estructural, no si solo repite lo que ya se dice después.

---

## 4. ECUACIONES Y FÓRMULAS

### 4.1 Regla: **Ecuación ↔ Texto**
Toda fórmula debe estar integrada con texto, nunca aislada.

#### 4.1.1 MALO
```
El operador está definido como:
\[
\hat{\Omega} = \begin{pmatrix} a & b \\ c & d \end{pmatrix}
\]
```

#### 4.1.2 BUENO
```
El operador $\hat{\Omega}$ es una transformación lineal representada en base estándar como:
\[
\hat{\Omega} = \begin{pmatrix} a & b \\ c & d \end{pmatrix}
\]
donde $a, b, c, d$ son coeficientes que satisfacen [propiedad]. Esta forma diagonal revela que $\hat{\Omega}$ actúa como [interpretación geométrica].
```

### 4.2 Declaración explícita de símbolos
Si una ecuación introduce variables nuevas, declararlas DENTRO o INMEDIATAMENTE DESPUÉS:

```
La relación de acoplamiento viene dada por:
\[
z = \varphi y
\]
donde $z$ denota la coordenada vertical, $y$ la coordenada imaginaria horizontal, y $\varphi$ es la razón áurea.
```

### 4.3 Alineación y espaciado
- **Ecuaciones cortas (<60 caracteres)**: `\[...\]` (displaymath)
- **Ecuaciones largas o múltiples**: `\begin{align*}...\end{align*}`
- **Entre ecuaciones**: párrafo de transición, no líneas en blanco + ecuación

---

## 5. PROPOSICIONES, TEOREMAS, COROLARIOS

### 5.1 Estructura
```
\begin{theorem}[Nombre descriptivo]\label{thm:...}
[ENUNCIADO FORMAL EN UNA O DOS LÍNEAS]

Si [hipótesis], entonces [conclusión]:
\[
[fórmula concisa]
\]
\begin{proof}
[Argumento principal en prosa, estructurado lógicamente]
[Si hay pasos algebraicos clave, mostrar UNO o DOS]
[Conclusión: "Por lo tanto, [conclusión del teorema]"]
\end{proof}
\end{theorem}
```

### 5.2 Diferencia: Theorem vs Proposition vs Lemma
- **Theorem**: Resultado PRINCIPAL. Puede cambiar toda una perspectiva.
- **Proposition**: Resultado IMPORTANTE pero subordinado. Herramienta para teoremas.
- **Lemma**: Resultado TÉCNICO necesario. No interesa por sí solo.

Si no es claro cuál es, errar hacia **Proposition** (es lo más flexible).

### 5.3 Observación vs Remark
- **Observation** (Observación): Insight geométrico o estructural que sale NATURALMENTE del teorema.
- **Remark** (Nota): Aclaración técnica o contexto sobre notación/convención.

### 5.4 Párrafos dentro de entornos de teoremas

**Verificado (2026-11-16)**: una línea en blanco en el fuente **sí** produce un párrafo nuevo dentro de `theorem`, `proposition`, `definition`, `corollary` (amsthm + la clase del documento + su `\parskip`). La premisa que antes encabezaba esta sección («los entornos de `amsthm` no muestran el salto aunque haya líneas en blanco») es **falsa** en el pipeline de la familia y se retiró; la evidencia es el PDF construido de cada repo, no una regla aquí.

- ✅ Separar párrafos del enunciado con **línea en blanco** (convención LaTeX).
- ❌ `\par` explícito: es exactamente lo que hace la línea en blanco; no aporta nada y hoy sobra.
- **Regla práctica**: un enunciado de más de 3-4 oraciones o que trata varios conceptos se divide en párrafos con línea en blanco.

**Evitar**: cuerpo de teorema escrito como una sola línea larga de fuente: se vuelve ilegible en el origen aunque el PDF salga bien.

### 5.5 Enumeración en enunciados de proposiciones/teoremas

**Regla para enunciados**:
- ✅ **Usar enumeración** cuando hay múltiples resultados relacionados que se demuestran juntos pero son conceptualmente distintos:
  ```
  \begin{proposition}[...]
  Al incrementar $\sigma \to \sigma+1$:
  \begin{enumerate}
  \item $\varepsilon(\sigma+1) = \varphi \cdot \varepsilon(\sigma)$
  \item $|z|_{\sigma+1} = \varphi |z|_\sigma$
  \end{enumerate}
  \end{proposition}
  ```
- ❌ **Evitar enumeración** cuando los resultados se pueden expresar fluidamente en una o dos oraciones:
  ```
  ❌ "El operador tiene tres propiedades: (1) Es hermítico, (2) Tiene espectro real, (3) Genera descomposición ortogonal"
  ✅ "El operador es hermítico, tiene espectro real y genera una descomposición ortogonal."
  ```

**Regla para proofs**:
- ✅ **Proof conciso**: Un párrafo fluido que conecta los pasos lógicamente, usando referencias a la enumeración cuando aplica:
  ```
  \begin{proof}[Por método]
  Por [teorema], [paso 1]. De [definición], [paso 2] implica (1). [Conclusión] establece (2).
  \end{proof}
  ```
- ❌ **Evitar**: Múltiples párrafos con `\par` a menos que cada párrafo trate un concepto completamente distinto. Un proof no debe ser una lista de pasos separados.
- ✅ **Balance**: El proof debe ser suficientemente completo para ser riguroso, pero no tan verboso que repita información del enunciado o sea artificialmente extenso.

**Criterio de decisión**: Si al leer el enunciado con enumeración es inmediatamente claro qué se está afirmando, y el proof puede referirse a los puntos numerados de forma natural, usar enumeración. Si la enumeración solo añade estructura artificial sin mejorar claridad, usar texto corrido.

### 5.6 Balance estilístico: Rigor filosófico sin redundancia artificial

**Tensión entre dos extremos**: (1) condensación artificial extrema estilo Elsevier que sacrifica claridad conceptual, y (2) verbosidad excesiva que repite información sin añadir valor.

**Criterio**: El texto debe fluir como una conversación entre científicos que se respetan mutuamente: suficiente contexto para entender el significado profundo (el "por qué" y el significado, a la manera de una carta científica del siglo XIX), pero sin repetir lo obvio hasta que un lector experto piense "ya lo entendí, sigue adelante".

**Principios del balance**:
- ✅ **Explicar el significado**: Incluir frases que expliquen por qué algo es importante o qué significa conceptualmente (ej: "Esta simultaneidad emerge de la necesidad de preservar...")
- ✅ **Naturalidad filosófica**: Usar lenguaje que refleje el pensamiento matemático profundo, no solo la mecánica (ej: "La coherencia geométrica demanda..." en lugar de solo "Por lo tanto...")
- ❌ **Evitar redundancia**: No repetir en el proof lo que ya se estableció en el enunciado. Si el enunciado dice "preservar la estructura geométrica bajo transformaciones de escala", el proof puede referirse simplemente a "coherencia geométrica" sin repetir toda la frase.
- ❌ **Evitar condensación artificial**: No eliminar palabras necesarias solo para sonar "más técnico". Preferir "El acoplamiento temporal establece:" sobre "Del acoplamiento temporal:" cuando la primera forma es más clara.
- ✅ **DRY en conceptos, no en explicación**: No repetir conceptos, pero sí explicar el significado cuando añade valor conceptual.

**Ejemplo de buen balance**:
```
\begin{proposition}[Escalamiento simultáneo del parámetro de escala y del módulo complejo]
La estructura autosimilar del sistema establece que al avanzar $\sigma \to \sigma+1$:
\begin{enumerate}
\item $\varepsilon(\sigma+1) = \varphi \cdot \varepsilon(\sigma)$
\item $|z|_{\sigma+1} = \varphi |z|_\sigma$
\end{enumerate}
Esta simultaneidad emerge de la necesidad de preservar la estructura geométrica...
\end{proposition}

\begin{proof}[Por cálculo directo]
El acoplamiento temporal establece: [ecuación]
De la definición del operador: [ecuación]
el escalamiento de la fase requiere (1).
La coherencia geométrica demanda (2), completando la demostración.
\end{proof}
```

**Contraste con extremos**:
- ❌ **Demasiado condensado**: "Del acoplamiento temporal, $\varepsilon(\sigma+1) = \varphi\varepsilon(\sigma)$ y $|z|_{\sigma+1} = \varphi|z|_\sigma$." (Pierde significado conceptual)
- ❌ **Demasiado verboso**: Repetir "preservar la estructura geométrica bajo transformaciones de escala" tanto en enunciado como en proof (Redundante)

---

## 6. EVITAR PATRONES AI

### 6.1 Patrón 1: Enumeración repetitiva innecesaria
❌ "Este concepto tiene varias propiedades. Primero, A. Segundo, B. Tercero, C. Estas propiedades implican que..." (cuando la enumeración no añade claridad)

✅ "Este concepto tiene tres propiedades distinguidas: A implica X, B implica Y, C implica Z. En conjunto, esto significa que..."

**Nota**: Las enumeraciones estructuradas (con `\textbf{}` o listas) son válidas cuando mejoran la claridad, organización o legibilidad. No deben eliminarse sistemáticamente; deben evaluarse caso por caso según su utilidad.

### 6.2 Patrón 2: Lista bullet + amplificación repetitiva
❌
```
El operador tiene las siguientes características:
• Es hermítico
• Tiene espectro real
• Genera una descomposición ortogonal

La hermiticidad del operador significa que...
El espectro real implica que...
```
(cuando la amplificación repite exactamente lo mismo que la lista)

✅
```
El operador es hermítico, asegurando espectro real y generando una descomposición ortogonal de $\mathcal{H}$. La hermiticidad emerge de [justificación]. El espectro real es consecuencia de [construcción].
```

**Nota**: Las listas bullet son apropiadas cuando organizan información técnica de forma clara y la amplificación posterior añade contexto o justificación, no repetición.

### 6.3 Patrón 3: "Observar que", "Es importante notar que"
❌ "Observe que esto implica que..."
✅ "Por lo tanto..." o "Esto implica..." o nada (dejar que la lógica sea clara)

### 6.4 Patrón 4: Parentéticas excesivas
❌ "El operador (que definimos antes) tiene (como mencionamos) la propiedad (importante) de..."
✅ "El operador tiene la propiedad de..." [Y usar \ref{} si necesitas remitir a definición anterior]

### 6.5 Patrón 5: Artefactos de AI en el código (→ §13)
Los artefactos generados por AI aparecen también en **código** —módulos monolitos, self-testing, stdout como API, registro por `append` con efectos de import, CLI a mano, asserts de frases de prosa, tolerancias por sitio— con la misma forma que los patrones 1–4: repetición disfrazada de utilidad y atajos que delegan trabajo en quien lea después. Su nomenclatura (**D1–D7**), la remediación con librerías estándar y la checklist correspondientes están en **§13**; aquí no se duplican.

---

## 7. COHERENCIA SECCIÓN A SECCIÓN

### 7.1 Dentro de una sección
- **Primera definición**: Introducir notación completa, ser explícito
- **Definiciones posteriores**: Reutilizar notación, no re-declarar
- **Transiciones**: "Ahora consideremos...", "El siguiente paso...", "Para entender [resultado anterior]..."

### 7.2 Entre secciones
- **Cross-references**: usar los macros de §2.2 (`\tref{...}`, `\dref{...}`, `\pref{...}`…), no «en la sección anterior» ni `Proposición~\ref{...}` escrito a mano
- **Notación**: Si cambias (ej: de real a complejo), explicar transición
- **Supuestos**: Si una sección asume resultado de anterior, mencionarlo explícitamente

---

## 8. CHECKLISTS POR TIPO DE AMBIENTE

### 8.1 Para cada DEFINITION
- [ ] ¿Enunciado conciso? (máx 2 líneas)
- [ ] ¿Fórmula principal clara?
- [ ] ¿Contexto/significado explicado en 1-2 párrafos?
- [ ] ¿Qué problema resuelve o qué intuición clarifica?
- [ ] ¿Cero bullet lists?

### 8.2 Para cada THEOREM/PROPOSITION
- [ ] ¿Hipótesis y conclusión claras?
- [ ] ¿Proof es argumento (no lista de pasos)?
- [ ] ¿Conexión con resultado anterior explícita?
- [ ] ¿Label descriptivo?

### 8.3 Para cada PROOF
- [ ] ¿Párrafo introductorio explica estrategia?
- [ ] ¿Pasos principales en prosa (no numerados)?
- [ ] ¿Ecuaciones muestran NO demuestran?
- [ ] ¿Conclusión: "Por lo tanto..." es clara?

(La checklist de código va en §13.6.)

---

## 9. CASOS ESPECIALES: CONTRADECIR ORTODOXIA

Cuando el paper contradice convenciones (porque la estructura geométrica lo requiere):

**Formato explícito:**
```
En contraste con [convención estándar], aquí encontramos que [resultado disruptivo].
Esto no contradice [teoría estándar], sino que revela que [interpretación que reconcilia].
La razón es que [explicación geométrica/estructural profunda].
```

**No esconder**. No pedir perdón. Ser claro sobre QUÉ contradice y POR QUÉ es necesario.

---

## 10. APLICACIÓN DEL GUIDE

### 10.1 Plantilla: Sección I

Sección I debe servir como patrón. Una vez esté perfecta:
- Cada definición sigue estructura estándar
- Cada párrafo es necesario (sin repetición)
- Notación es consistente
- Voz es formal, seria, clara
- NO hay bullet lists sin justificación

Luego, las otras secciones deben **coincidir exactamente** en estilo.

### 10.2 Procedimiento de uso

1. **Antes de revisar sección**: Leer este guide
2. **Mientras revisas**: Comparar contra checklists (§8 para texto, §14.4 para pipeline/proofreading, §13.6 para código)
3. **Si encuentras sección que NO cumple**: Preguntar "¿Qué regla quebrantó?" → luego arreglarlo
4. **Cuando encuentres NUEVA pauta** (patrón repetido, incoherencia): Agregar al guide
5. **Verificación de contenido**: Antes de agregar conceptos matemáticos nuevos, verificar contra el documento fuente original del repo (regla completa en el Principio editorial de la cabecera). Si no está fundamentado, mantener fidelidad al original.

**Ejemplo de la regla 5**: una sugerencia de formalización que introduce "kernel modular K(z,w)" cuando el original solo menciona "kernel" o "kernel PCF" debe revisarse primero para ver si está justificada; en caso de duda, mantener el texto original y solo mejorar la presentación formal.

### 10.3 Ciclo de mantenimiento

1. Aplicar este guide a **Sección I (Introducción)** completamente
2. Validar que queda como template
3. Replicar en Sección II y III
4. Ajustar guide según aprendamos

**Goal final**: Paper que sea **riguroso, claro, serio, sin artificialidad** y que sea genuinamente legible para su audiencia científica experta, con formación en teoría de números, análisis complejo, operadores hermíticos, física cuántica, geometría y verificación computacional, entre otros.

---

## 11. DETECCIÓN PROACTIVA DE INCONSISTENCIAS Y SUGERENCIAS EDITORIALES

### 11.1 Principio
El AI debe actuar como editor proactivo: detectar inconsistencias matemáticas, lógicas o estilísticas, incluso cuando no están explícitamente solicitadas en el prompt.

### 11.2 Protocolo de Detección

**Durante la tarea**, señalar cualquier:
- Inconsistencia matemática (contradicción, notación inconsistente, concepto no definido)
- "Feeling" fuerte de que algo valdría la pena editar (ambigüedad, falta de claridad, posible error)
- Desconexión entre el texto y el contenido matemático desarrollado

**Al finalizar la tarea (antes de commit si aplica):**

1. **Evaluar la intensidad de la sensación:**
   - **Fuerte**: Inconsistencia clara, posible error matemático, contradicción lógica
   - **Moderada**: Ambigüedad, falta de claridad, posible mejora
   - **Débil**: Sugerencia menor, optimización estilística

2. **Si la sensación es FUERTE o MODERADA:** presentar la sugerencia al usuario al final del task, con un análisis desmenuzado:
   - **Qué detectaste**: Descripción específica de la inconsistencia/sugerencia
   - **Dónde está**: Ubicación exacta (archivo, líneas, sección)
   - **Por qué es relevante**: Impacto potencial (matemático, lógico, estilístico)
   - **Contexto cognitivo**: Qué te hizo pensar que hay un problema (patrón, contradicción, falta de definición, etc.)
   - **Opciones**: Qué se podría hacer (corregir, verificar contra original, investigar más)

3. **Si el prompt incluye hacer commit al finalizar:**
   - **ANTES de ejecutar el commit**, presentar las sugerencias detectadas
   - Dar opción explícita al usuario: revisar y decidir sobre las sugerencias primero · proceder con el commit de todas formas · modificar el commit para incluir correcciones

### 11.3 Formato de Presentación

```
---
🔍 **SUGERENCIA EDITORIAL DETECTADA**

**Tipo**: [Inconsistencia matemática / Ambigüedad / Posible error / Mejora sugerida]
**Intensidad**: [Fuerte / Moderada]
**Ubicación**: [archivo:líneas]

**Qué detecté**: [Descripción específica del problema]

**Análisis cognitivo**: 
- [Qué patrón/contradicción/falta te hizo pensar que hay un problema]
- [Por qué es relevante matemáticamente/lógicamente]
- [Qué impacto podría tener si no se corrige]

**Opciones**:
1. [Opción 1: acción sugerida]
2. [Opción 2: alternativa]
3. [Opción 3: investigar más antes de decidir]

¿Deseas que proceda con el commit o prefieres revisar esto primero?
---
```

### 11.4 Ejemplos

1. **Inconsistencia matemática**: un concepto se nombra de una forma en una sección y de otra en el desarrollo (desconexión terminológica) → verificar si está fundamentado o es una adición no justificada.
2. **Falta de definición**: se usa un símbolo nuevo sin definición previa → el lector no puede seguir el argumento → agregar definición o referencia cruzada.
3. **Contradicción lógica**: se afirma X en una sección y no-X en otra → rompe la coherencia del argumento → verificar cuál es la afirmación correcta según el documento original.

### 11.5 Límites
- **NO** interrumpir el flujo de trabajo principal con sugerencias menores
- **NO** hacer cambios sin consultar si la sensación es fuerte
- **SÍ** presentar sugerencias al final, antes de commit
- **SÍ** ser específico y desmenuzado en el análisis

---

## 12. COMPARACIÓN DEL DOCUMENTO FUENTE CON EL MANUSCRIPTO

### 12.1 ⚠️ REGLA CRÍTICA: NO EDITAR EL DOCUMENTO FUENTE ORIGINAL

**El documento fuente original que el repositorio recibió NO debe ser modificado.** Todas las correcciones, mejoras y actualizaciones deben realizarse Únicamente en el `.tex` del repositorio (el archivo raíz y los `.tex` que incluya).

- ✅ **SÍ**: Editar el `.tex` del repo para corregir terminología, mejorar presentación, etc.
- ❌ **NO**: Editar el documento fuente original bajo ninguna circunstancia
- ✅ **SÍ**: Usarlo como referencia para verificar contenido original
- ✅ **SÍ**: Compararlo con el `.tex` del repo para detectar inconsistencias

### 12.2 Propósito
Cuando el usuario proporciona una referencia de sección (número como "1.5" o string descriptivo como "fundamento y alcance del presente trabajo"), generar un informe conciso de diferencias entre la versión fuente y la versión correspondiente del manuscrito LaTeX.

### 12.3 Protocolo de Búsqueda

**Paso 1: Interpretar la referencia**
- Si es un número (ej: "1.5", "2.3", "8.1.5"): buscar títulos de sección que contengan ese número
- Si es un string descriptivo (ej: "fundamento y alcance", "coherencia de axiomas"): buscar títulos o contenido que contenga esas palabras clave

**Paso 2: Buscar en el documento fuente**
- Buscar el patrón en títulos de sección (ej: `### 1.5`, `#### 2.3.1`)
- Extraer el contenido completo de la sección (incluyendo párrafos siguientes hasta la siguiente sección o subsección)

**Paso 3: Buscar en el manuscrito LaTeX**
- Buscar en todos los `.tex` del repositorio
- Buscar títulos equivalentes (ej: `\subsection{...}`, `\subsubsection{...}`) o contenido que corresponda a la misma sección
- Extraer el contenido completo correspondiente

**Paso 4: Comparar y generar informe**

### 12.4 Formato del Informe

El informe debe ser **muy conciso** e incluir:

1. **Ubicación**: Líneas y títulos exactos en ambos documentos
2. **Cambios principales**: Lista breve de diferencias estructurales y de contenido
3. **Resumen**: Síntesis de si el contenido conceptual es equivalente o si hay diferencias sustanciales

**Estructura del informe:**
```
## Informe de Comparación: Sección [referencia]

### Ubicación
- **Documento fuente**: Líneas X-Y (título: `...`)
- **Manuscrito `.tex` (archivo)**: Líneas X-Y (título: `...`)

### Cambios principales
Lista breve de diferencias estructurales y de contenido, incluyendo:

**A. Diferencias de contenido/concepto:**
1. [Diferencia terminológica, conceptual, o de información]

**B. Diferencias de estilo/estructura:**
1. [Repetición de estructuras, falta de paralelismo, verbos vagos, etc. - ver §1 (Evitar) y §6]
2. [Problemas de fluidez, claridad, o presentación]

**C. Diferencias de formato (solo si afectan significado):**
1. [Notación matemática diferente, referencias, etc.]

### Resumen
[Breve síntesis de equivalencia conceptual o diferencias sustanciales, incluyendo recomendaciones de corrección si hay problemas de estilo]
```

### 12.5 Ejemplos de Referencias Válidas

- Números de sección: `1.5`, `2.3`, `8.1.5`, `III.1.5`
- Strings descriptivos: `fundamento y alcance`, `coherencia de axiomas`, `verificación computacional`
- Referencias mixtas: `§1.5`, `Sección 1.5`

### 12.6 Notas Importantes

- **Buscar en ambos documentos**: Siempre comparar la fuente con el manuscrito, no solo uno
- **Herramientas del repo** (sustituyen la búsqueda a mano): cuando un repo trae scripts de comparación —referencias `§X.Y` de la fuente ausentes en el `.tex`, `§` → labels LaTeX, numeración fuente vs. PDF— se usan éstos; el inventario de scripts es de cada repo y no se lista aquí
- **Contexto suficiente**: Incluir suficiente contexto (párrafos anteriores/posteriores) para identificar la sección correcta
- **Formato diferente**: Recordar que la fuente puede usar Markdown mientras el manuscrito usa LaTeX - las diferencias de formato (notación matemática, referencias) son esperadas y no deben considerarse como diferencias de contenido a menos que cambien el significado
- **Concisión**: El informe debe ser breve y directo, enfocándose en diferencias sustanciales de contenido, no en diferencias menores de formato

---

## 13. CALIDAD DE SOFTWARE Y CÓDIGO

Las secciones §1–§12 prescriben la calidad del **texto**. Esta sección prescribe la del **código** que lo produce, lo verifica y le da soporte (scripts, tests, módulos de apoyo). Es de obligado cumplimiento en cualquier revisión de código del repositorio, con independencia de quién lo haya escrito.

### 13.1 Doctrina

- **No self-baked.** Ante cualquier necesidad funcional se usa la librería estándar o una librería consolidada del ecosistema. Con generación asistida por AI no existen pretextos de legado («así lo heredamos de un Fortran de los 90»): el código se reescribe contra la librería estándar.
- **Librería estándar primero.** La tabla §13.3 es normativa: `argparse` para CLI, `logging` para registro, `dataclasses` para datos, `numpy.testing` para verificación numérica, `pytest` para tests.
- **Code review seria.** Ningún módulo se incorpora sin revisión de código explícita —estructura, contratos, tests, naming—; la revisión no es formalidad ni trámite.
- **El módulo de producción nunca se testea a sí mismo.** Los asserts residen en la suite, nunca en el código que se ejecuta (defecto **D2**).

### 13.2 Taxonomía de defectos (D1–D7)

Nomenclatura estable, citable en auditorías (p. ej. «D4 ×47»):

- **D1 — Módulo monolito**: un solo archivo que mezcla datos, lógica y presentación sin fronteras internas; cambiar una cosa obliga a tocar todo.
- **D2 — Self-testing**: asserts de validación dentro del código de producción; el módulo se testea a sí mismo.
- **D3 — API que imprime / tests que parsean stdout**: la interfaz devuelve texto por impresión y los tests lo analizan por parseo en lugar de recibir valores.
- **D4 — Registro por `append` con efectos secundarios de import**: el registro se llena con `SECCIONES.append((46, '…', fn))` repetido (p. ej. ×47), de modo que simplemente importar el módulo ya tiene efectos sobre el estado global.
- **D5 — CLI a mano y `print` como log**: uso directo de `sys.argv` sin `argparse`, y `print` en lugar de `logging`.
- **D6 — Asserts de frases literales de prosa**: p. ej. `assert "rel. 6.1e-05" in run.stdout`; el test afirma un string, no un valor, y se rompe ante cualquier reflow del texto.
- **D7 — Tolerancias ad hoc escritas por sitio**: cada comparación numérica arrastra su propia tolerancia literal, sin una única fuente que defina la precisión.

### 13.3 Autohecho → estándar

| Autohecho (defecto) | Estándar obligatorio |
|---|---|
| `assert` internos del código de producción (D2) | `numpy.testing` — `assert_allclose` con `rtol` explícito y mensaje de fallo; precondiciones de entrada con `raise`. Lo que es test va a **`pytest`**. |
| API que imprime y tests que parsean stdout (D3) | **`dataclasses`** que devuelven objetos; **`syrupy`** / **`pytest-snapshot`** únicamente para el contrato de stdout que el paper cita (§13.4) |
| Registro por `append` con efectos de import (D4) | Mapa declarativo o decorador `@section(n, title)`; nunca `append` esparcido por el archivo |
| CLI a mano con `sys.argv` y `print` como log (D5) | **`argparse`** para CLI; **`logging`** para registro; el reporte se renderiza desde datos estructurados, no desde strings impresos |
| Verificación numérica escrita a mano y tolerancias por sitio (D6, D7) | **`numpy.testing`** + un **único helper de tolerancia**, cuyo valor es el ancho de la precisión que el documento imprime |

**Además**: invariantes aleatorizadas → **`hypothesis`**, donde aporte cobertura real.

### 13.4 Contrato de salida

Si el documento **cita lo que un script imprime** (una cifra, un ratio, un renglón de salida), ese stdout se congela con un **test golden/snapshot** (`syrupy` o `pytest-snapshot`): el test falla si la salida citada cambia. Todo lo demás pasa a afirmar **valores**, nunca strings — así se elimina D6 por construcción.

### 13.5 Naming de tests y testigos

- **Ids de test**: `test_<qué_afirma>` en snake_case, atados al claim que verifican (no al archivo que ejecutan).
- **Testigos internos** (`\tier`, `\witness`, `\testref`, y el censo de los ids citados): su gramática, sus reglas de escritura y su alfabeto son convención de cada repo y **no se copian aquí** — contrato en [`docs/citations.md`](citations.md) §8, justificación en [`docs/witness-rationale.md`](witness-rationale.md). Sólo el principio se enuncia: el nombre del testigo coincide **carácter a carácter** con el archivo `.lean` o la suite que lo declara; cualquier desviación es un defecto.

### 13.6 Checklist de calidad de código

- [ ] ¿Se usa la librería estándar en lugar de código autohecho (§13.3)?
- [ ] ¿Cero asserts dentro del módulo de producción (D2)?
- [ ] ¿La API devuelve datos (`dataclasses`) y no texto impreso (D3)?
- [ ] ¿El registro es declarativo, sin efectos secundarios de import (D4)?
- [ ] ¿CLI con `argparse` y log con `logging`, reporte renderizado desde datos (D5)?
- [ ] ¿Los tests afirman valores, no frases literales de prosa (D6)?
- [ ] ¿Existe un único helper de tolerancia, igual al ancho de precisión impreso (D7)?
- [ ] ¿El stdout que el paper cita está congelado en un test golden/snapshot (§13.4)?
- [ ] ¿Ids `test_<qué_afirma>` en snake_case y testigos que coinciden carácter a carácter (§13.5)?
- [ ] ¿Pasó code review seria (§13.1)?

### 13.7 Doctrina de refactor de succinctness

Cuando un conjunto de reglas (de este guide o de una taxonomía nueva) crezca, el refactor buscado es **densidad óptima**:

- Eliminar las **reglas intermedias** que, bajo un contexto más integrativo, serían **obvias para un modelo más grande**.
- Conservar **sólo la regla que aporta algo no deducible** de las demás.
- Consecuencia práctica: preferir **principios + criterios verificables** (auditables) frente a **listas de reglas enumeradas fruto de iteraciones pasadas**.
- Toda regla superviviente se justifica en un frente concreto (cabecera, «Sin justificaciones tontas»); si no aporta nada no deducible ni tiene frente, se elimina.

---

## 14. PIPELINE TEX Y PROOFREADING

Comandos del pipeline de la familia y reglas externas citadas; no duplica §1–§13, sólo lo que exige el tooling y el contraste con las fuentes de §14.5. Los comandos concretos, su verificación y sus artefactos viven en la documentación de cada área — **aquí no se repiten**.

### 14.1 Comandos del pipeline de familia

| Qué | Dónde está documentado |
|---|---|
| Compilar el PDF (`pnpm run build`), liberar (`pnpm run release`) y flujo diario | [`docs/usage.md`](usage.md) |
| Regenerar las figuras (`pnpm run generate:figures`) y garantías de determinismo | [`docs/figures.md`](figures.md) |
| Pipeline de citas (`citation.csl.json` → `src/bibliography.bib`, `CITATION.cff`, `.zenodo.json`) | [`docs/citations.md`](citations.md) §1–§7 |
| Requisitos e instalación (Node, pnpm, Docker, uv) | [`docs/installation.md`](installation.md) |
| Testigos, `\testref` y el censo de los tests citados | [`docs/citations.md`](citations.md) §8 (justificación en [`docs/witness-rationale.md`](witness-rationale.md)) |

- **Supresión de avisos chktex**, de menor a mayor alcance: `% chktex N` al final de la línea → `% chktex-file N` en el archivo → `--nowarn N` en `CmdLine` de `.chktexrc`. `lacheck` **no** admite supresión por aviso: no sirve como gate (fuentes en §14.5). El estado del lint de cada repo es suyo y no se afirma aquí.
- **§13 sigue siendo normativo para todo código nuevo**, con independencia del pipeline que el repo use.

### 14.2 Reglas tex con fuente externa (sólo no deducibles)

- **Entornos nuevos**: agregarse al bloque `\theoremstyle` del preámbulo compartiendo el contador — criterio verificable: `theorem` se reinicia con `[subsection]` y todo el resto declara `[theorem]`; si un entorno nuevo no comparte contador se rompe la numeración n.x.y (estilos `plain`/`definition`/`remark` documentados en Overleaf *Theorems and proofs*).
- **Párrafos en teoremas**: la línea en blanco basta; `\par` no añade nada (§5.4).
- **Conjuntos numéricos**: `\mathbb{…}` (`amsfonts`/`amssymb`); conjunto mínimo I N R Q Z; no crear macros propias `\R`/`\C` (TeX FAQ).
- **Delimitadores**: display `\[...\]`, o `equation` sólo si la ecuación se cita; inline `$...$`/`\(...\)`; `$$...$$` no está entre los delimitadores LaTeX que lista Overleaf → no usarlo.
- **Citas**: una sola fuente de metadatos de citas por repo, de la que los derivados se regeneran; en la familia es `citation.csl.json` → `src/bibliography.bib`. Reglas y criterio (toda clave citada existe en la fuente): [`docs/citations.md`](citations.md) §1 y §3, no se repiten aquí.

### 14.3 Proofreading: método (no duplica §1/§6)

1. **Orden**: primero contenido y estructura; el proofreading de superficie **al final** (UNC Writing Center).
2. **Pasadas separadas**: gramática → ortografía → puntuación → estilo/consistencia → claridad → tono; salida con tabla anotada de cambios y distinguiendo error objetivo de sugerencia subjetiva (proofreading SKILL.md).
3. **Técnicas verificables**: leer en voz alta frase a frase; leer hacia atrás desde la última frase; recuadrar cada pronombre y flechar su referente (GMU, *Editing Checklist*).
4. **Skills públicos revisados**: `anthropics/skills` **no** incluye un skill de proofreading (su README sólo lista `docx`/`pdf`/`pptx`/`xlsx`); como estándar `SKILL.md`, `easyzoom/proofreader-skill`; índice de skills académicas con categoría de peer review, `awesome-academic-skills`.

### 14.4 Checklist tex/proofreading

- [ ] ¿`pnpm run build` compila sin errores (latexmk + biber) — comandos en [`docs/usage.md`](usage.md)?
- [ ] ¿`chktex` sin avisos nuevos y cada `% chktex N` justificado en su línea?
- [ ] ¿Referencias cruzadas con los macros de §2.2, ninguna escrita a mano?
- [ ] ¿Toda clave citada existe en la fuente de citas del repo (§14.2, [`docs/citations.md`](citations.md) §3)?
- [ ] ¿Proofreading por pasadas y al final, con tabla de cambios (§14.3)?

### 14.5 Fuentes (todas recuperadas el 2026-11-16)

- Overleaf — *Theorems and proofs*: https://www.overleaf.com/learn/latex/Theorems_and_proofs
- Overleaf — *Mathematical expressions*: https://www.overleaf.com/learn/latex/Mathematical_expressions
- The TeX FAQ — *Symbols for the number sets* (Q-numbersets): https://texfaq.org/FAQ-numbersets
- TeX.SE — *Suppress lacheck error* (2014-01-22): https://tex.stackexchange.com/questions/155424/suppress-lacheck-error
- TeX.SE — *chktex warning: You ought to not use primitive TeX in LaTeX code* (2019-02-08, respuesta del mantenedor de ChkTeX): https://tex.stackexchange.com/questions/473890/chktex-warning-you-ought-to-not-use-primitive-tex-in-latex-code
- AMS/CTAN — `amsclass.dtx` (`amsart`/`amsthm`): https://mirrors.ctan.org/macros/latex/required/amscls/doc/amsclass.pdf
- UNC Writing Center — *Editing and Proofreading* (2011-12-28): https://writingcenter.unc.edu/tips-and-tools/editing-and-proofreading/
- GMU Writing Center — *Editing Checklist*: https://writingcenter.gmu.edu/writing-resources/writing-as-process/editing-checklist
- proofreading SKILL.md (MIT): https://raw.githubusercontent.com/seb1n/awesome-ai-agent-skills/main/writing-and-content/proofreading/SKILL.md
- anthropics/skills: https://github.com/anthropics/skills
- easyzoom/proofreader-skill: https://github.com/easyzoom/proofreader-skill
- O0000-code/awesome-academic-skills (CC0): https://github.com/O0000-code/awesome-academic-skills
