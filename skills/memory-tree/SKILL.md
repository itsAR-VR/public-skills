---
name: memory-tree
description: >
  Hierarchical memory management for persistent agent knowledge. Use when
  you need to remember something important (curate) or recall past decisions,
  preferences, or context (query). Replaces flat MEMORY.md with structured
  domain/topic/subtopic organization with auto-categorization, summaries,
  and token budgets.
triggers:
  - remember this
  - save to memory
  - recall
  - what do I know about
  - memory tree
  - curate memory
related_skills: [memory-systems, context-optimization, agent-md-refactor, session-handoff]
---

# Memory Tree Skill

Hierarchical memory system stored in `memory/tree/` as human-readable markdown.

## Quick Reference

The helper commands documented by this skill require companion scripts under
`scripts/memory-tree/`. If that directory is absent, do not run the examples;
use this file as the memory-tree contract and restore the companion scripts
before command-based curation, querying, summarization, archiving, or migration.

### Save Knowledge (Curate)
```bash
bash scripts/memory-tree/curate.sh "AR prefers phase-plan workflow for substantial tasks" "preferences"
```
- First arg: the knowledge to store
- Second arg (optional): category hint (e.g., "preferences", "infrastructure", "projects")
- Auto-classifies into domain/topic via the configured helper model; verify the
  script configuration before treating a model name as current
- Auto-generates summaries upward

### Recall Knowledge (Query)
```bash
bash scripts/memory-tree/query.sh "what are AR's workflow preferences?"
```
- Uses manifest-guided keyword scan + content grep
- Also queries QMD hybrid search (`qmd query "..." -c memory-tree`) for semantic matching
- Returns matching entries with parent context

### Other Commands
```bash
bash scripts/memory-tree/summarize.sh          # Regenerate all summaries
bash scripts/memory-tree/manifest.sh           # Rebuild manifest
bash scripts/memory-tree/archive.sh            # Archive stale entries
bash scripts/memory-tree/migrate.sh            # Migrate from MEMORY.md (one-time)
bash scripts/memory-tree/archive.sh --dry-run  # Preview what would be archived
bash scripts/memory-tree/migrate.sh --dry-run  # Preview MEMORY.md sections
```

## When to Use
- **Curate** after: learning user preferences, making architecture decisions, completing significant tasks, receiving feedback
- **Query** before: starting tasks that need past context, checking existing patterns/preferences, recalling decisions

## Architecture
- `memory/tree/` — hierarchical markdown files (domains → topics → subtopics)
- `_index.md` — auto-generated summaries at each level (d0=root, d1=domain, d2=topic)
- `_manifest.json` — token-budgeted registry of all entries sorted by importance
- `_archived/` — stubs for stale knowledge (still searchable, full content preserved in `.full.md`)
- All files git-friendly and human-readable

## Valid Domains
- `infrastructure` — servers, OpenClaw setup, gateways, deployments, networking
- `projects` — the project, mission-control, autoresearch, KALM, MIST, other codebases
- `preferences` — AR/Mo working style, behavior rules, doctrine
- `people` — team members, their roles and contact details
- `integrations` — external APIs, tools (QMD, GitHub, Granola), services

## QMD Integration
Collection `memory-tree` is registered in `~/.config/qmd/index.yml`.
After curating new entries, run `qmd update && qmd embed` to refresh semantic index.
If the companion scripts are installed, `curate.sh` also runs summarize and
manifest refreshes; QMD picks up changes on the next scheduled embed run.

## Notes
- Importance scale: 100=critical/permanent, 70=important, 40=useful, 20=trivial
- Archive decay: entries lose 1 importance point per week; archived when decayed < 35 AND status=draft
- Archive keeps a stub (.stub.md) that stays searchable; full content preserved in .full.md
- Do NOT delete or modify existing MEMORY.md — it's the legacy backup
