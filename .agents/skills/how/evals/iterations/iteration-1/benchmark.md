# Skill Benchmark: how

**Type**: Routing eval
**Agent**: codex
**Method**: agent_routing_judgment
**Runs per query**: 1

## Summary

| Metric | Value |
| --- | --- |
| Pass rate | 10/10 (100%) |
| Positive trigger cases | 8/8 |
| Negative near-miss cases | 2/2 |

## Cases

- PASS: expected=True, rate=100% - /how user signup
- PASS: expected=True, rate=100% - How does authentication work in this codebase?
- PASS: expected=True, rate=100% - How does the payment webhook flow work, including validation and idempotency?
- PASS: expected=True, rate=100% - Walk me through how background jobs are scheduled and executed here.
- PASS: expected=True, rate=100% - How does configuration get loaded and passed into services?
- PASS: expected=True, rate=100% - Explain the architecture of the search subsystem.
- PASS: expected=True, rate=100% - Can you critique the architecture of the billing module?
- PASS: expected=True, rate=100% - What is wrong with the way this app handles authorization?
- PASS: expected=False, rate=0% - Summarize the README.
- PASS: expected=False, rate=0% - Implement a new endpoint for exporting audit logs.
