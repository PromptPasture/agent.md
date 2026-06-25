# Workers and Queues

---

## Core Rules

- Every worker job must be idempotent. It is safe to process more than once.
- Acknowledge (ack) a message only after successful processing. Never before.
- Failed jobs must be retried with exponential backoff or moved to a dead-letter queue.
- Workers are independent processes. They share the DB but own their own lifecycle.

---

## Job Design

### Idempotency

Design every job so that running it twice produces the same outcome as running it once:

- Use a deduplication key (job ID, event ID, or a stable hash of the payload)
- Check whether the work was already done before doing it
- Use `INSERT ... ON CONFLICT DO NOTHING` or equivalent for DB writes

```pseudocode
function processOrder(job):
  if repo.isOrderProcessed(job.orderID):
    return  -- already done; safe to ack

  // do the work
  repo.markOrderProcessed(job.orderID)
```

### Payload design

- Include only IDs in the payload — load the full record from the DB at processing time
- Never include secrets or PII in the queue payload
- Include a `created_at` timestamp so consumers can detect stale jobs

```json
{
  "job_id":     "01HZK1...",
  "order_id":   "uuid",
  "created_at": "2024-06-21T12:00:00Z"
}
```

---

## Error Handling in Workers

```pseudocode
function processJob(message):
  try:
    handler(message)
    queue.ack(message)
  catch error:
    if isPermanentFailure(error):
      -- bad data, no point retrying
      log.error("permanent job failure", jobID: message.id, error: error)
      queue.nack(message, requeue: false)   -- send to dead-letter queue
    else:
      -- transient failure (DB timeout, downstream unavailable)
      log.warn("transient job failure, will retry", jobID: message.id, error: error)
      queue.nack(message, requeue: true)
```

Distinguish permanent failures (bad data — no point retrying) from transient failures (DB timeout, downstream unavailable — retry later).

---

## Retry and Backoff

Use exponential backoff with jitter on retries:

```pseudocode
delay = min(base_delay × 2^attempt, max_delay) + random_jitter
```

|Attempt|Base delay|Example with jitter|
|---|---|---|
|1|1 s|0.8–1.2 s|
|2|2 s|1.6–2.4 s|
|3|4 s|3.2–4.8 s|
|5|16 s|12.8–19.2 s|

Set a max retry count (typically 5–10). Move to a dead-letter queue after exhausting retries.

---

## Dead-Letter Queue (DLQ)

Route permanently failed jobs to a DLQ:

- Alert on DLQ depth — it signals a systemic problem
- Include the original payload, error reason, and retry count in the DLQ message
- Provide a requeue mechanism for recovering after fixing the underlying issue

---

## Graceful Shutdown

Workers must drain in-flight jobs before exiting:

```pseudocode
on SIGTERM / SIGINT:
  stop accepting new messages from the queue
  wait for all in-flight handlers to complete (with a timeout, e.g. 30 s)
  close queue connection
  exit
```

Wire shutdown to the OS signal handler at the process entry point.

---

## Concurrency

Limit concurrency explicitly — do not let the queue push unlimited parallel jobs:

```pseudocode
semaphore = Semaphore(maxConcurrency)

for each message in queue:
  semaphore.acquire()
  spawn:
    processJob(message)
    semaphore.release()
```

Tune `maxConcurrency` based on DB connection pool size and downstream rate limits.

---

## Observability

Log on every job lifecycle event:

```pseudocode
log.info("job started",   jobID: msg.id, type: msg.type)
log.info("job complete",  jobID: msg.id, durationMs: elapsed)
log.error("job failed",   jobID: msg.id, error: err, attempt: attempt)
```

Record metrics:

- Jobs enqueued, started, succeeded, failed per type
- Job processing duration (histogram)
- Queue depth (gauge, from queue API or DB count)
- DLQ depth (alert when non-zero)

---

## Scheduled Jobs (Cron)

- Use a distributed lock (Redis, DB advisory lock) when running scheduled jobs on multiple instances — only one instance should run a given job at a time
- Log start and end of every scheduled run
- Alert when a scheduled job does not run within its expected window
