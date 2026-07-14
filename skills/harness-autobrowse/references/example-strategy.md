# Strategy: <TASK_TITLE>

**Status:** baseline (no iterations yet)
**Last updated:** <ISO_DATE>

## Fast Path
<The shortest URL/sequence that gets the agent to the action. Often a
direct deep link skipping the homepage. This is usually the single
biggest reliability win once discovered.>

## Step-by-Step Workflow
```python
# browser-harness heredoc skeleton — fill in after iteration 1
new_tab("<TASK_URL>")
wait_for_load()
screenshot()  # always screenshot after navigation to verify state

# Step 1: <description>
# ...

# Step 2: <description>
# ...

# Final: extract output
result = {
    # populate per task.md schema
}
print(result)
```

## Site-Specific Heuristics
- <Add one bullet per learned rule. Examples below; delete on first edit.>
- _After clicking a Bootstrap dropdown, wait 500ms — the options animate in._
- _The cart count is at `#header-cart-count`, NOT `.cart-count` (multiple matches)._
- _Submit form via JS `document.querySelector('form').submit()` not click — the click handler is wrapped in a captcha check that fires a network call._

## Failure Recovery
- **Symptom:** _<what the agent sees>_
  **Fix:** _<what to do>_

- **Symptom:** _Page shows "Verify you're human" checkbox._
  **Fix:** _Bot detection tripped. Save a screenshot, abort, and surface to user — this site needs `browserbase-browser env remote`._

## Iteration Log
_Each line: iter#, status, hypothesis tested. Updated by finish-run.sh._

<!-- runs appended here -->
