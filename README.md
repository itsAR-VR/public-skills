# Public Skills

A curated public catalog exported from a larger private source.

The export is deliberately fail-closed and allowlisted. Skills containing company names, private
paths, client or operator names, credentials, session state, private datasets,
or restricted source bundles are omitted. Internal orchestration, client-delivery,
company-context, taste-layer, and machine-routing skills stay private by default.
The public development workflow is a generic rewrite, published as `dev-workflow`.

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

`PUBLIC_EXPORT.json` records the source type, checksums for kept skills, and
aggregate removal reasons. Private catalog names are not published.
`policy/public-skill-allowlist.txt` is the only set eligible for publication;
new private-source skills do not become public automatically.

To reproduce and verify an export from an authorized private-source checkout:

```bash
node scripts/export-public-skills.mjs /path/to/private-skill-source
node scripts/verify-public-skills.mjs
```

The source catalog and this export are MIT licensed. Individual bundled skills
may carry additional license or attribution files, which remain in their skill
directories.
