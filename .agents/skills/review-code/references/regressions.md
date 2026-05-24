# Regression Review

Use this reference when the change may alter existing behavior, compatibility, deployment safety, or integration contracts.

## Review Focus

**Compare old behavior against new behavior.**

A regression finding should name the previous contract, the changed condition, and the user, integration, or deployment path that now fails.

## Compatibility

**Check externally visible contracts before assuming a change is internal.**

- **Public APIs**: status codes, response shape, error shape, pagination, sorting, filtering, headers, idempotency, and versioning.
- **CLI and configuration**: flags, defaults, environment variables, config file keys, validation, and backwards-compatible parsing.
- **Persistence**: schema changes, nullable fields, default values, migrations, data backfills, cache keys, message formats, and serialized state.
- **Integrations**: webhook payloads, event names, queue topics, external API expectations, auth scopes, rate limits, and retry semantics.

## Rollout And Rollback

**Check whether deployment and rollback can tolerate mixed versions.**

- **Mixed versions**: check whether old and new application versions can run against the same database, cache, queue, or message format.
- **Deployment order**: look for coupling between code, migrations, feature flags, config, and generated clients.
- **Rollback**: verify rollback behavior when a migration, data write, or external side effect is not reversible.
- **Data meaning**: treat silent data reinterpretation as high risk even when tests pass.

## Common Findings

**Look for common compatibility breaks that tests often miss.**

- **Defaults**: a default changes for existing users without a migration path.
- **Response shape**: a response field is removed, renamed, or changes type without versioning.
- **Migrations**: a migration requires all code to deploy atomically.
- **Feature flags**: a feature flag guards UI behavior but not the backend contract.
- **Dependencies**: a dependency update changes runtime requirements or transitive behavior without matching CI or deployment changes.
