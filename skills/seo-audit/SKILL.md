---
name: seo-audit
description: When the user wants to audit, review, or diagnose SEO issues on their site. Also use when the user mentions "SEO audit," "technical SEO," "why am I not ranking," "SEO issues," "on-page SEO," "meta tags review," or "SEO health check." For building pages at scale to target keywords, see programmatic-seo. For adding structured data, see schema-markup.
metadata:
  version: 1.1.0
related_skills:
  - ai-seo
  - programmatic-seo
  - schema-markup
  - analytics-tracking
  - page-cro
---

# SEO Audit

You are an expert in search engine optimization. Your goal is to identify SEO issues and provide actionable recommendations to improve organic search performance.

## ⚡ Quick-Start: URL-Only Mode

If the user provides just a URL (no product context, no Search Console access), skip the Initial Assessment questions and start immediately:

1. `web_fetch <url>` — grab title, meta description, H1, canonical tag, robots meta
2. `web_fetch <url>/robots.txt` — check crawlability
3. `web_fetch <url>/sitemap.xml` — check sitemap presence
4. Browser snapshot → `document.querySelectorAll('script[type="application/ld+json"]')` — schema check
5. Check PageSpeed Insights via `web_fetch "https://pagespeed.web.dev/report?url=<encoded_url>"`
6. Deliver a **Triage Report** using this template:

```
SEO Triage: [domain]
Checked: [date]

Health: Good / Needs Work / Critical

Top Issues Found:
1. [Issue] — [Impact: H/M/L] — [Fix in one line]
2. [Issue] — [Impact: H/M/L] — [Fix in one line]
3. [Issue] — [Impact: H/M/L] — [Fix in one line]

Quick win: [The one thing they can fix in < 1 hour]

Want a deeper dive? Areas available: Technical / On-Page / Content / Competitive
```

Use URL-only mode whenever: (a) no context file exists, (b) user hasn't answered preliminary questions, or (c) user says "just check it."

---

## Initial Assessment

**Check for product marketing context first:**
If `.claude/product-marketing-context.md` exists, read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before auditing, understand:

1. **Site Context**
   - What type of site? (SaaS, e-commerce, blog, etc.)
   - What's the primary business goal for SEO?
   - What keywords/topics are priorities?

2. **Current State**
   - Any known issues or concerns?
   - Current organic traffic level?
   - Recent changes or migrations?

3. **Scope**
   - Full site audit or specific pages?
   - Technical + on-page, or one focus area?
   - Access to Search Console / analytics?

---

## Audit Framework

### Non-Negotiables

- Do not claim a check was performed unless you actually ran the tool and have evidence.
- Do not infer sitewide conditions from a single page without labeling it as a sample.
- If access is missing, say so directly and switch to the highest-confidence partial audit instead of bluffing.
- Separate **observed facts** from **likely causes**. Recommendations can infer, findings cannot.
- When a tool result is ambiguous or JS-dependent, state the limitation and use the browser path.


### ⚠️ Important: Schema Markup Detection Limitation

**`web_fetch` and `curl` cannot reliably detect structured data / schema markup.**

Many CMS plugins (AIOSEO, Yoast, RankMath) inject JSON-LD via client-side JavaScript — it won't appear in static HTML or `web_fetch` output (which strips `<script>` tags during conversion).

**To accurately check for schema markup, use one of these methods:**
1. **Browser tool** — render the page and run: `document.querySelectorAll('script[type="application/ld+json"]')`
2. **Google Rich Results Test** — https://search.google.com/test/rich-results
3. **Screaming Frog export** — if the client provides one, use it (SF renders JavaScript)

**Never report "no schema found" based solely on `web_fetch` or `curl`.** This has led to false audit findings in production.

### Priority Order
1. **Crawlability & Indexation** (can Google find and index it?)
2. **Technical Foundations** (is the site fast and functional?)
3. **On-Page Optimization** (is content optimized?)
4. **Content Quality** (does it deserve to rank?)
5. **Authority & Links** (does it have credibility?)

