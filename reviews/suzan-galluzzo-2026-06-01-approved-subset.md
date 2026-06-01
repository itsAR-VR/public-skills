# Suzan Galluzzo Public-Allowed Skills Review

Date: 2026-06-01

## Result

Approved subset for client-device sync:

- `deep-sweep`
- `goal-post`
- `deep-build`
- `deep-clean`
- `code-review`

Manifest: `manifest/suzan-galluzzo.json`

Manifest SHA-256:

```text
d156be4db359550569267d47897c60b1b03f2fa96d8c5db323fc66c42443d0cd
```

## Source

Source repo: `itsAR-VR/goatedskills`

Source revision:

```text
c11a99a09a814468836cb8c7c00fb348731328bf
```

## Skill Checksums

The checksum for each skill is the SHA-256 of the sorted per-file SHA-256 list.

| Skill | Checksum | Script review |
| --- | --- | --- |
| `deep-sweep` | `6554e757d4d556210c3a1416499eaa97ad75d18632466513f1712693a47b0626` | passed, no executable files |
| `goal-post` | `eb980a490952d58013c14bf1d858d7eb43abcf120ee72008683fe69b472514f1` | passed, no executable files |
| `deep-build` | `5dd0b59d168bc9b9c418269642c6f6ef4b958081d165f12c68fb819fd50237de` | passed, no executable files |
| `deep-clean` | `7d29f2ca1d39689495275c0fe0a14a3554d08ef5d6a7979ad42bd37cf346a44e` | passed, no executable files |
| `code-review` | `2a5546dca6657355267fed826d9a2ff51bf66a774f0b4ba4d6ee0e24baf7da05` | passed, no executable files |

## Scan Proof

Commands run from this repo after copying the approved subset:

```bash
rg -n "(/Users/AR180|ZTArepo/Z2A|sk-[A-Za-z0-9_-]{20,}|github_pat_|ghp_|xox[baprs]-|\\.env|auth\\.json|session_index|history\\.jsonl|/sessions/|refresh_token|access_token|client PII|raw transcript)" skills/deep-sweep skills/goal-post skills/deep-build skills/deep-clean skills/code-review
find skills/deep-sweep skills/goal-post skills/deep-build skills/deep-clean skills/code-review -type f -perm -111 -print
node -e "JSON.parse(require('fs').readFileSync('manifest/suzan-galluzzo.json','utf8'));"
shasum -a 256 manifest/suzan-galluzzo.json
```

Results:

- Forbidden-pattern scan returned no matches.
- Executable-file scan returned no files.
- Manifest JSON parse passed.
- Manifest checksum is recorded above.

## Deferred Candidates

The following candidates are not approved in this subset:

- `codex`
- `codex-workstation-bootstrap`
- `skill-installer`
- `browser-harness`
- `github`
- `agent-message-bus`
- `1password`

Reason: each needs separate review because it can affect execution, owner
restore/session history, token-aware installs, authenticated browser control,
GitHub credentials, plain-text message buses, or secret-manager workflows.
