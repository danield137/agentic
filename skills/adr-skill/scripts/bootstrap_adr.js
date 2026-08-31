#!/usr/bin/env node
/**
 * Bootstrap ADRs in a repo:
 * - create ADR directory
 * - create adr/README.md (index)
 * - create first ADR: "Adopt architecture decision records"
 */

const fs = require('node:fs');
const path = require('node:path');

function die(msg) {
  process.stderr.write(`${msg}\n`);
  process.exit(1);
}

function parseArgs(argv) {
  const out = {
    repoRoot: '.',
    dir: 'adr',
    forceIndex: false,
    indexFile: null,
    firstTitle: 'Adopt architecture decision records',
    firstStatus: 'accepted',
    decisionMakers: '',
    consulted: '',
    informed: '',
    strategy: 'date',
    json: false,
  };

  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    const next = () => {
      if (i + 1 >= argv.length) die(`Missing value for ${a}`);
      return argv[++i];
    };

    if (a === '--repo-root') out.repoRoot = next();
    else if (a === '--dir') out.dir = next();
    else if (a === '--force-index') out.forceIndex = true;
    else if (a === '--index-file') out.indexFile = next();
    else if (a === '--first-title') out.firstTitle = next();
    else if (a === '--first-status') out.firstStatus = next();
    else if (a === '--decision-makers') out.decisionMakers = next();
    else if (a === '--consulted') out.consulted = next();
    else if (a === '--informed') out.informed = next();
    else if (a === '--strategy') out.strategy = next();
    else if (a === '--json') out.json = true;
    else if (a === '--help' || a === '-h') {
      process.stdout.write(
        [
          'Usage: node bootstrap_adr.js [options]',
          '',
          'Options:',
          '  --repo-root <path>        Repo root (default: .)',
          '  --dir <path>              ADR directory (default: adr)',
          '  --index-file <path>       Override index file path (relative to repo root unless absolute)',
          '  --force-index             Overwrite index file if it exists',
          '  --first-title <text>      Title for initial ADR',
          '  --first-status <text>     Status for initial ADR (default: accepted)',
          '  --decision-makers <text>  Decision makers',
          '  --consulted <text>        Consulted people or teams',
          '  --informed <text>         Informed people or teams',
          '  --strategy date|slug|auto Filename strategy for initial ADR (default: date)',
          '  --json                    Output machine-readable JSON (default: off)',
          '',
        ].join('\n'),
      );
      process.exit(0);
    } else {
      die(`Unknown arg: ${a}`);
    }
  }

  if (!['auto', 'date', 'slug'].includes(out.strategy))
    die(`Invalid --strategy: ${out.strategy}`);
  return out;
}

function loadReadmeTemplate() {
  const skillRoot = path.resolve(__dirname, '..');
  const templatePath = path.join(
    skillRoot,
    'assets',
    'templates',
    'adr-readme.md',
  );
  if (!fs.existsSync(templatePath))
    die(`README template not found: ${templatePath}`);
  return fs.readFileSync(templatePath, 'utf8');
}

function writeIndex(indexFile, adrDirName, { force }) {
  if (fs.existsSync(indexFile) && !force) return;
  const content = loadReadmeTemplate().replaceAll('{ADR_DIR}', adrDirName);
  fs.mkdirSync(path.dirname(indexFile), { recursive: true });
  fs.writeFileSync(indexFile, `${content.trimEnd()}\n`, 'utf8');
}

