# STYLE GUIDE — Internal formal coherence and code quality

| Field | Value |
|---|---|
| **Document** | `docs/style-guide.md` |
| **Status** | In force |
| **Version** | 2.1 (generic family port) |
| **Date** | 2026-11-16 |
| **Language** | English |
| **Scope** | Editorial style (§1–§12) · Software and code quality (§13) · TeX pipeline and proofreading (§14) — generic to the family: free of conventions specific to any concrete repository |

**Objective**: Establish internal coherence in formal language, notation, and structure. The goal is NOT to imitate Elsevier. The goal is to be **extremely serious** without forcing matters into an artificial straitjacket.

**Framework (purpose)**:
- **Goal of the document**: maximize **auditability, best practices, and correctness**.
- **Target style**: elegant and **succinct**; succinctness is an explicit goal, not an aesthetic preference.
- **Register**: the register of this document is the one its header states. Phrasing dictated in conversation is intent to be rendered, not text to be copied; a colloquial analogy appears only beside the objective criterion it stands for, and never in place of one.
- **No justification by assertion**: every prescription carries its reason on a concrete front — mathematical, conventional, insight/characterization, or linguistic clarity; argumentative creativity is always subordinated to correctness.

**FUNDAMENTAL EDITORIAL PRINCIPLE**: This guide is **editorial**, not **authorial** — with respect to the text (§1–§12); the quality of the code that supports it is prescribed in §13. Its function is to:
- ✅ Prescribe **style, format, coherence of notation, presentation structure**
- ✅ Ensure **clarity, formal rigor, and consistency** in the writing
- ❌ **NOT** prescribe specific mathematical content (concepts, theorems, constructions)
- ❌ **NOT** add concepts that are not in the original text without explicit verification
- ❌ **NOT** make mathematical claims that require technical justification

**When a mathematical suggestion or doubt is raised**: the original document is the object under revision, not an authority for truth, so neither adoption nor dismissal rests on it. What follows instead:

- a suggestion the document does not support is not written in — and not
  dropped in silence either: it is reported, with the sentence it would
  change;
- a doubt about the document itself is reported with a reproducible check
  attached — a proof, a computation, a reference — and left to the author:
  fidelity to the original is no reason to keep an error, and it is no
  licence to correct one without evidence;
- what survives that exchange is the formal presentation, which is what
  this guide governs. Inventing mathematics is out of scope; so is hiding
  behind fidelity when a doubt has been found.

**Nature**: living document; it evolves with each revision (§10.3).

**Provenance**: port of `01-primitive-complex-field-dup/docs/style/STYLE_GUIDE.md` v2.1
(2026-11-16), the guide of the family. The port strips away what is specific to that repository (its
macros, its source document, its manuscript sites, its verified commands) and links to it
instead; the retention criterion is that of §13.7: no rule that a larger model would
deduce from the rest.

**Linked documents — each repository's own conventions are not copied here:**

| Repository-specific convention | Home |
|---|---|
| Witnesses (`\tier`, `\witness`, `\testref`): grammar, writing rules, alphabet, quantified inline criterion / own line, and the census of the cited tests | [`docs/citations.md`](citations.md) §8 |
| Rationale for the witnesses: why they exist and what they do not assert | [`docs/witness-rationale.md`](witness-rationale.md) |
| Deterministic, byte-stable figure pipeline (`pnpm run generate:figures`) | [`docs/figures.md`](figures.md) |
| Citation pipeline (`citation.csl.json` → `src/bibliography.bib`, `CITATION.cff`, `.zenodo.json`) | [`docs/citations.md`](citations.md) §1–§7 |
| Build, release, and commit convention commands | [`docs/usage.md`](usage.md) |
| Requirements and installation | [`docs/installation.md`](installation.md) |
| Concrete reports of this repo (inventories, decisions, verdicts, incidents) | [`docs/reports/`](reports/README.md) |

---

## 1. VOICE AND TONE

### 1.1 Principle
- **Formal**: No informality. Rigorously academic.
- **Direct**: Explain one thing once, well. No repetition.
- **Intellectually honest**: If it contradicts orthodoxy, say so explicitly (not hidden).
- **Non-apologetic**: the work is stated as it is, and an unusual choice
  is justified where it is made — by the problem, not by a preference.
  "Because the structure requires it" is not such a justification: it
  names nothing. The one that holds is specific: a question taken
  seriously, and read with its history, spills across areas of
  mathematics that were not separated under those names two centuries
  ago, and the zeta function and the golden ratio are questions of that
  kind by their nature. The division of the fields has ordinary reasons
  behind it — peer review and editorial work are costly, and
  specialization carries them — and this work does not argue with them.
  The context the problem brings in belongs in the paper; leaving it out
  for convenience is what would have to be apologised for.

### 1.2 Audience
- **Expert scientific audience**: The paper is aimed at scientists with advanced training in mathematics, but its multi-domain scope requires familiarity with number theory, complex analysis, Hermitian operators, quantum physics, geometry, and computational verification. The division of mathematics into fields has ordinary reasons — peer
review and editorial work are costly, and specialization carries them —
and this work does not argue against it; it follows the problem across
fields that were not separated under those names two centuries ago.
- **Do not trade clarity for the appearance of simplicity**: Do not use less clear or less concise words merely so that the text sounds less dense or less specialized. An expert audience expects and appreciates technical precision and appropriate terminology. Avoid periphrases that seek to "soften" the content at the cost of clarity.
- **Clarity over artificial simplicity**: Prefer precise, concise technical terms over unnecessary periphrases. Readability comes from structure, coherence, and precision, not from avoiding specialized terminology. The paper addresses deep mathematical problems that require a multi-domain approach; the writing must reflect this complexity without artificiality.

### 1.3 Paragraph structure
- **Topic + justification + consequence**
- No: "This is A, which is important because B, it is also C, and also D, finally E"
- Yes: "This is A. For [technical reason], this implies B and C. This differs from [orthodoxy] because [geometric/structural explanation]."

