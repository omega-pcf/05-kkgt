# Deterministic self-citation blocks in the family READMEs

| Field | Value |
|---|---|
| **Document** | `docs/specs/20261116_SPEC-001_deterministic_self_citations.md` |
| **Version** | 1.0.0 |
| **Status** | Draft — for Víctor's review |
| **Date** | 2026-11-16 |
| **Scope** | The `## Citation` segment (and the DOI badge line) of `README.md` in `01-hilbert-polya`, `02-odd-zeta`, `03-crystalline-worldsheet`, `04-mersenne-cr`, `05-kkgt`; the generator script, its wiring into the build, and the scaffold for future repos. Research + specification only: **no code is written**; the only pre-existing file touched alongside it is `docs/README.md` (index entry for `docs/specs/`, explicitly permitted). |
| **Authorship** | Hermes Agent (academic profile), at Víctor's request |

## 1. Purpose

Make the self-citation segment of every family `README.md` a **generated,
byte-deterministic artifact** driven by one command (`pnpm run
selfcitations`) from the repository's own citation identity, instead of five
hand-written variants that drift.

Why now: the five READMEs already carry five different realizations of the
same block (§2.3), one of them factually wrong (`04`, §2.4 D-1), and nothing
in any pipeline touches `README.md` (§2.6) — so the block rots every time the
identity root changes. Víctor's instruction: *"estandarizar un poco más este
segmento, que en todos los papers no veo realmente razón para que sean
distintos"* — the deliverable is a deterministic mechanism plus this spec,
not an implementation.

Non-goals are in §8.

## 2. Current state

### 2.1 Inspection method

Everything below was measured on 2026-11-16 against the working trees on
`/mnt/media/dev/`; `05-kk-golden-throat` at HEAD `8084490`
(`chore(repo): metadata parity with the family - bibtex citation, new names,
live project page`), tree clean. During the writing of this document a
docs-only commit landed on top (`80854a0`, touching only
`docs/style-guide.md`); no file cited below was affected. Line numbers are from `grep -n`/`read_file`
of the files named. External sources were fetched on 2026-11-16 with their
HTTP status recorded (Appendix B).

### 2.2 README inventory

| Repo | L | Citation block | Badges (top) | Heading of block | APA token | Identifier clause | bibtex key | `journal` | Identity DOI in block? |
|---|---|---|---|---|---|---|---|---|---|
| `01-hilbert-polya` | 133 | L25–38 | 4 (DOI L3, 2 project L4–5, Colab L6) | `## Citation` L25 | `Preprint.` L27 | DOI L27 | `Gonzalez2026HilbertPolya` L30 | `Preprint` L33 | yes — `10.5281/zenodo.17619486` = root |
| `02-odd-zeta` | 79 | L21–34 | 2 (DOI L3, project L4) | `## Citation` L21 | `Preprint.` L23 | DOI L23 | `Gonzalez2026OddZeta` L26 | `Preprint` L29 | yes — `10.5281/zenodo.19492791` = root |
| `03-crystalline-worldsheet` | 93 | L25–38 | 2 (DOI L3, project L4) | `## Citation` L25 | **`Zenodo.`** L27 | DOI L27 | **`CW6`** L30 | **`Zenodo`** L33 | yes — `10.5281/zenodo.21343602` = root |
| `04-mersenne-cr` | 121 | L21–34 | 2 (DOI L3, project L4) | `## Citation` L21 | `Preprint.` L23 | DOI L23 | `Gonzalez2026MersenneCR` L26 | `Preprint` L29 | **no — stale value, see D-1** |
| `05-kk-golden-throat` | 102 | L20–32 | 1 (project L3, **no DOI badge**) | `## Citation` L20 | `Preprint.` L22 | **`Repository:`** L22 | `Gonzalez2026KKGoldenThroat` L25 | `Preprint` L28 | n/a — root has no DOI (§3.5) |

Section sets outside the block (context only — the block is the target):
`01`/`03`/`04`/`05` use `## Repository Structure`, `02` uses `## Structure`
(`02/README.md:36`); `02` also uses `## Verification` (`:44`) instead of
`## Verification Execution` and **has no `## License` section at all** (file
ends at `:79`), while the other four end with `## License` (`01:131`,
`03:91`, `04:119`, `05:100`). `05` alone adds a `### Citations` subsection
(`05/README.md:41–44`) pointing at `docs/citations.md`.

Source of every block: hand-written. Measured: no file under `scripts/`
matches `README` in any of the five repos (`grep -rn README scripts/` →
empty), there is no CI (no `.github/` in any of the five, verified), and no
`README.template*` file exists anywhere in the family.

### 2.3 Divergence matrix

One shared skeleton (`## Citation` + one APA-style paragraph + one fenced
`bibtex` block) in 5/5; **five textual variants**, differing along five
axes:

| Axis | Variants | Evidence |
|---|---|---|
| A. Publisher token after the title | `Preprint.` ×4 vs `Zenodo.` ×1 | `03/README.md:27,33` vs `01:27,33` |
| B. Identifier clause | `DOI: [x](https://doi.org/x)` ×4 vs `Repository: [omega-pcf/05-kkgt](…)` ×1 | `05/README.md:22` |
| C. bibtex key scheme | `Gonzalez<Year><Slug>` ×4 vs internal cite key ×1 | `03/README.md:30` (`CW6`) |
| D. bibtex field set | `doi`+`url` ×4 vs `url` only ×1 | `05/README.md:24–31` |
| E. DOI value vs identity root | equal ×3, stale ×1, absent ×1 | `04` D-1; `05` has no DOI |

Author lists are *legitimately* different, not drift: `01` lists five authors
(`01/README.md:10`, … `& Moreno, M.`) and its `CITATION.cff:9–27` has five
entries; the other four list four authors (`02:8`, `03:8`, `04:8`, `05:7`),
matching their CFFs (`04/CITATION.cff:9–23`, `05/CITATION.cff:10–27`).

### 2.4 Concrete defects in the current blocks

