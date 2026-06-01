# Public Skills

Private-first reviewed skill manifests for client-device installs.

This repo exists so a client MacBook can sync only skills that have passed
public-allowed review. It is intentionally not a dump of a developer or client
home directory.

## Current Clients

| Client | Manifest | Status | Review |
| --- | --- | --- | --- |
| Suzan Galluzzo | `manifest/suzan-galluzzo.json` | approved subset, installable | https://github.com/itsAR-VR/public-skills/issues/1 |

## Rules

- Keep this repo private until every included skill is approved for
  public/client distribution.
- Do not copy full home snapshots, sessions, memories, history, OAuth state,
  `.env` files, private ZTA paths, or client data into this repo.
- Each approved skill must have a source revision, content checksum, script
  behavior review, and license/redistribution note.
- Client installers must fail closed when a manifest is missing, not installable,
  or has a checksum mismatch.
