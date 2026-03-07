# Performance Testing

## Definition

Performance testing verifies that a system meets non-functional requirements for speed, scalability, stability, and resource usage under expected and peak loads.

## Types of Performance Tests

### Load Testing
- Simulate **normal expected traffic** to verify the system handles it
- Example: 20 concurrent users browsing prices and managing portfolios
- Goal: confirm response times stay within thresholds

### Stress Testing
- Push the system **beyond normal capacity** to find the breaking point
- Example: ramp from 20 to 200 users until errors appear
- Goal: identify failure modes and recovery behavior

### Spike Testing
- Apply a **sudden burst** of traffic
- Example: jump from 10 to 100 users instantly, then back to 10
- Goal: verify the system recovers gracefully from traffic spikes

### Soak Testing (Endurance)
- Run at **normal load for an extended period** (hours)
- Example: 20 users for 4 hours continuously
- Goal: detect memory leaks, connection pool exhaustion, disk space issues

### Scalability Testing
- Gradually increase load while monitoring **resource utilization**
- Goal: determine how much capacity can be added by scaling up/out

## Key Metrics

| Metric | Definition | CryptoTracker Threshold |
|--------|-----------|------------------------|
| Response time (p50) | Median latency | < 200ms |
| Response time (p95) | 95th percentile | < 500ms |
| Response time (p99) | 99th percentile | < 1000ms |
| Throughput | Requests per second | > 10 req/s per user |
| Error rate | Failed requests / total | < 1% |
| CPU usage | Server processor load | < 80% |
| Memory usage | Server RAM consumption | Stable (no growth over time) |

## CryptoTracker Performance Results

Tested with Locust: 20 concurrent users, 30-second run.

| Endpoint | Median | p95 | Notes |
|----------|:------:|:---:|-------|
| GET /api/health | 2ms | 4ms | Fastest — no DB access |
| GET /api/prices | 2ms | 4ms | Static data, no auth |
| GET /api/portfolio | 3ms | 4ms | DB read + auth check |
| POST /api/portfolio | 5ms | 7ms | DB write + validation |
| DELETE /api/portfolio | 5ms | 6ms | DB write + ownership check |
| POST /api/login | 77ms | 78ms | Slow by design (bcrypt) |
| POST /api/register | 89ms | 100ms | Slow by design (bcrypt) |

**Why are login/register slow?** bcrypt password hashing is intentionally CPU-intensive to resist brute-force attacks. This is a security vs. performance tradeoff — the right tradeoff for authentication endpoints.

## Tools Comparison

| Tool | Best For |
|------|----------|
| **Locust** | Python teams, code-first approach, CI/CD pipelines |
| **JMeter** | GUI-based testing, protocol variety, enterprise environments |
| **k6** | JavaScript teams, developer-friendly, cloud integration |
| **Gatling** | Scala/Java teams, high-performance simulation |
| **Artillery** | Node.js teams, quick YAML-based tests |
| **wrk/hey** | Simple HTTP benchmarking, no scripting needed |

## Performance Testing in SDLC

```
Requirements  →  Define SLAs (response time < 500ms, 99.9% uptime)
Design        →  Capacity planning (expected users, peak hours)
Development   →  Developer profiling, micro-benchmarks
Testing       →  Load tests, stress tests, soak tests
Staging       →  Full performance test suite on production-like environment
Production    →  Monitoring, alerting, APM tools
```

## Common Interview Questions

**Q: What's the difference between load testing and stress testing?**
A: Load testing verifies the system works under *expected* traffic. Stress testing pushes *beyond* capacity to find the breaking point. Load test = "does it work?" Stress test = "when does it break?"

**Q: How do you determine performance thresholds?**
A: From SLA/SLO agreements, business requirements, or industry benchmarks. For APIs: p95 < 500ms is common. For web pages: Google recommends Largest Contentful Paint < 2.5s.

**Q: Why might response times degrade under load?**
A: Resource contention (CPU, memory, DB connections), thread pool exhaustion, garbage collection pauses, network saturation, or inefficient queries that scale poorly.

**Q: What is the "think time" in performance testing?**
A: The pause between user actions that simulates real human behavior. Without think time, tests generate unrealistically high request rates. Typical think time: 1-5 seconds.

**Q: How do you identify bottlenecks?**
A: Correlate performance metrics with system metrics. If CPU is at 100% but memory is low, it's CPU-bound. If response times spike when DB connections are maxed, it's a connection pool issue. Tools: APM (Application Performance Monitoring), profilers, DB query analyzers.
