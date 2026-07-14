---
name: company-research
description: Discover and deeply research target companies using a Plan -> Research -> Synthesize workflow, then compile scored markdown reports and a CSV. Best for outbound prospecting and ICP-fit research batches.
metadata:
  author: browserbase
  source: https://skills.sh/browserbase/skills/company-research
  version: 1.0.0
related_skills:
  - browse-qa
  - browser-automation
  - push-skills
---

# Company Research

Discover and deeply research companies to sell to. This skill uses a structured Plan -> Research -> Synthesize pattern for discovery, enrichment, scoring, and final report generation.

## When to Use

Use this when you need to:
- build a prospect list for outbound or partnerships
- research ICP-fit companies at scale
- enrich company websites into structured markdown reports
- produce a scored CSV plus per-company research notes

## Required

- `BROWSERBASE_API_KEY` set in the environment
- `bb` CLI installed and working

## First-run setup

On first use, expect approvals around commands like:
- `bb fetch`
- `bb search`
- `cat`
- `mkdir`
- `sed`
- `node`

If your environment supports persistent allow rules, the upstream skill suggests allowing patterns like:
- `Bash(bb:*)`
- `Bash(bunx:*)`
- `Bash(bun:*)`
- `Bash(node:*)`
- `Bash(cat:*)`
- `Bash(mkdir:*)`
- `Bash(sed:*)`
- `Bash(head:*)`
- `Bash(tr:*)`
- `Bash(rm:*)`

## Path rule

Always use the full literal path in shell commands. Do not use `~` or `$HOME` in prompts or generated shell snippets if the execution environment treats shell expansion as higher-risk.

## Output directory

Write research output to:

`~/Desktop/{company_slug}_research_{YYYY-MM-DD}/`

That directory should contain:
- one markdown file per researched company
- a compiled `results.csv`
- optional generated HTML overview/report artifacts

## Hard tool restrictions

Apply these rules consistently:

- Use `bb search` for web search
- Use `bb fetch "<url>"` for page extraction
- Do not hand-roll `bb fetch | sed` extraction pipelines for content parsing
- Write one markdown file per company into `{OUTPUT_DIR}`
- Compile `{OUTPUT_DIR}/results.csv` from the per-company markdown files
- Generated HTML overview/report artifacts are optional unless a local implementation provides helpers for them
- Deduplicate discovered URLs before deep research; use local helper scripts only if they exist in the installed copy

## Anti-hallucination rules

- Never infer product, industry, or audience from design style, fonts, or frontend framework
- Never project the user's ICP onto a target without source evidence
- `product_description` should quote or closely paraphrase a specific phrase from extracted page content
- If product evidence is missing, mark it unknown rather than guessing
- If `product_description` is unknown, cap `icp_fit_score` at 3 and explain that evidence is insufficient

## Prompt-minimization rules

To reduce permission churn and execution overhead:
- batch file writes into a single shell call when practical
- batch searches and fetches into grouped shell calls when practical

## Pipeline Overview

Follow this sequence:

1. Company research
2. Depth mode selection
3. Discovery
4. Deep research and scoring
5. Report and CSV compilation

---

## Step 0: Setup output directory

Create a dated output directory before starting.

```bash
OUTPUT_DIR=/full/path/to/Desktop/{company_slug}_research_{YYYY-MM-DD}
mkdir -p "$OUTPUT_DIR"
rm -f /tmp/company_discovery_batch_*.json
```

## Step 1: Deep company research

This is the highest-leverage step.

1. Ask for the company name or URL
2. Check for an existing company profile if your local implementation supports saved profiles
3. Research the user's company deeply before hunting targets
4. Synthesize a reusable company profile
5. Confirm it with the user
6. Save the confirmed profile if your implementation supports local profile storage
7. Ask clarifying targeting questions once, then execute silently until results are ready

### Minimum research pass

Use a plan-first pattern:
- search the company
- inspect the homepage
- inspect sitemap-discovered high-signal pages such as pricing, customers, industries, use cases, or about
- search for external context and competitors
- synthesize the findings into a working company profile

The profile should cover:
- company
- product
- existing customers
- competitors
- use cases

Do not lock in ICP prematurely. Keep that separate for the targeting step.

## Step 2: Depth mode selection

Choose depth based on requested output volume:

- `quick`: broad scan, light enrichment, around 100 companies
- `deep`: balanced research, around 50 companies
- `deeper`: high-effort intelligence, around 25 companies

## Step 3: Discovery

Discovery should over-source candidates because filtering removes many.

### Query strategy

Generate diverse searches across:
- industry + stage + geography
- technology stack + use case
- competitor adjacency
- buyer persona + pain point

### Discovery process

1. Run discovery across multiple queries
2. Store raw batches temporarily
3. Deduplicate discovered URLs
4. Filter out:
   - blog posts
   - news articles
   - directories and aggregators
   - the user's own competitors or existing customers when exclusion is appropriate
5. Keep only likely company homepages

## Step 4: Deep research and scoring

Research candidate companies in parallel when possible.

For each company:

### Phase A: Plan
Break the company into 2 to 5 sub-questions based on the ICP and desired enrichment fields.

### Phase B: Research loop
Search and inspect pages within a bounded step budget.

Typical research targets:
- homepage
- pricing
- use cases or solutions
- industry pages
- customer pages or case studies
- external search results for market context

### Phase C: Synthesize
Produce:
- ICP fit score from 1 to 10
- evidence-backed fit reasoning
- structured enrichment fields
- a markdown file for that company

## Step 5: Report and CSV

Compile the final output set.

Required artifacts:
- one markdown file per researched company
- `{OUTPUT_DIR}/results.csv`

Optional artifacts:
- `{OUTPUT_DIR}/index.html`
- `{OUTPUT_DIR}/companies/*.html`

Also provide a short chat summary with:
- total companies researched
- depth mode used
- score distribution
- report location

Then show top companies sorted by score and summarize the best 3 to 5 opportunities.

## Suggested output shape

Use a compact report like:

```text
## Company Research Complete

- Total companies researched: {count}
- Depth mode: {mode}
- Strong fit (8-10): {count}
- Partial fit (5-7): {count}
- Weak fit (1-4): {count}
- Report location: {OUTPUT_DIR}/index.html
```

And a table like:

```text
| Company | Score | Product | Industry | Fit Reasoning |
|---------|-------|---------|----------|---------------|
| Acme    | 9     | ...     | ...      | ...           |
```

## Notes

This public-skills version is a curated import of the Browserbase skill published at:
`https://skills.sh/browserbase/skills/company-research`

If you want full parity with the upstream implementation, also vendor any referenced helper scripts and reference docs used by that skill's repository.
