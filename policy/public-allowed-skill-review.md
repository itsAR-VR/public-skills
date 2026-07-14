# Public-Allowed Skill Review Policy

## Purpose

This policy keeps public skill installs useful without publishing private
operator state, client data, secrets, copyrighted source bundles, or
repo-specific implementation context.

## Review Steps

1. Export from the committed source revision, never from an operator's working tree.
2. Copy only skill directories that pass the fail-closed export policy.
3. Inspect `SKILL.md`, referenced files, assets, scripts, agents, and templates.
4. Reject the skill if it contains private paths, secrets, sessions, memories,
   OAuth state, client data, raw transcripts, or company-only implementation context.
5. Reject scripts that can mutate GitHub, Vercel, billing, messaging, payments,
   production data, or local filesystem state without a clear approval gate.
6. Record source revision, destination path, checksum, and the reason for every
   removal or edit in `PUBLIC_EXPORT.json`.
7. Keep the repository private until export verification and independent review pass.

## Required Export Fields For Kept Skills

Each approved skill entry must include:

```json
{
  "name": "skill-name",
  "sourceRevision": "commit-sha-or-tag",
  "sourcePath": "skills/skill-name",
  "destinationPath": "skills/skill-name",
  "sha256": "content-tree-sha256"
}
```

## Fail-Closed Publish Rule

Publication must stop when:

- The export or verification script exits nonzero.
- Any kept skill is missing a checksum or source revision.
- Any rejected pattern appears in the install payload.
- A private dataset, source bundle, credential, local session, or client path is present.
