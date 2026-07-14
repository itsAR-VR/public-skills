---
name: anthropic-academy-course-completion
description: Complete all Anthropic Academy / Skilljar courses for an account, including enrollment, non-quiz lesson completion, quiz/survey handling, verification, and final reporting.
related_skills:
  - browser-automation
  - skill-creator
  - memory-systems
  - course-certification-pipeline

---

# Anthropic Academy Course Completion

Use this skill when asked to complete all Anthropic Academy courses for an account on Anthropic's Skilljar-hosted academy.

## What this skill is for
- Logging into Anthropic Academy / Skilljar
- Enumerating and enrolling in all catalog courses
- Completing all non-quiz lessons
- Completing surveys, quizzes, and assessments
- Verifying certificate/completion status on the profile page
- Reporting final outcomes with evidence

## Canonical sites
- Anthropic Academy hub: `https://www.anthropic.com/learn`
- Skilljar catalog/home: `https://anthropic.skilljar.com/`
- Catalog: `https://anthropic.skilljar.com/catalog`
- Profile: `https://anthropic.skilljar.com/accounts/profile/`

## Execution model
There are three phases.

### Phase 1: Enroll + complete non-quiz lessons
Goal: move through every course, enrolling where needed and completing all non-quiz lessons fast.

Preferred approach:
1. Log into Skilljar with the account provided by the user.
2. Open the catalog.
3. Enumerate all courses.
4. For each course:
   - enroll if needed
   - enumerate lessons
   - for each lesson:
     - if video/reading/non-quiz, complete it
     - if quiz/survey/assessment, skip for Phase 2 and record it
5. Persist a machine-readable artifact with enrolled courses, completed lessons, and skipped quiz-like lessons.

Historical workflow reference from user-provided original prompt:
- Use browser/CDP against the selected browser profile
- Direct lesson navigation is acceptable
- `lessonPlayerCompleteCallback()` may fire the internal completion handler for non-quiz lessons where present
- Detection hints for quiz-like lessons may include:
  - `.quiz` or `.sj-quiz`
  - body text containing `Question 1 of`
  - `window.completeBeforeAdvance`

Example detection snippet from the user-provided prompt:
```js
var isQuiz = !!document.querySelector('.quiz, .sj-quiz') ||
  document.body.innerText.includes('Question 1 of') ||
  (typeof window.completeBeforeAdvance !== 'undefined' && window.completeBeforeAdvance);
```

If using browser evaluate/CDP, write a Phase 1 artifact similar to:
- enrolled courses (name, slug, total lessons)
- completed lessons (lesson id, course slug)
- skipped lessons (lesson id, course slug, lesson name)

### Phase 2: Quizzes, surveys, and assessments
Goal: finish all graded/interactive lessons that were skipped in Phase 1.

Rules:
- Do not fake completion via direct API POSTs.
- Read the question text and options.
- Reason about the best answer from course context.
- If it is clearly a satisfaction/survey item, choose the most positive answer.
- If a quiz fails and retakes are allowed, retake immediately.
- Keep notes on questions answered incorrectly so retries improve.

Answer heuristics from the user-provided original prompt:
- Source check: these heuristics were last checked against the user-provided
  prompt on 2026-06-10. If current course text, Anthropic docs, or quiz wording
  conflicts with them, refresh from the live lesson/source before answering.
- Claude/Anthropic:
  - Claude is stateless unless history/context is passed
  - temperature 0 is deterministic, higher values are more creative
  - do not put API keys client-side
  - streaming improves perceived latency
- MCP:
  - standardizes how AI connects to tools and data
  - servers expose tools and resources
  - common transports include stdio and HTTP/SSE
- AI Fluency:
  - Design, Describe, Discern, Diligence
- Prompt engineering/evals:
  - use multiple test cases
  - grader types may include code, human, and model graders
  - XML tags help structure prompts
  - few-shot means sample IO pairs
- Claude Code:
  - custom commands can live in `.claude/commands/`
  - hooks like PreToolUse and PostToolUse modify behavior
- Survey / linear scale questions:
  - choose the most positive option

Useful DOM pattern from the user-provided original prompt:
```js
var question = document.querySelector('.question-text p, #sj-quiz-question-text p')?.textContent.trim()
var radios = Array.from(document.querySelectorAll('input[type=radio][name=answer], input[type=radio][name=linear-scale-question], input[type=radio][name=chosen_answers]'))
var options = radios.map((r, i) => ({ idx: i, text: (r.closest('label') || r.parentElement).textContent.trim() }))
```

Then click the chosen answer and advance with the enabled `Next`, `Submit`, or `Finish` button.

### Phase 3: Verify + report
1. Open the profile page.
2. Confirm each course shows certificate availability or 100% completion.
3. Capture a screenshot if supported.
4. Produce a final summary with:
   - total courses completed
   - any remaining incomplete courses and why
   - certificate/profile verification links if available
5. Only report success after verification.

## Operating notes
- Skilljar authentication is separate from standard Claude app auth.
- A logged-in browser session is often the fastest unblock path.
- If the user gives credentials explicitly in-chat for the task, they may be used for that task. Do not echo them back.
- Prefer one active browser lane for account-sensitive completion work.
- Close tabs opened for the task once finished.

## Memory and provenance
This skill was created from:
1. live observed Anthropic Academy / Skilljar flow in-thread
2. the user-provided original prompt/spec pasted in chat

No prior memory-search hits were found for an older saved version of this workflow at creation time, so do not claim historical provenance beyond the prompt the user supplied in the current thread.

## Deliverable format
Keep updates outcome-based:
- kickoff with task / execution started / ETA / changed files
- milestone only when a real delta exists
- final digest with verified completion state