- **D-1 (`04`, wrong DOI).** README block and badge say
  `10.5281/zenodo.21681395` (`04/README.md:3,23,31,32`), the identity root
  says `10.5281/zenodo.21731878` (`04/CITATION.cff:318`,
  `04/package.json → metadata.doi`, `04/.zenodo.json → doi`).
  `04/CHANGELOG.md:14` records the root change (`metadata: update DOI to
  all-versions (10.5281/zenodo.21731878)`) and `:108` the older value; the
  README was never updated. Zenodo API (2026-11-16): all three values are of
  the same concept `10.5281/zenodo.21681394` — README `21681395` = v0.3.9,
  root `21731878` = v0.3.18, while the *current* release (`package.json`
  version `0.3.20`, `04/CITATION.cff:6–7` `version: 0.3.20` /
  `date-released: 2026-08-25`) is record `22088748`. So the README is eleven
  versions behind, the root is two behind, and neither is the all-versions
  DOI the CHANGELOG claims (§3.5).
- **D-2 (`01`, LaTeX leaking into prose).** `01/README.md:27` prints
  `The Hilbert--Pólya … Between $\mathbb{F}_1$` — the identity title is
  `The Hilbert-Pólya … Between 𝔽₁` (`01/package.json → description`,
  `01/CITATION.cff:3`). The `--` double hyphen is BibTeX syntax inside
  running text (measured: `--` present in the README paragraph, absent from
  the description).
- **D-3 (`04`, title case).** `04/README.md:1` (H1) is Title Case
  (`Simultaneous Identities of the Golden Ratio and Euler's Identity,
  Formally …`) while the identity title is sentence case
  (`04/package.json → description`, `04/CITATION.cff:3`), and the citation
  block (`:23,:28`) follows the identity. Three renderings of one title.
- **D-4 (`02`, malformed author).** `02/README.md:27` —
  `García Ordóñez, L. M}` is missing the final period (all four other
  bibtex blocks end `L. M.}`).
- **D-5 (`03`, inconsistent container).** `Zenodo.`/`journal = {Zenodo}`
  (`03/README.md:27,33`) vs the family's `Preprint.`, which is also what the
  pipeline itself declares (`scripts/tasks/citation.ts:332`,
  `publication_type: 'preprint'`).
- **D-6 (cross-family identity is not canonical either).** The same paper is
  keyed differently in sibling bibliographies: `01`'s paper appears as `V11`
  (`02/citation.csl.json`, DOI 17619486), `HP` (`03/citation.csl.json`) and
  `HP26` (`05/citation.csl.json`, DOI **21712308**); `02`'s paper as
  `gonzalez26` (`01/citation.csl.json`) and `F1` (`03`, `05`). `03`'s README
  key `CW6` is the one that *does* match family usage
  (`05/citation.csl.json → id CW6`, cited in `05/main.tex:191,205,235,246`).
  Consequence for this spec: the generated key cannot be invented — it must
  be pinned (Q3, §9).
- **D-7 (`01`/`02` have no lockfile).** `pnpm-lock.yaml` exists in `03`,
  `04`, `05` and is **absent in `01` and `02`** (measured `ls`). Any
  generator whose output depends on a resolved npm package version
  (citation.js APA rendering, YAML parser) is therefore *not* byte-stable
  across fresh installs in two of five repos.

### 2.5 The citation pipeline today

Order of operations, `05/scripts/build.ts:38–41` (`build.ts` is
byte-identical in all five repos — `diff -q` silent):

1. `cleanupOldVersions(config.buildDir)`
2. `syncCitationMetadata(version)` → `scripts/tasks/citation.ts:72–86`:
   `cleanup()` (deletes `build/`, `src/bibliography.bib`, `.zenodo.json`,
   `citation.ts:88–99`) → `syncBibtex()` (`citation.csl.json` →
   `src/bibliography.bib`, `:128–156`) → `syncCff()` → `syncZenodo()`.
3. `compilePDF(config)`
4. `generateChecksums(config)` (hashes **only** the PDF,
   `scripts/tasks/checksums.ts:12–13`)

Field ownership inside `syncCff()` (`citation.ts:158–269`), i.e. what a
build rewrites in `CITATION.cff`:

| CFF key | Written by the build from | Line |
|---|---|---|
| `version` | CLI arg / `package.json.version` | `citation.ts:163` |
| `date-released` | **clock** — `new Date().toISOString().split('T')[0]` | `citation.ts:164` |
| `title` | `package.json → description` | `citation.ts:165` |
| `abstract` | `package.json → metadata.abstract` (fallback: keep) | `citation.ts:166` |
| `keywords` | `package.json → keywords` | `citation.ts:167` |
| `doi` | `package.json → metadata.doi` (only if present) | `citation.ts:168` |
| `references` | `citation.csl.json` via citation-js | `citation.ts:171–265` |
| **`authors`, `license`, `repository-code`, `type`, `message`** | **hand-maintained; the build does not write them** | no write site in `citation.ts` |

`.zenodo.json` is rebuilt from the CFF (`citation.ts:273–386`,
`writeFileSync` at `:383`), so the chain is:
`package.json` + `citation.csl.json` + hand data → `CITATION.cff` →
`.zenodo.json`. Documented as doctrine in `05/docs/citations.md:22–37`
(single source of truth + "derived files — never edit by hand"), and
`05/docs/citations.md:9` asserts "the pipeline scripts are byte-identical
across them" — true for `build.ts` (verified), **not** for `citation.ts`:
`02/scripts/tasks/citation.ts` is 395 lines / 14,411 B and still contains
the pre-fix global key replacement (`diff` vs `05`: `02:143–145` uses
`bib.replace(new RegExp(escaped, 'g'), cslId)` where `01/03/04/05:136–150`
rewrite backwards from the last match to avoid collapsing duplicate keys).
Rollout must carry `02` up to the shared script (§6.1).

Release flow: `.release-it.ts` `hooks.after:bump` runs
`pnpm exec tsx scripts/build.ts ${version}` and `plugins['@release-it/bumper']`
writes `version` into `CITATION.cff`; `git.commit: true`,
`requireCleanWorkingDir: true` (`.release-it.ts:7,11,23–35`). So anything a build
rewrites can be committed *inside* the release commit.

### 2.6 What the pipeline does not touch

- `README.md`: no reference under `scripts/` in any repo (§2.2).
- No CI workflows (no `.github/` in any of the five), so no automated drift
  detector exists.
