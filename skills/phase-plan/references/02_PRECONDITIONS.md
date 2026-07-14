# Preconditions

Before writing any files:

1. Inspect the repository and verify `docs/planning/` exists.
   - If it does not exist, create it.
2. List existing phase directories under `docs/planning/`.
3. Identify the highest numbered `phase-N` directory.
4. Set `<N>` to:
   - `max(existing N) + 1`, or
   - `1` if none exist.

**Do not guess N.** Always compute it from the filesystem.