### 1.4 Avoid
- Unnecessary mechanical enumerations and bullet lists with repetitive later amplification → see **§6, patterns 1–2** (both are AI patterns)
- "Note that", "It is important to note that", "Worth mentioning that" → see **§6, pattern 3**
- Excessive parentheticals → see **§6, pattern 4**
- Repetition of the same idea with different notation

(Enumerations and bullet lists are valid when they improve clarity or structure; they are evaluated case by case, not eliminated systematically.)

### 1.5 Grammar and punctuation in Spanish

**Fundamental principle**: Rigorous mathematical writing does not justify neglecting the grammar, punctuation, or literary conventions of Spanish. Mathematical abstraction and linguistic elegance are complementary, not antagonistic.

**Common problem**: There is an artificial tendency in mathematical writing to omit prepositions, conjunctions, and other necessary grammatical elements under the false premise that "mathematical concision" requires sacrificing grammatical correctness. This practice creates ambiguity, hinders reading, and contradicts the goal of clarity and precision.

**Golden rules**:

1. **Complete sentences**: Every sentence must have a complete grammatical structure. Do not omit necessary prepositions, conjunctions, or articles.
   - ❌ "corresponde a rotación hiperbólica" (after an equation, the connection is missing)
   - ✅ "y que corresponde a rotación hiperbólica" (a conjunction connecting with the previous sentence)

2. **Necessary prepositions**: Use prepositions correctly to establish clear relations between concepts.
   - ❌ "El mapa preserva estructura algebraica mediante isomorfismo grupo de Lorentz"
   - ✅ "El mapa preserva la estructura algebraica mediante isomorfismo entre el grupo de Lorentz y..."

3. **Punctuation for clarity**: Commas, semicolons, and colons must be used according to the rules of Spanish to avoid ambiguity and facilitate reading.
   - Use commas to separate elements in enumerations
   - Use semicolons to separate related but independent clauses
   - Use colons before enumerations or explanations

4. **Connecting conjunctions**: When several related concepts or results are presented, use appropriate conjunctions ("y", "que", "donde", "mediante", etc.) to establish clear relations.

5. **Definite articles**: Do not omit articles when they are grammatically necessary for the clarity and correctness of Spanish.

6. **Reflexive passive and reflexive verbs**: When a mathematical object (representation, function, transformation, definition, construction, operator, matrix, space, metric, structure, system, operation, method, procedure, algorithm, theorem, proposition, lemma, corollary) performs an action on itself or has an inherent property, the reflexive construction "se + verb" (reflexive passive voice) must be used.
   - ❌ "La representación algebraica escribe $\mathbb{C} = ...$" (incorrect: it suggests the representation actively "writes")
   - ✅ "La representación algebraica se escribe como $\mathbb{C} = ...$" (correct: it indicates how the representation is expressed)
   - ❌ "La representación polar descompone $\mathbb{C} \cong ...$" (incorrect: it suggests active action)
   - ✅ "La representación polar se descompone como $\mathbb{C} \cong ...$" (correct: it indicates how the representation is structured)
   - ❌ "La representación euclidiana identifica $\mathbb{C} \cong ...$" (incorrect: the representation is not an agent that "identifies")
   - ✅ "En la representación euclidiana, $\mathbb{C}$ se identifica con ..." (correct: it indicates how the identification is established)
   - ❌ "La función define..." (when the function is the object being defined)
   - ✅ "La función se define como..." (when the function is being defined)
   - ❌ "La transformación preserva..." (it can be correct if the transformation is the active subject)
   - ✅ "La transformación se preserva bajo..." (when speaking of a property that is maintained)

   **Practical rule**: If the mathematical object is the **subject of the sentence** and the action describes **how that object is expressed, structured, defined, or characterized**, use "se + verb". If the object is the **active agent** performing an action on another object, use the verb without "se".

   **Avoid constructions in which mathematical objects are subjects of transitive verbs suggesting active action**: When a mathematical object cannot be an active agent (such as "representación", "definición", "construcción"), avoid using it as the subject of transitive verbs such as "identifica", "define", "construye", etc. Instead, use constructions such as "En X, Y se identifica con...", "Mediante X, Y se define como...", or "X establece la identificación/definición de...".

   **Common verbs requiring "se" in mathematical contexts**:
   - `se escribe`, `se define`, `se descompone`, `se caracteriza`, `se parametriza`, `se clasifica`, `se identifica`, `se representa`, `se expresa`, `se formula`, `se construye`, `se establece`, `se determina`, `se calcula`, `se evalúa`, `se resuelve`, `se aplica`, `se utiliza`, `se emplea`, `se preserva` (when it is a property), `se mantiene`, `se conserva`, `se genera`, `se produce`, `se obtiene`, `se resulta`, `se aparece`, `se surge`, `se emerge`, `se muestra`, `se revela`, `se establece`

**Justification**: Mathematical precision and grammatical correctness reinforce each other: a grammatically correct sentence eliminates interpretive ambiguities, and the reflexive passive is required in Spanish to express inherent properties and mathematical structures; omitting it yields ungrammatical constructions.

**Improvement example**:
- ❌ "La transformación preserva estructura, métrica, simetrías mediante isomorfismo grupo Lorentz corresponde rotación hiperbólica"
- ✅ "La transformación preserva la estructura, la métrica y las simetrías mediante un isomorfismo entre el grupo de Lorentz y las transformaciones conformes, y que corresponde a una rotación hiperbólica"

---

## 2. UNIFIED NOTATION

### 2.1 Notation Macros (declared in each repo's preamble)

**Principle**: Use macros only for document-specific notation that:
- Is frequently repeated
- Is complex or long to write
- Could change or require global adjustments

**Available macros**: those declared by the preamble of the repository itself. This
document does not list them — they are that document's notation, not the family's; the source is its
root `.tex` and its preamble.

**Standard notation (do NOT use macros):**
- ✅ Use `\mathbb{C}`, `\mathbb{R}`, `\mathbb{Z}`, `\mathbb{Q}`, `\mathbb{N}` directly (standard, well known)
- ✅ Use `\varphi` directly for the golden ratio (standard)
- ✅ Use `\mathcal{C}`, `\mathcal{H}`, etc. directly (standard)