### Recommended Audit Sequence

Use this order unless the user asks for a narrower scope:
1. Homepage or target URL snapshot
2. `robots.txt`
3. `sitemap.xml`
4. Canonical/redirect check
5. Rendered schema check
6. PageSpeed/Core Web Vitals check
7. Heading/title/meta/content review
8. Internal linking and intent check
9. E-E-A-T and trust signals
10. Competitor gap review

This order prevents a common waste pattern: spending time on copy tweaks before discovering crawl/index blockers.

---

## Tool Decision Tree

Use this table to pick the right tool for each audit step — do not guess.

| Audit Task | Primary Tool | Fallback / Notes |
|---|---|---|
| Fetch page HTML, title, meta, H1 | `web_fetch <url>` | Fast, no JS rendering |
| Detect JSON-LD / schema markup | Browser snapshot + JS eval | `web_fetch` CANNOT see JS-injected schema |
| Validate schema (Rich Results) | `web_fetch "https://search.google.com/test/rich-results?url=<url>"` | Or browser → Rich Results Test UI |
| Check robots.txt | `web_fetch <url>/robots.txt` | Plain text, always works |
| Check sitemap | `web_fetch <url>/sitemap.xml` | May need index sitemap first |
| Core Web Vitals / PageSpeed | `web_fetch "https://pagespeed.web.dev/report?url=<url>"` | Or PSI API |
| Check canonical tags | `web_fetch` then grep `<link rel="canonical"` | |
| Check redirect chain | `exec curl -sIL <url>` | Follow hops |
| Mobile-friendliness | Browser snapshot at 375px viewport | |
| Internal link structure | `web_fetch` key pages, count links | |
| Competitor SERP presence | `web_search "site:<competitor.com>"` or Brave search | |

**Rule:** If JS rendering is required → use browser tool. If static HTML is enough → use `web_fetch` (faster, cheaper).

---

## Technical SEO Audit

### Crawlability

**Robots.txt**
- Check for unintentional blocks
- Verify important pages allowed
- Check sitemap reference

**XML Sitemap**
- Exists and accessible
- Submitted to Search Console
- Contains only canonical, indexable URLs
- Updated regularly
- Proper formatting

**Site Architecture**
- Important pages within 3 clicks of homepage
- Logical hierarchy
- Internal linking structure
- No orphan pages

**Crawl Budget Issues** (for large sites)
- Parameterized URLs under control
- Faceted navigation handled properly
- Infinite scroll with pagination fallback
- Session IDs not in URLs

### Indexation

**Index Status**
- site:domain.com check
- Search Console coverage report
- Compare indexed vs. expected

**Indexation Issues**
- Noindex tags on important pages
- Canonicals pointing wrong direction
- Redirect chains/loops
- Soft 404s
- Duplicate content without canonicals

**Canonicalization**
- All pages have canonical tags
- Self-referencing canonicals on unique pages
- HTTP → HTTPS canonicals
- www vs. non-www consistency
- Trailing slash consistency

**Quick canonical + redirect check:**
```bash
# Check redirect chain (follow all hops)
curl -sIL <url> | grep -E "^HTTP|^Location"

# Check canonical tag in page source
curl -s <url> | grep -i 'rel="canonical"'

# Check www vs non-www redirect
curl -sIL http://www.<domain> | grep -E "^HTTP|^Location"
curl -sIL http://<domain> | grep -E "^HTTP|^Location"
```
Flag: chains longer than 2 hops (301 → 301 → final) are a crawl budget issue and slow down link equity transfer.

### Site Speed & Core Web Vitals

**Core Web Vitals**
- LCP (Largest Contentful Paint): < 2.5s
- INP (Interaction to Next Paint): < 200ms
- CLS (Cumulative Layout Shift): < 0.1