- No `docs/specs/` directory exists yet in `05` (`ls` → ENOENT); this file
  creates it. `docs/reports/` already follows the same
  `YYYYMMDD_TYPE-NNN_snake_case` naming (`05/docs/reports/README.md`).

## 3. Sources of truth

### 3.1 Candidate sources and verdicts

| Candidate | Carries title? | Carries authors (ordered, complete)? | Carries DOI? | Carries repository URL? | Verdict |
|---|---|---|---|---|---|
| `CITATION.cff` | yes (written from `package.json`, `citation.ts:165`) | **yes — only complete, ordered, hand-owned list in all five** (`01/CITATION.cff:9–27`, `04:9–23`, `05:10–27`) | yes (`doi`, optional; `05` has none) | yes (`repository-code`) | **chosen** |
| `package.json` | yes (`description`) | **no `authors` field at all** | yes (`metadata.doi`) | yes (`repository.url`, with `.git`) | upstream of CFF for title/DOI; insufficient alone |
| `citation.csl.json` | no | no | no (never contains the paper's own DOI — measured: 0 hits for each repo's DOI in all five files) | no | the paper's *references*, not the paper — excluded by construction |
| `.zenodo.json` | yes | yes (derived) | yes | related identifier only | derived (`citation.ts:383`), Zenodo-facing; excluded |
| `main.tex` frontmatter | `\title` only (partial: `01:86` short title, `05:122` typeset with `\\` breaks) | `\author` in `01:92–99`, `02:101–109`, `03:141–147`, `05:131–139` — **absent in `04`** (`grep '^\author' 04/main.tex` → 0 matches), and the order differs from README/CFF (`01/main.tex:92–99` puts Luz María before Itzel; README `:10` and CFF `:9–23` put Itzel first) | no | no | unusable as a source (04 has no byline; LaTeX is typeset, not metadata) |

### 3.2 Decision

**`CITATION.cff`, read *after* `syncCitationMetadata()` has run.**
Reasons, in order of weight:

1. It is the only file in every repo that already holds *all* the fields the
   block needs — title, ordered authors, DOI, repository URL — and the only
   place where `authors` is hand-owned (build writes seven other keys, not
   `authors`; §2.5). The family skill states the same ownership rule:
   `authors`, `license`, `repository-code` belong in the CFF and a hand fix
   there is the correct edit.
2. It is the format the ecosystem treats as the citation input: GitHub
   renders its sidebar "Cite this repository" APA/BibTeX from `CITATION.cff`
   (§4.2), Zenodo reads it when no `.zenodo.json` exists (§4.5), and
   `cffconvert` converts *only* `CITATION.cff` → APA/BibTeX (§4.4). Reading
   the CFF makes our block the same object GitHub already displays.
3. Reading it post-sync means the block sees the same values the build just
   wrote into the CFF (`title`, `doi`, `version`), so the README cannot lag
   the identity root — the exact failure of D-1.
4. It is one parse of one YAML file; `yaml` is already a direct dependency
   (`citation.ts:2`) — no new dependency, and no coupling to citation.js
   output formatting, which is version-sensitive (D-7).

`citation.csl.json` stays the single source for the paper's *references*,
per `05/docs/citations.md:24`; it is explicitly **not** a source here (no
self-record exists, verified §3.1).

### 3.3 Field derivation table (the block's contract)

| Block element | Source | Rule |
|---|---|---|
| Author list, order | `CFF.authors[]` | order as in file |
| APA author string | same | `Family, G. A.` per author; `, ` between; ` & ` before the last (reproduces `01/README.md:27` shape); accents preserved verbatim |
| bibtex `author` | same | `Family, G. A. and Family, G. A. …` |
| Title | `CFF.title` | verbatim, inside `*…*` (APA) and `{…}` (bibtex); **no** `--`/`$\mathbb{F}_1$` rewriting — the CFF title is canonical (fixes D-2, D-3 by construction) |
| Year | `CFF.date-released` year | `YYYY` only — see §3.4 |
| Publisher token | constant `Preprint` | fixes D-5 (matches `citation.ts:332`) |
| DOI | `CFF.doi` | if present: `DOI: [x](https://doi.org/x)` + bibtex `doi`/`url`; if absent: repository clause + bibtex `url` only (the current `05` shape) |
| Repository | `CFF.repository-code` | always emitted in the no-DOI variant; optional one-line note in the DOI variant (Q6) |
| bibtex `journal` | constant `Preprint` | fixes D-5 |
| bibtex `year` | same as Year | |
| bibtex key | `package.json → metadata.citationKey` (new, explicit) | seeded with each repo's current key, so **no key changes** and `03` keeps `CW6` (§2.4 D-6, Q3) |
| DOI badge line | `CFF.doi` | rendered only when `doi` exists; markup fixed to the current Zenodo badge form (`01/README.md:3`) |

### 3.4 Volatile fields

`date-released` is rewritten to *today* on every build
(`citation.ts:164`), so a block embedding the full date would change on any
build that runs past midnight — churn with no information. Policy:

- the block embeds the **year only**; the full date is banned (AC-8);
- `version` is **not** embedded (Q5): today no README block contains it, and
  omitting it decouples the README from every release bump. GitHub's Cite
  button already shows the version (§4.2);
- consequence: a build on a quiet tree changes neither the year nor any
  other block input → the README is byte-stable under `pnpm run build`
  (AC-3).

### 3.5 DOI kind — prerequisite decision (Zenodo API, retrieved 2026-11-16)

| Repo | DOI in README | kind | DOI in root (`CFF`/`package.json`) | kind | Concept DOI of the record |
|---|---|---|---|---|---|
| `01` | `17619486` | concept (API: `conceptrecid 17619486`, latest record `21712308`, v2.5.4) | `17619486` | concept | `10.5281/zenodo.17619486` |
| `02` | `19492791` | concept (latest record `21712006`, v1.7.2) | `19492791` | concept | `10.5281/zenodo.19492791` |
| `03` | `21343602` | concept (latest record `22237572`, v1.2.1) | `21343602` | concept | `10.5281/zenodo.21343602` |
| `04` | `21681395` | **version** (v0.3.9, 2026-07-29) | `21731878` | **version** (v0.3.18, 2026-08-01) — while the current release is v0.3.20 = record `22088748` | `10.5281/zenodo.21681394` — *neither* of the two values in use; it resolves to the latest record `22088748` |
| `05` | — | no deposit yet | — | `CITATION.cff` has no `doi:` key; `package.json` has no `metadata.doi` | none yet |

