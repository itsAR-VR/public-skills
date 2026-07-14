---
name: conditional-activation
description: "Convention for declaring environment-conditional skill activation via YAML frontmatter fields. Use when building or auditing skills that should only appear when certain tools, binaries, or platforms are present."
related_skills: [find-local-skills, skill-creator, skill-judge, agent-md-refactor]
---

# Conditional Skill Activation

Skills can declare their own activation conditions using YAML frontmatter fields.
Activation-aware routing tools read these fields and filter the skill list
based on the current runtime environment.

## Why This Exists

Not every skill makes sense in every environment. A `duckduckgo-search` skill
only helps if the `ddg` binary is installed. A `macos-screenshot` skill should
only appear on macOS. Conditional activation lets the skill-index stay honest
without manually curating per-host lists.

## Frontmatter Fields

Add any of these to your `SKILL.md` YAML frontmatter:

```yaml
---
name: my-skill
description: "What this skill does."
requires: [tool1, tool2]       # optional: binaries that must exist in PATH
fallback_for: [other-skill]    # optional: only active when named skills are absent
platforms: [linux, darwin]     # optional: OS filter (linux | darwin | windows)
---
```

### `requires`

List of binary names that must exist in `$PATH`. All must be present for the
skill to be considered active.

```yaml
requires: [ffmpeg, jq]   # only active if both ffmpeg and jq are installed
```

### `fallback_for`

List of skill names. The skill is only active when **none** of the listed skills
exist (their skill directory is absent). Use this for fallback implementations.

```yaml
fallback_for: [web-search]   # only active if the web-search skill is not installed
```

### `platforms`

List of OS identifiers. Compared against `$(uname -s)` lowercased.
Accepted values: `linux`, `darwin`, `windows`.

```yaml
platforms: [linux, darwin]   # only active on Linux or macOS; skip on Windows
```

## Usage

When a skill-index filter is present in the workspace, it should read the skill
index plus each skill's SKILL.md frontmatter, then output a filtered JSON array
of active skills:

```bash
# Default: filter the skill index against current environment
bash path/to/skill-activation-filter.sh

# Filter a specific index file
bash path/to/skill-activation-filter.sh path/to/skill-index.json

# Show reasons for each skip
bash path/to/skill-activation-filter.sh --verbose
```

Output should be a JSON array of skill objects containing only skills whose
conditions are satisfied.

## Defaults (when fields are absent)

If none of the conditional fields are present, the skill is always active — same
behavior as before this convention existed. Existing skills need no changes.

## Example: ddg fallback search

```yaml
---
name: duckduckgo-search
description: "Search with DuckDuckGo CLI (ddg) as a lightweight web-search fallback."
requires: [ddg]
fallback_for: [web-search]
platforms: [linux, darwin]
---
```

This skill only appears when `ddg` is in PATH, the `web-search` skill directory
does not exist, and the OS is Linux or macOS.

## Integration with skill-index.json

Skill-index generation should list eligible skills without applying these
conditions. Apply the activation filter at routing time to get the
environment-appropriate subset.