**Reason**: Macros for standard notation add unnecessary complexity with no real benefit. They only make sense for document-specific notation that repeats a great deal.

### 2.2 Cross-Reference Macros (declared in each repo's preamble)

For consistent references to mathematical constructions, each repo declares **one macro
per construction type** —`\tref` → "Theorem X.Y.Z", `\dref` → "Definition X.Y.Z",
`\pref` → "Proposition X.Y.Z", `\lref`, `\cref`, `\oref`, `\corref`, `\conjref`
analogues — **or** loads the `cleveref` package, which covers them with `\cref`, `\autoref`, and
`\eqref`. The concrete list of a repo is its own; only the use is prescribed here.

**Caution**: if the preamble defines its own reference macros using the names of
`cleveref` (`\cref` among them), do not load `cleveref` —nor copy code that uses it—
without renaming those macros first: the package and the in-house macro collide on the same
name.

**Recommended usage:**
- ✅ Use these macros instead of manually writing "Theorem~\ref{...}"
- ✅ Example: `As shown in \pref{prop:<label>}...` instead of `As shown in Proposition~\ref{prop:<label>}...`
- ✅ This ensures consistent formatting and facilitates global changes

### 2.3 Complex numbers
- **Modulus**: always `|z|` in algebraic contexts, "magnitude" in geometric contexts
- **Complex variable**: `z = x + iy` at first definition, then just `z`
- **Euler**: `e^{i\theta}` (no `e^{i\theta}` variants)

### 2.4 Spaces
- **Complex plane**: `ℂ` (use `\mathbb{C}`)
- **Real numbers**: `ℝ` (use `\mathbb{R}`)
- **Integers**: `ℤ` (use `\mathbb{Z}`)
- **Hilbert**: `ℋ` or `H` (CHOOSE ONE per section and keep it)
- **Sobolev/L² spaces**: `L²(domain)` - be explicit about the domain

### 2.5 Operators
- **Document-specific operator**: if it repeats a great deal and its name is long, declare a macro for it in the preamble and always use it; a standard operator never takes a macro (§2.1)
- **Fourier**: `ℱ` (use `\mathcal{F}`)
- **Integral**: always `∫_X f(x) dx` with clear limits

### 2.6 Golden ratio
- **Symbol**: φ (use `\varphi`, not variants)
- **Value**: φ ≈ 1.618... (if a numeric value is needed) or just φ (algebraic)
- **Powers**: `φ^σ` or `φ^n` - be consistent with the index

### 2.7 Sets/indexing
- **Discrete indices**: `k, n, m ∈ ℤ` or `σ ∈ ℤ`
- **Continuous parameters**: `t ∈ ℝ`, `θ ∈ [0, 2π)`
- **Sequences**: `{a_n}_{n∈ℕ}` or just `{a_n}` if the context is clear

---

## 3. STRUCTURE OF DEFINITIONS

### 3.1 Standard format
```
\begin{definition}[Descriptive name]
[CONCISE STATEMENT IN ONE SENTENCE]

For [elements at play], [fundamental property]:
\[
[main formula]
\]

[CONTEXT/MEANING: at most 1-2 paragraphs explaining what it means, why it matters, how it relates to the preceding material]
\end{definition}
```

### 3.2 GOOD example
```
\begin{definition}[Modulus in the complex plane]
For $z = x + iy \in \mathbb{C}$ with $x, y \in \mathbb{R}$, the modulus is the Euclidean norm:
\[
|z| := \sqrt{x^2 + y^2}
\]
Geometrically, $|z|$ is the distance from the point $z$ to the origin. This magnitude inherits the properties of the Euclidean norm on $\mathbb{R}^2$, including the triangle inequality: $|z_1 + z_2| \leq |z_1| + |z_2|$.
\end{definition}
```

### 3.3 BAD example
```
\begin{definition}[Modulus]
The modulus is defined as...
\textbf{Properties:}
\begin{itemize}
\item It is always positive
\item It satisfies the triangle inequality
\item It is invariant under rotation
\item Etc.
\end{itemize}
[Additional explanation that repeats the properties]
\end{definition}
```

**Why**: The bad one has 3 problems:
1. It repeats content ("It is positive" → "properties" → explanation)
2. It does not explain the MEANING of the modulus, it only lists attributes without context
3. The enumeration adds no clarity because it only repeats what the later explanation already says

**Note**: An enumeration would be valid if it organized technical information clearly and added structural value, not if it merely repeated what is already stated afterwards.

---

## 4. EQUATIONS AND FORMULAS

### 4.1 Rule: **Equation ↔ Text**
Every formula must be integrated with text, never isolated.

#### 4.1.1 BAD
```
The operator is defined as:
\[
\hat{\Omega} = \begin{pmatrix} a & b \\ c & d \end{pmatrix}
\]
```

#### 4.1.2 GOOD
```
The operator $\hat{\Omega}$ is a linear transformation represented in the standard basis as:
\[
\hat{\Omega} = \begin{pmatrix} a & b \\ c & d \end{pmatrix}
\]
where $a, b, c, d$ are coefficients satisfying [property]. This diagonal form reveals that $\hat{\Omega}$ acts as [geometric interpretation].
```

### 4.2 Explicit declaration of symbols
If an equation introduces new variables, declare them INSIDE or IMMEDIATELY AFTER:

```
The coupling relation is given by:
\[
z = \varphi y
\]
where $z$ denotes the vertical coordinate, $y$ the horizontal imaginary coordinate, and $\varphi$ is the golden ratio.
```

### 4.3 Alignment and spacing
- **Short equations (<60 characters)**: `\[...\]` (displaymath)
- **Long or multiple equations**: `\begin{align*}...\end{align*}`
- **Between equations**: a transition paragraph, not blank lines + equation

---

## 5. PROPOSITIONS, THEOREMS, COROLLARIES

