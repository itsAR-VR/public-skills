#!/usr/bin/env node

import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import os from 'node:os';
import { execFileSync } from 'node:child_process';

const repoRoot = path.resolve(import.meta.dirname, '..');
const sourceRoot = path.resolve(process.argv[2] ?? '../goatedskills');
const outputSkills = path.join(repoRoot, 'skills');

if (!fs.existsSync(path.join(sourceRoot, '.git'))) {
  console.error(`Usage: ${path.basename(process.argv[1])} /path/to/goatedskills`);
  process.exit(2);
}

const sourceRevision = execFileSync('git', ['rev-parse', 'origin/main'], {
  cwd: sourceRoot,
  encoding: 'utf8',
}).trim();
const archiveRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'public-skills-export-'));
const archivePath = path.join(archiveRoot, 'skills.tar');
fs.writeFileSync(archivePath, execFileSync('git', ['archive', '--format=tar', 'origin/main', 'skills'], {
  cwd: sourceRoot,
  maxBuffer: 512 * 1024 * 1024,
}));
execFileSync('tar', ['-xf', archivePath, '-C', archiveRoot]);
const sourceSkills = path.join(archiveRoot, 'skills');

const explicitRemovals = new Map([
  ['ai-audit', 'contains a company-specific client audit delivery system'],
  ['ai-readiness-report', 'contains a company-specific client report and brand renderer'],
  ['audit-chain-eval-harness', 'tests the private client audit delivery chain'],
  ['business-context-intelligence', 'contains private company-context routing'],
  ['canonical-meeting-archive', 'contains private meeting archive conventions'],
  ['codex-rr-setup', 'contains private account-pool and workstation routing'],
  ['codex-workstation-bootstrap', 'contains private workstation restore behavior'],
  ['feasibility-tester', 'contains a company-specific client feasibility delivery system'],
  ['granola-github-meetings-sync', 'contains private meeting sync conventions'],
  ['hormozi-book-brain', 'bundles copyrighted books and a derived database'],
  ['infinity-investment-memo', 'contains a private investor-deck source bundle'],
  ['knowledge-base', 'contains a local derived knowledge database'],
  ['knowledge-base.quarantine-20260225-043142', 'quarantined local database snapshot'],
  ['memory-chain', 'contains a company-specific client research and report chain'],
  ['kensho-eod-delivery-brief', 'person-specific internal operating workflow'],
  ['kensho-spin', 'person-specific internal operating workflow'],
  ['mo-book-creator', 'person-specific writing workflow'],
  ['mo-book-crisis-scenario-stress-testing', 'person-specific writing workflow'],
  ['mo-book-digital-acceleration-readiness', 'person-specific writing workflow'],
  ['mo-book-ecom-lifecycle-flows', 'person-specific writing workflow'],
  ['mo-book-email-behavioral-segmentation', 'person-specific writing workflow'],
  ['mo-book-email-corrections-apology', 'person-specific writing workflow'],
  ['mo-book-email-deliverability-setup', 'person-specific writing workflow'],
  ['mo-book-email-diagnostic-audit', 'person-specific writing workflow'],
  ['mo-book-email-frequency-strategy', 'person-specific writing workflow'],
  ['mo-book-email-lifecycle-analytics', 'person-specific writing workflow'],
  ['mo-book-email-preference-center', 'person-specific writing workflow'],
  ['mo-book-email-qa-checklist', 'person-specific writing workflow'],
  ['mo-book-email-rendering-design', 'person-specific writing workflow'],
  ['mo-book-email-subject-line-optimizer', 'person-specific writing workflow'],
  ['mo-book-how-to-win-friends-digital-age', 'person-specific writing workflow'],
  ['mo-book-mckinsey-way', 'person-specific writing workflow'],
  ['mo-book-mckinsey-way-consultant-career', 'person-specific writing workflow'],
  ['mo-book-mckinsey-way-consulting-workflow', 'person-specific writing workflow'],
  ['mo-book-mckinsey-way-presenting-solutions', 'person-specific writing workflow'],
  ['mo-book-mckinsey-way-problem-solving', 'person-specific writing workflow'],
  ['mo-book-stakeholder-decision-scorecard', 'person-specific writing workflow'],
  ['mo-book-supply-chain-resilience-evaluator', 'person-specific writing workflow'],
  ['mo-book-surveillance-privacy-tradeoff', 'person-specific writing workflow'],
  ['mo-book-systemic-risk-interconnection-mapper', 'person-specific writing workflow'],
  ['mo-infinity-investor-deck', 'person-specific private investor workflow'],
  ['mo-nano-banana-pro', 'person-specific operating workflow'],
  ['mo-post-call-auditor', 'person-specific internal call workflow'],
  ['mo-pre-call-strategist', 'person-specific internal call workflow'],
  ['mo-writing-voice-system', 'person-specific writing voice'],
  ['mo-youtube-gemini-video-analyst', 'person-specific operating workflow'],
  ['setup-skill-packs', 'contains private workstation and source-repository setup'],
  ['skill-portfolio-evals', 'contains private team handoffs and quality-routing context'],
  ['z2a-loop', 'company-specific orchestration workflow'],
  ['zta-ai-audit-deck', 'company-specific client-delivery workflow'],
  ['zta-pdf', 'company-specific client-delivery workflow'],
]);

