#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import crypto from "node:crypto";

const args = new Set(process.argv.slice(2));
const apply = args.has("--apply");
const home = os.homedir();
const timestamp = new Date().toISOString().replace(/[:.]/g, "-");

function argValue(name, fallback = null) {
  const prefix = `${name}=`;
  for (const arg of process.argv.slice(2)) {
    if (arg.startsWith(prefix)) return arg.slice(prefix.length);
  }
  const idx = process.argv.indexOf(name);
  if (idx >= 0 && process.argv[idx + 1]) return process.argv[idx + 1];
  return fallback;
}

const rootArg = argValue("--roots", null);
const requestedRoots = (rootArg ? rootArg.split(",") : [
  path.join(home, ".hermes", "skills"),
  path.join(home, ".codex", "skills"),
  path.join(home, ".claude", "skills"),
  path.join(home, ".openclaw", "skills"),
]).map((p) => path.resolve(p));

const roots = [];
const seenRootRealpaths = new Set();
for (const root of requestedRoots) {
  if (!exists(root)) continue;
  const real = fs.realpathSync(root);
  if (seenRootRealpaths.has(real)) continue;
  seenRootRealpaths.add(real);
  roots.push(root);
}

const archiveRoot = path.resolve(argValue("--archive-dir", path.join(home, ".skill-consolidation-archive", timestamp)));
const reportArg = argValue("--report", null);
const defaultReportPath = path.join(home, "agent-command-center", "skill-consolidation-report.json");
const reportPath = path.resolve(reportArg ?? defaultReportPath);

const EMBEDDED_HOME_MARKERS = new Set([
  ".hermes",
  ".codex",
  ".claude",
  ".openclaw",
  ".agents",
  ".cursor",
  ".opencode",
  ".kiro",
  ".slate",
  ".factory",
]);

function exists(p) {
  try {
    fs.lstatSync(p);
    return true;
  } catch {
    return false;
  }
}

function sha(text) {
  return crypto.createHash("sha256").update(text).digest("hex");
}

function mkdirp(p) {
  fs.mkdirSync(p, { recursive: true });
}

function writeReport(targetPath, report) {
  try {
    mkdirp(path.dirname(targetPath));
    fs.writeFileSync(targetPath, `${JSON.stringify(report, null, 2)}\n`);
    return targetPath;
  } catch (error) {
    if (reportArg) throw error;
    const fallbackPath = path.join(os.tmpdir(), `skill-consolidation-report-${timestamp}.json`);
    mkdirp(path.dirname(fallbackPath));
    fs.writeFileSync(fallbackPath, `${JSON.stringify(report, null, 2)}\n`);
    console.warn(`WARN: could not write default report path ${targetPath}: ${error.message}`);
    return fallbackPath;
  }
}

// Normalize wrapped frontmatter scalars so duplicate grouping uses the text,
// not the source formatting.
function normalizeFrontmatterText(value) {
  return String(value ?? "").replace(/\s+/g, " ").trim();
}

function stripPlainScalarInlineComment(value) {
  for (let i = 0; i < value.length; i++) {
    if (value[i] !== "#") continue;
    if (i === 0 || /\s/.test(value[i - 1])) {
      return value.slice(0, i).trimEnd();
    }
  }
  return value;
}

function parseInlineScalar(raw) {
  const value = raw.trim();
  if (value === "") return "";
  if (value.startsWith('"') && value.endsWith('"')) {
    try {
      return JSON.parse(value);
    } catch {
      return value.slice(1, -1);
    }
  }
  if (value.startsWith("'") && value.endsWith("'")) {
    return value.slice(1, -1).replace(/''/g, "'");
  }
  return stripPlainScalarInlineComment(value);
}

function decodeDoubleQuotedEscape(ch) {
  switch (ch) {
    case '"':
      return '"';
    case "\\":
      return "\\";
    case "/":
      return "/";
    case "b":
      return "\b";
    case "f":
      return "\f";
    case "n":
      return "\n";
    case "r":
      return "\r";
    case "t":
      return "\t";
    case "a":
      return "\x07";
    case "e":
      return "\x1b";
    case "v":
      return "\v";
    case "0":
      return "\0";
    case "_":
      return "\u00a0";
    case "N":
      return "\u0085";
    case "L":
      return "\u2028";
    case "P":
      return "\u2029";
    default:
      return `\\${ch}`;
  }
}