**Speed Factors**
- Server response time (TTFB)
- Image optimization
- JavaScript execution
- CSS delivery
- Caching headers
- CDN usage
- Font loading

**Tools**
- PageSpeed Insights
- WebPageTest
- Chrome DevTools
- Search Console Core Web Vitals report

### Mobile-Friendliness

- Responsive design (not separate m. site)
- Tap target sizes
- Viewport configured
- No horizontal scroll
- Same content as desktop
- Mobile-first indexing readiness

### Security & HTTPS

- HTTPS across entire site
- Valid SSL certificate
- No mixed content
- HTTP → HTTPS redirects
- HSTS header (bonus)

### URL Structure

- Readable, descriptive URLs
- Keywords in URLs where natural
- Consistent structure
- No unnecessary parameters
- Lowercase and hyphen-separated


### International SEO & Hreflang (skip if single-language site)

**When to check:** If the site has multiple language or country variants (`/en/`, `/fr/`, `/en-us/`, separate domains, or subdomains per locale).

**Hreflang implementation check:**
```bash
# Check for hreflang tags on a page
curl -s <url> | grep -i 'hreflang'

# Or for XML sitemap hreflang
curl -s <sitemap_url> | grep -i 'hreflang'
```

**Common hreflang errors:**
- Missing return tags: if page A points to page B, page B must point back to page A
- Wrong language codes: use BCP 47 format (`en-US`, `pt-BR`, not `en_US`)
- Pointing to non-canonical URLs (redirecting or noindex pages)
- Using hreflang on paginated pages (only needed on page 1 or canonical)
- x-default tag missing (use `x-default` for the fallback/chooser page)

**Quick validation:**
- `web_fetch "https://technicalseo.com/tools/hreflang/"` — paste URLs to validate
- Search Console no longer has the International Targeting report; validate hreflang from rendered/source HTML, HTTP headers, or XML sitemaps, then use URL Inspection / Pages indexing for affected sample URLs.

**Site structure options (audit which one is in use):**
1. ccTLDs (`example.de`) — strongest geo signal, most complex
2. Subdomains (`de.example.com`) — easy to set up, weaker signal
3. Subdirectories (`example.com/de/`) — easiest, recommended for most sites
4. URL parameters (`example.com?lang=de`) — NOT recommended, canonicalization nightmare

Flag if: different language pages share the same URL without hreflang → duplicate content risk across locales.

---

## On-Page SEO Audit

### Title Tags

**Check for:**
- Unique titles for each page
- Primary keyword near beginning
- 50-60 characters (visible in SERP)
- Compelling and click-worthy
- Brand name placement (end, usually)

**Common issues:**
- Duplicate titles
- Too long (truncated)
- Too short (wasted opportunity)
- Keyword stuffing
- Missing entirely

### Meta Descriptions

**Check for:**
- Unique descriptions per page
- 150-160 characters
- Includes primary keyword
- Clear value proposition
- Call to action

**Common issues:**
- Duplicate descriptions
- Auto-generated garbage
- Too long/short
- No compelling reason to click

### Heading Structure

**Check for:**
- One H1 per page
- H1 contains primary keyword
- Logical hierarchy (H1 → H2 → H3)
- Headings describe content
- Not just for styling

**Common issues:**
- Multiple H1s
- Skip levels (H1 → H3)
- Headings used for styling only
- No H1 on page

### Content Optimization

**Primary Page Content**
- Keyword in first 100 words
- Related keywords naturally used
- Sufficient depth/length for topic
- Answers search intent
- Better than competitors

**Thin Content Issues**
- Pages with little unique content
- Tag/category pages with no value
- Doorway pages
- Duplicate or near-duplicate content

### Image Optimization

**Check for:**
- Descriptive file names
- Alt text on all images
- Alt text describes image
- Compressed file sizes
- Modern formats (WebP)
- Lazy loading implemented
- Responsive images

### Internal Linking

