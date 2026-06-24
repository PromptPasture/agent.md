# Observability — Logging, Tracing, Metrics

---

## Core Rules

- Every request gets a structured log entry with method, path, status, and latency.
- Every error gets a structured log entry with enough context to reproduce.
- Every external call (DB, HTTP, queue, cache) gets a tracing span.
- Metrics must cover request count, error rate, and latency at minimum.

---

## Structured Logging

Use structured (key-value) logging throughout. Never use string interpolation to build log messages.

```pseudocode
// Request complete
log.info("request_complete",
  method:      request.method,
  path:        request.path,
  status:      response.status,
  duration_ms: elapsed,
  request_id:  context.requestID
)

// Error
log.error("create_user_failed",
  error:      err.message,
  request_id: context.requestID,
  email:      input.email    // safe field — not a secret
)
```

Use the structured logging library available in the project stack. The shape (key-value pairs, not interpolated strings) is what matters.

### Log Levels

| Level | When |
| --- | --- |
| `DEBUG` | Detailed internal state; off in production by default |
| `INFO` | Normal operations: request complete, job started, config loaded |
| `WARN` | Degraded but recoverable: retry attempt, slow query, fallback used |
| `ERROR` | Failure requiring investigation: unhandled error, job failed permanently |

Never log at ERROR for expected failures (user not found, validation error) — those are INFO or WARN.

### What Never Goes in a Log

- Passwords, secrets, API keys, tokens
- Full credit card numbers, SSNs, or raw PII (email is acceptable at INFO; raw body is not)
- Full request/response bodies in production

---

## Request ID Propagation

Generate a unique request ID at the entry point. Attach it to every log line and return it in the response header:

```pseudocode
middleware requestID(request, next):
  id = request.headers["X-Request-ID"] ?? generateUUID()
  request.context.requestID = id
  response.headers["X-Request-ID"] = id
  return next(request)
```

When calling downstream services, forward the request ID in the outbound `X-Request-ID` header.

---

## Distributed Tracing

Use OpenTelemetry. Create a span for every operation that crosses a boundary:

```pseudocode
function createUser(context, input):
  span = tracer.startSpan("UserService.createUser", parent: context.span)
  span.setAttribute("user.role", input.role)

  try:
    result = doWork(...)
    return result
  catch error:
    span.recordError(error)
    span.setStatus(ERROR, error.message)
    throw error
  finally:
    span.end()
```

Instrument:

- Every DB query (use the ORM/driver integration if available)
- Every outbound HTTP call
- Every queue publish and consume
- Every cache read/write

Propagate trace context in HTTP headers (`traceparent`) and queue message metadata.

---

## Metrics

Expose metrics in Prometheus format or export via OpenTelemetry Metrics. Instrument at minimum:

```text
# Request metrics
http_requests_total{method, path, status}        Counter
http_request_duration_seconds{method, path}       Histogram

# Error metrics
http_errors_total{method, path, code}             Counter

# DB metrics
db_query_duration_seconds{operation, table}       Histogram
db_connections_open                               Gauge
db_connections_idle                               Gauge

# Queue metrics (when applicable)
queue_messages_published_total{queue}             Counter
queue_messages_consumed_total{queue, status}      Counter
queue_message_processing_duration_seconds{queue}  Histogram
queue_depth{queue}                                Gauge
```

---

## Health Endpoints

Expose health endpoints that load balancers and orchestrators can probe:

```text
GET /health/live   → 200 OK when the process is running
GET /health/ready  → 200 OK when the service is ready to serve traffic
                     (DB connected, migrations applied, dependencies reachable)
```

`/health/ready` should check real dependencies. Return `503` if any required dependency is down.

---

## Request Logging Middleware

Log every request at the exit point (after the handler completes, so status is known):

```pseudocode
middleware requestLogging(request, next):
  start = now()
  response = next(request)
  log.info("request",
    method:      request.method,
    path:        request.path,
    status:      response.status,
    duration_ms: now() - start,
    request_id:  request.context.requestID
  )
  return response
```