### 5.1 Structure
```
\begin{theorem}[Descriptive name]\label{thm:...}
[FORMAL STATEMENT IN ONE OR TWO LINES]

If [hypothesis], then [conclusion]:
\[
[concise formula]
\]
\begin{proof}
[Main argument in prose, logically structured]
[If there are key algebraic steps, show ONE or TWO]
[Conclusion: "Therefore, [theorem's conclusion]"]
\end{proof}
\end{theorem}
```

### 5.2 Difference: Theorem vs Proposition vs Lemma
- **Theorem**: The MAIN result. It can change an entire perspective.
- **Proposition**: An IMPORTANT but subordinate result. A tool for theorems.
- **Lemma**: A necessary TECHNICAL result. It is not interesting in its own right.

If it is not clear which one it is, err toward **Proposition** (the most flexible).

### 5.3 Observation vs Remark
- **Observation** (*Observación*): a geometric or structural insight that arises NATURALLY from the theorem.
- **Remark** (*Nota*): a technical clarification or context about notation/convention.

### 5.4 Paragraphs inside theorem environments

**Verified (2026-11-16)**: a blank line in the source **does** produce a new paragraph inside `theorem`, `proposition`, `definition`, `corollary` (amsthm + the document class + its `\parskip`). The premise that previously headed this section ("the `amsthm` environments do not show the break even with blank lines") is **false** in the family's pipeline and was removed; the evidence is the built PDF of each repo, not a rule here.

- ✅ Separate the paragraphs of the statement with a **blank line** (LaTeX convention).
- ❌ explicit `\par`: it is exactly what the blank line does; it adds nothing and is redundant today.
- **Practical rule**: a statement of more than 3-4 sentences or covering several concepts is split into paragraphs with a blank line.

**Avoid**: a theorem body written as a single long line of source: it becomes unreadable in the source even if the PDF comes out fine.

### 5.5 Enumeration in proposition/theorem statements

**Rule for statements**:
- ✅ **Use enumeration** when there are multiple related results that are proven together but are conceptually distinct:
  ```
  \begin{proposition}[...]
  As $\sigma \to \sigma+1$ increases:
  \begin{enumerate}
  \item $\varepsilon(\sigma+1) = \varphi \cdot \varepsilon(\sigma)$
  \item $|z|_{\sigma+1} = \varphi |z|_\sigma$
  \end{enumerate}
  \end{proposition}
  ```
- ❌ **Avoid enumeration** when the results can be expressed fluently in one or two sentences:
  ```
  ❌ "The operator has three properties: (1) It is Hermitian, (2) It has real spectrum, (3) It generates an orthogonal decomposition"
  ✅ "The operator is Hermitian, has real spectrum and generates an orthogonal decomposition."
  ```

**Rule for proofs**:
- ✅ **Concise proof**: a fluent paragraph that connects the steps logically, using references to the enumeration where it applies:
  ```
  \begin{proof}[By <method>]
  By [theorem], [step 1]. From [definition], [step 2] implies (1). [Conclusion] establishes (2).
  \end{proof}
  ```
- ❌ **Avoid**: multiple paragraphs with `\par` unless each paragraph treats a completely different concept. A proof must not be a list of separated steps.
- ✅ **Balance**: the proof must be complete enough to be rigorous, but not so verbose that it repeats information from the statement or is artificially long.

**Decision criterion**: if, upon reading the enumerated statement, it is immediately clear what is being asserted, and the proof can refer to the numbered points naturally, use enumeration. If the enumeration only adds artificial structure without improving clarity, use running text.

### 5.6 Stylistic balance: philosophical rigor without artificial redundancy

**Tension between two extremes**: (1) extreme artificial condensation in the Elsevier style that sacrifices conceptual clarity, and (2) excessive verbosity that repeats information without adding value.

**Criterion**: the text should flow like a conversation between scientists who respect each other: enough context to understand the deep meaning (the "why" and the significance, in the manner of a nineteenth-century scientific letter), but without repeating the obvious until an expert reader thinks "I already understood that, move on".

**Principles of the balance**:
- ✅ **Explain the meaning**: include sentences that explain why something matters or what it means conceptually (e.g., "This simultaneity arises from the need to preserve...")
- ✅ **Philosophical naturalness**: use language that reflects deep mathematical thought, not just the mechanics (e.g., "Geometric coherence demands..." instead of merely "Therefore...")
- ❌ **Avoid redundancy**: do not repeat in the proof what was already established in the statement. If the statement says "preserve the geometric structure under scale transformations", the proof can simply refer to "geometric coherence" without repeating the whole phrase.
- ❌ **Avoid artificial condensation**: do not delete necessary words just to sound "more technical". Prefer "The temporal coupling establishes:" over "From the temporal coupling:" when the first form is clearer.
- ✅ **DRY in concepts, not in explanation**: do not repeat concepts, but do explain the meaning when it adds conceptual value.

**Example of good balance**:
```
\begin{proposition}[Simultaneous scaling of the scale parameter and the complex modulus]
The self-similar structure of the system establishes that as $\sigma \to \sigma+1$:
\begin{enumerate}
\item $\varepsilon(\sigma+1) = \varphi \cdot \varepsilon(\sigma)$
\item $|z|_{\sigma+1} = \varphi |z|_\sigma$
\end{enumerate}
This simultaneity arises from the need to preserve the geometric structure...
\end{proposition}

\begin{proof}[By direct calculation]
The temporal coupling establishes: [equation]
From the definition of the operator: [equation]
the scaling of the phase requires (1).
Geometric coherence demands (2), completing the proof.
\end{proof}
```

**Contrast with the extremes**:
- ❌ **Too condensed**: "From the temporal coupling, $\varepsilon(\sigma+1) = \varphi\varepsilon(\sigma)$ and $|z|_{\sigma+1} = \varphi|z|_\sigma$." (It loses conceptual meaning)
- ❌ **Too verbose**: repeating "preserve the geometric structure under scale transformations" in both the statement and the proof (Redundant)

---

## 6. AVOIDING AI PATTERNS

### 6.1 Pattern 1: unnecessary repetitive enumeration
❌ "This concept has several properties. First, A. Second, B. Third, C. These properties imply that..." (when the enumeration adds no clarity)

