---
name: openclaw-guide-synthesis
description: Synthesize OpenClaw setup and operating guides from source material (tweets, playbooks, prior guides, notes), then produce production-ready onboarding, hardening, and operations guides with consistent structure, evidence mapping, and verification steps.
related_skills: [agent-md-refactor, memory-systems, skill-creator, doc-coauthoring]
---

# OpenClaw Guide Synthesis

Purpose: turn messy source material into reliable, versioned guides that teach people how to use OpenClaw safely and effectively.

## When to Use
Use this skill when user asks for:
- “Create/update an OpenClaw guide”
- “Synthesize threads + playbook into onboarding docs”
- “Turn notes/tweets into a setup / hardening playbook”
- “Build a reusable guide process for beginners”

## Sources of Record (for this workspace)
Resolve local source paths before reading them, then use these sources first:
- `OPENCLAW_THREADS_DIGEST.md` (thread syntheses and key takeaways)
- `the project` Playbook: `Playbook App Building 101+102 (Advanced Agentic Engineering...)` (source guide references)
- `the project/AGENTS.md` and `the project/the organization Course Playbook/AGENTS MD ...` (context + operating assumptions)
- OpenClaw project docs and runbooks in the repo
- Any previous versions of the guide you are regenerating

## Core Principles
1. **Signal over noise**: preserve only decision-grade patterns.
2. **Do not invent**: every claim should trace to a source and/or explicit assumption.
3. **Teach the first action**: each section starts with what to do now.
4. **Safe defaults**: always include guardrails and verification.
5. **Consistent style**: no fluff, plain language, operator-first.

## Mandatory Output Structure
Every synthesized guide should include in this order:
1. **Goal** (what success looks like in one sentence)
2. **Quick start (10–20 minute path)**
3. **Prerequisites**
4. **Step-by-step setup**
5. **Security + compliance checks**
6. **Operational best practices**
7. **Verification checklist**
8. **Common failure modes + fixes**
9. **FAQ / troubleshooting**
10. **Future updates** (how to keep guide current)

Use this exact heading set unless user asks for different format.

## Standard Workflow
### 1) Intake + normalization
- Ask clarifying questions only if one of these is missing:
  - Target audience (AR/Mo/non-technical operators)
  - Operating environment (desktop/server/cron)
  - Scope (single-agent setup vs full Mission Control)
  - Safety level (high-risk tools or public bot)
- If not missing, proceed directly.

### 2) Source extraction
- Scan local sources and build a claim map with:
  - *Claim*
  - *Source*
  - *Confidence* (high/medium/low)
  - *Actionability* (immediate/high/low)

### 3) Consolidation
- Cluster claims into modules:
  - Setup
  - Security posture
  - Workflow architecture
  - Tooling
  - Monitoring / cron
  - Escalation

### 4) Draft generation
- Write in plain language.
- Prefer tables only for checklists and matrices.
- Include commands exactly as runnable.
- Mark uncertain statements as assumptions.

### 5) Validation pass
Before finalizing, run this hardening pass:
- Is every required action explicitly actionable?
- Can user execute in first 10 minutes?
- Are security risks called out?
- Is there a rollback path?
- Are error paths mapped to diagnostics?

### 6) Delivery
- Provide: `Guide`, `Diff` (what changed from previous if updating), and `Next 24h Action Plan`.
- If user asks for files, write/update the destination `.md` + companion `.docx`/`.doc` and note hash/paths.

## Execution Commands
Use these defaults if you can run shell:
- Locate primary sources:
  - `OPENCLAW_THREADS_DIGEST_PATH=$(find "$HOME" -maxdepth 6 -name OPENCLAW_THREADS_DIGEST.md -print -quit)`
  - `Z2A_PLAYBOOK_PATH=$(find "$HOME" -maxdepth 8 -name 'Playbook App Building 101+102*.md' -print -quit)`
- Read primary sources only after the path resolves:
  - `sed -n '1,220p' "$OPENCLAW_THREADS_DIGEST_PATH"`
  - `sed -n '1,220p' "$Z2A_PLAYBOOK_PATH"`
- Build/refresh source index:
  - `UPLOAD_JS=$(find "$HOME" -maxdepth 8 -path '*/integrations/google-drive-mcp/upload.js' -print -quit)`
  - `python3 "$UPLOAD_JS" list <folderId>` (if you need Drive verification)
- Save final guide in:
  - `/tmp/openclaw/guide-drafts/<slug>.md`

## Quality Gate (required)
Final guide must pass all checks:
- [ ] No unsupported claim
- [ ] Every section has a next action
- [ ] Security section includes Telegram policy, OAuth, least privilege
- [ ] Includes a verification checklist
- [ ] Includes at least one troubleshooting entry per major section

## Optional Automation (if requested)
If user wants repeatable synthesis runs:
- Create a small source manifest JSON:
  - sources array: file paths, tweet URLs, command outputs
- Save manifests per run with date stamps.
- Use one-file-per-guide pattern and daily changelog.

## Example Prompt Pattern
When user asks for a guide, respond with:

> "I’ll synthesize this into one guide now.
> Sources: [list].
> I’ll keep plain-language, operator-first wording and include security + verification.
> If you want, I can also generate a 1-page owner checklist and a 30-day maintenance cadence."
