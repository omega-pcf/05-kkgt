#!/usr/bin/env tsx
/**
 * Generated counts for the living documents (follow-up of CVR-001 §5).
 *
 * The numbers the documentation asserts about the repository — the pytest
 * suite total, the not-slow total, the census size, the `\testref{...}`
 * anchors, the Lean source statistics and the figure inventory — are
 * MEASURED, never typed.  `pnpm run counts` rewrites every marked region of
 * the living documents and regenerates `docs/counts.md` from the working
 * tree; `pnpm run counts:check` (wired into `validate`) fails with a
 * unified diff when either has drifted, so a stale count is loud instead of
 * a report's footnote.
 *
 * Markers follow the selfcitations precedent (SPEC-001 §5.2) and come in three
 * forms, because a code fence prints HTML comments as text and a `%` comments
 * out the rest of its TeX line:
 *
 *   inline (HTML comment, prose):
 *     <!-- counts:begin id="suite" -->498 tests<!-- counts:end id="suite" -->
 *   block (shell comment, inside a fenced code block):
 *     # counts:begin id="commands"
 *     uv run pytest tests/ -q   # whole suite (498 tests)
 *     # counts:end id="commands"
 *
 *   tex (LaTeX comment, in main.tex — the markers sit on their own lines, as
 *   the selfcite version markers do, because `%` comments out the rest of a
 *   line):
 *     % counts:begin id="macros"
 *     \newcommand{\CountTests}{498}
 *     % counts:end id="macros"
 *
 * The manuscript's counted claims are declared ONCE, as \newcommand macros in
 * the `macros` region of `main.tex`, and the prose regions quote those macros
 * instead of a raw number: a value is therefore typed into the tree only by
 * this task, and a hand-typed digit in the prose fails `counts:check`.
 * \newcommand rather than \def or an \input'ed generated file is deliberate:
 * it refuses to shadow an already-defined name, so a collision with a package
 * fails the compile instead of silently redefining (TeX FAQ, "Package reports
 * 'command already defined'" — a redefiner that does not use \newcommand
 * changes behaviour with no error at all), the definitions stay collected in
 * the preamble rather than scattered through the document (Overleaf,
 * "Commands"), and the region is rewritten whole, which keeps the task
 * idempotent (f(f(x)) = f(x)) exactly like the README regions.
 *
 * Determinism: no Date, no locale, no network — only local measurements, so
 * f(f(x)) = f(x).  Dated reports under `docs/reports/` and the specs under
 * `docs/specs/` are snapshots of a moment and are deliberately OUTSIDE this
 * mechanism; they are corrected by hand with their reason recorded.
 *
 * Modes:
 *   (default)  rewrite the stale regions and docs/counts.md
 *   --check    compare, print the diffs, exit 1 on any drift
 */
import { existsSync, readFileSync, readdirSync, statSync, writeFileSync } from 'fs';
import { execSync } from 'child_process';

/* ------------------------------------------------------------- measurement */

