# Knowledge Layer — Grounding the Debate in Your Data

Without a knowledge layer, autoreason debates from general copywriting principles. With one, it debates from **your results**. The critic can say "this reads like the subject lines that averaged 12% open rate, not the 38% ones" instead of "this feels weak." The loop gets sharper every campaign because each result feeds back in.

## What to include

Five layers, listed in descending order of leverage for marketing/copy tasks:

### 1. Past campaign performance (highest leverage)

Numbers that matter to this task:
- Open rates, CTR, conversion, revenue per segment
- Retention / churn signals
- Activation funnel drop-off points

**Format:** a short summary, not raw data. Top decile vs bottom decile, pattern differences, what moved revenue.

```markdown
## Performance patterns (last 90 days)

TOP DECILE subject lines (38%+ open rate):
- Specific number + timeframe: "3 apps in 40 minutes", "$2M ARR in 14 months"
- Contrarian frame: "why [thing everyone does] fails", "stop [common advice]"
- Named stakes: "for founders raising under $5M"

BOTTOM DECILE (<12% open rate):
- Vague benefit: "grow your business faster"
- Industry jargon without specifics: "leverage synergies"
- Positive without friction: "amazing news!"
```

### 2. Winning vs losing copy (concrete pairs)

Don't just describe patterns — show paired examples.

```markdown
## Winning/losing pairs

WINNING (34% open): "3 hires I regret, 2 I'd make again"
LOSING (9% open): "Hiring lessons from the trenches"

WINNING (31%): "What happens after Stripe rate-limits you"
LOSING (11%): "Scaling payment infrastructure"
```

The critic references these pairs directly: "this line reads like the 11%-open losing set, not the 31% winning set — it describes the topic ('scaling infrastructure') instead of the consequence ('what happens after Stripe rate-limits you')."

### 3. Audience research (what customers actually say)

Raw language from:
- Product reviews (App Store, G2, Trustpilot)
- Support tickets (common phrasings of the same problem)
- Reddit / HN threads about your category
- Sales call transcripts (objection phrasing, excitement phrasing)

```markdown
## Customer language

Pain (from support tickets):
- "I keep losing track of which draft is the live one"
- "Every PM on our team has their own spreadsheet"
- "I spend 2 hours Monday morning just figuring out what changed"

Excitement (from reviews):
- "Finally something that matches how my brain works"
- "Stopped being the bottleneck"
- "My team actually uses it"
```

### 4. Competitor positioning

How each competitor describes themselves, in their own words. Used to detect generic copy (anything a competitor could say verbatim).

```markdown
## Competitor positioning (homepage H1s)

- Linear: "The issue tracking tool you'll enjoy using"
- Notion: "The AI workspace that works for you"
- Asana: "Work on big ideas, without the busywork"

Generic patterns to avoid:
- "built for modern teams"
- "powerful yet simple"
- "get started in minutes"
```

### 5. Brand voice rules

Specific words / tone / patterns that sound like **you** vs. anyone.

```markdown
## Brand voice

DO:
- Start with a specific scenario, not an abstraction
- Use numbers ≥ 2 digits ("40 minutes", not "minutes")
- Lowercase except proper nouns — no Title Case Marketing

DON'T:
- "game-changing", "revolutionary", "seamlessly"
- Exclamation marks in headlines
- Second-person "you" + benefit claim ("you'll love it") without proof
```

## How to inject it

Add a `KNOWLEDGE LAYER` section to the **critic** system prompt and the **judge** system prompt. Do not inject it into the author or synthesizer — they produce; they don't evaluate.

### Modified critic system prompt

```
You are a critical reviewer. Your only job is to find real problems. Be specific and concrete. Do not suggest fixes.

KNOWLEDGE LAYER (use for grounding critiques):
{knowledge_layer_summary}

When critiquing, reference specific patterns from the knowledge layer where relevant. Prefer critiques of the form "this pattern-matches the losing set" over critiques from general principle.
```

### Modified judge system prompt

```
You are an independent evaluator. You have no authorship stake in any version. Evaluate which version best accomplishes the original task.

KNOWLEDGE LAYER (use for grounding verdicts):
{knowledge_layer_summary}

When ranking, favor proposals that pattern-match the top-decile examples and penalize proposals that pattern-match the bottom-decile examples. Explain verdicts with specific references to the knowledge layer where relevant.
```

Keep the knowledge layer under **~1500 tokens** — it goes to every critic and every judge every pass. Summarize, don't dump.

## The feedback loop

Each autoreason run **produces** knowledge-layer input for the next run:

1. The winning copy is deployed.
2. Its performance gets measured (open rate, conversion, etc.).
3. The result joins the top- or bottom-decile set in your knowledge layer.
4. The next run's critic + judges have sharper evidence to argue over.

Over time, the knowledge layer accumulates until it **dominates** the argument. At that point, autoreason is debating almost entirely from your data, and the output quality tracks your operational quality rather than the base model's general taste.

## Minimum viable knowledge layer

If you're starting from zero data:

1. Collect 10 winning and 10 losing examples of the artifact type (subject lines, landing heroes, pitches).
2. Write the top-3 pattern differences.
3. Write 5 brand-voice DOs and 5 DON'Ts.
4. Start running autoreason. After 5 campaigns, you'll have enough to refine the knowledge layer with real numbers.

## Storage

Keep the knowledge layer in a versioned markdown file (`knowledge/<domain>.md`) so you can diff how it evolves and roll back changes that hurt output quality.
