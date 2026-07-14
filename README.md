# Public Skills

A public, reusable catalog exported from the private `goatedskills` source.

The export is deliberately fail-closed. Skills containing company names, private
paths, client or operator names, credentials, session state, private datasets,
or restricted source bundles are omitted. The public development workflow is a
generic rewrite, published as `dev-workflow`.

## Use

Copy any directory under `skills/` into the skill directory used by your agent.
Each package is self-contained unless its `SKILL.md` names related skills.

The Faceplant workflow family is included:

- `deep-sweep`
- `deep-build`
- `deep-clean`
- `goal-post`
- `dev-workflow`

## Audit trail

`PUBLIC_EXPORT.json` records the exact private-source revision, checksums for
kept skills, and the reason every omitted or edited skill was handled that way.

To reproduce and verify an export from a local `goatedskills` checkout:

```bash
node scripts/export-public-skills.mjs /path/to/goatedskills
node scripts/verify-public-skills.mjs
```

The source catalog and this export are MIT licensed. Individual bundled skills
may carry additional license or attribution files, which remain in their skill
directories.