function sh(cmd: string): string {
  return execSync(`${cmd} 2>&1`, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
}

/**
 * The collected count of a `pytest --collect-only` run.  pytest prints either
 * `498 tests collected in 1.27s` or, when a `-m` filter deselected some,
 * `495/498 tests collected (3 deselected) in 0.82s`; the first number is the
 * count the command actually selects, which is what the docs state.
 */
function collected(cmd: string): number {
  const out = sh(cmd);
  const matches = [...out.matchAll(/(\d+)\/(\d+) tests collected|\b(\d+) tests collected/g)];
  if (matches.length === 0) {
    throw new Error(`no "N tests collected" summary in: ${cmd}\n${out.slice(-400)}`);
  }
  const last = matches[matches.length - 1];
  return Number(last[1] ?? last[3]);
}

/**
 * Strip Lean comments (`--` to end of line, nested `/- … -/`) so the
 * declaration counters never count a word that only appears in prose.
 */
function stripLeanComments(src: string): string {
  let out = '';
  let depth = 0;
  let i = 0;
  while (i < src.length) {
    if (depth === 0) {
      if (src.startsWith('--', i)) {
        const nl = src.indexOf('\n', i);
        i = nl === -1 ? src.length : nl;
        continue;
      }
      if (src.startsWith('/-', i)) {
        depth = 1;
        i += 2;
        continue;
      }
      out += src[i];
      i += 1;
    } else {
      if (src.startsWith('/-', i)) {
        depth += 1;
        i += 2;
        continue;
      }
      if (src.startsWith('-/', i)) {
        depth -= 1;
        i += 2;
        continue;
      }
      i += 1;
    }
  }
  return out;
}

const DECLARATION = /^[ \t]*(?:@\S+[ \t]+)*(?:private[ \t]+|protected[ \t]+|noncomputable[ \t]+|noncommutative[ \t]+)*(?:theorem|lemma)[ \t]/gm;
const AXIOM = /^[ \t]*(?:@\S+[ \t]+)*axiom[ \t]/gm;
const SORRY = /\bsorry\b/g;

function matches(text: string, re: RegExp): number {
  return [...text.matchAll(re)].length;
}

function countFiles(dir: string): number {
  if (!existsSync(dir)) return 0;
  return readdirSync(dir).filter((name) => statSync(`${dir}/${name}`).isFile()).length;
}

/* ----------------------------------------------------------------- config */

/**
 * The command that collects this repository's suite.  `03-crystalline-worldsheet`
 * needs the `python -m` form (`uv run pytest` fails to spawn there); the
 * repositories without a pytest suite simply declare no pytest counter.
 */
const PYTEST = 'uv run pytest tests/ -q';

/** The census module whose collected size the docs state. */
const CENSUS = 'tests/test_section_census.py';

/** Lean sources whose statistics the docs state (comments stripped). */
const LEAN_FILES = ['lean/TorreKK_LYR_v35.lean'];

/** The manuscript whose `\testref{...}` anchors the docs state. */
const TEX = 'main.tex';

/**
 * The test modules whose `TestSection<N>` classes are the numbered sections
 * of the package `main.tex` counts ("forty-seven numbered sections"): the
 * section-to-test map of `tests/README.md` is hand-written, so the count is
 * measured from the classes themselves — a section added to the suite without
 * touching the map still moves the number.
 */
const SECTION_MODULES = /^test_sections_.*\.py$/;

interface Counter {
  id: string;
  /** How the value is measured — printed verbatim in `docs/counts.md`. */
  source: string;
  measure: () => number;
}

const COUNTERS: Counter[] = [
  {
    id: 'pytest.collected',
    source: `\`${PYTEST} --collect-only\``,
    measure: () => collected(`${PYTEST} --collect-only`),
  },
  {
    id: 'pytest.not_slow',
    source: `\`${PYTEST} -m 'not slow' --collect-only\``,
    measure: () => collected(`${PYTEST} -m 'not slow' --collect-only`),
  },
  {
    id: 'pytest.census',
    source: `\`${PYTEST.replace('tests/ -q', `${CENSUS} -q`)} --collect-only\``,
    measure: () => collected(`${PYTEST.replace('tests/ -q', `${CENSUS} -q`)} --collect-only`),
  },
  {
    id: 'testref.occurrences',
    source: `occurrences of \`\\testref{\` in \`${TEX}\``,
    measure: () => matches(readFileSync(TEX, 'utf8'), /\\testref\{/g),
  },
  {
    id: 'testref.distinct',
    source: `distinct ids inside \`\\testref{…}\` in \`${TEX}\``,
    measure: () => new Set([...readFileSync(TEX, 'utf8').matchAll(/\\testref\{([^{}]*)\}/g)].map((m) => m[1])).size,
  },
  {
    id: 'lean.theorems',
    source: `declarations in ${LEAN_FILES.map((f) => `\`${f}\``).join(', ')} (comments stripped)`,
    measure: () => LEAN_FILES.reduce((n, f) => n + matches(stripLeanComments(readFileSync(f, 'utf8')), DECLARATION), 0),
  },
  {
    id: 'lean.axioms',
    source: `axioms in ${LEAN_FILES.map((f) => `\`${f}\``).join(', ')} (comments stripped)`,
    measure: () => LEAN_FILES.reduce((n, f) => n + matches(stripLeanComments(readFileSync(f, 'utf8')), AXIOM), 0),
  },
  {
    id: 'lean.sorry',
    source: `\`sorry\` in ${LEAN_FILES.map((f) => `\`${f}\``).join(', ')} (comments stripped)`,
    measure: () => LEAN_FILES.reduce((n, f) => n + matches(stripLeanComments(readFileSync(f, 'utf8')), SORRY), 0),
  },
  {
    id: 'kkgt.sections',
    source: 'distinct `TestSection<N>` classes in `tests/test_sections_*.py`',
    measure: () => {
      const modules = readdirSync('tests').filter((name) => SECTION_MODULES.test(name));
      const sections = new Set<string>();
      for (const module of modules) {
        for (const match of readFileSync(`tests/${module}`, 'utf8').matchAll(/\bclass\s+TestSection(\d+)/g)) {
          sections.add(match[1]);
        }
      }
      if (sections.size === 0) throw new Error('no `TestSection<N>` class found under tests/');
      return sections.size;
    },
  },
  {
    id: 'images.files',
    source: 'file inventory of `images/`',
    measure: () => countFiles('images'),
  },
];

/* ---------------------------------------------------------------- regions */

type Counts = Record<string, number>;

interface Region {
  file: string;
  id: string;
  /** `inline` = one HTML-comment pair around a span of prose; `block` = a
   *  pair of shell-comment lines around whole lines inside a code fence;
   *  `tex` = a pair of `%` comment lines around whole lines of main.tex. */
  kind: 'inline' | 'block' | 'tex';
  /** The counters this region quotes (drives the "quoted in" column). */
  uses: string[];
  render: (c: Counts) => string;
}

const REGIONS: Region[] = [
  {
    file: 'README.md',
    id: 'lean',
    kind: 'inline',
    uses: ['lean.theorems', 'lean.axioms', 'lean.sorry'],
    render: (c) => `${c['lean.theorems']} theorems, ${c['lean.axioms']} axioms, ${c['lean.sorry']} \`sorry\``,
  },
  {
    file: 'README.md',
    id: 'suite',
    kind: 'inline',
    uses: ['pytest.collected', 'pytest.not_slow'],
    render: (c) => `${c['pytest.collected']} tests; ${c['pytest.not_slow']} with \`-m 'not slow'\``,
  },
  {
    file: 'tests/README.md',
    id: 'commands',
    kind: 'block',
    uses: ['pytest.collected', 'pytest.not_slow'],
    render: (c) =>
      [
        `uv run pytest tests/ -q                 # whole suite   (${c['pytest.collected']} tests)`,
        `uv run pytest tests/ -q -m 'not slow'   # without >10 s (${c['pytest.not_slow']} tests)`,
      ].join('\n'),
  },
  {
    file: 'tests/README.md',
    id: 'suite-total',
    kind: 'inline',
    uses: ['pytest.collected'],
    render: (c) => String(c['pytest.collected']),
  },
  {
    // The manuscript's declarations: the single place a count is written into
    // main.tex.  Everything the prose prints goes through these macros.
    file: 'main.tex',
    id: 'macros',
    kind: 'tex',
    uses: ['kkgt.sections', 'pytest.collected', 'pytest.not_slow', 'lean.theorems', 'lean.axioms', 'lean.sorry'],
    render: (c) =>
      [
        `\\newcommand{\\CountSections}{${c['kkgt.sections']}}`,
        `\\newcommand{\\CountTests}{${c['pytest.collected']}}`,
        `\\newcommand{\\CountNotSlow}{${c['pytest.not_slow']}}`,
        `\\newcommand{\\CountTheorems}{${c['lean.theorems']}}`,
        `\\newcommand{\\CountAxioms}{${c['lean.axioms']}}`,
        `\\newcommand{\\CountSorry}{${c['lean.sorry']}}`,
      ].join('\n'),
  },
  {
    file: 'main.tex',
    id: 'sections',
    kind: 'tex',
    uses: ['kkgt.sections'],
    render: () => '\\CountSections{} numbered sections',
  },
  {
    file: 'main.tex',
    id: 'sections-map',
    kind: 'tex',
    uses: ['kkgt.sections'],
    render: () => '\\CountSections{} sections',
  },
  {
    file: 'main.tex',
    id: 'suite-total',
    kind: 'tex',
    uses: ['pytest.collected'],
    render: () => '$\\CountTests{}$',
  },
  {
    file: 'main.tex',
    id: 'suite-not-slow',
    kind: 'tex',
    uses: ['pytest.not_slow'],
    render: () => '$\\CountNotSlow{}$',
  },
  {
    file: 'main.tex',
    id: 'lean',
    kind: 'tex',
    uses: ['lean.theorems', 'lean.axioms', 'lean.sorry'],
    render: (c) =>
      c['lean.sorry'] === 0
        ? '\\CountTheorems{} theorems and \\CountAxioms{} axioms, no \\code{sorry},'
        : '\\CountTheorems{} theorems and \\CountAxioms{} axioms, \\CountSorry{} occurrences of \\code{sorry},',
  },
  {
    file: 'main.tex',
    id: 'axioms',
    kind: 'tex',
    uses: ['lean.axioms'],
    render: () => '\\CountAxioms{} axioms,',
  },
  {
    file: 'main.tex',
    id: 'sorry-claim',
    kind: 'tex',
    uses: ['lean.sorry'],
    render: (c) =>
      c['lean.sorry'] === 0 ? 'There is no \\code{sorry}.' : 'There are \\CountSorry{} occurrences of \\code{sorry}.',
  },
];

