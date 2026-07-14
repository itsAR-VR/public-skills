---
name: style-forensics-extractor
description: Extracts an author's writing style at deep linguistic and psychological levels and outputs a replication-ready JSON blueprint. Use when the user asks to analyze writing style, deconstruct voice/tone, build a style guide from samples, or recreate an author's communication fingerprint.
related_skills: [humanizer, writers-studio, writing-voice-system, mo-writing-voice-system, copywriting, writing-clearly-and-concisely]
---

# Style Forensics Extractor

Use this skill to reverse-engineer writing style into an actionable, high-fidelity blueprint.

## Trigger Signals
Activate when users ask to:
- "analyze writing style"
- "extract tone/voice"
- "deconstruct this author"
- "make me write like this"
- "build a style profile"
- "stylometric analysis" or "linguistic fingerprint"

## Required Input (ask if missing)
1. **Content samples** (minimum 3 passages, or 500+ words total)
2. **Content type** (newsletter, book chapter, landing page, tweets, etc.)
3. **Desired output use** (imitation, team style guide, QA rubric, prompt conditioning)
4. **Audience/context** (B2B/B2C, technical/non-technical, stage of funnel)

If content type is not provided, ask this exact question first:
**"What type of content are we analyzing? (book chapter, newsletter, posts, etc.)"**

## Analysis Methodology (Cognitive Archaeology)
Run this sequence every time:

1. **Surface Patterns**
   - Formatting conventions (paragraph length, bullets, headers, white space)
   - Punctuation signatures (dash use, colon cadence, parentheticals, ellipses)
   - Vocabulary profile (register, jargon density, concreteness)
   - Sentence structure (average length, branching depth, clause stacking)

2. **Psychological Architecture**
   - Persuasion frameworks in use (PAS, AIDA, jobs-to-be-done framing, contrast)
   - Emotional trigger map (fear, status, relief, aspiration, belonging)
   - Positioning mechanics (enemy, promise, authority, identity alignment)

3. **Subconscious Rhythms**
   - Pacing cycles (setup → tension → release)
   - Beat frequency (short/long sentence alternation)
   - Prosody and "musicality" (repetition, alliteration, cadence)

4. **Linguistic Fingerprints**
   - Recurring syntax templates
   - Preferred transition patterns
   - Characteristic openings/closings
   - Idiosyncratic micro-habits (e.g., one-line pivots, rhetorical questions)

5. **Influence Mechanisms**
   - Attention hooks and curiosity loops
   - Cognitive load management (chunking, signposting, contrast)
   - Behavioral pressure points (urgency, specificity, social proof cues)

6. **Replication Blueprint**
   - Rules that must be preserved
   - Degrees of freedom (what can vary without breaking style)
   - Red lines (what immediately makes writing feel "off")

## Output Contract
Return a **single JSON object** matching this schema:

```json
{
  "style_metadata": {
    "content_type": "string",
    "sample_size": {
      "documents": 0,
      "approx_words": 0
    },
    "analysis_confidence": 0,
    "uniqueness_score": 0,
    "notes": "string"
  },
  "surface_characteristics": {
    "formatting_patterns": [],
    "vocabulary_profile": {
      "register": "string",
      "technical_density": "low|medium|high",
      "concreteness": "low|medium|high",
      "signature_terms": []
    },
    "structure_patterns": [],
    "punctuation_capitalization": []
  },
  "psychological_architecture": {
    "persuasion_frameworks": [
      {
        "name": "string",
        "evidence": "string",
        "confidence": 0
      }
    ],
    "emotional_appeals": [],
    "positioning_strategy": []
  },
  "rhythm_flow": {
    "pacing_pattern": "string",
    "sentence_length_dynamics": "string",
    "musical_qualities": [],
    "cognitive_load_management": []
  },
  "linguistic_fingerprints": {
    "syntax_signatures": [],
    "transition_habits": [],
    "opening_closing_tendencies": [],
    "distinctive_idiolect_markers": []
  },
  "influence_mechanisms": {
    "attention_capture": [],
    "engagement_maintenance": [],
    "behavioral_influence": []
  },
  "voice_personality": {
    "dominant_traits": [],
    "communication_stance": "string",
    "value_expression_patterns": []
  },
  "replication_blueprint": {
    "non_negotiable_rules": [],
    "practical_guidelines": [],
    "consistency_checks": [],
    "dos": [],
    "donts": []
  },
  "effectiveness_assessment": {
    "strongest_techniques": [],
    "sophistication_level": "basic|intermediate|advanced|expert",
    "uniqueness_factors": [],
    "risks_when_imitating": []
  },
  "evidence_map": [
    {
      "pattern": "string",
      "example_quote": "string",
      "source_ref": "string",
      "confidence": 0
    }
  ]
}
```

## Quality Standards (Hard)
Every major finding must be:
- **Precise:** anchored to quoted evidence
- **Comprehensive:** cover all framework sections
- **Actionable:** usable as writing instructions
- **Deep:** mechanism + surface observation
- **Consistent:** validated across multiple examples
- **Distinctive:** isolate what is truly signature

## Confidence Scoring Rules
- 0.90+ only when pattern appears repeatedly across multiple samples and contexts
- 0.70-0.89 for strong but context-bound patterns
- 0.50-0.69 for tentative signals requiring more data
- Never present <0.50 as a core signature

## Failure Modes to Avoid
- Generic tone comments with no evidence
- Confusing topic/content with style
- Overfitting to one paragraph
- Ignoring rhythm/cadence and focusing only on vocabulary
- Giving prose summaries instead of JSON blueprint

## Minimal Workflow
1. Confirm content type and intended use.
2. Segment samples and mark recurring patterns.
3. Build evidence map first.
4. Populate JSON sections from evidence.
5. Run consistency check: every major claim must tie to evidence.
6. Return final JSON only.

## Optional Add-on
If asked, provide a **"style emulator prompt"** generated from `replication_blueprint.non_negotiable_rules` + `dos` + `donts`.

If the user wants the extracted style reused across skills, turn the blueprint
into a `writing-voice-system` profile instead of creating a one-off writing
skill. Keep the profile files small: style guide, banned patterns if needed,
primer, and revision checklist.
