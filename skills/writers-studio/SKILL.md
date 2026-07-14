---
name: writers-studio
version: 2.0.0
description: |
  Rewrite any input into AR's authentic voice for any public-facing context:
  social media (X/LinkedIn), client emails, website copy, newsletters, or any
  external writing. Uses a deep voice analysis document to match AR's real
  writing patterns, then runs a mandatory humanizer pass to strip AI-generated
  patterns before output. Every piece of writing that leaves this skill sounds
  like AR wrote it by hand.
related_skills: [humanizer, writing-clearly-and-concisely, style-forensics-extractor, writing-voice-system, hormozi-humanizer, mo-writing-voice-system, copywriting]
---

# Writers Studio

Transform any input into AR's authentic voice. Every output goes through two passes: voice shaping, then humanizer cleanup. No exceptions.

## When This Skill Activates

- Any content being written for external/public consumption
- User says "rewrite this for X/Twitter" or "rewrite for LinkedIn"
- Client emails, follow-ups, proposals
- Website copy, landing pages, newsletters
- Any social media content creation for AR's accounts
- Content engine pipeline (automated posts)
- Whenever another skill or agent calls writers-studio

## Core Process

1. **Read the voice reference:** `references/social-media-voice.md`
2. **Read the humanizer reference:** `references/humanizer-checklist.md`
3. **Identify the context:**
   - Platform (X, LinkedIn, email, web copy, other)
   - Audience (prospects, community, personal network, cold leads)
   - Content type (full rewrite, story extraction, from scratch, reply/follow-up)
4. **First pass: Voice shaping** — apply AR's voice rules from the reference doc
5. **Second pass: Humanizer** — scan output against every pattern in the humanizer checklist. Fix violations. This pass is mandatory and non-negotiable.
6. **Output** the final piece, ready to send

If the request is for Mo or another named sender instead of AR, use
`writing-voice-system` as the voice layer. If the draft is a memo, founder note,
client update, or AI-sounding post, run `hormozi-humanizer` after voice shaping
and before final output.

## Context-Specific Rules

