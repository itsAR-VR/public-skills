---
name: brave-search
description: Web search and content extraction via Brave Search. Use for searching documentation, facts, or any web content. Lightweight, no browser or API key required.
---

# Brave Search

Headless web search and content extraction using Brave Search. No browser or API key required.

## Setup

Run once before first use:

```bash
cd skills/brave-search
npm ci
```

Run from the public-skills repo root, or `cd` into this skill directory before using the scripts below.

## Search

```bash
./search.js "query"                    # Basic search (5 results)
./search.js "query" -n 10              # More results
./search.js "query" --content          # Include page content as markdown
./search.js "query" -n 3 --content     # Combined
```

## Extract Page Content

```bash
./content.js https://example.com/article
```

Fetches a URL and extracts readable content as markdown.

## Output Format

```
--- Result 1 ---
Title: Page Title
Link: https://example.com/page
Snippet: Description from search results
Content: (if --content flag used)
  Markdown content extracted from the page...

--- Result 2 ---
...
```

## When to Use

- Searching for documentation or API references
- Looking up facts or current information
- Fetching content from specific URLs
- Any task requiring web search without interactive browsing
