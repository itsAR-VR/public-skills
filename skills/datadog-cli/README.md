# Datadog CLI Skill

A Claude Code skill for debugging and triaging with [Datadog](https://www.datadoghq.com/) logs, metrics, and dashboards.

## What it does

This skill enables Claude to use the `npx @leoflores/datadog-cli` command surface for:

- **Log search** - Query and filter logs with Datadog syntax
- **Real-time tailing** - Stream logs as they arrive
- **Trace analysis** - Follow distributed requests across services
- **Pattern detection** - Group similar log messages automatically
- **Metrics query** - Query timeseries metrics with PromQL-style syntax
- **Dashboard management** - List, create, update, and delete dashboards

## Prerequisites

Set environment variables:
```bash
export DD_API_KEY="your-api-key"
export DD_APP_KEY="your-app-key"
```

Get keys from: https://app.datadoghq.com/organization-settings/api-keys

## Running the CLI

```bash
npx @leoflores/datadog-cli <command>
```

## Usage

Once credentials are available, Claude will use the Datadog CLI skill when you ask questions like:

- "Search for error logs in the last hour"
- "Tail logs from the payments service"
- "Trace this request ID across services"
- "Show me error patterns from today"
- "What dashboards do we have?"
- "Please explain this Datadog dashboard https://app.datadoghq.com/dashboard/xxx-xxx-xxx"
- "Create a new Datadog dashboard for the metrics cpu.usage, memory.used"

## Commands Reference

| Command | Purpose |
|---------|---------|
| `npx @leoflores/datadog-cli logs search` | Search and filter logs |
| `npx @leoflores/datadog-cli logs tail` | Stream logs in real-time |
| `npx @leoflores/datadog-cli logs trace` | Find logs for a trace ID |
| `npx @leoflores/datadog-cli logs patterns` | Group similar log messages |
| `npx @leoflores/datadog-cli logs compare` | Compare current vs previous period |
| `npx @leoflores/datadog-cli logs context` | Get logs around a timestamp |
| `npx @leoflores/datadog-cli logs agg` | Aggregate logs by facet |
| `npx @leoflores/datadog-cli logs multi` | Run multiple queries in parallel |
| `npx @leoflores/datadog-cli metrics query` | Query timeseries metrics |
| `npx @leoflores/datadog-cli dashboards list` | List dashboards |
| `npx @leoflores/datadog-cli dashboards get` | Get dashboard definition |
| `npx @leoflores/datadog-cli dashboards create` | Create a dashboard |
| `npx @leoflores/datadog-cli dashboards update` | Update a dashboard |
| `npx @leoflores/datadog-cli dashboards delete` | Delete a dashboard |
| `npx @leoflores/datadog-cli errors` | Quick error summary |
| `npx @leoflores/datadog-cli services` | List services with log activity |

See the reference docs in this skill for complete command documentation.

## License

MIT