/* ---------------------------------------------------------------- markers */

function inlineBegin(id: string): RegExp {
  return new RegExp(`<!--\\s*counts:begin\\s+id="${id}"[^>]*-->`, 'g');
}
function inlineEnd(id: string): RegExp {
  return new RegExp(`<!--\\s*counts:end\\s+id="${id}"[^>]*-->`, 'g');
}
function blockBegin(id: string): RegExp {
  return new RegExp(`^[\\t ]*#\\s*counts:begin\\s+id="${id}"[\\t ]*$`, 'gm');
}
function blockEnd(id: string): RegExp {
  return new RegExp(`^[\\t ]*#\\s*counts:end\\s+id="${id}"[\\t ]*$`, 'gm');
}
/** The `%` comment form used by main.tex (a `%` swallows the rest of its line,
 *  so — like the selfcite version markers — each marker owns a whole line). */
function texBegin(id: string): RegExp {
  return new RegExp(`^[\\t ]*%\\s*counts:begin\\s+id="${id}"[\\t ]*$`, 'gm');
}
function texEnd(id: string): RegExp {
  return new RegExp(`^[\\t ]*%\\s*counts:end\\s+id="${id}"[\\t ]*$`, 'gm');
}

interface Span {
  contentStart: number;
  contentEnd: number;
}

