---
name: shopify-admin-api
description: >
  Shopify Admin API integration skill for OAuth/requested-vs-granted scopes,
  protected customer data, Admin REST/GraphQL version pinning, GraphQL cost
  throttling, defensive 429 handling, and Bulk Operations safety. Use when
  building or reviewing Shopify Admin API code, lifecycle historical order
  proof, read_all_orders, currentAppInstallation.accessScopes, bulk
  operations, webhook registration, or Shopify rate-limit handling.
---

# Shopify Admin API

Use this skill for Shopify Admin API work where correctness depends on official
API behavior rather than local assumptions.

## Source-First Rules

- Check official Shopify docs before changing API-version, scope, protected-data,
  rate-limit, webhook, or bulk-operation behavior.
- Pin explicit API versions in code and config. Do not use `latest` as a runtime
  contract.
- Treat REST Admin, GraphQL Admin, and webhooks as versioned surfaces. Use one
  shared version policy only if compatibility is verified.
- If Shopify docs conflict, choose the safer operational policy and record the
  conflict in the phase/PR notes.

Primary docs:

- Bulk Operations guide: https://shopify.dev/docs/api/usage/bulk-operations/queries
- `bulkOperationRunQuery`: https://shopify.dev/docs/api/admin-graphql/latest/mutations/bulkOperationRunQuery
- `BulkOperation` object: https://shopify.dev/docs/api/admin-graphql/latest/objects/BulkOperation
- GraphQL Admin limits: https://shopify.dev/docs/api/usage/limits
- Access scopes: https://shopify.dev/docs/api/usage/access-scopes
- Protected customer data: https://shopify.dev/docs/apps/launch/protected-customer-data
- `currentAppInstallation`: https://shopify.dev/docs/api/admin-graphql/latest/queries/currentAppInstallation
- `Order` object: https://shopify.dev/docs/api/admin-graphql/latest/objects/Order
- `CustomerJourneySummary`: https://shopify.dev/docs/api/admin-graphql/latest/objects/CustomerJourneySummary

## Access And Scope Rules

- Separate requested scopes, granted installed scopes, and protected customer
  data approval. Never collapse them into one boolean.
- Requested scopes from app config or env prove only intent.
- Runtime lifecycle readiness must use granted installed scopes from Shopify,
  preferably `currentAppInstallation.accessScopes`, or an equivalent safe
  refresh/probe.
- Historical orders older than 60 days require all-order access such as
  `read_all_orders` together with order scopes.
- Protected customer data approval is separate from OAuth scopes. Missing or
  redacted customer fields must fail closed with safe issue codes.
- Do not store raw email, phone, or customer-linked order identifiers in proof
  artifacts, logs, tests, or rollout notes.

## OAuth And Connection Rules

- Apply the same brand/state/shop binding checks to every install path:
  classic OAuth callback, managed token exchange, and manual-token connection.
- Persist granted-scope metadata consistently for callback and token-exchange
  paths.
- Manual-token installs should be marked scope-unknown until a safe probe proves
  scope/protected-data readiness.
- Do not accept caller-provided proof flags, such as `hasLifetimeProof`, as a
  trust-bearing contract.

## GraphQL Rate-Limit Rules

- Admin GraphQL rate limits use calculated query cost and
  `extensions.cost.throttleStatus`.
- Handle GraphQL `THROTTLED` errors explicitly.
- Handle HTTP `429` defensively. Honor `Retry-After` when present, but do not
  assume it is the primary GraphQL query-cost contract.
- Keep retry budgets bounded. Do not introduce unbounded sleeps in Next.js
  request handlers.
- Separate request-layer backoff from durable workflow polling cadence.

## Bulk Operation Rules

- Use Bulk Operations for large historical exports.
- Result URLs expire; completed-without-usable-URL paths should retry/replan,
  not bypass safety.
- Webhooks are preferred when available, but polling may still be required.
- Shopify docs can differ by API version on bulk-operation concurrency and
  polling query shape. Keep Kynship serialized unless multi-operation ownership,
  window claims, and CAS completion are explicitly designed.
- For API versions that support it, prefer specific operation visibility such as
  `bulkOperation(id:)`; use `currentBulkOperation` only when appropriate for the
  pinned version or as a tested compatibility fallback.

## Test Matrix

At minimum, cover:

- requested-but-not-granted scope;
- missing `read_all_orders`;
- missing protected-data evidence;
- redacted/missing protected customer fields;
- callback, token exchange, and manual-token connection modes;
- GraphQL `THROTTLED`;
- HTTP `429` with and without `Retry-After`;
- low `throttleStatus.currentlyAvailable`;
- max retry exhaustion;
- active remote bulk operation contention;
- completed bulk operation with expired or missing URL.