`01`–`03` are internally consistent on the concept DOI; `04` uses two
different version DOIs in two places, and its CHANGELOG calls `21731878`
"all-versions" (`04/CHANGELOG.md:14`) although the API reports
`conceptdoi 10.5281/zenodo.21681394`. Generating the block from the root
*as is* would publish `04`'s version DOI (stale after every release) while
`01`–`03` publish concepts. **Recommendation: the block emits whatever the
root holds, and the roots are normalised to concept DOIs first** — for `04`
that means a root correction `21731878 → 21681394`, which needs Víctor's
go-ahead (Q1). Every DOI named here resolves — `curl -o /dev/null -w
'%{http_code}' https://doi.org/<doi>` returned `302` for each of
`17619486`, `19492791`, `21343602`, `21681395`, `21731878`, `21681394`,
`21712308` (measured 2026-11-16), and `/api/records/21681394` returns
`conceptdoi 10.5281/zenodo.21681394` with latest record `22088748`.

## 4. Prior art

All URLs fetched 2026-11-16; status codes in Appendix B. Extracts are quoted
verbatim.

### 4.1 Citation File Format (spec site)

https://citation-file-format.github.io/ — *"When you put a `CITATION.cff`
file in the default branch of your GitHub repository, it is automatically
linked from the repository landing page, and the citation information is
rendered on the repository page, and also provided as BibTeX snippet which
users can simply copy!"* and *"if you publish your software in an archive or
registry, they (or their systems) can re-use the citation metadata from your
`CITATION.cff` file."* The site points to the converter
(`cff-converter-python`) as the supported conversion path. Relevance: one
file, many renderings — exactly the model of §3.2.

### 4.2 GitHub — supported formats

https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files —
*"When you add a `CITATION.cff` file to the default branch of your
repository, a link is automatically added to the repository landing page in
the right sidebar, with the label 'Cite this repository.'"*; *"We currently
support APA and BibTeX file formats."*; the example shows GitHub's own
rendering (`Lisa, M., & Bot, H. (2017). My Research Software (Version 2.0.4)
[Computer software]. https://doi.org/10.5281/zenodo.1234`) and warns
*"Note the example above produces a* software *citation (that is, `@software`
type in BibTeX rather than `@article`)"*. The page also documents
`preferred-citation` with a `CFF type → BibTeX type → APA annotation` table
(`article → @article`, `software → @software [Computer software]`).
Relevance: fixes the two formats we standardise (APA + BibTeX), and shows
the `@software`/`@article` fork our `type: software` CFFs sit on
(`05/CITATION.cff:7`) — Q6/§9.

### 4.3 Citation.js — the engine already in the pipeline

https://citation.js.org/api/0.8/tutorial-cite_.html — *"To format data in a
`Cite` instance, you use the `Cite#format()` method"*, example
`example.format('bibliography', { format: 'html', style: 'apa' })`.
https://citation.js.org/api/0.8/module-@citation-js_plugin-bibtex.html —
*"This plugin adds input and output support for BibTeX … output format is
`bibtex`"* and *"… BibLaTeX … output format is `biblatex`"*. The family
already imports `@citation-js/core`, `plugin-csl`, `plugin-cff`,
`plugin-bibtex`, `plugin-zenodo` (`05/scripts/tasks/citation.ts:6–10`) and
calls `data.format('biblatex')` for the bibliography (`:134`).
Relevance: APA and BibTeX generation from our data is one `format()` call
away — but output text is pinned to the *resolved* citation.js version, and
two of five repos have no lockfile (D-7). Hence Q2: strict-APA via
citation.js vs the family's own format string (recommended, §5.2).

### 4.4 cffconvert — CLI precedent for CFF → APA/BibTeX + validation

https://github.com/citation-file-format/cffconvert — *"Command line program
to validate and convert `CITATION.cff` files"*; supported outputs: *"1.
APA-like plaintext 2. BibTeX 3. CodeMeta 4. EndNote 5. RIS 6. schema.org
JSON 7. Zenodo JSON"*; `cffconvert --validate`; ships a `pre-commit` hook
(`validate-cff`). Note its limitation: *"`cffconvert` does not support
converting items from `references` or `preferred-citation` keys at the
moment."* Relevance: confirms (a) CFF alone is a sufficient input for exactly
our two formats, (b) `--validate` is a cheap extra gate, (c) a Python CLI
would be a *new* runtime dependency in a pnpm pipeline — one more reason to
render in-process with the `yaml` package already present.

### 4.5 Zenodo — which file Zenodo reads, and validation advice

https://help.zenodo.org/docs/github/describe-software/citation-file/ —
*"If your repository also contains a `.zenodo.json` file, Zenodo will
**only** use the `.zenodo.json` metadata and ignore the `CITATION.cff`
entirely. However, we still recommend having a `CITATION.cff` file because
GitHub uses it to display a citation suggestion on your repository page"*;
*"Zenodo's long-term preference is for open metadata formats like
`CITATION.cff` to eventually make the `.zenodo.json` format unnecessary"*;
*"A `CITATION.cff` can be validated using tools such as cff-convert."*
https://help.zenodo.org/docs/github/describe-software/zenodo-json/ —
*"`CITATION.cff` will be completely ignored for the GitHub release
archiving"* when `.zenodo.json` is present; `.zenodo.json` exists for
Zenodo-only fields (`grants`, `communities`, `access_right`, …).
Relevance: our repos deliberately keep both (`.zenodo.json` generated from
the CFF, `citation.ts:383`); the README block, like GitHub's sidebar, must
read the **CFF**, not the Zenodo file.

### 4.6 Generated README citation blocks — negative result