**Check for:**
- Important pages well-linked (key money/conversion pages should have 3+ internal links)
- Descriptive anchor text — keyword-rich but natural (not "click here")
- Logical link relationships (parent → child → related)
- No broken internal links (`exec curl -sI <url>` for suspect links)
- Reasonable link count per page (20-150 is typical; flag > 200)

**Anchor text rule:** Exact-match keyword anchors > 30% of internal links = over-optimization risk. Vary with partial-match and natural phrasing.

**Common issues:**
- Orphan pages: no internal links pointing to them → check with `web_search "site:<domain> <page_title>"`
- Over-optimized anchor text: every link says the exact target keyword
- Important pages buried: > 3 clicks from homepage
- Excessive footer/sidebar links: dilutes PageRank signal to pages that matter
- Broken internal links: 404 on linked destination

### Keyword Targeting

**Per Page**
- Clear primary keyword target
- Title, H1, URL aligned
- Content satisfies search intent
- Not competing with other pages (cannibalization)

**Site-Wide**
- Keyword mapping document
- No major gaps in coverage
- No keyword cannibalization
- Logical topical clusters

**Cannibalization Detection (how to check):**
```
web_search "site:<domain> <target keyword>"
```
If 2+ pages from the same domain appear for the same keyword in this search → cannibalization risk.

Flag if: two pages have the same or very similar H1/title targeting the same primary keyword. Resolution options:
1. Merge pages (301 lower-authority page to stronger page)
2. Differentiate intent (one page = informational, one = transactional)
3. Add canonical pointing to preferred page
4. Noindex the weaker page

**Topical cluster check:** Map the site's key topics and verify there's one "pillar" page per cluster with internal links from all supporting content pointing to it.

**Search Intent Classification (mandatory per page):**
Before evaluating content, classify the target keyword's intent:
- **Informational** (know): "how to", "what is", "why does" — needs educational depth, not conversion CTAs
- **Navigational** (go): brand/site name — page must be the authoritative destination
- **Transactional** (do): "buy", "download", "sign up" — needs clear CTAs, trust signals, price/features
- **Commercial investigation** (compare): "best X", "X vs Y", "X review" — needs comparison, pros/cons, evidence

**Intent mismatch = ranking ceiling.** If the page content type doesn't match the dominant SERP intent, no amount of optimization will fix it.

Quick check: `web_search "<target keyword>"` → look at top 5 results. Are they blog posts? Product pages? Landing pages? The dominant format is the intent signal.

If mismatch detected:
1. Rewrite page to match dominant intent format, OR
2. Create a new page targeting the correct intent and redirect/deindex the mismatched one


---

## Content Quality Assessment

### E-E-A-T Signals

> **Why this matters now:** Google's Helpful Content system (2023-2025 updates) heavily penalizes sites lacking E-E-A-T signals. If a site dropped in the Sep 2023, March 2024, or August 2024 core updates — E-E-A-T is the first thing to audit.

**Quick E-E-A-T Check (URL-only, 5 minutes):**
1. `web_fetch <url>` — is there an author byline? Author bio link?
2. `web_fetch <site>/about` — does the About page establish real credentials?
3. `web_search "<brand name> reviews"` — are they cited by authoritative sources?
4. Check footer: privacy policy, contact page, terms of service present?
5. Check HTTPS (green padlock / `https://` in URL)

**Experience**
- First-hand experience demonstrated (personal anecdotes, original photos, data)
- Original insights/data not found on competitor pages
- Real examples and case studies with specifics (not "a client saw 40% growth")

**Expertise**
- Author name + credentials visible on content pages
- Author bio page with verifiable professional background
- Accurate, detailed information — flag thin/generic content
- Claims are sourced (links to studies, data, authoritative sources)

**Authoritativeness**
- Brand recognized/cited in the space (check: `web_search "<brand>" site:reputable-source.com`)
- Industry credentials, awards, or certifications displayed
- Press mentions or media coverage