function parseQuotedScalar(lines, startIndex, endIndex, rest, quoteChar) {
  const initial = rest.trimStart();
  if (initial[0] !== quoteChar) {
    return { value: parseInlineScalar(rest), nextIndex: startIndex + 1 };
  }

  let value = "";
  let i = startIndex;

  while (i < endIndex) {
    const line = i === startIndex ? initial.slice(1) : lines[i];

    if (quoteChar === '"') {
      let escape = false;
      for (let j = 0; j < line.length; j++) {
        const ch = line[j];
        if (escape) {
          if ((ch === "x" || ch === "u" || ch === "U") && j + 1 < line.length) {
            const width = ch === "x" ? 2 : ch === "u" ? 4 : 8;
            const hex = line.slice(j + 1, j + 1 + width);
            if (hex.length === width && /^[0-9a-fA-F]+$/.test(hex)) {
              const codePoint = Number.parseInt(hex, 16);
              if (codePoint <= 0x10ffff) {
                value += String.fromCodePoint(codePoint);
                j += width;
                escape = false;
                continue;
              }
            }
          }

          value += decodeDoubleQuotedEscape(ch);
          escape = false;
          continue;
        }

        if (ch === "\\") {
          escape = true;
          continue;
        }

        if (ch === '"') {
          return { value, nextIndex: i + 1 };
        }

        value += ch;
      }

      if (escape) {
        // A trailing backslash escapes the physical newline.
        i++;
        continue;
      }
    } else {
      for (let j = 0; j < line.length; j++) {
        const ch = line[j];
        if (ch === "'") {
          if (line[j + 1] === "'") {
            value += "'";
            j++;
            continue;
          }
          return { value, nextIndex: i + 1 };
        }
        value += ch;
      }
    }

    if (i + 1 < endIndex) {
      value += " ";
    }
    i++;
  }

  return { value, nextIndex: endIndex };
}

function parseBlockScalar(lines, startIndex, endIndex, keyIndent, style) {
  const rawLines = [];
  let minIndent = Infinity;
  let i = startIndex + 1;

  while (i < endIndex) {
    const line = lines[i];
    if (!line.trim()) {
      rawLines.push("");
      i++;
      continue;
    }

    const indent = line.match(/^\s*/)[0].length;
    if (indent <= keyIndent) break;

    minIndent = Math.min(minIndent, indent);
    rawLines.push(line);
    i++;
  }

  if (rawLines.length === 0 || minIndent === Infinity) {
    return { value: "", nextIndex: i };
  }

  const dedented = rawLines.map((line) => (line === "" ? "" : line.slice(minIndent)));
  const value = style === "|" ? dedented.join("\n") : dedented.map((line) => line.trimEnd()).join(" ");
  return { value, nextIndex: i };
}

function parseSkillFrontmatter(text) {
  const lines = text.split(/\r?\n/);
  if (lines[0]?.trim() !== "---") return {};

  let end = -1;
  for (let i = 1; i < lines.length; i++) {
    if (lines[i].trim() === "---") {
      end = i;
      break;
    }
  }

  if (end === -1) return {};

  const frontmatter = {};
  for (let i = 1; i < end; i++) {
    const raw = lines[i];
    if (!raw.trim() || /^\s*#/.test(raw)) continue;

    const indent = raw.match(/^\s*/)[0].length;
    if (indent !== 0) continue;

    const colonIndex = raw.indexOf(":");
    if (colonIndex === -1) continue;

    const key = raw.slice(0, colonIndex).trim();
    const rest = raw.slice(colonIndex + 1);
    const trimmed = rest.trimStart();

    if (trimmed.startsWith('"') || trimmed.startsWith("'")) {
      const { value, nextIndex } = parseQuotedScalar(lines, i, end, rest, trimmed[0]);
      frontmatter[key] = value;
      i = nextIndex - 1;
      continue;
    }

    if (trimmed.startsWith(">") || trimmed.startsWith("|")) {
      const { value, nextIndex } = parseBlockScalar(lines, i, end, indent, trimmed[0]);
      frontmatter[key] = value;
      i = nextIndex - 1;
      continue;
    }

    frontmatter[key] = parseInlineScalar(rest);
  }

  return frontmatter;
}

function* walk(dir) {
  let entries = [];
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return;
  }
  for (const entry of entries) {
    const full = path.join(dir, entry.name);
    if (entry.isSymbolicLink()) continue;
    yield { full, entry };
    if (entry.isDirectory()) yield* walk(full);
  }
}

function hasNestedSkillFiles(dir) {
  for (const { full, entry } of walk(dir)) {
    if (entry.isFile() && entry.name === "SKILL.md") return true;
  }
  return false;
}

function skillRecords(root) {
  const records = [];
  if (!exists(root)) return records;
  for (const { full, entry } of walk(root)) {
    if (!entry.isFile() || entry.name !== "SKILL.md") continue;
    const text = fs.readFileSync(full, "utf8");
    const rel = path.relative(root, full);
    const frontmatter = parseSkillFrontmatter(text);
    const norm = text.trim().replace(/\s+/g, " ");
    records.push({
      root,
      rel,
      path: full,
      name: normalizeFrontmatterText(frontmatter.name ?? path.basename(path.dirname(full))),
      description: normalizeFrontmatterText(frontmatter.description ?? ""),
      sha: sha(text),
      normSha: sha(norm),
      bytes: Buffer.byteLength(text),
    });
  }
  return records;
}