A search for an established "generated README citation block" convention
(queries: `"CITATION.cff" README generated citation block script generate`;
`generate README citation section automatically from CITATION.cff script
tool`, 2026-11-16) returned only generic one-off generators (e.g.
https://github.com/ezefranca/github-citation — *"A web, CLI, MCP, and
agent-skill tool to generate BibTeX, APA, MLA, Chicago, IEEE, and Harvard
citations from any GitHub repository"*), a `cffinit` form, and community
guidance that *"Preferred citations are commonly placed in readme files or
CITATION.cff files"*. **No widely adopted standard for a generated README
citation segment was found**, and no template-plus-script precedent inside
this family (§2.2). Conclusion: the design in §5 is ours to specify; the
*inputs* (CFF) and *formats* (APA + BibTeX) are standard, the *mechanism* is
not — so it must be documented here rather than assumed.

## 5. Design

### 5.1 Mechanism: template file vs. marker regions

| | **A. `README.template.md` → `README.md`** (Víctor's wording) | **B. Marker regions inside `README.md`** (recommended) |
|---|---|---|
| Single source for prose | template; README fully derived | README itself; only the marked region is derived |
| Standardizes | the whole README skeleton, automatically | exactly the segment in scope (Víctor's *"este segmento"*) |
| Cost | the per-repo prose differs today (§2.2: `Repository Structure` vs `Structure`, missing `License` in `02`, `05`'s extra `### Citations`) → either 5 templates (no standardization) or a heavily parameterised template (larger change, larger diff) | none outside the markers; the divergent prose is untouched and can be standardized later as its own task |
| Drift direction 1 (hand edit of generated area) | caught by `--check` (README ≠ render(template)) | caught by `--check` (region ≠ render(CFF)) |
| Drift direction 2 (hand edit of the template only) | README stale until regeneration — **needs the check** | n/a (no second copy) |
| Failure mode | regeneration silently discards hand edits to `README.md` outside the citation block | regeneration cannot touch anything outside the markers |

**Recommendation: B**, with the marker pair treated as part of the
standard: a generator that can only ever rewrite a delimited region cannot
damage hand-written prose, it keeps exactly one home for each paragraph (the
family's own DRY rule, `05/docs/citations.md:137–138`), and it satisfies the
requested behaviour (*"procesamos y generamos el `.md` donde se inserta ese
bloque"*) without pretending the rest of the README is uniform when it is
not. Option A remains available later: the same renderer can be pointed at a
template in a second phase (Q4).

Marker syntax (chosen to survive GitHub rendering — HTML comments are
invisible in Markdown):

```markdown
<!-- selfcite:begin -->
…generated content…
<!-- selfcite:end -->
```

Two regions per README, each with a required `id`:

1. `id="badge"` — the DOI badge line, directly under the H1 (replaces the
   line currently at `01/README.md:3` and `04/README.md:3`). Empty content
   when the CFF has no `doi` (the `05` state); the markers stay.
2. `id="citation"` — the whole `## Citation` section body: heading, APA
   paragraph, blank line, bibtex fence.

Hand-authored badge lines (project page, Colab) stay outside the markers.

### 5.2 Canonical block format

Exact output (with DOI present):

````markdown
## Citation

<!-- selfcite:begin id="citation" generated — edit CITATION.cff or package.json, never this block -->
González García, J. A., González García, V. M., Dressler Pérez, I. M., García Ordóñez, L. M. (2026). *<CFF.title>*. Preprint. DOI: [<doi>](https://doi.org/<doi>).

```bibtex
@article{<citationKey>,
  author  = {<authors bibtex>},
  title   = {<CFF.title>},
  journal = {Preprint},
  year    = {2026},
  doi     = {<doi>},
  url     = {https://doi.org/<doi>}
}
```
<!-- selfcite:end id="citation" -->
````

No-DOI variant (`05`): identifier clause becomes
`Repository: [<owner/name>](<repository-code>).`; the bibtex entry drops
`doi` and sets `url = {<repository-code>}`; the `badge` region is empty.

Invariants: field order in the bibtex entry is a fixed literal (never
object-key order), two-space field alignment and `=` column at 10 as today,
UTF-8, LF, exactly one trailing newline inside the region, no clock read
anywhere (§3.4). Escaping: no re-escaping of accents; `{`/`}`/`_` in titles
are passed through as they already are in the five current blocks.

### 5.3 Script contract

New file `scripts/tasks/selfcitations.ts` (byte-identical across siblings,
like `build.ts`), exposed as `pnpm run selfcitations`.

- **Inputs:** `CITATION.cff` (parsed with the `yaml` package already used by
  `citation.ts:2`), `package.json → metadata.citationKey`, `README.md`.
- **Algorithm:**
  1. read `README.md`; locate each required region id; **0 or >1 pairs of a
     given id ⇒ exit 1** naming the file and the id;
  2. validate the CFF has `title`, `authors[]` (non-empty), and
     `repository-code`; `doi` optional — missing `title`/`authors` ⇒ exit 1
     (mirrors the existing guard *"it also refuses to run until
     `CITATION.cff` exists with the full author list"*);
  3. render both region strings from §3.3/§5.2;
  4. `--check` mode: compare rendered bytes with the on-disk region; on
     mismatch print a unified diff and **exit 1**; otherwise exit 0;
     default mode: rewrite only the bytes between the markers.
- **Determinism rules:** no `Date`, no `Math.random`, no locale-dependent
  formatting (`Array.sort` on a fixed list only), no network, fixed field
  order, fixed newline convention. Output must satisfy `f(f(x)) = f(x)`.
- **Type-check:** `tsconfig.json → include: ["scripts/**/*"]` (05) already
  covers the new file, so `pnpm run type-check` gates it with no change.

### 5.4 Wiring: into the build, plus a standalone check

| | **W1. Called from the build** (recommended) | **W2. Standalone only** |
|---|---|---|
| Freshness | README is regenerated exactly when its inputs change — the D-1 class of bug becomes impossible | README lags until someone runs the script; D-1 recurs |
| Doctrine fit | matches `05/docs/citations.md:27` *"Derived files — never edit by hand, always regenerated by the build"* (README joins `bib`/CFF/`.zenodo.json`) | keeps README hand-owned, contradicting the goal |
| Churn risk | only if the block embeds clock/release fields — excluded by §3.4 (AC-3 proves it) | none |
| Release integration | free: `.release-it.ts` `after:bump` already runs `build.ts`, and `git.commit: true` folds the refreshed README into the release commit | needs its own hook |
| Surprise factor | a build modifies a tracked file the author may consider prose | lower |

**Recommendation: W1 + a standalone check.** Concretely:
`scripts/build.ts` calls `syncSelfCitations()` immediately after
`syncCitationMetadata(config.version)` (`build.ts:39`) and *before*
`compilePDF`, so the block reads the CFF values the same run just wrote;
`build.ts`'s log list (`:44–48`) gains the README line. Add two scripts to
`package.json`:

```json
"selfcitations":      "pnpm exec tsx scripts/tasks/selfcitations.ts",
"selfcitations:check":"pnpm exec tsx scripts/tasks/selfcitations.ts --check"
```

and make `validate` run the check first:
`"validate": "pnpm run selfcitations:check && pnpm run verify:py && pnpm run
verify:lean"`. This is not an editorial test — it verifies a build invariant
(a generated artifact equals its generator's output), which is the same
class as the generated-file idempotence check the family already performs;
it re-derives nothing that a document asserts. Wiring the check into
`validate` is the one gate change this spec proposes (AC-2 depends on it).

### 5.5 Why this is byte-stable

- inputs: one YAML parse of `CITATION.cff` (post-sync) + one JSON field;
- no lockfile-dependent formatting (we do **not** call citation.js —
  D-7 neutralised; if Q2 selects strict APA, committing `pnpm-lock.yaml` in
  `01`/`02` becomes a prerequisite, §6.1);
- region-scoped writes: everything outside the markers is untouched by
  construction;
- `build.ts` is byte-identical across the five repos (verified §2.5), so the
  one-line hook propagates as an identical edit everywhere.

### 5.6 Drift model

| Drift | Caught by |
|---|---|
| Identity root changes (`package.json`/`CFF`), README not regenerated | build hook (W1) regenerates; if someone reverts, `selfcitations:check` fails |
| Hand edit inside a marker region | `selfcitations:check` (exit 1 + diff) |
| Marker pair deleted or duplicated | script error (exit 1) at next `build`/`validate` |
| Template (option A, if adopted) edited without regenerating | `selfcitations:check` |
| Block renders a clock-derived value | AC-8 (grep gate) |

## 6. Rollout plan

### 6.1 Prerequisites (all five repos)

1. Answer Q1–Q6 (§9). Q1 (DOI kind) blocks `04`; Q2 (APA engine) blocks the
   lockfile step; Q4 (template vs markers) blocks nothing else.
2. Normalise root DOIs to the concept DOI (§3.5) — `04` only
   (`21731878 → 21681394`), touching `CITATION.cff`, `package.json →
   metadata.doi` (and `.zenodo.json` follows on the next build).
3. Commit `pnpm-lock.yaml` in `01` and `02` (D-7) — required only if Q2
   picks citation.js; harmless otherwise.
4. Bring `02/scripts/tasks/citation.ts` to the shared 400-line version
   (§2.5) so the five pipeline scripts are actually byte-identical again.

### 6.2 Phases

| Phase | Repo(s) | Content | Why this order |
|---|---|---|---|
| 0 | `05-kkgt` | script + markers + `build.ts` hook + `validate` gate + docs (`docs/citations.md` gains `README.md` as a derived file; `docs/README.md` gains the `specs/` entry) | newest tree, cleanest, has a lockfile, has **no DOI** → exercises the no-DOI branch first; a failure here costs nothing published |
| 1 | `03-crystalline-worldsheet` | block regeneration: `Zenodo.`→`Preprint.`, `journal={Zenodo}`→`{Preprint}`, key stays `CW6` | largest visible change among published repos; do it right after the pilot |
| 2 | `02-odd-zeta` | block regeneration (fixes D-4 `L. M}`), `License` gap left out of scope | |
| 3 | `01-hilbert-polya` | block regeneration (fixes D-2: title becomes the identity title with `𝔽₁`); 5-author list preserved from CFF | |
| 4 | `04-mersenne-cr` | root DOI normalisation (§6.1, item 2) **then** block regeneration → D-1 fixed | last: needs the Q1 decision |
| 5 | scaffold | new repos are born with `scripts/tasks/selfcitations.ts`, both marker pairs in the scaffolded `README.md`, the two `package.json` entries, the `build.ts` line and the `validate` chain | prevents a sixth variant |

Each phase = one conventional commit per repo, no push/tag/release (family
standing rule). Rollout is complete when AC-1…AC-10 hold in all five.

Scaffold details (phase 5): the sibling-shell `git archive` copy already
carries `scripts/`, `package.json`, `README.md`, `docs/` — so adding the
script file plus the marker pair in the README step (identity, step 4 of the
scaffold) is sufficient; the generator then fails loudly if a new repo ships
without markers (§5.3 error path), which is the desired behaviour.

### 6.3 What the family gains

- one command (`pnpm run selfcitations`) and one check
  (`pnpm run selfcitations:check`) that mean the same thing in every repo;
- the README's citation segment becomes reviewable as *data* (a CFF diff)
  instead of *prose*;
- a README that cannot repeat D-1.

## 7. Acceptance criteria

Each is a command run at the repo root on a clean tree; all must exit 0.

- **AC-1 (idempotence).** `pnpm run selfcitations && pnpm run selfcitations
  && git diff --exit-code README.md` — the second run changes nothing.
- **AC-2 (check catches hand edits).** `pnpm run selfcitations:check` exits 0
  on the clean tree; after editing one character inside
  the `id="citation"` marker pair (begin/end, §5.2) it exits 1
  with a unified diff, and `pnpm run selfcitations` restores the file.
- **AC-3 (build does not churn the README).** `pnpm run build && git diff
  --exit-code README.md` on a quiet tree (the build may still touch
  `CITATION.cff`'s date — the README must not follow it).
- **AC-4 (cross-sibling identity of the segment).** For the five repos,
  extract each `## Citation` section, replace the four variable strings
  (title, authors, DOI/URL, key) by placeholders, and `sha256sum` the
  results: **one** distinct hash. (Badge regions: identical modulo presence
  of the DOI line.)
- **AC-5 (no stale identifier).** `grep -F "$(jq -r .metadata.doi
  package.json)" README.md` returns a match in every repo that has a DOI,
  and `grep -oE 'zenodo\.[0-9]+' README.md | sort -u` yields exactly one
  distinct DOI in every repo that has one (zero in `05`); `04` currently
  fails: `21681395` in README vs `21731878` in the root.
- **AC-6 (marker discipline).** Exactly two marker pairs in each README
  (`grep -c 'selfcite:begin'` = 2, `grep -c 'selfcite:end'` = 2), and the
  script exits 1 when a pair is removed.
- **AC-7 (type-check).** `pnpm run type-check` exits 0 with the new script
  present (covered by `tsconfig.json → include: ["scripts/**/*"]`).
- **AC-8 (no clock in the output).** `grep -nE '[0-9]{4}-[0-9]{2}-[0-9]{2}'
  README.md` finds no full date inside either marker region (the year is
  the only date-derived token).
- **AC-9 (DOI-less branch).** In `05` (no DOI): no DOI badge line is
  rendered, the citation clause is the `Repository:` form, and
  `selfcitations:check` exits 0; after a DOI lands in
  `package.json → metadata.doi` + build, both variants switch without any
  hand edit.
- **AC-10 (docs).** `docs/citations.md` lists `README.md` among the derived
  files of its own §1 table (`05/docs/citations.md:27–37`), and
  `docs/README.md` indexes `docs/specs/`.

## 8. Out of scope

- Minting or changing Zenodo records/DOIs for `05` (no deposit yet; the
  release is separately gated) — only the *shape* of the DOI-less block is
  specified here.
- `05-granularity` and `01-primitive-complex-field-dup` (Víctor's explicit
  exclusions; the latter is historical).
- Standardizing the rest of the README (section headings, `License` gap in
  `02`, badge set beyond the DOI line, the Colab badge) — listed as
  inventory in §2.2, separately runnable under option A if Q4 asks for it.
- Rewriting `citation.csl.json` self-records or unifying the cross-family
  keys `V11`/`HP`/`HP26`, `gonzalez26`/`F1` (D-6) — that touches reference
  data in siblings and needs its own task; §3.3 pins the README key instead.
- The manuscript (`main.tex`) bylines and titles; `omega-pcf.com` site
  entries; tags, releases and pushes.

## 9. Open questions for Víctor

1. **DOI kind (Q1).** Emit the *concept* (all-versions) DOI everywhere —
   recommended, because `01`–`03` already do and it never goes stale? This
   authorises correcting `04`'s root (`21731878 → 21681394`, §3.5) before
   its block is generated. Alternative: keep version DOIs everywhere (then
   `01`–`03` change too, and the block changes every release).
2. **Bibliography engine (Q2).** (a) Render with our own format string over
   the CFF fields — recommended: byte-stable, matches the five current
   blocks, no lockfile dependency; or (b) strict APA via citation.js's
   `format('bibliography', {style:'apa'})` + `format('bibtex')` — canonical
   APA (adds `(Version x)` and `[Preprint]`), but requires committing
   `pnpm-lock.yaml` in `01`/`02` first (D-7).
3. **bibtex key (Q3).** Add `package.json → metadata.citationKey`, seeded
   with each repo's current key (recommended: zero churn, `03` keeps `CW6`,
   which is what siblings actually cite) — or derive it from the repo slug
   (churns `MersenneCR`→`MersenneCr` and `CW6`) — or adopt one family-wide
   id scheme (requires touching every sibling's `citation.csl.json`, D-6)?
4. **Mechanism (Q4).** Marker regions inside `README.md` (recommended,
   §5.1) or the full `README.template.md` → `README.md` generation you
   proposed? If the latter, say whether `02`'s divergent section headings
   are normalised in the same pass (they are currently different, §2.2).
5. **Version in the block (Q5).** Add `(Version x.y.z)` to the APA line and
   `version = {…}` to the bibtex entry? Recommended: no — no README has it
   today, and omitting it keeps the block release-independent (GitHub's
   Cite button shows the version anyway).
6. **Scope of the generated region (Q6).** Is the DOI badge line generated
   too (recommended — it is citation metadata and `04`'s is stale), and
   should the block's CFF `type: software` be switched to
   `preferred-citation: type: article` so GitHub's button renders
   `@article` instead of `@software` (§4.2)? The latter changes the CFF
   root, so it needs an explicit yes.

## Appendix A — Verbatim diffs of the current citation blocks

Extracted 2026-11-16 with the `## Citation` section of each `README.md`
(lines cited in §2.2); `diff -u`, baseline `01-hilbert-polya`.

````diff
--- 01-hilbert-polya/README.md (L25–38)
+++ 02-odd-zeta/README.md (L21–34)
 ## Citation
 
-González García, J. A., González García, V. M., Dressler Pérez, I. M., García Ordóñez, L. M., & Moreno, M. (2026). *The Hilbert--Pólya Operator and the Primitive Structure of the Complex Plane: Between $\mathbb{F}_1$, String Theory, and Ancient Geometry*. Preprint. DOI: [10.5281/zenodo.17619486](https://doi.org/10.5281/zenodo.17619486).
+González García, J. A., González García, V. M., Dressler Pérez, I. M., & García Ordóñez, L. M. (2026). *Odd Zeta Values from the PCF Torus: φ and π as Arithmetic-Geometric Sources*. Preprint. DOI: [10.5281/zenodo.19492791](https://doi.org/10.5281/zenodo.19492791).
 
 ```bibtex
-@article{Gonzalez2026HilbertPolya,
-  author  = {González García, J. A. and González García, V. M. and Dressler Pérez, I. M. and García Ordóñez, L. M. and Moreno, M.},
-  title   = {The Hilbert--Pólya Operator and the Primitive Structure of the Complex Plane: Between $\mathbb{F}_1$, String Theory, and Ancient Geometry},
+@article{Gonzalez2026OddZeta,
+  author  = {González García, J. A. and González García, V. M. and Dressler Pérez, I. M. and García Ordóñez, L. M},
+  title   = {Odd Zeta Values from the PCF Torus: φ and π as Arithmetic-Geometric Sources},
   journal = {Preprint},
   year    = {2026},
-  doi     = {10.5281/zenodo.17619486},
-  url     = {https://doi.org/10.5281/zenodo.17619486}
+  doi     = {10.5281/zenodo.19492791},
+  url     = {https://doi.org/10.5281/zenodo.19492791}
 }
 ```
````

````diff
--- 01-hilbert-polya/README.md (L25–38)
+++ 03-crystalline-worldsheet/README.md (L25–38)
-González García, J. A., … (2026). *The Hilbert--Pólya Operator …*. Preprint. DOI: [10.5281/zenodo.17619486](…).
+González García, J. A., … (2026). *The Crystalline Worldsheet: A String Theoretical Framework based on $\mathbb{F}_1$ for the de Sitter observer problem*. Zenodo. DOI: [10.5281/zenodo.21343602](https://doi.org/10.5281/zenodo.21343602).
 ```bibtex
-@article{Gonzalez2026HilbertPolya,
+@article{CW6,
   …
-  journal = {Preprint},
+  journal = {Zenodo},
````

````diff
--- 01-hilbert-polya/README.md (L25–38)
+++ 04-mersenne-cr/README.md (L21–34)
+… *Simultaneous identities of the golden ratio and Euler's identity, formally verified in Lean 4 over the known Mersenne prime exponents*. Preprint. DOI: [10.5281/zenodo.21681395](https://doi.org/10.5281/zenodo.21681395).
-  doi     = {10.5281/zenodo.17619486},
+  doi     = {10.5281/zenodo.21681395},   ← stale: root says 10.5281/zenodo.21731878 (D-1)
````

````diff
--- 01-hilbert-polya/README.md (L25–38)
+++ 05-kk-golden-throat/README.md (L20–32)
+… *One object instead of a choice of vacuum …*. Preprint. Repository: [omega-pcf/05-kkgt](https://github.com/omega-pcf/05-kkgt).
+@article{Gonzalez2026KKGoldenThroat,
+  journal = {Preprint},
+  year    = {2026},
+  url     = {https://github.com/omega-pcf/05-kkgt}   ← no `doi` field (no deposit yet)
````

Badge lines (region 1 of the design):

| Repo | Lines | Content |
|---|---|---|
| `01` | L3–6 | DOI badge `zenodo.17619486` + 2 project-page badges + Colab badge |
| `02` | L3–4 | DOI badge `zenodo.19492791` + project-page badge |
| `03` | L3–4 | DOI badge `zenodo.21343602` + project-page badge |
| `04` | L3–4 | DOI badge `zenodo.21681395` (stale) + project-page badge |
| `05` | L3 | project-page badge only |

## Appendix B — Sources

### B.1 Internal (all read 2026-11-16)

| File | Anchors used |
|---|---|
| `01/README.md` | L1, L3–6, L10, L25–38, L40, L131 |
| `02/README.md` | L3–4, L8, L21–34 (esp. L23, L27), L36, L44, L79 |
| `03/README.md` | L3–4, L25–38 (esp. L27, L30, L33), L91 |
| `04/README.md` | L1, L3, L21–34 (esp. L23, L26, L31), L119 |
| `05-kk-golden-throat/README.md` | L3, L5, L20–32, L41–44, L100 |
| `*/CITATION.cff` | `01:3,6–7,9–27,29–30,2462`; `02:3,5–6,622`; `03:3,6–7,1777`; `04:3,6–7,9–23,318`; `05:1–3,7–9,10–27,28–29` (no `doi:` key) |
| `*/scripts/tasks/citation.ts` | `05:1–16,21–29,72–99,128–156,158–169,171–265,267,273–386,392–400`; `02:143–145` (pre-fix key replacement) |
| `*/scripts/build.ts` | `05:38–48` (byte-identical in all five, `diff -q`) |
| `05/.release-it.ts` | L7 `requireCleanWorkingDir`, L11 `git.commit`, L23–35 (hooks `after:bump`, bumper → `CITATION.cff`) |
| `05/scripts/tasks/checksums.ts` | L12–13 (PDF only) |
| `05/docs/citations.md` | L1–9 (byte-identical claim), L22–37 (single source + derived-file table), L47–56 (order of operations) |
| `05/docs/README.md` | L5–27 (directory doctrine, `reports/` index pattern) |
| `05/tsconfig.json` | `include: ["scripts/**/*"]` |
| `04/CHANGELOG.md` | L14, L108 (DOI history) |
| `05/main.tex` | L122, L131–139, L191/205/235/246 (`\cite{CW6}`) |
| `*/citation.csl.json` | self-record absence (0 hits per DOI); family ids `V11`, `HP`, `HP26`, `gonzalez26`, `F1`, `CW6` |
| `*/package.json` | `name`, `version`, `description`, `repository`, `keywords`, `metadata.doi`, `scripts`, `pnpm-lock.yaml` presence |

### B.2 External (fetched 2026-11-16; status as returned by the fetcher)

| URL | Status | Used for |
|---|---|---|
| https://citation-file-format.github.io/ | 200 | §4.1 CFF purpose, GitHub/Zenodo/Zotero support, converter link |
| https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files | 200 | §4.2 APA+BibTeX only, `@software` vs `@article`, `preferred-citation` table |
| https://citation.js.org/api/0.8/tutorial-cite_.html | 200 | §4.3 `Cite#format()` APA example |
| https://citation.js.org/api/0.8/module-@citation-js_plugin-bibtex.html | 200 | §4.3 `bibtex`/`biblatex` output formats |
| https://github.com/citation-file-format/cffconvert | 200 | §4.4 outputs, `--validate`, pre-commit hook, `preferred-citation` limitation |
| https://help.zenodo.org/docs/github/describe-software/citation-file/ | 200 | §4.5 `.zenodo.json` precedence, CFF still recommended, cff-convert validation |
| https://help.zenodo.org/docs/github/describe-software/zenodo-json/ | 200 | §4.5 `.zenodo.json` fields not in CFF |
| https://github.com/ezefranca/github-citation | search result (2026-11-16) | §4.6 negative-result context only |
| `https://doi.org/10.5281/zenodo.{17619486,21712308,19492791,21343602,21681395,21681394,21731878}` | `302` each (curl, 2026-11-16) | §3.5 DOI resolution |
| `https://zenodo.org/api/records/{17619486,21712308,19492791,21712006,21343602,22237572,21681395,21731878,21681394}` | JSON, `200`/`302→200` (curl, 2026-11-16) | §3.5 and D-1 `conceptrecid`, `conceptdoi`, `version`, `publication_date` (incl. latest record `22088748` = v0.3.20) |
