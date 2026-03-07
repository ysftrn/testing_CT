# Smoke Testing

## What Is It?
Smoke testing is a **quick, shallow** test to verify that the most critical functionality works after a new build or deployment. It answers: **"Is this build stable enough to test further?"**

Also known as: **Build Verification Test (BVT)** or **Sanity Check**.

The name comes from hardware testing — when you power on a new circuit board, if it doesn't smoke, it passes the first test.

## When Is It Used?
- **After every deployment** to a test environment
- **After every build** in CI/CD
- **Before starting** a full test cycle
- It's the **gatekeeper** — if smoke tests fail, the build is rejected and sent back to development

## Key Characteristics

| Property | Smoke Test | Full Test Suite |
|----------|-----------|----------------|
| Scope | Critical paths only | All features |
| Depth | Shallow | Deep |
| Duration | 5-15 minutes | Hours to days |
| Automation | Almost always automated | Mix of auto + manual |
| Frequency | Every build | Per sprint/release |

## How to Design a Smoke Suite

Pick **one positive test** for each critical feature. No negative tests, no edge cases — just "does the happy path work?"

## CryptoTracker Smoke Test Suite

| # | Test | Endpoint | Expected |
|:-:|------|----------|----------|
| 1 | Server is running | `GET /api/health` | 200, `{"status":"healthy"}` |
| 2 | Can register | `POST /api/register` | 201 |
| 3 | Can login | `POST /api/login` | 200, token returned |
| 4 | Can add to portfolio | `POST /api/portfolio` | 201 |
| 5 | Can view portfolio | `GET /api/portfolio` | 200, array with item |
| 6 | Can view prices | `GET /api/prices` | 200, non-empty array |

That's 6 tests. If any one fails, the build is rejected.

### As a Shell Script

```bash
#!/bin/bash
# smoke-test.sh — Run after deployment
BASE_URL="http://localhost:8080"
PASS=0
FAIL=0

# Test 1: Health check
STATUS=$(curl -s -o /dev/null -w "%{http_code}" $BASE_URL/api/health)
if [ "$STATUS" = "200" ]; then ((PASS++)); echo "PASS: Health check"
else ((FAIL++)); echo "FAIL: Health check (got $STATUS)"; fi

# Test 2: Register
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST $BASE_URL/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"smokeuser'$RANDOM'","password":"smoke123"}')
if [ "$STATUS" = "201" ]; then ((PASS++)); echo "PASS: Register"
else ((FAIL++)); echo "FAIL: Register (got $STATUS)"; fi

# Test 3: Login
RESPONSE=$(curl -s -X POST $BASE_URL/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"smokeuser","password":"smoke123"}')
TOKEN=$(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin).get('token',''))" 2>/dev/null)
if [ -n "$TOKEN" ]; then ((PASS++)); echo "PASS: Login"
else ((FAIL++)); echo "FAIL: Login"; fi

# ... continue for portfolio and prices

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ $FAIL -eq 0 ] && echo "SMOKE TEST: PASSED" || echo "SMOKE TEST: FAILED"
```

## Smoke vs Sanity Testing

These terms are often confused:

| | Smoke Testing | Sanity Testing |
|---|---------------|----------------|
| **When** | After a new build | After a minor change or bug fix |
| **Scope** | Entire application (critical paths) | Specific module that changed |
| **Purpose** | Is the build stable? | Is the fix working? |
| **Depth** | Very shallow | Slightly deeper in the affected area |

## Common Interview Questions
- **Q: What happens if a smoke test fails?**
  A: The build is rejected. No further testing is done until the issue is fixed and a new build is deployed.
- **Q: Who writes smoke tests?**
  A: Usually the test lead or senior tester. They're often automated and run in CI/CD.
- **Q: How many test cases should a smoke suite have?**
  A: As few as possible while covering all critical features. Typically 5-20 tests.