✅ "This concept has three distinguished properties: A implies X, B implies Y, C implies Z. Together, this means that..."

**Note**: Structured enumerations (with `\textbf{}` or lists) are valid when they improve clarity, organization, or readability. They must not be eliminated systematically; they must be evaluated case by case according to their usefulness.

### 6.2 Pattern 2: bullet list + repetitive amplification
❌
```
The operator has the following characteristics:
• It is Hermitian
• It has real spectrum
• It generates an orthogonal decomposition

The Hermiticity of the operator means that...
The real spectrum implies that...
```
(when the amplification repeats exactly what the list already says)

✅
```
The operator is Hermitian, ensuring real spectrum and generating an orthogonal decomposition of $\mathcal{H}$. The Hermiticity arises from [justification]. The real spectrum is a consequence of [construction].
```

**Note**: Bullet lists are appropriate when they organize technical information clearly and the subsequent amplification adds context or justification, not repetition.

### 6.3 Pattern 3: "Note that", "It is important to note that"
❌ "Note that this implies that..."
✅ "Therefore..." or "This implies..." or nothing (let the logic be clear)

### 6.4 Pattern 4: excessive parentheticals
❌ "The operator (which we defined earlier) has (as we mentioned) the (important) property of..."
✅ "The operator has the property of..." [and use \ref{} if you need to refer to a previous definition]

### 6.5 Pattern 5: AI artifacts in code (→ §13)
AI-generated artifacts also appear in **code** —monolithic modules, self-testing, stdout as API, logging via `append` with import side effects, hand-rolled CLI, prose-sentence asserts, per-site tolerances— with the same shape as patterns 1–4: repetition disguised as utility and shortcuts that delegate work to whoever reads next. Their nomenclature (**D1–D7**), the remediation with standard libraries, and the corresponding checklist are in **§13**; they are not duplicated here.

---

## 7. SECTION-TO-SECTION COHERENCE

### 7.1 Within a section
- **First definition**: introduce complete notation, be explicit
- **Later definitions**: reuse notation, do not re-declare it
- **Transitions**: "Now consider...", "The next step...", "To understand [previous result]..."

### 7.2 Between sections
- **Cross-references**: use the macros of §2.2 (`\tref{...}`, `\dref{...}`, `\pref{...}`…), not "in the previous section" nor a hand-written `Proposition~\ref{...}`
- **Notation**: if you change it (e.g., from real to complex), explain the transition
- **Assumptions**: if a section assumes a result from a previous one, mention it explicitly

---

## 8. CHECKLISTS BY ENVIRONMENT TYPE

### 8.1 For each DEFINITION
- [ ] Concise statement? (max 2 lines)
- [ ] Clear main formula?
- [ ] Context/meaning explained in 1-2 paragraphs?
- [ ] What problem does it solve or what intuition does it clarify?
- [ ] Zero bullet lists?

### 8.2 For each THEOREM/PROPOSITION
- [ ] Clear hypothesis and conclusion?
- [ ] Is the proof an argument (not a list of steps)?
- [ ] Explicit connection to a previous result?
- [ ] Descriptive label?

### 8.3 For each PROOF
- [ ] Does the introductory paragraph explain the strategy?
- [ ] Main steps in prose (not numbered)?
- [ ] Do the equations show, not prove?
- [ ] Is the conclusion "Therefore..." clear?

(The code checklist is in §13.6.)

---

## 9. SPECIAL CASES: CONTRADICTING ORTHODOXY

A conflict with a convention or with the literature is justified by what
the paper derives, never by announcing a reason for it. "The geometric
structure requires it" is not such a reason when it is quoted as the
premise: it is the conclusion, and the sentence that uses it as a premise
is circular - the excuse the section used to license.

Four things carry the claim, in this order:

1. **The convention, quoted and cited.** What is contradicted, in the form
   its source states it, with the reference. Contradicting a paraphrase of
   a convention is not contradicting the convention.
2. **The point of conflict**, shown rather than summarised: the step, the
   formula, or the number where the two disagree.
3. **The class of the conflict**: genuine · different hypotheses or
   definitions · notation only · an error in the source. Only the first is
   a contradiction; the others are labelled as they are, because presenting
   a difference of hypotheses as a conflict misleads the reader about what
   is at stake. If the check dissolves the conflict, the text says so at
   the place where it raised it.
4. **The derivation that resolves it.** The reconciling interpretation and
   the structural reason are results of the paper: they appear with their
   argument, so the reader can follow them from what precedes. A closing
   clause that asserts them asserts nothing.

**Form**: the convention and its citation, the conflict and its evidence,
what the paper derives instead, and what would show the paper wrong - at
the place where the reader meets the conflict, not in a disclaimer and
not in a footnote.

**Do not hide it. Do not apologize.** The hedging formula and the
triumphant one are the same failure in opposite directions: both replace
the evidence with a posture. State what contradicts, what does not, and
why, in the order above.

---

## 10. APPLICATION OF THE GUIDE

### 10.1 Template: Section I

Section I must serve as the pattern. Once it is perfect:
- Every definition follows the standard structure
- Every paragraph is necessary (no repetition)
- Notation is consistent
- The voice is formal, serious, clear
- There are NO unjustified bullet lists

Then, the other sections must **match exactly** in style.

### 10.2 Usage procedure

1. **Before reviewing a section**: read this guide
2. **While reviewing**: compare against the checklists (§8 for text, §14.4 for pipeline/proofreading, §13.6 for code)
3. **If you find a section that does NOT comply**: ask "Which rule was broken?" → then fix it
4. **When you find a NEW guideline** (repeated pattern, inconsistency): add it to the guide
5. **Content verification**: before adding new mathematical concepts, verify them against the repository's original source document (full rule in the Editorial principle of the header). If it is not grounded, remain faithful to the original.

**Example of rule 5**: a formalization suggestion that introduces "kernel modular K(z,w)" when the original only mentions "kernel" or "kernel PCF" must first be reviewed to see whether it is justified; in case of doubt, keep the original text and only improve the formal presentation.

### 10.3 Maintenance cycle

