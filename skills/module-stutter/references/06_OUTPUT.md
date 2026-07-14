# Output Format

A single Markdown report:

- Summary (1 paragraph)
- Findings:
  - Strongly Recommended (public API stutter)
  - Suggestions (internal/low-impact)
- For each finding:
  - Location (file + symbol + line)
  - Why it’s stutter
  - Minimal fix (rename suggestion)
  - Safer intermediate step (if renaming is risky)
