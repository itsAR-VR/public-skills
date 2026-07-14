---
name: yc-intent-radar-skill
description: Higher-level "intent radar" concept that wraps the yc-jobs-scraper skill. Filters scraped YC Workatastartup job listings by intent signals (GTM, DevRel, Growth, Content hiring) to surface companies signaling expansion, then exports them as a research-ready JSON payload. Use when the user says "yc intent radar", "find companies hiring GTM", "scrape YC jobs by intent", or wants to convert raw YC job-board data into a filtered list of buyers/partners. The actual scraping implementation lives in `skills/yc-jobs-scraper/`; this skill is the analytical wrapper that defines what intent signals to filter on.
related_skills:
  - yc-jobs-scraper
  - vc-curated-match
  - vc-finder
  - twitter-GTM-find-Skill
  - linkedin-job-post-to-buyer-pain-map
---

# YC Intent Radar

A higher-level lens over [yc-jobs-scraper](../yc-jobs-scraper/). The scraper pulls every YC Workatastartup job listing into a local SQLite database; this skill filters those rows by **intent signals** that surface companies in expansion mode:

- **GTM hiring** — "Head of GTM", "Sales Lead", "Founding AE", "Revenue Operations"
- **DevRel hiring** — "Developer Relations", "Developer Advocate", "DevRel Engineer"
- **Growth hiring** — "Head of Growth", "Growth Marketer", "Performance Marketing"
- **Content hiring** — "Content Lead", "Technical Writer", "Founding Editor"

A company posting these roles is usually signaling: "we have product-market fit, we're scaling, we need help." That's the highest-signal moment for outbound, partnership pitches, or competitive intelligence.

## How to run it

The scraping pipeline lives in the canonical scraper skill:

```bash
cd skills/yc-jobs-scraper/scripts
npm install
npx browser-harness install
node auth.js          # one-time: log in to YC in the spawned browser
node scraper.js       # pulls all listings into jobs.db
node export_radar_candidates.js   # filters by intent + writes radar_candidates.json
```

`export_radar_candidates.js` queries `jobs.db` for the four intent buckets and emits `radar_candidates.json` — a payload designed for secondary research tools (Notion ingest, CRM enrichment, outbound sequencer).

## Why a separate wrapper skill

The scraper is a generic data-collection tool — anyone could use it for any YC analysis. The "intent radar" lens is one specific application: GTM-stage signal detection for outbound and competitive work. Splitting them keeps the scraper reusable for unrelated questions ("which startups use Rust?", "which YC companies are in healthcare?") while giving this specific use case a discoverable name.

## Discoverability

- `/yc-intent-radar-skill` (this skill) — the lens. Read this when you want to know what intent filters exist and how the export works.
- `/yc-jobs-scraper` (the implementation) — the engine. Read this when you want to extend the scraping logic itself (new platforms, additional fields, deduplication tweaks).

## Sensitive files

The scraper's `.gitignore` protects `state.json` (authentication cookies) and `jobs.db` (local scrape history). Never commit either.
