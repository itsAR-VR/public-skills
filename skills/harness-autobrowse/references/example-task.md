# Task: <TASK_TITLE>

**URL:** <TASK_URL>
**Site:** <SITE_HOST>
**Created:** <ISO_DATE>

## Goal
<ONE_SENTENCE_GOAL>

## Inputs
<List any inputs the agent needs — credentials reference, search query,
file path, etc. Don't paste secrets here. Reference env vars or files
in the user's home directory.>

## Steps (loose — strategy.md tightens these)
1. Navigate to the URL.
2. <step 2>
3. <step 3>
4. ...

## Expected Output
```json
{
  "<field>": "<example value>",
  "<field2>": "<example value>"
}
```

## Success Criteria
A run is `pass` when ALL of these hold:
- [ ] <criterion 1>
- [ ] <criterion 2>
- [ ] The output JSON matches the schema above.

A run is `partial` when the agent reaches the goal page but extraction is
incomplete. Otherwise `fail`.

## Constraints
- <e.g., "Don't trigger any 'are you sure?' dialogs">
- <e.g., "Stay logged in — never log out">

## Notes
<Free-form scratch space — links to selectors, prior debugging notes, etc.
This file is READ-ONLY after init. Move evolving content into strategy.md.>