/** Locate the single marker pair of `region` in `text`, or throw. */
function findSpan(text: string, region: Region): Span {
  const beginRe =
    region.kind === 'inline' ? inlineBegin(region.id) : region.kind === 'block' ? blockBegin(region.id) : texBegin(region.id);
  const endRe = region.kind === 'inline' ? inlineEnd(region.id) : region.kind === 'block' ? blockEnd(region.id) : texEnd(region.id);
  const begins = [...text.matchAll(beginRe)];
  const ends = [...text.matchAll(endRe)];
  const where = `${region.file} id="${region.id}"`;
  if (begins.length !== 1 || ends.length !== 1 || begins[0].index === undefined || ends[0].index === undefined) {
    throw new Error(
      `${where}: expected exactly one marker pair, found ${begins.length} begin / ${ends.length} end marker(s)`
    );
  }
  const beginEnd = begins[0].index + begins[0][0].length;
  const endStart = ends[0].index;
  if (endStart < beginEnd) throw new Error(`${where}: marker pair is inverted (end before begin)`);

  if (region.kind !== 'inline') {
    // Markers sit on their own lines; the content is everything between them,
    // without the newline that terminates the last content line.
    const contentStart = text.charAt(beginEnd) === '\n' ? beginEnd + 1 : beginEnd;
    if (contentStart !== endStart && text.charAt(endStart - 1) !== '\n') {
      throw new Error(`${where}: a ${region.kind} marker must sit on a line of its own`);
    }
    return { contentStart, contentEnd: endStart - 1 };
  }
  const contentStart = text.charAt(beginEnd) === '\n' ? beginEnd + 1 : beginEnd;
  return { contentStart, contentEnd: endStart };
}