function slugify(text) {
  const t = String(text || '')
    .trim()
    .toLowerCase();
  const noQuotes = t.replace(/['"`]/g, '');
  const dashed = noQuotes.replace(/[^a-z0-9]+/g, '-').replace(/-{2,}/g, '-');
  const trimmed = dashed.replace(/^-+/, '').replace(/-+$/, '');
  return trimmed || 'decision';
}

function toPosix(p) {
  return p.split(path.sep).join('/');
}

function generateFirstAdr({
  title,
  status,
  date,
  decisionMakers,
  consulted,
  informed,
  adrDir,
}) {
  return `---
status: ${status}
date: ${date}
decision-makers: ${decisionMakers}
consulted: ${consulted}
informed: ${informed}
---

# ${title}

## Context and Problem Statement

Architecture decisions in this project are made implicitly through code, conversations, and tribal knowledge. When a new contributor or coding agent joins the codebase, there is no durable record of why things are built the way they are.

How should this repository record important architecture decisions so the reasoning stays close to the code?

## Decision Drivers

* Decisions should be easy to find in the same repository as the code they affect
* Records should be short enough that people maintain them
* The format should preserve why an option was chosen, not just what was chosen
* Superseded decisions should remain discoverable for future readers

## Considered Options

* Keep decisions implicit in code and conversations
* Store decisions in an external wiki or document system
* Adopt Architecture Decision Records in \`${adrDir}/\` using the MADR bare template

## Decision Outcome

Chosen option: "Adopt Architecture Decision Records in \`${adrDir}/\` using the MADR bare template", because it keeps decisions version-controlled next to the code, captures the drivers behind each choice, and includes enough structure to compare options without becoming a heavyweight RFC process.

### Consequences

* Good, because decisions are discoverable and version-controlled alongside the code
* Good, because contributors and coding agents can understand why architecture choices were made
* Good, because the team has a shared decision log that reduces relitigation
* Bad, because writing ADRs takes time
* Bad, because outdated decisions need explicit follow-up ADRs or notes when they are superseded

### Confirmation

This decision is confirmed when the ADR directory, index, and this first ADR are committed to the repository.

## Pros and Cons of the Options

### Keep decisions implicit in code and conversations

* Good, because it requires no new process
* Neutral, because some reasoning may still appear in comments or pull requests
* Bad, because context is lost and decisions get relitigated

### Store decisions in an external wiki or document system

* Good, because non-code collaborators may find wiki pages easier to edit
* Neutral, because external docs can work if ownership is clear
* Bad, because they drift away from code and are harder for coding agents to discover

### Adopt Architecture Decision Records in \`${adrDir}/\` using the MADR bare template

* Good, because decisions live with the code they govern
* Good, because the bare template captures drivers, outcome, consequences, confirmation, and option tradeoffs
* Neutral, because ADRs add a small amount of documentation work
* Bad, because the team must remember to supersede or update stale decisions

## More Information

* MADR: <https://adr.github.io/madr/>
* Bare template: <https://github.com/adr/madr/blob/develop/template/adr-template-bare.md>`;
}

function updateIndexFile(indexFile, { relLink, title, status, date }) {
  if (!fs.existsSync(indexFile)) return;
  let content = fs.readFileSync(indexFile, 'utf8');
  if (content.includes(relLink)) return;

  const entryLine = `- [${title}](${relLink}) (${status}, ${date})`;
  const normalized = content.replace(/\r\n/g, '\n');
  const lines = normalized.split('\n');
  const headingIdx = lines.findIndex(l => /^##\s+ADRs\s*$/i.test(l));

  if (headingIdx !== -1) {
    let insertAt = headingIdx + 1;
    while (insertAt < lines.length && lines[insertAt].trim() === '') insertAt++;
    lines.splice(insertAt, 0, entryLine);
  } else {
    lines.push(entryLine);
  }

  fs.writeFileSync(indexFile, lines.join('\n'), 'utf8');
}

function main() {
  const args = parseArgs(process.argv);

  const repoRoot = path.resolve(process.cwd(), args.repoRoot);
  if (!fs.existsSync(repoRoot)) die(`Repo root does not exist: ${repoRoot}`);

  const adrDir = path.resolve(repoRoot, args.dir);
  fs.mkdirSync(adrDir, { recursive: true });

  const indexFile = args.indexFile
    ? path.isAbsolute(args.indexFile)
      ? args.indexFile
      : path.resolve(repoRoot, args.indexFile)
    : path.join(adrDir, 'README.md');

  const indexExistedBefore = fs.existsSync(indexFile);
  writeIndex(indexFile, args.dir, { force: args.forceIndex });
  const indexWritten =
    fs.existsSync(indexFile) && (!indexExistedBefore || args.forceIndex);

  const relIndex = path.isAbsolute(indexFile)
    ? path.relative(repoRoot, indexFile)
    : indexFile;
  const today = new Date().toISOString().slice(0, 10);

  const firstAdrContent = generateFirstAdr({
    title: args.firstTitle,
    status: args.firstStatus,
    date: today,
    decisionMakers: args.decisionMakers,
    consulted: args.consulted,
    informed: args.informed,
    adrDir: args.dir,
  });

  const strategy = args.strategy === 'auto' ? 'date' : args.strategy;
  let firstAdrFilename;
  if (strategy === 'date') {
    firstAdrFilename = `${today}-${slugify(args.firstTitle)}.md`;
  } else {
    firstAdrFilename = `${slugify(args.firstTitle)}.md`;
  }
  const firstAdrPath = path.join(adrDir, firstAdrFilename);
  fs.writeFileSync(firstAdrPath, `${firstAdrContent.trimEnd()}\n`, 'utf8');

  const relLink = toPosix(path.relative(path.dirname(indexFile), firstAdrPath));
  updateIndexFile(indexFile, {
    relLink,
    title: args.firstTitle,
    status: args.firstStatus,
    date: today,
  });

  if (args.json) {
    const payload = {
      repoRoot,
      adrDir,
      adrDirRelPath: toPosix(path.relative(repoRoot, adrDir)),
      indexPath: indexFile,
      indexRelPath: toPosix(relIndex),
      indexExistedBefore,
      indexWritten,
      firstAdr: {
        createdAdrPath: firstAdrPath,
        createdAdrRelPath: toPosix(path.relative(repoRoot, firstAdrPath)),
        title: args.firstTitle,
        status: args.firstStatus,
        strategy,
        date: today,
      },
      date: today,
    };
    process.stdout.write(`${JSON.stringify(payload)}\n`);
    return;
  }

  process.stdout.write(`${firstAdrPath}\n`);
  process.stdout.write(`Bootstrapped ADRs at ${adrDir} (${today})\n`);
  process.stdout.write(`Index: ${indexFile}\n`);
}

main();
