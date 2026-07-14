---
name: x-thread-fetcher
description: >
  Detect X or Twitter links and fetch the full thread, article context, and substantive outbound links using research-scout by default, with browser and web-fetch fallbacks. Use when the user provides an x.com or twitter.com link or asks to analyze an X thread/article. Does not depend on a dedicated X-only bot.
related_skills: [lastXdays, web-to-markdown, perplexity, social-content]
---

# X Thread Fetcher

This skill handles X links as a research problem, not as a dedicated bot lane.

## Trigger Conditions
- User message contains `x.com/` or `twitter.com/`
- The link is relevant to the task, not incidental
- The user wants analysis, summary, relevance, extraction, or downstream action

## Default Routing

1. **Route through `research-scout` by default** if that lane exists in the current environment.
2. If no dedicated research-scout lane is available, use the browser tool to pull the thread/article directly.
3. Use `web_fetch` for linked articles and substantive outbound references.
4. Spawn a focused child lane only when the thread/article is genuinely large, anti-bot handling is needed, or the follow-on synthesis is heavy enough to justify it.

## Workflow

### 1. Extract the X link
Identify the primary X/Twitter URL from the user message.

### 2. Pull the thread/article context
Preferred order:
- `research-scout`
- browser snapshot/evaluate on the X page
- broader web fallback only if the above fail

If the X post is an article-style post, pull the full article text, not just the opener.

### 3. Expand linked sources
If the post or article contains outbound URLs:
- extract them
- skip obvious tracking/share junk
- fetch each substantive linked resource
- fold those sources into the summary

### 4. Return the useful answer
Respond with:
- key claims
- important quoted evidence when needed
- relevance to the user's project/question
- recommendation or next move

## What Changed From The Old Pattern

Do **not** assume:
- a Grok-only sub-agent
- a dedicated X bot lane
- that comments are always required

The goal is reliable thread/article analysis with the lightest viable path.

## Fallbacks

### Browser capture is incomplete
- Scroll, snapshot again, or use page evaluation to extract article text
- If there is an embedded article, fetch it separately with `web_fetch`

### Thread is huge
- Spawn a focused child lane only for extraction or synthesis that is too large for one pass

### X page is noisy or blocked
- Use available article links, quoted text, and broader web coverage to reconstruct the important context

## Verification
After extraction, cross-check at least one key quote or claim against the pulled page/article text before final synthesis.

## Output Standard
Prefer compact output:
- what the post says
- why it matters here
- what to do with it
