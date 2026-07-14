# Intent

This skill "materializes" the current discussion into a **new planning phase**
on disk:

- Creates `docs/planning/phase-<N>/`
- Writes `docs/planning/phase-<N>/plan.md` summarizing the current discussion
  as a dependency graph of agent-ready workstreams
- Derives *only* the necessary subtasks from the conversation and scaffolds:
  - `docs/planning/phase-<N>/<letter>/plan.md` for each subphase (a, b, c, ...)
- Treats subphase letters as stable IDs in a graph, not a promise of
  alphabetical execution
- Prefers safe parallel execution with explicit dependencies, verification, and
  synthesis ownership
- Ensures **all outputs are written to the filesystem** (not just in-chat)

Use this whenever the conversation reaches a new direction, architecture
decision, or a "we should plan this" moment.
