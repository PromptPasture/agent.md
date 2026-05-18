# Performance Review

Use this reference when a change touches hot paths, data access, rendering, background work, payload size, concurrency, or resource consumption.

## Review Focus

A performance finding should identify the runtime path, the scaling variable, and why the change makes work grow or block. Avoid comments that only say something "might be slower" without a plausible size or frequency.

## Backend And Data

- Look for N+1 queries, unbounded scans, missing indexes, inefficient joins, repeated serialization, large payloads, and synchronous calls inside request paths.
- Check pagination, batching, streaming, caching, cache invalidation, query plans, transaction length, connection pool pressure, and lock contention.
- Review background jobs for queue fanout, retry storms, idempotency, rate limits, memory growth, and partial failure behavior.

## Frontend

- Look for render loops, unnecessary re-renders, expensive derived state, unstable keys, layout thrash, large bundles, unoptimized images, and blocking work on the main thread.
- Check loading, pagination, virtualization, memoization, data caching, optimistic updates, and error retries.
- Verify responsive changes do not create layout shifts or hidden expensive media loads.

## Concurrency And Resource Use

- Check unbounded parallelism, missing cancellation, timeout changes, polling frequency, event listener leaks, file handle leaks, and retained references.
- Verify backpressure exists for streams, queues, WebSockets, and external API calls.
- Treat cost regressions as performance regressions when the path runs frequently or scales with customer data.