1. Apply this guide fully to **Section I (Introduction)**
2. Validate that it stands as the template
3. Replicate in Sections II and III
4. Adjust the guide as we learn

**Final goal**: a paper that is **rigorous, clear, serious, without artificiality** and genuinely readable for its expert scientific audience, trained in number theory, complex analysis, Hermitian operators, quantum physics, geometry, and computational verification, among others.

---

## 11. PROACTIVE DETECTION OF INCONSISTENCIES AND EDITORIAL SUGGESTIONS

### 11.1 Principle
The AI should act as a proactive editor: detect mathematical, logical, or stylistic inconsistencies, even when they are not explicitly requested in the prompt.

### 11.2 Detection Protocol

**During the task**, flag any of:
- Mathematical inconsistency (contradiction, inconsistent notation, undefined concept)
- A strong "feeling" that something is worth editing (ambiguity, lack of clarity, possible error)
- Disconnection between the text and the mathematical content developed

**At task completion (before committing, if applicable):**

1. **Assess the intensity of the feeling:**
   - **Strong**: clear inconsistency, possible mathematical error, logical contradiction
   - **Moderate**: ambiguity, lack of clarity, possible improvement
   - **Weak**: minor suggestion, stylistic optimization

2. **If the feeling is STRONG or MODERATE:** present the suggestion to the user at the end of the task, with a detailed analysis:
   - **What you detected**: specific description of the inconsistency/suggestion
   - **Where it is**: exact location (file, lines, section)
   - **Why it is relevant**: potential impact (mathematical, logical, stylistic)
   - **Cognitive context**: what made you think there is a problem (pattern, contradiction, missing definition, etc.)
   - **Options**: what could be done (correct, verify against the original, investigate further)

3. **If the prompt includes committing at the end:**
   - **BEFORE running the commit**, present the detected suggestions
   - Give the user an explicit choice: review and decide on the suggestions first · proceed with the commit anyway · modify the commit to include corrections

### 11.3 Presentation Format

```
---
🔍 **EDITORIAL SUGGESTION DETECTED**

**Type**: [Mathematical inconsistency / Ambiguity / Possible error / Suggested improvement]
**Severity**: [Strong / Moderate]
**Location**: [file:lines]

**What I detected**: [Specific description of the problem]

**Cognitive analysis**: 
- [Which pattern/contradiction/missing definition made you think there is a problem]
- [Why it is relevant mathematically/logically]
- [What impact it could have if it is not corrected]

**Options**:
1. [Option 1: suggested action]
2. [Option 2: alternative]
3. [Option 3: investigate further before deciding]

Would you like me to proceed with the commit, or would you prefer to review this first?
---
```

### 11.4 Examples

1. **Mathematical inconsistency**: a concept is named one way in a section and another way in the development (terminological disconnect) → verify whether it is grounded or an unjustified addition.
2. **Missing definition**: a new symbol is used without a prior definition → the reader cannot follow the argument → add a definition or cross-reference.
3. **Logical contradiction**: X is asserted in one section and not-X in another → it breaks the coherence of the argument → verify which assertion is correct according to the original document.

### 11.5 Limits
- **Do NOT** interrupt the main workflow with minor suggestions
- **Do NOT** make changes without consulting when the feeling is strong
- **DO** present suggestions at the end, before committing
- **DO** be specific and detailed in the analysis

---

## 12. COMPARING THE SOURCE DOCUMENT WITH THE MANUSCRIPT

### 12.1 ⚠️ CRITICAL RULE: DO NOT EDIT THE ORIGINAL SOURCE DOCUMENT

**The original source document that the repository received must not be modified.** All corrections, improvements, and updates must be made ONLY in the repo's `.tex` (the root file and the `.tex` files it includes).

- ✅ **YES**: edit the repo's `.tex` to correct terminology, improve presentation, etc.
- ❌ **NO**: edit the original source document under any circumstances
- ✅ **YES**: use it as a reference to verify the original content
- ✅ **YES**: compare it with the repo's `.tex` to detect inconsistencies

### 12.2 Purpose
When the user provides a section reference (a number such as "1.5" or a descriptive string such as `fundamento y alcance del presente trabajo`), generate a concise report of differences between the source version and the corresponding version of the LaTeX manuscript.

### 12.3 Search Protocol

**Step 1: Interpret the reference**
- If it is a number (e.g., "1.5", "2.3", "8.1.5"): search for section titles containing that number
- If it is a descriptive string (e.g., `fundamento y alcance`, `coherencia de axiomas`): search for titles or content containing those keywords

**Step 2: Search in the source document**
- Search for the pattern in section titles (e.g., `### 1.5`, `#### 2.3.1`)
- Extract the full content of the section (including following paragraphs up to the next section or subsection)

**Step 3: Search in the LaTeX manuscript**
- Search across all `.tex` files in the repository
- Search for equivalent titles (e.g., `\subsection{...}`, `\subsubsection{...}`) or content corresponding to the same section
- Extract the corresponding full content

**Step 4: Compare and generate the report**

### 12.4 Report Format

The report must be **very concise** and include:

1. **Location**: exact lines and titles in both documents
2. **Main changes**: a short list of structural and content differences
3. **Summary**: a synthesis of whether the conceptual content is equivalent or whether there are substantial differences

**Report structure:**
```
## Comparison Report: Section [reference]

### Location
- **Source document**: lines X-Y (title: `...`)
- **Manuscript `.tex` (file)**: lines X-Y (title: `...`)

### Main changes
Short list of structural and content differences, including:

**A. Content/concept differences:**
1. [Terminological, conceptual, or informational difference]

**B. Style/structure differences:**
1. [Repetition of structures, lack of parallelism, vague verbs, etc. - see §1 (Avoid) and §6]
2. [Flow, clarity, or presentation problems]

**C. Format differences (only if they affect meaning):**
1. [Different mathematical notation, references, etc.]

### Summary
[Brief synthesis of conceptual equivalence or substantial differences, including correction recommendations if there are style problems]
```

### 12.5 Examples of Valid References

