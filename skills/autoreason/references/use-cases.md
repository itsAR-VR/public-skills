# Autoreason Use-Case Playbooks

Specific recipes for the subjective tasks autoreason handles best. Each playbook names the **task prompt shape**, the **knowledge layer** to preload, and the **convergence expectations**.

---

## 1. Product positioning

**Task prompt shape:**
```
Write a positioning statement for {product}.

Context:
- Target customer: {who, pain, budget, why-now}
- Primary competitor(s): {list}
- Proof point(s): {numbers / logos / traction}

Deliverable (≤ 120 words):
- One-sentence category definition
- One-sentence primary differentiator
- One-sentence outcome the customer can measure
- Proof

Constraint: If a competitor could say your differentiator word-for-word, it's not a differentiator.
```

**Knowledge layer:** competitor positioning page captures (literal text), customer discovery-call quotes, any YC/investor positioning docs you've seen work.

**Convergence:** ~10 passes.

**Trajectory you'll see:** early passes kill generic claims; middle passes contest what counts as "measurable"; later passes stabilize on the most specific proof.

---

## 2. Landing-page hero copy

**Task prompt shape:**
```
Write a landing-page hero for {product} targeting {segment}.

Deliverable:
- H1 (≤ 12 words, no punctuation except hyphens)
- H2 (≤ 24 words, concrete)
- Primary CTA (verb + object + outcome)
- One-line proof

Constraint: No metaphors. No "revolutionary / seamless / cutting-edge". Every claim must be numbered or named.
```

**Knowledge layer:** top-performing and bottom-performing hero sections from your own history, category benchmarks (Unbounce, Lusha reports), audience-research quotes.

**Convergence:** 7–12 passes. Landing copy is short so each pass is cheap — feel free to run 7 judges.

**Watch for:** the critic flagging the H1 as jargon in early passes, then the H2 as vague in middle passes, then the CTA's verb choice in late passes. If all three stabilize, you're done.

---

## 3. Email subject-line tournament

**Task prompt shape:**
```
Write one subject line for this email:

Email body:
---
{email_body}
---

Audience: {segment + prior engagement level}

Constraint:
- ≤ 50 characters (mobile preview cap)
- Must work without a preview line (assume it's clipped)
- No clickbait — content must deliver what the line promises
- Match the top-decile patterns in the knowledge layer
```

**Knowledge layer:** your open-rate data, top/bottom decile line patterns (this is the single most data-rich domain for autoreason — lean into it).

**Convergence:** 5–8 passes when the knowledge layer is tight.

**Trick:** run **5 parallel autoreason streams** with different initial A's (different angles). Then run a **5-way judge** to pick the winner across streams. This is cheap per line and gets past the tyranny of a single starting frame.

---

## 4. Ad brief / creative brief

**Task prompt shape:**
```
Write a creative brief for {campaign_goal}.

Sections:
- Single strategic insight (one sentence, not a paragraph)
- Tension to resolve (what the audience feels; what we want them to feel)
- One-line must-have (the thing that can't change)
- Three can-haves (nice but negotiable)
- Legal/brand must-nots

Constraint: A brief is useful to a creative team. If it reads like a marketing plan, rewrite.
```

**Knowledge layer:** past briefs sorted by creative output quality (which ones produced work that shipped well vs. which ones produced rounds of revisions).

**Convergence:** 12–20 passes. Briefs have many interacting sections; synthesis often wins in middle passes as B takes one section further and A holds stronger on another.

---

## 5. Brand voice document

**Task prompt shape:**
```
Write a brand voice document for {brand}.

Sections:
- Voice principles (3 max — each must contain a DO and a DON'T)
- Word/phrase whitelist (20 words we use)
- Word/phrase blocklist (20 words we never use)
- Three worked examples: same message in on-voice vs. off-voice

Constraint: If the principles apply to any SaaS brand, rewrite. Principles must be ownable.
```

**Knowledge layer:** your best and worst-performing copy side by side, founder / CEO writing samples (brand voice is often a codification of the founder's voice), any internal style guides.

**Convergence:** up to 25 passes. Voice docs are subtle — they need several rounds to stabilize which principles are load-bearing.

**Higher convergence_threshold**: set to **3** for brand voice — the cost of a flaky voice doc is team-wide drift, so demand more stability.

---

## 6. Pitch deck narrative (not slide design)

**Task prompt shape:**
```
Write the narrative arc of a 10-slide seed pitch for {company}.

For each slide, produce:
- Slide title (4 words max)
- Single headline claim
- Single proof element
- The emotional beat it hits (tension / relief / momentum)

Constraint: A deck is not a document. If a slide needs a paragraph to make sense, it belongs in a memo.
```

**Knowledge layer:** decks from companies that raised at your target stage, investor partner call notes (what lands / what kills), your own past decks with outcomes.

**Convergence:** 15–28 passes. Pitch narrative has the most stakeholders (team + investor + market fit) and the highest synthesis win rate — AB wins often because A and B each do one act well.

---

## 7. One-liner / elevator pitch

**Task prompt shape:**
```
Write a one-sentence description of {product} that could appear in a press release.

Constraint:
- ≤ 25 words
- Category + primary benefit + differentiator + one proof
- Must be parseable by someone who has never heard of the product
- No superlatives ("the best", "#1", "leading")
```

**Knowledge layer:** TechCrunch / The Information / Pitchbook descriptions of similar companies, customer-call paraphrases ("so basically you do X"), investor-email descriptions.

**Convergence:** 6–10 passes. One-liners are a pure compression task — autoreason shines here because every word is contested.

---

## 8. Internal announcement / all-hands memo

**Task prompt shape:**
```
Write a team-wide memo announcing {decision}.

Structure:
- What changed
- Why now
- What it means for each team (list specifically)
- What's explicitly NOT changing
- When to ask questions (and where)

Constraint: No corporate euphemism. "We're letting 10 people go" beats "we're restructuring for efficiency."
```

**Knowledge layer:** internal memos that landed well, internal memos that caused rumor/panic, employee Slack reactions to past announcements.

**Convergence:** 10–15 passes. Tone matters as much as content; synthesis often wins by taking A's structure and B's frankness.

---

## When to increase convergence_threshold

Default is 2 (A wins twice in a row). Increase to 3 when:
- The artifact is high-stakes and will ship without further review (brand voice doc, investor one-liner)
- You've seen a pattern of A winning once then getting displaced in past runs
- The knowledge layer is thin and you want to avoid premature lock-in

Decrease to 1 (single-pass confirmation) only for near-trivial tasks, and only if you're willing to accept noisier outputs.

---

## When to increase num_judges

Default is 3. Increase to 7 when:
- Wall-clock matters (3× faster convergence)
- Cost is not the binding constraint
- You're seeing flaky verdicts that flip pass-to-pass with 3 judges

Do not go to **1 judge** — the paper's ablation shows 1 judge is both slow and noisy.

---

## Template for a new use case

```markdown
## {Use case name}

**Task prompt shape:**
<one literal template>

**Knowledge layer:**
<what to load — sources and rough size>

**Convergence:** <expected pass count from smallest similar task>

**Watch for:** <what the trajectory typically looks like>

**Config overrides:** <convergence_threshold / num_judges changes, if any>
```
