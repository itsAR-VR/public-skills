# Public-Allowed Skill Review Policy

## Purpose

This policy keeps client-device skill installs useful without copying private
operator state, client data, secrets, or repo-specific implementation context
onto a client's laptop.

## Review Steps

1. Select one candidate skill from an approved source.
2. Copy only the skill directory needed for review into a staging branch.
3. Inspect `SKILL.md`, referenced files, assets, scripts, agents, and templates.
4. Reject the skill if it contains private paths, secrets, sessions, memories,
   OAuth state, client data, raw transcripts, or ZTA-only implementation context.
5. Reject scripts that can mutate GitHub, Vercel, billing, messaging, payments,
   production data, or local filesystem state without a clear approval gate.
6. Record source repo, source revision, destination path, checksum, script review,
   license/redistribution note, and reviewer in the client manifest.
7. Keep `installable` false until every listed skill has passed review.

## Required Manifest Fields For Approved Skills

Each approved skill entry must include:

```json
{
  "name": "skill-name",
  "sourceRepo": "owner/repo",
  "sourceRevision": "commit-sha-or-tag",
  "sourcePath": "skills/skill-name",
  "destinationPath": "skills/skill-name",
  "sha256": "content-tree-or-archive-sha256",
  "license": "license-name-or-review-note",
  "scriptReview": "passed|not-applicable",
  "approvedBy": "github-handle",
  "approvedAt": "YYYY-MM-DD"
}
```

## Fail-Closed Install Rule

Client installers must refuse to sync this repo when:

- `installable` is false.
- Manifest checksum differs from the queue job.
- Any approved skill is missing a checksum, source revision, or review note.
- Any rejected pattern appears in the install payload.
- The repo/ref differs from the queue-approved manifest.