function findEmbeddedMirrorHomes(root) {
  const candidates = [];
  if (!exists(root)) return candidates;
  for (const { full, entry } of walk(root)) {
    if (!entry.isDirectory() || !EMBEDDED_HOME_MARKERS.has(entry.name)) continue;
    const relParts = path.relative(root, full).split(path.sep);
    // A top-level ~/.codex/skills/.foo is not expected, but require this marker
    // to be nested inside at least one skill pack before archiving.
    if (relParts.length < 2) continue;
    const skillsDir = path.join(full, "skills");
    if (!exists(skillsDir) || !hasNestedSkillFiles(skillsDir)) continue;
    candidates.push({
      root,
      path: full,
      rel: path.relative(root, full),
      skillFiles: skillRecords(skillsDir).length,
    });
  }
  return candidates;
}

function duplicateGroups(records, key) {
  const groups = new Map();
  for (const record of records) {
    const value = record[key];
    if (!value) continue;
    if (!groups.has(value)) groups.set(value, []);
    groups.get(value).push(record);
  }
  return [...groups.values()].filter((group) => group.length > 1);
}

function archiveMirror(candidate) {
  if (!exists(candidate.path)) return null;
  const rootLabel = path.basename(path.dirname(candidate.root)) || path.basename(candidate.root);
  const dest = path.join(archiveRoot, rootLabel, candidate.rel);
  mkdirp(path.dirname(dest));
  if (exists(dest)) throw new Error(`archive destination already exists: ${dest}`);
  fs.renameSync(candidate.path, dest);
  return dest;
}

const beforeRecords = roots.flatMap((root) => skillRecords(root));
const mirrorHomes = roots.flatMap((root) => findEmbeddedMirrorHomes(root));
const archived = [];

if (apply) {
  mkdirp(archiveRoot);
  const seenCandidates = new Set();
  for (const candidate of mirrorHomes) {
    if (!exists(candidate.path)) continue;
    const real = fs.realpathSync(candidate.path);
    if (seenCandidates.has(real)) continue;
    seenCandidates.add(real);
    const archivedTo = archiveMirror(candidate);
    if (archivedTo) archived.push({ ...candidate, archivedTo });
  }
}

const afterRecords = roots.flatMap((root) => skillRecords(root));
const report = {
  generatedAt: new Date().toISOString(),
  mode: apply ? "apply" : "dry-run",
  principle: "Keep as many skills as necessary; archive generated mirrors and report duplicate variants instead of enforcing an arbitrary count.",
  roots,
  archiveRoot: apply ? archiveRoot : null,
  counts: {
    before: beforeRecords.length,
    after: afterRecords.length,
    byRootBefore: Object.fromEntries(roots.map((root) => [root, beforeRecords.filter((r) => r.root === root).length])),
    byRootAfter: Object.fromEntries(roots.map((root) => [root, afterRecords.filter((r) => r.root === root).length])),
  },
  embeddedMirrorHomes: mirrorHomes,
  archived,
  duplicates: {
    exactContentGroups: duplicateGroups(afterRecords, "normSha").map((group) => group.map(({ root, rel, name }) => ({ root, rel, name }))),
    sameNameVariantGroups: duplicateGroups(afterRecords, "name").filter((group) => new Set(group.map((r) => r.normSha)).size > 1).map((group) => group.map(({ root, rel, name, description, normSha }) => ({ root, rel, name, description, normSha }))),
    sameDescriptionGroups: duplicateGroups(afterRecords.filter((r) => r.description), "description").map((group) => group.map(({ root, rel, name, description }) => ({ root, rel, name, description }))),
  },
};

const writtenReportPath = writeReport(reportPath, report);

console.log(`skill consolidation ${apply ? "applied" : "dry-run"}`);
console.log(`roots: ${roots.length}`);
console.log(`skills before: ${beforeRecords.length}`);
console.log(`embedded mirror homes: ${mirrorHomes.length}`);
console.log(`embedded mirror skill files: ${mirrorHomes.reduce((sum, item) => sum + item.skillFiles, 0)}`);
if (apply) {
  console.log(`skills after: ${afterRecords.length}`);
  console.log(`archive: ${archiveRoot}`);
}
console.log(`exact duplicate content groups after: ${report.duplicates.exactContentGroups.length}`);
console.log(`same-name variant groups after: ${report.duplicates.sameNameVariantGroups.length}`);
console.log(`report: ${writtenReportPath}`);

if (!apply && mirrorHomes.length > 0) {
  console.log("\nPreview mirror homes to archive:");
  for (const item of mirrorHomes.slice(0, 20)) {
    console.log(`- ${item.path} (${item.skillFiles} skill files)`);
  }
  if (mirrorHomes.length > 20) console.log(`... ${mirrorHomes.length - 20} more`);
  console.log("\nRun with --apply to move these generated mirror homes to the archive.");
}