/** Replace the spans of `text`, back to front so earlier offsets stay valid. */
function replaceSpans(text: string, spans: { region: Region; span: Span }[]): string {
  const ordered = [...spans].sort((a, b) => b.span.contentStart - a.span.contentStart);
  let out = text;
  for (const { region, span } of ordered) {
    out = out.slice(0, span.contentStart) + region.render(COUNTS) + out.slice(span.contentEnd);
  }
  return out;
}

/* ----------------------------------------------------------------- ledger */

const LEDGER = 'docs/counts.md';

function renderLedger(): string {
  const quoted = new Map<string, string[]>();
  for (const region of REGIONS) {
    for (const id of region.uses) {
      const list = quoted.get(id) ?? [];
      const entry = `\`${region.file}\` (\`${region.id}\`)`;
      if (!list.includes(entry)) list.push(entry);
      quoted.set(id, list);
    }
  }
  const rows = COUNTERS.map(
    (counter) =>
      `| \`${counter.id}\` | ${COUNTS[counter.id]} | ${counter.source} | ${
        (quoted.get(counter.id) ?? ['—']).join(', ')
      } |`
  );
  return [
    '# Counts',
    '',
    '<!-- Generated by `pnpm run counts` (scripts/tasks/counts.ts) — do not edit.',
    '     Every value is measured from the working tree; `pnpm run counts:check`',
    '     fails with a diff when this file or a marked region has drifted.',
    '     Dated reports and specs are snapshots and stay outside the mechanism. -->',
    '',
    '| counter | value | measured from | quoted in |',
    '|---|---:|---|---|',
    ...rows,
    '',
    'The marked regions live in the documents that state the numbers: ' +
      REGIONS.map((r) => `[\`${r.file}\`](../${r.file}) \`${r.id}\``).join(', ') +
      '.  Regenerate everything with `pnpm run counts`; `validate` runs `pnpm run counts:check` after `parity`.',
    '',
    '`pnpm run build` re-syncs every region before the render (`syncCounts()` in ' +
      '`scripts/build.ts`), because the numbers the manuscript prints come from them. That makes the suite ' +
      'counters a per-build cost: three `pytest --collect-only` runs (collection only — seconds, never a ' +
      'test run). The alternative, measuring at release time, would let a PDF print a stale count, which is ' +
      'exactly the defect this mechanism exists to prevent.',
    '',
  ].join('\n');
}

/* -------------------------------------------------------------------- run */

let COUNTS: Counts = {};

function measure(): Counts {
  const counts: Counts = {};
  for (const counter of COUNTERS) {
    try {
      counts[counter.id] = counter.measure();
    } catch (error) {
      throw new Error(`counter ${counter.id} failed: ${error instanceof Error ? error.message : String(error)}`);
    }
  }
  return counts;
}

function unifiedDiff(onDisk: string, rendered: string, header: string): string {
  const a = onDisk.split('\n');
  const b = rendered.split('\n');
  const n = a.length;
  const m = b.length;
  const lcs: number[][] = Array.from({ length: n + 1 }, () => new Array<number>(m + 1).fill(0));
  for (let i = n - 1; i >= 0; i--) {
    for (let j = m - 1; j >= 0; j--) {
      lcs[i][j] = a[i] === b[j] ? lcs[i][j + 1] + 1 : Math.max(lcs[i + 1][j], lcs[i][j + 1]);
    }
  }
  const body: string[] = [];
  let i = 0;
  let j = 0;
  while (i < n && j < m) {
    if (a[i] === b[j]) {
      body.push(` ${a[i]}`);
      i++;
      j++;
    } else if (lcs[i + 1][j] >= lcs[i][j + 1]) {
      body.push(`-${a[i]}`);
      i++;
    } else {
      body.push(`+${b[j]}`);
      j++;
    }
  }
  while (i < n) body.push(`-${a[i++]}`);
  while (j < m) body.push(`+${b[j++]}`);
  return `--- ${header} (on disk)\n+++ ${header} (rendered from the measurements)\n@@ -1,${n} +1,${m} @@\n${body.join('\n')}\n`;
}