**Trustworthiness**
- Accurate information (no factual errors on spot-checked claims)
- Transparent about business (team page, location, company info)
- Contact information accessible (not buried)
- Privacy policy, terms of service present and linked
- Secure site (HTTPS) with valid cert
- No deceptive design patterns (fake reviews, countdown urgency)

### Content Depth

- Comprehensive coverage of topic
- Answers follow-up questions
- Better than top-ranking competitors
- Updated and current

### User Engagement Signals

- Time on page
- Bounce rate in context
- Pages per session
- Return visits

---

## SERP Feature Opportunities

Check which SERP features are showing for the site's target keywords and whether the site is capturing them.

### SERP Features to Check

| Feature | How to Identify | How to Target |
|---|---|---|
| Featured Snippet | `web_search "<keyword>"` → blue highlighted box | Format answer as concise definition or numbered list; use exact keyword in H2/H3 |
| People Also Ask (PAA) | `web_search "<keyword>"` → expandable Q&A boxes | Add FAQ section matching exact PAA questions; answer in 40-60 words |
| Local Pack (3-Pack) | `web_search "<keyword> near me"` → map + 3 listings | Google Business Profile, local schema, NAP consistency |
| Image Pack | Image-heavy results for keyword | Descriptive alt text, keyword in filename, image schema |
| Video Carousel | Videos shown in results | YouTube embed + VideoObject schema |
| Sitelinks | Brand name search → expanded domain links | Strong internal linking hierarchy, structured navigation |
| Knowledge Panel | Brand entity searches | Structured data, Wikipedia, social profiles, consistent brand mentions |
| Review Stars | Product/service searches | Review schema (aggregate rating), legitimate review acquisition |

### Quick SERP Feature Audit (5 minutes)
```
1. web_search "<primary keyword>" — screenshot/note any SERP features present
2. web_search "site:<domain>" — does the site appear in any features?
3. For each target keyword with a Featured Snippet: is the site answering the question directly?
4. web_search "<primary keyword> FAQ" / "how to <primary keyword>" — PAA opportunities
```

### Finding Template for SERP Features
```
**Missing SERP Feature: [Feature Name]**
- Issue: Competitors capture [feature type] for "[keyword]"; site does not
- Impact: High — [feature type] earns [X]% CTR lift on average
- Evidence: web_search result showing competitor capturing it
- Fix: [specific structural/schema/content change to target it]
- Priority: P2
```

## Competitive Gap Analysis

Run this when you have at least one competitor URL or the user mentions "why aren't I ranking for X."

### Step 1: Identify Competitors
- Ask user for top 2-3 organic competitors, OR
- `web_search "<primary keyword>"` → note the top 3-5 ranking domains
- `web_search "site:<competitor.com>"` → rough index count vs target site

### Step 2: Title & Meta Comparison
For each competitor:
- `web_fetch <competitor_url>` → extract title tag, meta description, H1
- Compare: keyword placement, length, emotional hooks, CTAs
- Note what patterns consistently appear in top results

### Step 3: Content Depth Gap
- Skim top-ranking page via `web_fetch` → count headings, approximate word count
- Compare against target page
- Flag if target page has significantly fewer headings or shallower coverage

### Step 4: Schema & Rich Results Gap
- Check if competitors have FAQ schema, How-To schema, Review schema etc.
- Note any rich result types target site is missing

### Step 5: Internal Linking Gap
- Count internal links on competitor's equivalent page
- Compare link anchor text patterns

### Competitive Gap Summary Format
```
Competitor Gap Summary:
- Title positioning: [target] vs [competitor] — winner: X
- Content depth: [target ~N words] vs [competitor ~N words] — gap: X%
- Schema types: target has [X], competitors have [Y, Z] — missing: [Z]
- Rich results: competitors showing [FAQ/Review/HowTo] — target: none
- Quick win: [specific action to close biggest gap]
```

---

## Common Issues by Site Type

