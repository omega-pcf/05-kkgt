# Lean build performance — where the 603 s actually goes, and what is worth changing

| Field | Value |
|---|---|
| **id** | `PRF-001` |
| **title** | Profile of `lake build` in `05-kk-golden-throat`: measured time of `TorreKK_LYR_v34.lean`, granularity versus slow declarations, and a classified candidate list |
| **status** | report only — measurements and this document; no `.lean` file, no manuscript, no test and no `citation.csl.json` touched |
| **date** | 2026-11-17 |
| **version** | 1.0 |
| **repository** | `05-kk-golden-throat` (public as `omega-pcf/05-kkgt`), task base `e9ff411`; while these measurements ran, other tasks committed `fb477a2`, `1307ee5` and `9a987f3`, so this report's own commit sits on top of them |
| **evidence** | session scratch `prf001_full_profile.log` (53 MB profiler trace), `prf001_runB_lakebuild.log`, `prf001_decl_times.json`, `prf001_importonly.lean`, `prf001_smoke.lean`; all under `~/.hermes/profiles/academic/cache/scratch/` |

**Scope.** This report answers one question: on this repository, what does
`lake build` spend its time on, and which of the possible fixes are mechanical
versus which require proof refactors with manuscript spillover. It records
measurements taken on 2026-11-17 on the author's host (Lean 4.33.1, Mathlib
v4.33.1, Lake 5.0.0) and the sources consulted for each recommendation. It
deliberately changes nothing: the file under measurement
(`lean/TorreKK_LYR_v34.lean`, 1523 lines, 180 theorems and definitions plus 6
axioms, `import Mathlib` on line 28) was read and rebuilt only; its content
hash was `89a9125af428abcb02f1d41204bdd373` before and after the timed rebuild,
and this task never wrote to it. All edits are
left to the author's last pass, as requested.

---

## 1. Method

Five runs, strictly serial (the host had 57–62 GB of 62 GB RAM in use and swap
full at 15/15 GB, so nothing was run in parallel):

| # | run | command | wall | what it measures |
|---|---|---|---|---|
| A1 | no-change build (dry) | `lake build --no-build` | 45.345 s | job-graph + hash replay of 8707 jobs, no compilation |
| A2 | no-change build (dry), second sample | `lake build --no-build` | 33.863 s | idem, less contention |
| B | no-change build, real | `lake build` | **35.37 s** (user 8.80, sys 14.85, 9815 major faults) | the baseline an unchanged tree pays |
| C | profiled elaboration | `lake env lean -D profiler=true -D profiler.threshold=100 -D trace.profiler=true -D trace.profiler.threshold=50 TorreKK_LYR_v34.lean` | **666.76 s** (user 49.38, sys 56.65, 15 % CPU, max RSS 2.49 GB, 892 777 major faults, exit 0) | cumulative categories plus per-declaration trace |
| D | faithful rebuild of the changed module | delete `TorreKK_LYR_v34.{olean,olean.hash,ilean,ilean.hash,trace}` then `lake build` | **493.64 s**, of which Lake reports `Built TorreKK_LYR_v34 (467s)` | exactly what a one-line edit costs, with the lakefile `leanOptions` applied |
| E | import-only probe | `lake env lean -D profiler=true` on a file whose only content is `import Mathlib` | did not finish within 420 s (killed) | the fixed import cost in isolation |

