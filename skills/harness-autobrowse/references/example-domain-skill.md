# <site> / <task> — browser-harness domain skill

**Source:** Graduated from harness-autobrowse on <ISO_DATE> after passing
2 of the last 3 iterations. Replaces ad-hoc exploration of this site.

## When to Use
<One sentence describing when an agent on this site should reach for this map.>

## Fast Path
<Same as strategy.md's Fast Path — the shortcut URL/sequence.>

## Workflow
```python
new_tab("<URL>")
wait_for_load()
# ... the proven helper sequence ...
```

## Selectors and Endpoints
| What | Where | Notes |
|---|---|---|
| <element> | `#some-id` | <stability note: "rare A/B test variant uses .alt-id"> |
| <element 2> | `[data-testid="..."]` | <stability note> |

## Heuristics
- <Site-specific rule 1>
- <Site-specific rule 2>

## Traps
- **<Symptom>** → <fix>

## Last Verified
<ISO_DATE> — by harness-autobrowse iteration <N>. Re-graduate if the
site's structure changes.