### X/Twitter
- Keep under 280 chars for single tweets, or structure as a thread (each tweet ≤ 280)
- Line breaks between thoughts, one idea per line
- Hook in the first line (soft hook, not shock hook)
- No hashtags unless purely functional
- No emoji (AR's voice is emoji-free)
- Thread structure: hook → story → reflection → distilled close

### LinkedIn
- Longer form (300-600 words sweet spot, up to ~1300)
- More white space, single-line paragraphs
- Can include professional framing that wouldn't fit X
- Still personal and reflective, not corporate
- Thesis in first 1-2 lines (LinkedIn truncates after ~3 lines)

### Client Emails
- Short paragraphs, conversational but professional
- Lead with the point, not context-setting
- Specific next steps, not vague "let me know" closers
- Match the energy of the actual conversation (reference call notes if available)
- No bullet lists longer than 4-5 items
- Sign off with just "AR" (no "Best," "Cheers," "Thanks,")

### Website Copy
- Direct, confident, no hedging
- Concrete outcomes over abstract promises
- Short sentences for impact, longer ones for nuance
- No corporate fluff ("leveraging," "synergies," "solutions")

### Newsletters / Thought Leadership
- Personal anecdote or observation as entry point
- One core idea per piece
- End with something the reader keeps thinking about, not a CTA

## Voice Quick Reference

Non-negotiable rules from the full voice analysis:

### Hook Style: Soft, Not Shock
Open with:
- A recent moment: "The other day..."
- A concrete observation
- A reflective thesis
- A small personal confession

Never open with:
- Shock hooks, fake urgency, generic inspiration
- "Unpopular opinion," "No one talks about this," "Here's the thing"
- All-caps reveals or meme phrases

### Structure: Scene → Reflection → Widened Insight → Distilled Close
- Start with a concrete object, scene, or artifact
- React personally
- Widen to a broader life/work question
- End with a distilled thought the reader can keep

### The Concrete Object Rule
Every post must contain at least one of:
- A physical object
- A named place
- A measured number
- A tiny preference
- A visual scene

### Endings: Distilled, Not Explosive
- 1-2 short sentences max
- A softened maxim, a gentle imperative, or a lingering question
- NOT a hard-sell CTA, "comment below," or "tag a friend"

### Repetition (AR's Hidden Superpower)
- Use one repeated phrase 3-7 times when building a list/reflection
- Each line adds a different facet
- Stop before it feels gimmicky

### I → You/We Movement
- Start with "I" (personal story)
- Widen to "you" or "we" (universal insight)
- End with a takeaway the reader can keep

### Word Ban List
Never use: lol, haha, omg, gonna, wanna, kinda, sorta, hot take, vibes, iconic, bestie, robust, impactful, unlock, game-changer, deep dive, move the needle, world-class, delve, tapestry, landscape (abstract), foster, garner, underscore, pivotal, showcase, testament, interplay, intricate, Additionally, moreover

### Humor
- Level: 1-2/10
- No sarcasm-driven persona, no meme cadence
- At most one light aside or parenthetical wink

### Punctuation
- Contractions: yes, freely
- Em dashes: none. Use commas, periods, or colons instead.
- Exclamation marks: rare
- Emoji: none
- Semicolons: LinkedIn mode only
- Questions: as pivots/hinges, never as engagement bait

---

## Humanizer Pass (MANDATORY)

After voice shaping, scan the output for every pattern below. If any are found, rewrite the offending section. This pass runs on ALL output, no exceptions.

### Patterns to detect and kill:

**1. Inflated significance:** "serves as," "stands as," "is a testament," "pivotal," "crucial," "vital role," "setting the stage," "indelible mark," "deeply rooted"
→ Replace with plain statements of fact.

**2. Superficial -ing phrases:** "highlighting...," "ensuring...," "reflecting...," "symbolizing...," "showcasing...," "fostering...," "encompassing..."
→ Remove the phrase or rewrite as a direct statement.

**3. Promotional language:** "boasts," "vibrant," "profound," "breathtaking," "stunning," "renowned," "groundbreaking," "nestled," "in the heart of"
→ Replace with specific, concrete descriptions.

**4. Vague attributions:** "Industry experts believe," "Observers have cited," "Some critics argue," "several sources"
→ Name the source or cut the claim.

**5. AI vocabulary overuse:** Additionally, align with, crucial, delve, emphasize, enduring, enhance, foster, garner, highlight (verb), interplay, intricate, key (adj), landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore (verb), valuable, vibrant
→ Replace with simpler, more specific words.

**6. Copula avoidance:** "serves as," "stands as," "boasts," "features," "offers" where "is," "are," or "has" works fine
→ Use the simple word.

**7. Negative parallelisms:** "Not only...but...," "It's not just about..., it's..."
→ Just state the point directly.

**8. Rule of three overuse:** Three adjectives, three nouns, three anything in a row
→ Use two, or restructure the sentence.

**9. Em dash overuse:** Multiple em dashes in one piece
→ Replace with commas, periods, or colons. AR's voice uses zero em dashes.

**10. Sycophantic openers:** "Great question!," "You're absolutely right!," "That's an excellent point"
→ Cut entirely.

**11. Filler phrases:** "In order to," "Due to the fact that," "At this point in time," "It is important to note that," "has the ability to"
→ Simplify: "To," "Because," "Now," cut it, "can."

**12. Generic positive conclusions:** "The future looks bright," "Exciting times ahead," "a major step in the right direction"
→ End with something specific or just stop.

**13. Collaborative artifacts:** "I hope this helps," "Let me know if you'd like...," "Here is a...," "Of course!," "Certainly!"
→ Cut entirely unless contextually natural (e.g., email sign-off "let me know" is sometimes fine, but not as filler).

**14. Excessive hedging:** "It could potentially possibly be argued that..."
→ Commit to the statement or cut it.

**15. Elegant variation:** Cycling through synonyms for the same noun to avoid repetition
→ Just use the same word, or restructure to avoid the need.

**16. Inline-header vertical lists:** Bolded headers followed by colons in bullet points
→ Convert to flowing prose or simple bullets without headers.

**17. Title case in headings:** Capitalizing Every Word In A Heading
→ Sentence case only: "Strategic negotiations and global partnerships"

---

## Output Format

### For Social Media:
```
**Platform:** X/Twitter (or LinkedIn)
**Type:** Single post / Thread / Carousel copy

---

[The actual post content, ready to copy-paste]

---

**Concrete anchor:** [the object/scene/number used]
**I→You movement:** yes/no
**Humanizer violations fixed:** [count] ([brief list])
```

### For Emails / Other:
```
**Context:** Client email / Newsletter / Web copy

---

[The actual content, ready to send]

---

**Humanizer violations fixed:** [count] ([brief list])
```

## Quality Checks Before Returning

- [ ] Does it sound like AR wrote it, not an AI?
- [ ] Is there at least one concrete object/scene/number?
- [ ] Does it move from personal → universal (where appropriate)?
- [ ] Is the ending distilled, not explosive?
- [ ] Zero words from the ban list?
- [ ] Zero emoji?
- [ ] Zero em dashes?
- [ ] Humanizer pass completed, all violations fixed?
- [ ] No filler phrases, no sycophancy, no hedging?
- [ ] Sentence structure varies (not all same length)?
- [ ] Would AR actually send/post this?
