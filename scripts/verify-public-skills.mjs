#!/usr/bin/env node

import fs from 'node:fs';
import crypto from 'node:crypto';
import path from 'node:path';
import process from 'node:process';

const repoRoot = path.resolve(import.meta.dirname, '..');
const report = JSON.parse(fs.readFileSync(path.join(repoRoot, 'PUBLIC_EXPORT.json'), 'utf8'));
const skillsRoot = path.join(repoRoot, 'skills');
const failures = [];
const allowlist = new Set(fs.readFileSync(path.join(repoRoot, 'policy', 'public-skill-allowlist.txt'), 'utf8')
  .split(/\r?\n/u)
  .map((line) => line.trim())
  .filter((line) => line && !line.startsWith('#')));

const forbidden = [
  /(?:\/Users\/(?!operator(?:\/|$))[^/\s]+|\/home\/(?!operator(?:\/|$))[^/\s]+|[A-Z]:\\Users\\(?!operator(?:\\|$))[^\\\s]+)/iu,
  /(?:github_pat_|ghp_|xox[baprs]-|sk-[A-Za-z0-9_-]{20,})/u,
];
const textExtensions = new Set([
  '', '.cjs', '.css', '.csv', '.html', '.ini', '.js', '.json', '.jsonl', '.md', '.mjs',
  '.py', '.rb', '.sh', '.sql', '.svg', '.toml', '.ts', '.tsx', '.txt', '.xml', '.yaml', '.yml',
]);

function walk(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const absolute = path.join(directory, entry.name);
    if (entry.isSymbolicLink()) {
      failures.push(`symlink: ${path.relative(repoRoot, absolute)}`);
      return [];
    }
    return entry.isDirectory() ? walk(absolute) : [absolute];
  });
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

for (const file of walk(skillsRoot)) {
  if (!textExtensions.has(path.extname(file).toLowerCase())) failures.push(`unreviewed binary or data asset: ${path.relative(repoRoot, file)}`);
  if (fs.statSync(file).size > 2_000_000) failures.push(`oversized unreviewed file: ${path.relative(repoRoot, file)}`);
  if (fs.statSync(file).size > 2_000_000 || !textExtensions.has(path.extname(file).toLowerCase())) continue;
  const content = fs.readFileSync(file, 'utf8');
  for (const pattern of forbidden) {
    if (pattern.test(content)) failures.push(`forbidden content: ${path.relative(repoRoot, file)}`);
  }
}

const directories = fs.readdirSync(skillsRoot, { withFileTypes: true }).filter((entry) => entry.isDirectory());
if (directories.length !== report.counts.kept) {
  failures.push(`count mismatch: report=${report.counts.kept}, disk=${directories.length}`);
}
for (const skill of report.kept) {
  const directory = path.join(skillsRoot, skill.name);
  if (!fs.existsSync(path.join(directory, 'SKILL.md'))) {
    failures.push(`missing SKILL.md: ${skill.name}`);
    continue;
  }
  for (const field of ['sourceRevision', 'sourcePath', 'destinationPath', 'sha256']) {
    if (!skill[field]) failures.push(`missing ${field}: ${skill.name}`);
  }
  if (skill.sourceType === 'private_catalog' && skill.sourceRevision !== report.source.revision) failures.push(`source revision mismatch: ${skill.name}`);
  if (skill.sourceType === 'public_override' && skill.sourceRevision !== 'public-override') failures.push(`override provenance mismatch: ${skill.name}`);
  if (skill.destinationPath !== `skills/${skill.name}`) failures.push(`destination path mismatch: ${skill.name}`);
  if (!allowlist.has(skill.name) && !allowlist.has(path.basename(skill.sourcePath))) {
    failures.push(`skill is not allowlisted: ${skill.name}`);
  }
  if (hashDirectory(directory) !== skill.sha256) failures.push(`checksum mismatch: ${skill.name}`);
}
for (const required of ['deep-build', 'deep-clean', 'deep-sweep', 'goal-post', 'dev-workflow']) {
  if (!fs.existsSync(path.join(skillsRoot, required, 'SKILL.md'))) failures.push(`missing required skill: ${required}`);
}
if (failures.length) {
  console.error(failures.join('\n'));
  process.exit(1);
}
console.log(`Verified ${directories.length} public skills with no blocked content.`);