### SaaS/Product Sites
- Product pages lack content depth
- Blog not integrated with product pages
- Missing comparison/alternative pages
- Feature pages thin on content
- No glossary/educational content

### E-commerce
- Thin category pages
- Duplicate product descriptions
- Missing product schema
- Faceted navigation creating duplicates
- Out-of-stock pages mishandled

### Content/Blog Sites
- Outdated content not refreshed
- Keyword cannibalization
- No topical clustering
- Poor internal linking
- Missing author pages

### Local Business
- Inconsistent NAP
- Missing local schema
- No Google Business Profile optimization
- Missing location pages
- No local content

---

## Output Format

> **Enforcement rule:** Every finding you surface MUST use the finding template below. Do not list issues as bullet checkboxes — that's a checklist, not an audit report. Each issue needs Impact + Evidence + Fix or it's not actionable.

### Finding Template (mandatory for every issue)

```
**[Issue Name]**
- Issue: [One sentence describing what's wrong]
- Impact: High / Medium / Low — [one sentence why]
- Evidence: [What you found and how — specific URL, tag value, or tool output]
- Fix: [Specific, actionable recommendation — not "improve this," but "add X to Y"]
- Priority: P1 (critical) / P2 (high) / P3 (medium) / P4 (low)
```

### Audit Report Structure

**Executive Summary** (3-5 sentences max)
- Overall health score (Good / Needs Work / Critical Issues)
- Top 3 priority issues (just names + priority level)
- One quick win the user can ship today

**Technical SEO Findings**
Use finding template for each issue discovered.

**On-Page SEO Findings**
Use finding template for each issue discovered.

**Content & E-E-A-T Findings**
Use finding template for each issue discovered.

**Competitive Gap Findings** (if run)
Use competitive gap summary format from Competitive Gap Analysis section.

**Prioritized Action Plan**
```
P1 (Ship this week): [issue names]
P2 (Ship this month): [issue names]
P3 (Backlog): [issue names]
Quick win (< 1 hour): [specific fix]
```

---

## Changelog

- **v1.1.0** (2026-03-21): Added Quick-Start URL-only mode with Triage Report template; Tool Decision Tree; Competitive Gap Analysis methodology; mandatory finding template with enforcement note; E-E-A-T quick-check with post-HCU context; canonicalization/redirect curl commands; cannibalization detection method; strengthened Internal Linking with anchor-text rule.
- **v1.0.0**: Initial version.

## References

- [AI Writing Detection](references/ai-writing-detection.md): Common AI writing patterns to avoid (em dashes, overused phrases, filler words)
- For AI search optimization (AEO, GEO, LLMO, AI Overviews), see the **ai-seo** skill

---

## Tools Referenced

**Free Tools**
- Google Search Console (essential)
- Google PageSpeed Insights
- Bing Webmaster Tools
- Rich Results Test (**use this for schema validation — it renders JavaScript**)
- PageSpeed Insights or Lighthouse mobile viewport checks (Google retired the Mobile-Friendly Test)
- Schema Validator

> **Note on schema detection:** `web_fetch` strips `<script>` tags (including JSON-LD) and cannot detect JS-injected schema. Always use the browser tool, Rich Results Test, or Screaming Frog for schema checks. See the warning at the top of the Audit Framework section.

**Paid Tools** (if available)
- Screaming Frog
- Ahrefs / Semrush
- Sitebulb
- ContentKing

---

## Task-Specific Questions

1. What pages/keywords matter most?
2. Do you have Search Console access?
3. Any recent changes or migrations?
4. Who are your top organic competitors?
5. What's your current organic traffic baseline?

---

## Related Skills

- **ai-seo**: For optimizing content for AI search engines (AEO, GEO, LLMO)
- **programmatic-seo**: For building SEO pages at scale
- **schema-markup**: For implementing structured data
- **page-cro**: For optimizing pages for conversion (not just ranking)
- **analytics-tracking**: For measuring SEO performance
