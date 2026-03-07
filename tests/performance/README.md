# Performance Testing

Load and stress testing for CryptoTracker API using **Locust** (Python) and **JMeter**.

## Tools

| Tool | Type | Strengths |
|------|------|-----------|
| **Locust** | Code-based (Python) | Version-controllable, easy scripting, real-time web UI |
| **JMeter** | GUI-based (Java) | Industry standard, rich plugin ecosystem, no coding needed |

Both tools test the same scenarios. Showing both demonstrates flexibility with different approaches.

## Test Scenarios

The load test simulates a realistic user journey:

1. **Health check** — verify server is up
2. **Register** — create a new account
3. **Login** — authenticate and get token
4. **Get prices** — browse market data (most frequent action)
5. **Add to portfolio** — buy crypto
6. **View portfolio** — check holdings
7. **Delete from portfolio** — sell/remove crypto

Task weights reflect real usage: price checks (5x) > portfolio views (3x) > adds (2x) > deletes (1x).

## Performance Test Types

| Type | Purpose | Configuration |
|------|---------|---------------|
| **Load test** | Normal expected traffic | 20 users, steady state |
| **Stress test** | Find breaking point | Ramp to 100+ users |
| **Spike test** | Sudden traffic burst | Jump from 10 to 100 users instantly |
| **Soak test** | Memory leaks, degradation | 20 users for 30+ minutes |

## Key Metrics

| Metric | What It Means | Typical Threshold |
|--------|---------------|-------------------|
| **Response time (p50)** | Median latency | < 200ms |
| **Response time (p95)** | Worst-case for most users | < 500ms |
| **Response time (p99)** | Tail latency | < 1000ms |
| **Throughput (req/s)** | Requests handled per second | Depends on capacity |
| **Error rate** | % of failed requests | < 1% |
| **Concurrent users** | Simultaneous active users | Depends on requirements |

---

## Locust

### Install

```bash
source tests/api/python/.venv/bin/activate
pip install locust
```

### Run with Web UI

```bash
# Start the server first
./server &

# Launch Locust (opens http://localhost:8089)
locust -f tests/performance/locust/locustfile.py --host=http://localhost:8080
```

Open http://localhost:8089 in your browser, set user count and ramp-up rate, and start the test.

### Run Headless (CLI only)

```bash
# 50 users, ramp 5/sec, run 60 seconds
locust -f tests/performance/locust/locustfile.py --host=http://localhost:8080 \
    --headless -u 50 -r 5 -t 60s

# Save results to CSV
locust -f tests/performance/locust/locustfile.py --host=http://localhost:8080 \
    --headless -u 50 -r 5 -t 60s --csv=results
```

### Actual Results (20 users, 30s)

| Endpoint | Requests | Failures | Median (ms) | p95 (ms) | p99 (ms) |
|----------|:--------:|:--------:|:-----------:|:--------:|:--------:|
| GET /api/health | 20 | 0 | 2 | 4 | 4 |
| POST /api/register | 20 | 0 | 89 | 100 | 100 |
| POST /api/login | 20 | 0 | 77 | 78 | 78 |
| GET /api/prices | 112 | 0 | 2 | 4 | 4 |
| GET /api/portfolio | 58 | 0 | 3 | 4 | 5 |
| POST /api/portfolio | 51 | 0 | 5 | 7 | 9 |
| DELETE /api/portfolio/* | 9 | 0 | 5 | 6 | 6 |
| **Aggregated** | **291** | **0** | **3** | **86** | **99** |

- **Error rate: 0%**
- **Throughput: ~10.6 req/s**
- Registration/login are slowest due to bcrypt password hashing (by design — security vs speed tradeoff)

---

## JMeter

### Install

```bash
# macOS
brew install jmeter

# Or download from https://jmeter.apache.org/download_jmeter.cgi
```

### Run with GUI

```bash
jmeter -t tests/performance/jmeter/CryptoTracker.jmx
```

### Run Headless (CLI)

```bash
jmeter -n -t tests/performance/jmeter/CryptoTracker.jmx \
    -l results.jtl -e -o report/
```

This generates an HTML report in `report/`.

### Test Plan Structure

```
CryptoTracker Load Test
  |-- User Defined Variables (BASE_URL, PORT)
  +-- Thread Group: User Journey (20 threads, 5 loops, 10s ramp-up)
      |-- HTTP Request Defaults
      |-- HTTP Header Manager (Content-Type: application/json)
      |-- Counter (unique usernames per thread)
      |-- Health Check (GET /api/health)
      |-- Register (POST /api/register)
      |-- Login (POST /api/login) + JSON Extractor (token)
      |-- Auth Header Manager (Bearer ${TOKEN})
      |-- Get Prices (GET /api/prices)
      |-- Add to Portfolio (POST /api/portfolio) + JSON Extractor (item ID)
      |-- Get Portfolio (GET /api/portfolio)
      |-- Delete from Portfolio (DELETE /api/portfolio/${ITEM_ID})
      |-- Think Time (1s constant timer)
      +-- Summary Report
```

### JMeter Key Concepts

| Concept | Description |
|---------|-------------|
| **Thread Group** | Simulates concurrent users (threads = users) |
| **Sampler** | An HTTP request |
| **Assertion** | Validates response (status code, body content) |
| **Extractor** | Pulls data from response (e.g., token from login) |
| **Timer** | Adds delay between requests (think time) |
| **Listener** | Collects and displays results (Summary Report, Graph) |
| **Config Element** | Shared settings (HTTP defaults, headers) |

---

## Locust vs JMeter

| Feature | Locust | JMeter |
|---------|--------|--------|
| Language | Python | Java (XML config) |
| Interface | Web UI + CLI | Desktop GUI + CLI |
| Scripting | Python code | GUI drag-and-drop |
| Version control | Easy (`.py` files) | Harder (`.jmx` XML) |
| Distributed | Built-in master/worker | Built-in remote testing |
| Learning curve | Low (if you know Python) | Medium |
| Plugins | Python packages | Large plugin ecosystem |
| Protocols | HTTP (+ custom) | HTTP, JDBC, JMS, LDAP, FTP |
| CI/CD | Simple CLI integration | CLI mode available |
| Reports | Real-time web charts + CSV | HTML report generation |
