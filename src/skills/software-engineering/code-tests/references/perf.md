# Load & Performance Testing Reference

Guidance for writing load, stress, soak, and spike tests (k6, Locust, Artillery, Gatling).

---

## Framework Detection

| Signal | Framework |
| --- | --- |
| `k6/` dir or `.js` files importing `k6` | k6 |
| `locustfile.py` or `locust` in deps | Locust |
| `artillery.yml` / `artillery` in deps | Artillery |
| `gatling` in pom.xml or build.gradle | Gatling |

---

## Load Profile Types

Identify the correct profile from user intent:

| Test type | Pattern | Purpose |
| --- | --- | --- |
| Load test | Ramp to target VUs, hold, ramp down | Verify behaviour under expected traffic |
| Stress test | Ramp beyond expected capacity | Find the breaking point |
| Soak test | Hold target VUs for extended duration (hours) | Detect memory leaks and degradation over time |
| Spike test | Sudden large VU increase, then drop | Verify recovery from traffic bursts |

---

## Test Plan Format

When drafting the test plan in Phase 2, define the load profile and acceptance thresholds:

```text
Target:     POST /api/v1/search
Profile:    Load test
Duration:   5 min ramp-up → 10 min hold → 2 min ramp-down
VUs:        0 → 200 → 200 → 0

Thresholds:
  http_req_duration p(95) < 500ms
  http_req_duration p(99) < 1000ms
  http_req_failed   < 1%
  http_reqs         > 100/s (throughput floor)

Scenarios:
  Search with typical query (80% of traffic)
  Search with empty results (15%)
  Search with max result page size (5%)
```

---

## k6 Script Structure

```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';
import { Rate } from 'k6/metrics';

const errorRate = new Rate('errors');

export const options = {
  stages: [
    { duration: '5m', target: 200 },
    { duration: '10m', target: 200 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
    errors: ['rate<0.01'],
  },
};

export default function () {
  const res = http.post(`${__ENV.BASE_URL}/api/v1/search`, JSON.stringify({
    query: 'laptop',
    page: 1,
  }), { headers: { 'Content-Type': 'application/json' } });

  const ok = check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
    'has results field': (r) => JSON.parse(r.body).results !== undefined,
  });

  errorRate.add(!ok);
  sleep(1);
}
```

---

## Threshold Design

Always define thresholds — a load test without thresholds does not pass or fail CI:

- **p(95) latency**: covers the experience of 95% of users; primary SLO metric
- **p(99) latency**: catches long tail; set 2–3× the p95 threshold
- **error rate**: set below 1% for production-critical paths
- **throughput floor**: set a minimum req/s to catch performance regressions disguised as low traffic

Thresholds must match the team's SLOs. If SLOs are unknown, ask in Phase 2 before writing.

---

## Realistic Traffic Shaping

- Mix scenario weights to reflect real traffic distribution
- Include think time (`sleep`) between requests to simulate realistic user behaviour
- Use parameterised data (CSV or generated) to avoid cache effects skewing results
- If auth is required, pre-generate tokens in `setup()` — do not authenticate during the load run

```javascript
export function setup() {
  const res = http.post(`${__ENV.BASE_URL}/auth/token`, JSON.stringify({
    username: __ENV.TEST_USER,
    password: __ENV.TEST_PASSWORD,
  }), { headers: { 'Content-Type': 'application/json' } });
  return { token: JSON.parse(res.body).access_token };
}

export default function (data) {
  http.get(`${__ENV.BASE_URL}/api/v1/profile`, {
    headers: { Authorization: `Bearer ${data.token}` },
  });
}
```

---

## CI Integration

- Run load tests in a dedicated CI stage, not alongside unit or integration tests
- Use environment variables for `BASE_URL`, credentials, and VU counts
- k6 exits with a non-zero code automatically when any threshold is breached — no extra flag needed; the CI step fails on its own
- Store HTML or JSON results as CI artifacts for trend analysis

---

## P2 Checklist (Load-specific)

- [ ] Thresholds defined for p95 latency, error rate, and throughput
- [ ] Load profile matches the declared test type (load, stress, soak, spike)
- [ ] Auth tokens generated in `setup()`, not during the load loop
- [ ] Traffic mix reflects realistic scenario weights
- [ ] Think time (`sleep`) included between requests
- [ ] Parameterised data used to avoid cache skewing results
- [ ] BASE_URL and credentials loaded from environment variables
- [ ] CI step fails on threshold breach
