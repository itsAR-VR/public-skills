#!/usr/bin/env node

import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import os from 'node:os';
import { execFileSync } from 'node:child_process';

const repoRoot = path.resolve(import.meta.dirname, '..');
const sourceRoot = path.resolve(process.argv[2] ?? '../private-skill-source');
const outputSkills = path.join(repoRoot, 'skills');
const allowlistPath = path.join(repoRoot, 'policy', 'public-skill-allowlist.txt');
const allowlist = new Set(fs.readFileSync(allowlistPath, 'utf8')
  .split(/\r?\n/u)
  .map((line) => line.trim())
  .filter((line) => line && !line.startsWith('#')));

if (!fs.existsSync(path.join(sourceRoot, '.git'))) {
  console.error(`Usage: ${path.basename(process.argv[1])} /path/to/private-skill-source`);
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

const explicitRemovals = new Map();

const editedSkills = new Map([
  ['deep-build', 'deep-build'],
  ['deep-clean', 'deep-clean'],
  ['deep-sweep', 'deep-sweep'],
  ['goal-post', 'goal-post'],
  ['brave-search', 'brave-search'],
  ['browser-harness', 'browser-harness'],
  ['gitnexus', 'gitnexus'],
  ['verify', 'verify'],
]);

const privatePatterns = [
  ['private operator path', /(?:\/Users\/[^/\s]+|\/home\/[^/\s]+|[A-Z]:\\Users\\[^\\\s]+)/iu],
  ['reusable credential', /(?:github_pat_|ghp_|xox[baprs]-|sk-[A-Za-z0-9_-]{20,})/u],
];

const scrubReplacements = [
  [/\/Users\/[^/\s]+/gu, '/Users/operator'],
  [/\/home\/[^/\s]+/gu, '/home/operator'],
  [/[A-Z]:\\Users\\[^\\\s]+/giu, 'C:\\Users\\operator'],
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

  const publicName = editedSkills.get(sourceName) ?? sourceName;
  if (!allowlist.has(sourceName) && !allowlist.has(publicName)) {
    removed.push({ name: sourceName, reason: 'not in the curated public allowlist' });
    continue;
  }

  if (explicitRemovals.has(sourceName)) {
    removed.push({ name: sourceName, reason: explicitRemovals.get(sourceName) });
    continue;
  }

  if (editedSkills.has(sourceName)) {
    const override = path.join(repoRoot, 'overrides', publicName);
    fs.cpSync(override, path.join(outputSkills, publicName), { recursive: true });
    edited.push({ source: sourceName, public: publicName, reason: 'removed company branding and repo-specific implementation details' });
    kept.push({
      name: publicName,
      sourceType: 'public_override',
      sourceRevision: 'public-override',
      sourcePath: `overrides/${publicName}`,
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
      sourceType: 'private_catalog',
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
    sourceType: 'private_catalog',
    sourceRevision,
    sourcePath: `skills/${sourceName}`,
    destinationPath: `skills/${sourceName}`,
    sha256: hashDirectory(destination),
  });
}

if (allowlist.has('dev-workflow')) {
  const publicName = 'dev-workflow';
  const override = path.join(repoRoot, 'overrides', publicName);
  const destination = path.join(outputSkills, publicName);
  fs.cpSync(override, destination, { recursive: true });
  edited.push({ source: 'private development workflow', public: publicName, reason: 'published as a generic self-contained workflow' });
  kept.push({
    name: publicName,
    sourceType: 'public_override',
    sourceRevision: 'public-override',
    sourcePath: `overrides/${publicName}`,
    destinationPath: `skills/${publicName}`,
    sha256: hashDirectory(destination),
  });
}

const removedSummary = Object.entries(removed.reduce((summary, item) => {
  summary[item.reason] = (summary[item.reason] ?? 0) + 1;
  return summary;
}, {})).map(([reason, count]) => ({ reason, count })).sort((a, b) => b.count - a.count || a.reason.localeCompare(b.reason));

const report = {
  schemaVersion: 'public-skills-export/v1',
  generatedAt: new Date().toISOString(),
  source: { catalog: 'private canonical catalog', revision: sourceRevision },
  counts: { kept: kept.length, removed: removed.length, edited: edited.length },
  edited,
  removedSummary,
  kept,
};

fs.writeFileSync(path.join(repoRoot, 'PUBLIC_EXPORT.json'), `${JSON.stringify(report, null, 2)}\n`);
fs.rmSync(archiveRoot, { recursive: true, force: true });
console.log(`Exported ${kept.length}; removed ${removed.length}; edited ${edited.length}.`);