Mechanism notes. `lean --help` of the installed toolchain documents the knobs
used: `--profile` ("display elaboration/type checking time for each
definition/theorem"), `-D name=value` ("set a configuration option"), and the
experimental `--incr-save` / `--incr-load` flags. Run C uses `-D
profiler=true` (the option the mathlib speed-up guide prescribes, threshold in
milliseconds, default 100) for the cumulative category table, plus `-D
trace.profiler=true` for the structured per-command tree (threshold in
milliseconds, default 10; both defaults confirmed in the toolchain's own
`src/lean/Lean/Util/Profile.lean` and `Trace.lean`). Two quirks of Lean 4.33
shaped the extraction: proof bodies are elaborated *asynchronously*
(`[Elab.async] elaborating proof of <decl>`), so a theorem's `[Elab.command]`
span covers only its statement; and a `lake env lean` invocation does **not**
receive the lakefile's `[leanOptions]`, which is why run C is the profiling
run and run D is the faithful timing.

---

## 2. Measured profile

### 2.1 The shape of the wall clock

| quantity | measured |
|---|---|
| no-change build (8707 jobs replayed, nothing compiled) | 35.37 s (samples: 35.37 / 33.87 / 45.35) |
| one-line change → full rebuild of the module | 493.64 s total; 467 s inside the module |
| profiled rebuild of the module | 666.76 s total, of which **`import 641 s` (96.1 %)** |
| everything the module itself elaborates after the import | ≈ 26 s of wall (666.76 − 641) |
| recorded declaration work in run C (statements + proofs, executed concurrently on 16 threads) | 44.51 s across 159 declarations |

The cumulative category table printed by run C at exit:

| category | time |
|---|---|
| import | **641 s** |
| interpretation (tactic/attribute extensions loaded from oleans) | 28 s |
| typeclass inference | 16.7 s |
| tactic execution | 6.26 s |
| elaboration | 5.54 s |
| type checking | 3 s |
| `norm_num` | 2.42 s |
| `simp` | 2.08 s |
| `ring` | 1.77 s |
| linting (incl. `overlappingInstancesLinter`) | 0.423 s |
| parsing | 0.151 s |

Two figures characterise the runs as I/O-bound rather than CPU-bound: 15–20 %
CPU with system time exceeding user time (666.76 s wall vs 106 s CPU), and
616 333–892 777 **major** page faults per run. The host was paging in olean
data, not proving mathematics.

### 2.2 The five slowest declarations

Per-declaration times extracted from the trace (statement span `[Elab.command]`
plus asynchronous proof span `[Elab.async] elaborating proof of …`).
`% run` is against the 666.76 s profiled run; `% decl` is against the 44.51 s
of recorded declaration work.

| # | declaration | statement (s) | proof (s) | total (s) | % run | % decl |
|---|---|---|---|---|---|---|
| 1 | `TorreKK.no_unit_below_golden` | — | 2.050 | 2.050 | 0.31 % | 4.6 % |
| 2 | `TorreKK.golden_pow_fib` | — | 1.891 | 1.891 | 0.28 % | 4.2 % |
| 3 | `TorreKK.old_symmetrizer_fails` | — | 1.555 | 1.555 | 0.23 % | 3.5 % |
| 4 | `TorreKK.window_crosses_half` | — | 1.425 | 1.425 | 0.21 % | 3.2 % |
| 5 | `TorreKK.two_tile_entropy` | — | 1.423 | 1.423 | 0.21 % | 3.2 % |

Next in line: `ring_resolution_irrational` 1.388 s, `eta_eq_exp_fourA` 0.968 s,
`cardy_is_tower_entropy` 0.942 s, `clifford_stereographic_torus` 0.831 s,
`sq_add_inv_sq` 0.758 s, `clifford_square` 0.723 s, `pisano_orders` 0.717 s,
`closedStringMass2` (statement side only) 0.694 s, `ring_mode_below_BF`
0.667 s, `phase_quarter_iff` 0.655 s. The **top 15 sum to 16.69 s**, i.e.
37.5 % of all recorded declaration work and **2.5 % of the build's wall time**.

159 declarations were individually timed at the 50 ms threshold; 44.51 s of
declaration work in total; nothing anywhere in the file exceeds 2.1 s.

Tactic-level evidence from the same run: the single largest tactic execution
was `decide` at 682 ms (inside `pisano_orders`, whose proof totals 0.717 s and
whose statement carries `set_option maxRecDepth 100000`), then `refine` at
608 ms and 217 ms. The largest single `simp` was 309 ms. Every `decide` in the
file together costs on the order of **one second** of a 494–667 s build.

### 2.3 Declaration census (source, read-only)

| pattern | occurrences | declarations touched |
|---|---|---|
| `decide` | 6 | 5 |
| `native_decide` | **0** | 0 |
| bare `simp` (not `simp only`) | 23 | 20 |
| `simp only` | 7 | — |
| `norm_num` | 60 | 50 |
| `ring` | 62 | 50 |
| `field_simp` | 41 | 34 |
| `nlinarith` | 44 | 28 |
| `linarith` | 41 | 28 |
| `positivity` | 18 | 16 |
| `omega` | 10 | 6 |
| `exact?` / `apply?` left in proofs | 0 | 0 |
| `set_option maxHeartbeats …` | 0 | 0 |
| `set_option maxRecDepth 100000` | 1 (line 528, on `pisano_orders`) | 1 |

---

## 3. Structural diagnosis — granularity or slow declarations?

**Neither, exactly: the dominant term is the fixed `import Mathlib` cost,
re-paid on every rebuild.**

1. **Slow declarations are ruled out by measurement.** The worst proof in the
   file is 2.05 s; the whole file's recorded declaration work is 44.51 s
   (≈ 26 s of wall, already parallelised across 16 threads by Lean's async
   proof elaboration). Even if every proof were made free, run D would fall
   from 493.6 s to ≈ 467 s — a 5 % saving.

2. **Granularity is real but second-order.** The file is one module, so any
   edit invalidates the module's single trace and Lake rebuilds it whole
   (Lake reference, §25.1.2: "Lake uses saved *trace files* to determine which
   artifacts require building … If the inputs are all unmodified, then the
   corresponding artifact is not rebuilt"). The price of that all-or-nothing
   granularity is the re-elaboration of the *unchanged* declarations, which
   the profile puts at ≈ 26 s of wall (5.3 % of the 493.6 s rebuild). Splitting
   the file into N modules would recover at most that amount per edit, and
   only for the modules actually untouched — while each new module process
   would still pay the import.

3. **The import line is the structural lever.** `import Mathlib` (line 28)
   pulls the whole library into every rebuild. In run C that phase was 641 s
   of 666.76 s (96.1 %); run E shows an `import Mathlib`-only file did not
   finish in 420 s. A narrower import list scales the import with the olean
   bytes actually needed, which is the only change that attacks the dominant
   term without touching a single proof.

4. **The host amplifies it.** The same import of a sub-chain
   (`Mathlib.Data.Nat.Basic`, probe `prf001_smoke.lean`) took 4.6 s, so the
   full-library import is ~140× that on this machine; with 57–62 GB of RAM in
   use, swap full and 0.6–0.9 M major faults per run, most of the wall clock
   is page-in, not deserialisation. This is why the author's 603 s and the
   measured 493.6 s / 666.8 s bracket each other: the number moves with memory
   pressure, not with proof difficulty.

**Verdict for the author's premise.** The `decide` versus `native_decide`
instinct is not what is costing time here: the file contains no
`native_decide`, all its `decide` calls together cost ≈ 1 s, and the fix with
the largest measured payoff is the import line, not any proof.

---

## 4. Recommendations with sources

Each item carries the URL and the date it was read (2026-11-17) plus a literal
extract; nothing below is paraphrased from memory.

### R1 — Narrow `import Mathlib` before touching any proof (mechanical, largest measured lever)

- Lean reference manual, *Lake*, §25.1.2 —
  <https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Lake/>:
  "Lake automatically analyzes the imports of Lean modules to discover their
  dependencies" and "Rather than rebuilding everything in the dependency graph
  from scratch, Lake uses saved *trace files* to determine which artifacts
  require building. During a build, Lake records which source files or other
  artifacts were used to produce each artifact, saving a hash of each input."
  The rebuild unit is the module and its declared imports — so the import line
  is the size of what every rebuild must page in.
- mathlib4 issue #24020, *Why is Mathlib so slow to load even when cached?*
  (opened 2025-04-14) — <https://github.com/leanprover-community/mathlib4/issues/24020>:
  "Running an executable that transitively imports all of Mathlib is going to
  take a long time: the cache mechanism provides oleans, but not …". The same
  issue measures `lake env lean --run` on an `import Mathlib` file at
  `real 0m15.878s` — i.e. the community already treats whole-library import as
  the cost centre.
- Measured here: 641 s of 666.76 s (96.1 %) and an import-only file that did
  not finish in 420 s, against 4.6 s for a sub-chain import.

How: replace line 28 with the modules actually used, rebuild, and add back
only what the errors name — a mechanical, error-driven loop that never touches
a statement. Expected effect: the import phase shrinks roughly with the olean
bytes loaded; the elaboration side (≈ 26 s) is unaffected.

### R2 — Do not refactor proofs for speed, and do not introduce `native_decide`

- Lean 4 community docs, *decide & native_decide* —
  <https://lean4.dev/tactics/automation/decide>: "`decide` runs at kernel
  level—it actually computes the answer. This means it can be slow for large
  computations." and "⚠ `native_decide` trusts the compiler—it doesn't verify
  the computation in the kernel. For critical proofs where correctness is
  paramount, prefer `decide`."
- Mathlib deprecated-syntax linter docs —
  <https://leanprover-community.github.io/mathlib4_docs/Mathlib/Tactic/Linter/DeprecatedSyntaxLinter.html>:
  "The `native_decide` tactic is not allowed in mathlib, as it trusts the
  entire Lean compiler (and not just the Lean kernel). Because the latter is
  large and complicated, at present it is probably possible to prove `False`
  using `native_decide`." The same page: "The option `linter.style.native` …
  flags usages of tactics which use `nativeEqTrue` such as `native_decide` and
  `decide +native`, which are disallowed in mathlib." — and it flags an
  unexplained `set_option maxHeartbeats n in`: "flags usages of `set_option
  <name-containing-maxHeartbeats> n in cmd` that do not add a comment explaining
  the reason for the modification of the `maxHeartbeats`."
- Zulip archive, stream `lean4`, *soundness bug: native_decide leakage*
  (2023-10-10) —
  <https://leanprover-community.github.io/archive/stream/270676-lean4/topic/soundness.20bug.3A.20native_decide.20leakage.html>:
  Mario Carneiro: "You don't need the `ofReduceBool` axiom for weirdness from
  the real world to affect the logical system"; Scott Morrison: "lean4#2654
  adds an axiom that `Lean.reduceBool` and `Lean.reduceNat` depend on."
- leanprover/lean4 issue #12216, *RFC: One axiom per native computation* —
  <https://github.com/leanprover/lean4/issues/12216>, which documents the shape
  `native_decide` emits: "A tactic like `native_decide` produces the following
  declarations: `def thm._nativeDecide_1_1 : Bool := decide (1 + 2 = 3) …`".
- Local doctrine: skill `lean-file-fixing` § *native_decide policy (RED LINE)*
  — "Never finish with `native_decide` — it adds the `Lean.ofReduceBool` axiom
  (trusts the compiler, not the kernel)"; its prescribed remedy when `decide`
  is slow is to *shrink the decision space with real math* (e.g. characterise a
  Finset as a closed-form filter and decide the equality once), keeping
  statements unchanged. Skill `lean-community-conventions` adds: "Avoid
  raising heartbeat limits as a long-term fix for fragile code."

Applied to this file: the `decide` sites (`modular_orders` L522,
`pisano_orders` L532, `crossing_group_mod_two` L646,
`bottom_is_lattice_point` L1075, `two_not_unit` L1183) measure ≈ 0.7 s for the
slowest and ≈ 1 s in total — under 0.2 % of a rebuild. Switching any of them to
`native_decide` would trade a measurable 0.2 % for a new trusted axiom, against
mathlib's stated position and this project's own red line. **Recommendation:
leave every `decide` as it is; the performance case for `native_decide` does
not exist in this file.**

### R3 — Fix the loop around the build (memory, import, incremental workflow)

- Lean reference manual, *Lake*, §25.1.3 *Caching Builds* —
  <https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Lake/>:
  "Builds of large packages can consume significant time. Compounding this,
  switching between local development branches can cause Lake to rebuild the
  same code many times." and "Because this is an experimental feature, the
  local cache is disabled by default. It is only enabled when the
  `LAKE_ARTIFACT_CACHE` environment variable is set to `true` or when the
  `enableArtifactCache` field is set to `true` in the configuration file."
- Toolchain `lean --help` (Lean 4.33.1, local): `--incr-save=file` /
  `--incr-load=file` — "EXPERIMENTAL: save a full incremental snapshot of
  post-elaboration state at end of run" / "reuse a snapshot saved by
  `--incr-(header-)save` at start of run". The language server keeps the
  imported environment resident, so iterative checking in the editor or via
  the server does not re-pay the import that dominates a cold `lake build`.
- Lean 4.8.0 release notes — <https://lean-lang.org/blog/2024-6-1-lean-480/>:
  "The trace profiler can be used to understand time usage by elaboration steps
  (subterms, tactics, ...) and by Lean subsystems."

Concrete steps: (a) run the heavy builds when the host has free page cache —
measured here at 15–20 % CPU with swap full, every rebuild pages in 0.6–0.9 M
faults; (b) keep iterating in the Lean server instead of cold `lake build`
per edit; (c) consider the experimental `LAKE_ARTIFACT_CACHE=true` for branch
switching; (d) keep the profiling flags documented in §1 as the standing way
to re-check any claim about build time (`-D profiler=true -D
profiler.threshold=100 -D trace.profiler=true -D trace.profiler.threshold=50`,
imported options given on the command line because `lake env lean` does not
read the lakefile's `[leanOptions]`).

### R4 (context) — How the community profiles, and the known blind spot

- mathlib, *How to speed up a Mathlib file* —
  <https://leanprover-community.github.io/extras/speedup.html>: "The first step
  is to find out which parts of the code are slow. To do so, add a line
  `set_option profiler true` after the import statements. This will produce
  lines of the form `<blah> took <number>ms` (or even `<number>s`) in the
  infoview, recording steps that took at least `100ms` (the lower bound in ms
  can be adapted via `set_option profiler.threshold <num>`)." Its per-symptom
  advice: "### simp took <a long time> … Replace the relevant `simp/simpa`
  call by `simp?/simpa?` and click on the `Try this:` suggestion to replace it
  by a `simp/simpa only` call." — with the documented trade-off "Proofs can get
  several dense lines longer, and will now mention many lemmas by name, each
  of which might be renamed in the future, breaking your proof."
- External Lean skill `lean4-skills`, `references/profiling-workflows.md`
  (<https://raw.githubusercontent.com/cameronfreer/lean4-skills/main/plugins/lean4/skills/lean4/references/profiling-workflows.md>,
  "Verified on: Lean `v4.33.1` and `v4.35.0` … Last validated: 2026-10-19"):
  "**Threshold units.** `trace.profiler.threshold` is in milliseconds (default
  `10`, or in heartbeats when `trace.profiler.useHeartbeats` is true)" and
  "**Pitfall: set the output path on the command line.** `set_option
  trace.profiler.output "…"` *inside* the file suppresses the trace messages
  but writes no file (checked on `v4.33.1` and `v4.35.0`), so the profile is
  silently lost."
- Same skill, `references/performance-optimization.md` —
  <https://raw.githubusercontent.com/cameronfreer/lean4-skills/main/plugins/lean4/skills/lean4/references/performance-optimization.md>:
  "| `simp [*]` or `simp` | Broad simp set | `simp only [lemma1, lemma2]` |",
  "| `exact?` / `apply?` | Searching all lemmas | Replace with explicit
  lemma |", "| `decide` / `native_decide` | Large computation | Manual proof or
  cache result |".
- Known blind spot, for honesty about the numbers: leanprover/lean4 issue
  #8038 (opened 2025-04-21, open at time of reading) —
  <https://github.com/leanprover/lean4/issues/8038>, titled "`#time` and
  `trace.profiler` miss nearly all of the time spent in some files".
- Local skills consulted: `lean-proof-methodology`, `lean-file-fixing`,
  `lean-generated-proof-audit`, `lean4-cameronfreer`, `lean-axiom-provenance`,
  `lean-community-conventions`. The first four say nothing that contradicts
  the measurements; `lean-axiom-provenance` and `lean-generated-proof-audit`
  supply the trust argument of R2 (`native_decide` emits
  `Lean.ofReduceBool` / `Lean.ofReduceNat`, "the compiler and runtime are
  trusted, not the kernel"); `lean-community-conventions` adds the standing
  rules "Benchmark or at least inspect performance for changes to imports,
  classes, instances, `simp` lemmas, definitions, or nontrivial refactors" and
  "Avoid raising heartbeat limits as a long-term fix for fragile code."

---

## 5. Candidates, classified by risk and spillover

Counts are over the 180 declarations of `lean/TorreKK_LYR_v34.lean`. "Deep"
candidates are deferred to the author's last pass by the doctrine stated in
the request (refactors with manuscript spillover are done when everything is
already passing).

### 5.1 Mechanical, low risk — **21 candidates** (proof bodies and one import line; no statement changes)

| # | candidate | sites | risk | spillover |
|---|---|---|---|---|
| M1–M20 | replace bare `simp` with `simp only […]` in 20 declarations (23 occurrences), list taken from each `simp?` suggestion | 23 | low: proof body only; each change verified by one build cycle | none to the manuscript; only resilience to future Mathlib renames (documented trade-off of the speed-up guide) |
| M21 | narrow `import Mathlib` (line 28) to the modules actually used, driven by rebuild errors | 1 | low–medium: iterative, mechanical; a missing import is a build error, never a silent weakening | none: no declaration, statement or `\lean{}` tag changes |

### 5.2 Deep proof refactor with potential manuscript spillover — **19 candidates** (defer to the last pass)

| group | declarations | why it is deep |
|---|---|---|
| D1 `decide` decision-space shrink (5) | `modular_orders` L522, `pisano_orders` L532 (carries `set_option maxRecDepth 100000`), `crossing_group_mod_two` L646, `bottom_is_lattice_point` L1075, `two_not_unit` L1183 | needs helper lemmas that characterise the matrices/finsets up front (the `lean-file-fixing` remedy), i.e. new statements in the file, and possibly changes to what the note points at |
| D2 slowest proofs (15, of which `pisano_orders` and `golden_pow_fib` already counted above) | `no_unit_below_golden` 2.05 s, `golden_pow_fib` 1.89 s, `old_symmetrizer_fails` 1.56 s, `window_crosses_half` 1.43 s, `two_tile_entropy` 1.42 s, `ring_resolution_irrational` 1.39 s, `eta_eq_exp_fourA` 0.97 s, `cardy_is_tower_entropy` 0.94 s, `clifford_stereographic_torus` 0.83 s, `sq_add_inv_sq` 0.76 s, `clifford_square` 0.72 s, `ring_mode_below_BF` 0.67 s, `phase_quarter_iff` 0.66 s, `cardy_entropy` 0.64 s, + `pisano_orders` | restructuring into helper lemmas changes the shape of what the manuscript's `\lean{}` tags point at; statements must stay byte-identical |

**Union: 19 distinct declarations** (5 + 15 − 1 overlap), i.e. 10.6 % of the
file. One declaration, `golden_pow_fib`, appears in both lists.

### 5.3 Structural (optional, not a proof change)

| candidate | expected effect | when |
|---|---|---|
| S1 split `TorreKK_LYR_v34.lean` into several modules with a shared import module | saves at most ≈ 26 s per rebuild (the re-elaboration of unchanged declarations, 5.3 % of 493.6 s) and enables `lake -j` to work across modules; it does **not** remove the import cost | only worth doing together with R1 (narrower imports per module); needs care with the `\lean{}` tags in `main.tex` if any declaration moves file |

---

## 6. Plan for the final pass — what to do, and when

1. **Now (nothing is green yet / other tasks in flight): do nothing to
   proofs.** This report is measurement only. The single highest-value change
   (`import Mathlib` narrowing, M21) touches `lean/` and is therefore left to
   the author's explicit go-ahead, as are all `.lean` edits here.
2. **When the tree is passing:** mechanical pass A — M21 (narrow imports),
   then M1–M20 (`simp` → `simp only`), in batches with one full `lake build`
   per batch; record the warning census before and after (per
   `lean-file-fixing`). Re-run runs B and C afterwards and replace the numbers
   in §2 with the new ones in a later report (reports are snapshots).
3. **Last pass (everything green):** the deep group D1–D2 *only if* a fresh
   profile still shows a declaration above the author's patience threshold.
   On today's data nothing exceeds 2.05 s, so the honest expectation is that
   this pass is a no-op; if it is done, statements stay byte-identical, any
   statement that must change is reported to `main.tex` immediately, and the
   `#print axioms` gate (only `propext`, `Classical.choice`, `Quot.sound`;
   zero `sorryAx`, zero `Lean.ofReduceBool`) is re-run at the end.
4. **Never, without an explicit author decision:** `native_decide`,
   `decide +native`, or a raise of `maxHeartbeats` without a comment — three
   separate red lines (local skill, mathlib linter docs, community style).
5. **Standing practice:** before any future "this build is slow" claim, run
   the §1 profiling command once; the import-versus-elaboration split it prints
   settles the question in one run.

---

## 7. Gaps and limits of this report

- **Memory-confounded absolutes.** Every run happened with 57–62 GB of 62 GB
  resident and swap full (15/15 GB); runs took 15–20 % CPU with 0.6–0.9 M
  major faults. The relative split (import ≈ 96 %, elaboration ≈ 4 %) is
  robust across three runs, but the absolute seconds are not reproducible on
  an idle host and were not re-derived for the author's 603 s figure.
- **The profiling run is not bit-identical to a build.** Run C used
  `lake env lean`, which does not pass the lakefile's `[leanOptions]`
  (`relaxedAutoImplicit = false`, `maxSynthPendingDepth = 3`,
  `weak.linter.mathlibStandardSet = true`), so its linting time
  (0.423 s) understates a faithful build's; run D (493.64 s) is the faithful
  figure. Run C also paid the profiler's own overhead (53 MB of trace text).
- **50 ms threshold.** Commands and sub-steps below `trace.profiler.threshold
  50` are not individually timed: 49 statement spans (of the file's 186
  top-level declarations plus its section/option commands) and 49 of the 163
  proofs are absent from the table, each bounded by 50 ms (≤ ≈ 5 s together).
  A 10 ms rerun would close this at the cost of another ≈ 8–11 min run.
- **Async spans are work, not wall.** `[Elab.async] elaborating proof of …`
  durations sum to 39.1 s while the post-import wall is ≈ 26 s: proofs overlap
  across threads (and spans may include queue wait), so `% decl` is a share of
  work, not of elapsed time.
- **Import isolation.** Run E (import-only, with `profiler=true`) was killed at
  420 s rather than completed, so the import term is quoted from run C's
  cumulative `import 641 s` and inferred for run D (467 s module − ≈ 26 s
  elaboration ≈ 440 s) rather than measured on its own without the profiler.
- **Known profiler blind spot.** leanprover/lean4#8038 (open) reports that
  `#time` and `trace.profiler` "miss nearly all of the time spent in some
  files"; some of the ≈ 26 s post-import wall is unattributed in §2.
- **Not measured:** the effect of narrowing imports (would require editing the
  file), the effect of splitting the module (S1), a warm-cache rebuild on an
  idle host, and a re-run of the `#print axioms` gate (each of these needs a
  full import cycle of ≈ 8–11 min and, for the first two, `.lean` edits that
  this task forbids).
- **Package warnings.** All nine `.lake/packages/*` checkouts report "local
  changes"; their oleans are up to date (`lake build --no-build`: "All targets
  up-to-date (8707 jobs)"), so no dependency was rebuilt during any measurement,
  but the dirty checkouts are worth a separate look.

---

## Related documents

- `docs/reports/README.md` — the report convention this file follows.
- `docs/reports/20261117_TST-001_aud001_test_gaps_and_tolerances.md` — the
  previous same-day pass; tests untouched by this report.
- `lean/lakefile.toml`, `lean/lean-toolchain` — the configuration measured.