const editedSkills = new Map([
  ['deep-build', 'deep-build'],
  ['deep-sweep', 'deep-sweep'],
  ['z2a-dev-workflow', 'dev-workflow'],
]);

const privatePatterns = [
  ['company name', /ZeroToAgent|Zero To Agent|\bZ2A\b|\bZTA(?:repo|[-_][A-Za-z0-9-]+)?\b|zerotoagent\.com/iu],
  ['private operator path', /(?:\/Users\/[^/\s]+|\/home\/[^/\s]+|[A-Z]:\\Users\\[^\\\s]+)/iu],
  ['private client path', /docs\/(?:clients|meetings)\//iu],
  ['person or client name', /\b(?:Momin|Moahid|Kensho|Manco|Invenio)\b/iu],
  ['operator identifier', /\bAR180\b/iu],
  ['operator identifier', /\bmmoahid11\b/iu],
  ['reusable credential', /(?:github_pat_|ghp_|xox[baprs]-|sk-[A-Za-z0-9_-]{20,})/u],
];

const scrubReplacements = [
  [/itsAR-VR\/goatedskills/giu, 'itsAR-VR/public-skills'],
  [/\bgoatedskills\b/giu, 'public-skills'],
  [/z2a-loop/giu, 'workflow-orchestrator'],
  [/ZeroToAgent|Zero To Agent/giu, 'the organization'],
  [/\bZ2A\b/giu, 'the project'],
  [/\bZTA(?:repo|[-_][A-Za-z0-9-]+)?\b/giu, 'PROJECT'],
  [/zerotoagent\.com/giu, 'example.com'],
  [/\/Users\/[^/\s]+/gu, '/Users/operator'],
  [/\/home\/[^/\s]+/gu, '/home/operator'],
  [/[A-Z]:\\Users\\[^\\\s]+/giu, 'C:\\Users\\operator'],
  [/\bAR180\b/giu, 'contributor'],
  [/\bmmoahid11\b/giu, 'contributor'],
  [/docs\/clients\//giu, 'private/client-records/'],
  [/docs\/meetings\//giu, 'private/meeting-records/'],
  [/\b(?:Momin|Moahid|Kensho)\b/giu, 'operator'],
  [/\b(?:Manco|Invenio)\b/giu, 'client'],
];

const textExtensions = new Set([
  '', '.cjs', '.css', '.csv', '.html', '.ini', '.js', '.json', '.jsonl', '.md', '.mjs',
  '.py', '.rb', '.sh', '.sql', '.svg', '.toml', '.ts', '.tsx', '.txt', '.xml', '.yaml', '.yml',
]);

function walk(directory) {
  const files = [];
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const absolute = path.join(directory, entry.name);
    if (entry.isSymbolicLink()) throw new Error(`Symlink is not public-exportable: ${absolute}`);
    if (entry.isDirectory()) files.push(...walk(absolute));
    else if (entry.isFile()) files.push(absolute);
  }
  return files;
}

function inspectSkill(directory) {
  for (const file of walk(directory)) {
    const extension = path.extname(file).toLowerCase();
    const relativePath = path.relative(directory, file);
    for (const [label, pattern] of privatePatterns) {
      if (pattern.test(relativePath)) return `path contains ${label}`;
    }
    if (!textExtensions.has(extension)) return `contains unreviewed binary or data asset ${path.basename(file)}`;
    if (fs.statSync(file).size > 2_000_000) return `contains oversized unreviewed text asset ${path.basename(file)}`;
    const content = fs.readFileSync(file, 'utf8');
    for (const [label, pattern] of privatePatterns) {
      if (pattern.test(content)) return `contains ${label}`;
    }
  }
  return null;
}

function needsScrub(directory) {
  for (const file of walk(directory)) {
    if (fs.statSync(file).size > 2_000_000 || !textExtensions.has(path.extname(file).toLowerCase())) continue;
    const content = fs.readFileSync(file, 'utf8');
    if (scrubReplacements.some(([pattern]) => {
      pattern.lastIndex = 0;
      return pattern.test(content);
    })) return true;
  }
  return false;
}

function scrubDirectory(directory) {
  for (const file of walk(directory)) {
    if (fs.statSync(file).size > 2_000_000 || !textExtensions.has(path.extname(file).toLowerCase())) continue;
    let content = fs.readFileSync(file, 'utf8');
    for (const [pattern, replacement] of scrubReplacements) content = content.replace(pattern, replacement);
    fs.writeFileSync(file, content);
  }
}

function hashDirectory(directory) {
  const hash = crypto.createHash('sha256');
  for (const file of walk(directory).sort()) {
    hash.update(path.relative(directory, file));
    hash.update('\0');
    hash.update(fs.readFileSync(file));
    hash.update('\0');
  }
  return hash.digest('hex');
}

fs.rmSync(outputSkills, { recursive: true, force: true });
fs.mkdirSync(outputSkills, { recursive: true });

const removed = [];
const kept = [];
const edited = [];

for (const entry of fs.readdirSync(sourceSkills, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
  if (!entry.isDirectory()) continue;
  const sourceName = entry.name;
  const sourceDirectory = path.join(sourceSkills, sourceName);

  if (!fs.existsSync(path.join(sourceDirectory, 'SKILL.md')) && !editedSkills.has(sourceName)) {
    removed.push({ name: sourceName, reason: 'not a loader-facing skill package' });
    continue;
  }

  if (explicitRemovals.has(sourceName)) {
    removed.push({ name: sourceName, reason: explicitRemovals.get(sourceName) });
    continue;
  }

  if (editedSkills.has(sourceName)) {
    const publicName = editedSkills.get(sourceName);
    const override = path.join(repoRoot, 'overrides', publicName);
    fs.cpSync(override, path.join(outputSkills, publicName), { recursive: true });
    edited.push({ source: sourceName, public: publicName, reason: 'removed company branding and repo-specific implementation details' });
    kept.push({
      name: publicName,
      sourceRevision,
      sourcePath: `skills/${sourceName}`,
      destinationPath: `skills/${publicName}`,
      sha256: hashDirectory(path.join(outputSkills, publicName)),
    });
    continue;
  }

  const destination = path.join(outputSkills, sourceName);
  const scrub = needsScrub(sourceDirectory);
  if (scrub) {
    fs.cpSync(sourceDirectory, destination, { recursive: true });
    scrubDirectory(destination);
    const rejection = inspectSkill(destination);
    if (rejection) {
      fs.rmSync(destination, { recursive: true, force: true });
      removed.push({ name: sourceName, reason: rejection });
      continue;
    }
    edited.push({ source: sourceName, public: sourceName, reason: 'scrubbed company, operator, client, or private-path references' });
    kept.push({
      name: sourceName,
      sourceRevision,
      sourcePath: `skills/${sourceName}`,
      destinationPath: `skills/${sourceName}`,
      sha256: hashDirectory(destination),
    });
    continue;
  }

  const rejection = inspectSkill(sourceDirectory);
  if (rejection) {
    removed.push({ name: sourceName, reason: rejection });
    continue;
  }

  fs.cpSync(sourceDirectory, destination, { recursive: true });
  kept.push({
    name: sourceName,
    sourceRevision,
    sourcePath: `skills/${sourceName}`,
    destinationPath: `skills/${sourceName}`,
    sha256: hashDirectory(destination),
  });
}

const report = {
  schemaVersion: 'public-skills-export/v1',
  generatedAt: new Date().toISOString(),
  source: { catalog: 'private canonical catalog', revision: sourceRevision },
  counts: { kept: kept.length, removed: removed.length, edited: edited.length },
  edited,
  removed,
  kept,
};

fs.writeFileSync(path.join(repoRoot, 'PUBLIC_EXPORT.json'), `${JSON.stringify(report, null, 2)}\n`);
fs.rmSync(archiveRoot, { recursive: true, force: true });
console.log(`Exported ${kept.length}; removed ${removed.length}; edited ${edited.length}.`);
