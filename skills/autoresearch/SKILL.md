---
name: autoresearch
version: 1.0.0
description: Autonomous ML experimentation loop for train.py/autoloop.sh repos; use when optimizing a fixed-budget ML run with val_bpb or another single target metric
triggers:
  - autoresearch
  - autonomous experiment
  - ML experiment loop
  - train.py optimization
  - val_bpb
  - hyperparameter search
  - Karpathy autoresearch
related_skills: [karpathy-guidelines, evaluation, advanced-evaluation, llm-application-dev, python-development]
---

# Autoresearch — Autonomous ML Experimentation

Run an autonomous experiment loop that modifies training code, runs experiments with a fixed time budget, measures results, and keeps/discards changes based on a target metric. Inspired by Karpathy's autoresearch pattern.

Last refreshed: 2026-06-10. Before relying on benchmark constants, defaults, or helper commands in this skill, verify them against the target repo's `train.py`, `prepare.py`, `autoloop.sh`, and `results.tsv`; refresh this skill if those source files change the metric, budget, output schema, or keep/discard commands.

## Core Loop

```
FOREVER:
  1. Analyze current state (git log, results.tsv, best val_bpb)
  2. Generate hypothesis (architecture change, hyperparameter tweak, optimizer mod)
  3. Modify train.py with the change
  4. git commit -m "experiment: <description>"
  5. Run: bash autoloop.sh run (5-min training, captures all metrics)
  6. Read results: bash autoloop.sh results
  7. If improved → bash autoloop.sh keep "<description>"
  8. If worse/equal → bash autoloop.sh discard "<description>"
  9. If crashed → bash autoloop.sh crash "<description>", diagnose, try fix or move on
  10. GOTO 1 — never stop, never ask permission
```

## Setup Requirements

Before starting the loop:

1. **Verify the repo**: Must have `train.py` (editable), `prepare.py` (read-only), `autoloop.sh`
2. **Create experiment branch**: `git checkout -b autoresearch/<tag>` (e.g., `autoresearch/mar9`)
3. **Verify data**: Check `~/.cache/autoresearch/` has data shards + tokenizer
4. **Initialize results.tsv**: Header row exists
5. **Run baseline**: First run is always unmodified to establish the metric to beat
6. **Record baseline**: `bash autoloop.sh keep "baseline — DEPTH=X, dim=Y, params=ZM"`
7. **Confirm current constants**: Read `train.py` before treating names/defaults such as DEPTH, RoPE base, softcap, batch size, or optimizer settings as current truth

## What You CAN Modify

- `train.py` — everything: model architecture, optimizer, hyperparams, batch size, model size, learning rates, schedules, activations, normalization, attention patterns, etc.

## What You CANNOT Modify

- `prepare.py` — read-only (evaluation harness, data loading, tokenizer, constants)
- Dependencies — only what's in `pyproject.toml`
- Time budget — always 5 minutes of training

## Experiment Ideas (Ordered by Expected Impact)

### High Impact
- **Model sizing**: Adjust DEPTH, ASPECT_RATIO, DEVICE_BATCH_SIZE to maximize VRAM usage
- **Learning rate tuning**: Scale MATRIX_LR, EMBEDDING_LR, UNEMBEDDING_LR
- **Batch size**: TOTAL_BATCH_SIZE affects gradient noise vs throughput tradeoff
- **Architecture**: GQA (n_kv_head < n_head), different MLP widths, activation functions

### Medium Impact
- **Window patterns**: Mix of S(hort) and L(ong) attention windows
- **Warmup/warmdown schedule**: WARMUP_RATIO, WARMDOWN_RATIO, FINAL_LR_FRAC
- **Weight decay**: WEIGHT_DECAY schedule and magnitude
- **Value embeddings**: Frequency and gating strategy

### Lower Impact / Exploratory
- **Softcap value**: Original benchmark snapshot used 15; verify current `train.py`, affects logit range
- **RoPE base frequency**: Original benchmark snapshot used 10000; verify current `train.py`
- **Optimizer betas**: ADAM_BETAS, Muon momentum
- **Initialization**: Weight init scales

## Decision Rules

- **Keep** if val_bpb improves (lower is better)
- **Discard** if val_bpb is equal or worse
- **Simplicity wins**: If two approaches give similar results, keep the simpler one
- **VRAM is soft constraint**: Some increase OK for meaningful gains, but don't OOM
- **Never stop**: Run experiments indefinitely until manually interrupted
- **Stack wins**: Previous kept changes compound — build on them

## Output Format

Each run prints a summary block:
```
---
val_bpb:          X.XXXXXX
training_seconds: 300.X
peak_vram_mb:     XXXX.X
mfu_percent:      X.XX
total_tokens_M:   XXX.X
num_steps:        XXX
num_params_M:     XX.X
depth:            X
```

Extract via: `grep "^val_bpb:\|^peak_vram_mb:" run.log`

## Results TSV Format

Tab-separated, 5 columns:
```
commit	val_bpb	memory_gb	status	description
```

## Integration Notes

- Works with any single-GPU training setup that has a fixed time budget and single metric
- The pattern generalizes beyond ML: any modify→run→measure→keep/discard loop
- The `autoloop.sh` helper handles run/results/keep/discard/crash/status
- For multi-GPU, adapt the run command but keep the same loop structure