interface RunResult {
  staleFiles: string[];
  staleRegions: string[];
  staleLedger: boolean;
  changed: boolean;
}

function run(check: boolean): RunResult {
  COUNTS = measure();

  const staleFiles: string[] = [];
  const staleRegions: string[] = [];
  const byFile = new Map<string, { region: Region; span: Span }[]>();
  for (const region of REGIONS) {
    if (!existsSync(region.file)) throw new Error(`missing document: ${region.file}`);
    const text = readFileSync(region.file, 'utf8');
    const span = findSpan(text, region);
    const onDisk = text.slice(span.contentStart, span.contentEnd);
    if (onDisk !== region.render(COUNTS)) {
      staleRegions.push(`${region.file} id="${region.id}"`);
      if (check) process.stdout.write(unifiedDiff(onDisk, region.render(COUNTS), `${region.file} id="${region.id}"`));
      const list = byFile.get(region.file) ?? [];
      list.push({ region, span });
      byFile.set(region.file, list);
    }
  }

  if (!check) {
    for (const [file, spans] of byFile) {
      writeFileSync(file, replaceSpans(readFileSync(file, 'utf8'), spans));
      staleFiles.push(file);
    }
  } else {
    staleFiles.push(...new Set(staleRegions.map((entry) => entry.split(' id=')[0])));
  }

  const ledger = renderLedger();
  const ledgerOnDisk = existsSync(LEDGER) ? readFileSync(LEDGER, 'utf8') : '';
  const staleLedger = ledgerOnDisk !== ledger;
  if (check && staleLedger) process.stdout.write(unifiedDiff(ledgerOnDisk, ledger, LEDGER));
  if (!check && staleLedger) {
    writeFileSync(LEDGER, ledger);
    staleFiles.push(LEDGER);
  }

  return { staleFiles, staleRegions, staleLedger, changed: staleFiles.length > 0 };
}

function main(): number {
  const check = process.argv.includes('--check');
  try {
    const result = run(check);
    if (check) {
      if (result.staleRegions.length > 0 || result.staleLedger) {
        process.stderr.write(
          `counts:check failed — stale: ${[...result.staleRegions, ...(result.staleLedger ? [LEDGER] : [])].join(', ')}. ` +
            `Run \`pnpm run counts\`.\n`
        );
        return 1;
      }
      console.log(
        `counts:check ✓ ${REGIONS.length} marked region(s) and ${LEDGER} match the measured values ` +
          `(${Object.entries(COUNTS).map(([id, value]) => `${id}=${value}`).join(', ')}).`
      );
      return 0;
    }
    if (result.changed) console.log(`counts ✓ updated: ${result.staleFiles.join(', ')}`);
    else console.log(`counts ✓ ${LEDGER} and every marked region already up to date.`);
    return 0;
  } catch (error) {
    process.stderr.write(`counts: ${error instanceof Error ? error.message : String(error)}\n`);
    return 1;
  }
}

/**
 * Called by `scripts/build.ts` before the render, exactly where it calls
 * `syncSelfCitations()`: the count regions are a build artifact, so the
 * manuscript is brought up to date with the measurements before it is
 * compiled, and a stale number can never reach the PDF.
 */
export function syncCounts(): void {
  const result = run(false);
  console.log(
    result.changed
      ? `  ✓ count regions regenerated (${[...new Set(result.staleRegions.map((entry) => entry.split(' id=')[0]))].join(', ')}${
          result.staleLedger ? `, ${LEDGER}` : ''
        }).`
      : '  ✓ count regions up to date.'
  );
}

// Only run when invoked directly (tsx scripts/tasks/counts.ts), not when
// build.ts imports syncCounts().
const invokedDirectly = process.argv[1] !== undefined && process.argv[1].endsWith('counts.ts');
if (invokedDirectly) {
  process.exit(main());
}