- Section numbers: `1.5`, `2.3`, `8.1.5`, `III.1.5`
- Descriptive strings: `fundamento y alcance`, `coherencia de axiomas`, `verificación computacional`
- Mixed references: `§1.5`, `Sección 1.5`

### 12.6 Important Notes

- **Search both documents**: always compare the source with the manuscript, not just one of them
- **Repo tools** (they replace hand search): when a repo ships comparison scripts —source `§X.Y` references missing in the `.tex`, `§` → LaTeX labels, source vs. PDF numbering— use those; the script inventory belongs to each repo and is not listed here
- **Enough context**: include enough context (preceding/following paragraphs) to identify the correct section
- **Different format**: remember that the source may use Markdown while the manuscript uses LaTeX - format differences (mathematical notation, references) are expected and must not be treated as content differences unless they change the meaning
- **Concision**: the report must be brief and direct, focusing on substantial content differences, not on minor format differences

---

## 13. SOFTWARE AND CODE QUALITY

Sections §1–§12 prescribe the quality of the **text**. This section prescribes the quality of the **code** that produces it, verifies it, and supports it (scripts, tests, supporting modules). It is mandatory in any code review of the repository, regardless of who wrote it.

### 13.1 Doctrine

- **No hand-rolled implementation where a library covers the need.** For
  any functional need, the standard library or a maintained library of the
  ecosystem is used. A hand-written implementation is admissible only
  where no maintained library provides the behaviour, and it then carries
  tests against the contract that library would have offered. The choice is
  recorded where the code is read: library, version, and the reason it
  covers the need. Provenance is not the criterion — that an
  implementation was inherited does not keep it, and that a need is new
  does not license reinventing it.
- **Standard library first.** The table §13.3 is normative: `argparse` for CLI, `logging` for logging, `dataclasses` for data, `numpy.testing` for numerical verification, `pytest` for tests.
- **Serious code review.** No module is incorporated without explicit code review —structure, contracts, tests, naming—; the review is neither a formality nor a mere procedure.
- **The production module never tests itself.** Asserts live in the suite, never in the code that runs (defect **D2**).

### 13.2 Defect taxonomy (D1–D7)

Stable nomenclature, citable in audits (e.g., "D4 ×47"):

- **D1 — Monolithic module**: a single file mixing data, logic, and presentation with no internal boundaries; changing one thing forces touching everything.
- **D2 — Self-testing**: validation asserts inside production code; the module tests itself.
- **D3 — Printing API / tests that parse stdout**: the interface returns text by printing and the tests parse it instead of receiving values.
- **D4 — Logging via `append` with import side effects**: the log is filled with repeated `SECCIONES.append((46, '…', fn))` (e.g., ×47), so merely importing the module already has effects on global state.
- **D5 — Hand-rolled CLI and `print` as log**: direct use of `sys.argv` without `argparse`, and `print` instead of `logging`.
- **D6 — Asserts on literal prose sentences**: e.g., `assert "rel. 6.1e-05" in run.stdout`; the test asserts a string, not a value, and breaks on any reflow of the text.
- **D7 — Ad hoc tolerances written per site**: every numerical comparison drags along its own literal tolerance, with no single source defining the precision.

### 13.3 Self-baked → standard

| Self-baked (defect) | Mandatory standard |
|---|---|
| Internal `assert`s in production code (D2) | `numpy.testing` — `assert_allclose` with explicit `rtol` and failure message; input preconditions with `raise`. What is a test goes to **`pytest`**. |
| Printing API and tests that parse stdout (D3) | **`dataclasses`** returning objects; **`syrupy`** / **`pytest-snapshot`** only for the stdout contract the paper cites (§13.4) |
| Logging via `append` with import effects (D4) | Declarative map or `@section(n, title)` decorator; never `append` scattered through the file |
| Hand-rolled CLI with `sys.argv` and `print` as log (D5) | **`argparse`** for CLI; **`logging`** for logging; the report is rendered from structured data, not from printed strings |
| Hand-written numerical verification and per-site tolerances (D6, D7) | **`numpy.testing`** + a **single tolerance helper**, whose value is the width of the precision the document prints |

**In addition**: randomized invariants → **`hypothesis`**, where it provides real coverage.

### 13.4 Output contract

If the document **cites what a script prints** (a figure, a ratio, an output line), that stdout is frozen with a **golden/snapshot test** (`syrupy` or `pytest-snapshot`): the test fails if the cited output changes. Everything else moves to asserting **values**, never strings — this eliminates D6 by construction.

### 13.5 Naming of tests and witnesses

- **Test ids**: `test_<qué_afirma>` in snake_case, tied to the claim they verify (not to the file they run).
- **Internal witnesses** (`\tier`, `\witness`, `\testref`, and the census of the cited ids): their grammar, writing rules, and alphabet are each repo's convention and **are not copied here** — contract in [`docs/citations.md`](citations.md) §8, rationale in [`docs/witness-rationale.md`](witness-rationale.md). Only the principle is stated: the witness's name matches **character by character** with the `.lean` file or the suite that declares it; any deviation is a defect.

### 13.6 Code quality checklist

- [ ] Is the standard library used instead of self-baked code (§13.3)?
- [ ] Zero asserts inside the production module (D2)?
- [ ] Does the API return data (`dataclasses`) and not printed text (D3)?
- [ ] Is the logging declarative, with no import side effects (D4)?
- [ ] CLI with `argparse` and log with `logging`, report rendered from data (D5)?
- [ ] Do the tests assert values, not literal prose sentences (D6)?
- [ ] Is there a single tolerance helper, equal to the printed precision width (D7)?
- [ ] Is the stdout cited by the paper frozen in a golden/snapshot test (§13.4)?
- [ ] Ids `test_<qué_afirma>` in snake_case and witnesses matching character by character (§13.5)?
- [ ] Did it pass serious code review (§13.1)?

### 13.7 Succinctness refactor doctrine

When a set of rules (from this guide or a new taxonomy) grows, the sought refactor is **optimal density**:

- Remove the **intermediate rules** that, under a more integrative context, would be **obvious to a larger model**.
- Keep **only the rule that contributes something not deducible** from the others.
- Practical consequence: prefer **principles + verifiable (auditable) criteria** over **enumerated rule lists resulting from past iterations**.
- Every surviving rule is justified on a concrete front (header, "No justification by assertion"); if it contributes nothing non-deductive and has no front, it is removed.

---

## 14. TEX PIPELINE AND PROOFREADING

Commands of the family's pipeline and cited external rules; it does not duplicate §1–§13, only what the tooling requires and the contrast with the sources of §14.5. The concrete commands, their verification, and their artifacts live in each area's documentation — **they are not repeated here**.

### 14.1 Family pipeline commands

| What | Where it is documented |
|---|---|
| Compile the PDF (`pnpm run build`), release (`pnpm run release`), and daily workflow | [`docs/usage.md`](usage.md) |
| Regenerate the figures (`pnpm run generate:figures`) and determinism guarantees | [`docs/figures.md`](figures.md) |
| Citation pipeline (`citation.csl.json` → `src/bibliography.bib`, `CITATION.cff`, `.zenodo.json`) | [`docs/citations.md`](citations.md) §1–§7 |
| Requirements and installation (Node, pnpm, Docker, uv) | [`docs/installation.md`](installation.md) |
| Witnesses, `\testref`, and the census of the cited tests | [`docs/citations.md`](citations.md) §8 (rationale in [`docs/witness-rationale.md`](witness-rationale.md)) |

- **Suppression of chktex warnings**, from narrowest to broadest scope: `% chktex N` at the end of the line → `% chktex-file N` in the file → `--nowarn N` in `CmdLine` of `.chktexrc`. `lacheck` does **not** support per-warning suppression: it does not work as a gate (sources in §14.5). The lint status of each repo is its own and is not asserted here.
- **§13 remains normative for all new code**, regardless of the pipeline the repo uses.

### 14.2 TeX rules with external sources (only non-deductive ones)

- **New environments**: they are added to the preamble's `\theoremstyle` block sharing the counter — verifiable criterion: `theorem` is reset with `[subsection]` and everything else declares `[theorem]`; if a new environment does not share the counter, the n.x.y numbering breaks (styles `plain`/`definition`/`remark` documented in Overleaf *Theorems and proofs*).
- **Paragraphs in theorems**: a blank line suffices; `\par` adds nothing (§5.4).
- **Numeric sets**: `\mathbb{…}` (`amsfonts`/`amssymb`); minimal set I N R Q Z; do not create your own `\R`/`\C` macros (TeX FAQ).
- **Delimiters**: display `\[...\]`, or `equation` only if the equation is cited; inline `$...$`/`\(...\)`; `$$...$$` is not among the LaTeX delimiters listed by Overleaf → do not use it.
- **Citations**: a single source of citation metadata per repo, from which the derived files are regenerated; in the family it is `citation.csl.json` → `src/bibliography.bib`. Rules and criterion (every cited key exists in the source): [`docs/citations.md`](citations.md) §1 and §3, not repeated here.

### 14.3 Proofreading: method (does not duplicate §1/§6)

1. **Order**: content and structure first; surface proofreading **last** (UNC Writing Center).
2. **Separate passes**: grammar → spelling → punctuation → style/consistency → clarity → tone; output with an annotated table of changes, distinguishing objective errors from subjective suggestions (proofreading SKILL.md).
3. **Verifiable techniques**: read aloud sentence by sentence; read backwards from the last sentence; box every pronoun and arrow its referent (GMU, *Editing Checklist*).
4. **Reviewed public skills**: `anthropics/skills` does **not** include a proofreading skill (its README only lists `docx`/`pdf`/`pptx`/`xlsx`); as a `SKILL.md` standard, `easyzoom/proofreader-skill`; index of academic skills with a peer-review category, `awesome-academic-skills`.

### 14.4 TeX/proofreading checklist

- [ ] Does `pnpm run build` compile without errors (latexmk + biber) — commands in [`docs/usage.md`](usage.md)?
- [ ] Is `chktex` free of new warnings and is each `% chktex N` justified on its line?
- [ ] Cross-references using the macros of §2.2, none written by hand?
- [ ] Does every cited key exist in the repo's citation source (§14.2, [`docs/citations.md`](citations.md) §3)?
- [ ] Proofreading done in passes and at the end, with a table of changes (§14.3)?

### 14.5 Sources (all retrieved on 2026-11-16)

- Overleaf — *Theorems and proofs*: https://www.overleaf.com/learn/latex/Theorems_and_proofs
- Overleaf — *Mathematical expressions*: https://www.overleaf.com/learn/latex/Mathematical_expressions
- The TeX FAQ — *Symbols for the number sets* (Q-numbersets): https://texfaq.org/FAQ-numbersets
- TeX.SE — *Suppress lacheck error* (2014-01-22): https://tex.stackexchange.com/questions/155424/suppress-lacheck-error
- TeX.SE — *chktex warning: You ought to not use primitive TeX in LaTeX code* (2019-02-08, answer from the ChkTeX maintainer): https://tex.stackexchange.com/questions/473890/chktex-warning-you-ought-to-not-use-primitive-tex-in-latex-code
- AMS/CTAN — `amsclass.dtx` (`amsart`/`amsthm`): https://mirrors.ctan.org/macros/latex/required/amscls/doc/amsclass.pdf
- UNC Writing Center — *Editing and Proofreading* (2011-12-28): https://writingcenter.unc.edu/tips-and-tools/editing-and-proofreading/
- GMU Writing Center — *Editing Checklist*: https://writingcenter.gmu.edu/writing-resources/writing-as-process/editing-checklist
- proofreading SKILL.md (MIT): https://raw.githubusercontent.com/seb1n/awesome-ai-agent-skills/main/writing-and-content/proofreading/SKILL.md
- anthropics/skills: https://github.com/anthropics/skills
- easyzoom/proofreader-skill: https://github.com/easyzoom/proofreader-skill
- O0000-code/awesome-academic-skills (CC0): https://github.com/O0000-code/awesome-academic-skills
