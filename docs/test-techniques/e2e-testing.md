# End-to-End (E2E) Testing

## What Is It?
End-to-End testing validates a **complete user workflow** from start to finish, through all layers of the application. It simulates real user behavior — a full journey, not isolated features.

It answers: **"Can a user accomplish their goal using this application?"**

## When Is It Used?
- Before release (final validation)
- After integration of all components
- To validate critical business workflows
- In CI/CD as a final gate before deployment

## How It Differs from Other Test Types

| Test Type | Scope | Example |
|-----------|-------|---------|
| Unit Test | Single function | `Register()` validates username length |
| Integration Test | Two components together | Handler correctly calls Service |
| System Test | All requirements | FR-002 is satisfied |
| **E2E Test** | **Complete user journey** | **User registers, logs in, manages portfolio, logs out** |

## The Testing Pyramid

```
        /  E2E  \          ← Few, slow, expensive
       /  System  \
      / Integration \
     /   Unit Tests   \    ← Many, fast, cheap
    /___________________\
```

E2E tests sit at the top — you write fewer of them because they're slow and expensive to maintain. But they catch issues that lower-level tests miss (like a UI that doesn't send the right data to the API).

## CryptoTracker E2E Scenarios

### E2E-001: New User Complete Journey

**Precondition:** Application is deployed. No existing user "e2euser".

| Step | User Action | System Response | Verify |
|:----:|-------------|----------------|--------|
| 1 | Open browser to http://localhost:8080 | Login page displayed | Page loads, form visible |
| 2 | Enter username "e2euser", password "secure123" | — | Fields accept input |
| 3 | Click "Register" | "Registered! You can now login." | Success message shown |
| 4 | Click "Login" (same credentials) | Dashboard appears | Auth section hidden, dashboard visible |
| 5 | View market prices table | BTC, ETH, SOL, ADA, DOT listed | 5 rows with prices |
| 6 | Enter "BTC", amount "0.5", click "Add" | "Added BTC!" message | Success message shown |
| 7 | Enter "ETH", amount "10", click "Add" | "Added ETH!" message | Portfolio shows 2 items |
| 8 | Click "Delete" on ETH row | ETH removed from table | Portfolio shows only BTC |
| 9 | Click "Logout" | Login page reappears | Dashboard hidden, form visible |
| 10 | Login again with same credentials | Dashboard with BTC in portfolio | Data persisted |

### E2E-002: Authentication Failure Flow

| Step | User Action | System Response | Verify |
|:----:|-------------|----------------|--------|
| 1 | Open browser to http://localhost:8080 | Login page displayed | — |
| 2 | Enter username "nobody", password "wrong123" | — | — |
| 3 | Click "Login" | Error: "invalid credentials" | Error message shown in red |
| 4 | Correct the username to a registered user, click "Login" | Dashboard appears | Recovery works |

### E2E-003: API-Only Journey (No UI)

This is the same workflow but via API calls — useful for automated E2E in CI/CD:

```bash
# 1. Register
curl -X POST http://localhost:8080/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"e2euser","password":"secure123"}'

# 2. Login
TOKEN=$(curl -s -X POST http://localhost:8080/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"e2euser","password":"secure123"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['token'])")

# 3. Add BTC
BTC_ID=$(curl -s -X POST http://localhost:8080/api/portfolio \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"symbol":"BTC","amount":0.5}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 4. Add ETH
ETH_ID=$(curl -s -X POST http://localhost:8080/api/portfolio \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"symbol":"ETH","amount":10}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 5. Verify portfolio has 2 items
curl -s http://localhost:8080/api/portfolio -H "Authorization: Bearer $TOKEN"

# 6. Delete ETH
curl -X DELETE "http://localhost:8080/api/portfolio/$ETH_ID" \
  -H "Authorization: Bearer $TOKEN"

# 7. Verify portfolio has only BTC
curl -s http://localhost:8080/api/portfolio -H "Authorization: Bearer $TOKEN"
```

## Common Interview Questions
- **Q: What's the difference between E2E and system testing?**
  A: E2E follows user journeys (workflows). System testing checks all individual requirements. E2E might skip requirements that aren't part of a user flow.
- **Q: Why not write only E2E tests?**
  A: They're slow, brittle, and hard to debug. When an E2E fails, you don't know which layer broke. The testing pyramid says: many unit tests, some integration, few E2E.
- **Q: Who writes E2E tests?**
  A: Usually QA/test engineers. In some teams, developers write them too. They're often automated with tools like Selenium (UI) or Postman/Python (API).
