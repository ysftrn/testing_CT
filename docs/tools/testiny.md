# Testiny — Test Management

## What is Testiny?

Testiny is a modern test management tool for organizing test cases, planning test runs, and tracking execution results. It's a lightweight alternative to TestRail or Zephyr.

## Core Concepts

| Concept | Description | CryptoTracker Example |
|---------|-------------|----------------------|
| **Project** | Top-level container | CryptoTracker |
| **Test Case** | A single test with steps and expected results | TC-001: Successful registration |
| **Test Suite** | Group of related test cases | Auth Tests (TC-001 to TC-010) |
| **Test Run** | An execution session | Sprint 1 Regression Run |
| **Test Result** | Pass/Fail/Blocked per case per run | TC-001: PASS |

## Mapping CryptoTracker Test Cases to Testiny

Our markdown test cases map directly to Testiny's structure:

### Example: TC-001 in Testiny

```
Title:        Successful User Registration
Suite:        Authentication Tests
Priority:     High
Precondition: Server running, no existing user "testuser"

Steps:
  1. Send POST /api/register
     Body: {"username": "testuser", "password": "secure123"}

Expected Result:
  - Status code 201
  - Response contains "message": "Registered successfully"

Linked Requirements: FR-001, FR-002
Tags: positive, smoke, API
```

### Test Suites

| Testiny Suite | Test Cases | Maps To |
|--------------|:----------:|---------|
| Authentication | TC-001 to TC-010 | `docs/test-cases/auth-test-cases.md` |
| Portfolio Management | TC-011 to TC-020 | `docs/test-cases/portfolio-test-cases.md` |
| Prices & Health | TC-021 to TC-025 | `docs/test-cases/prices-health-test-cases.md` |

## Test Run Workflow

```
Create Test Run
    │
    ├── Select test cases (all, by suite, or by tag)
    ├── Assign to tester
    ├── Set environment (Chrome, Firefox, API)
    │
    v
Execute Tests
    │
    ├── Mark each case: Pass / Fail / Blocked / Skipped
    ├── Add comments, screenshots, logs
    ├── Link defects (JIRA bug IDs)
    │
    v
Review Results
    │
    ├── Pass rate dashboard
    ├── Failed cases → create JIRA bugs
    └── Export report (PDF, CSV)
```

## Testiny vs Other Test Management Tools

| Feature | Testiny | TestRail | Zephyr (JIRA) | Xray (JIRA) |
|---------|---------|----------|---------------|-------------|
| Standalone | Yes | Yes | No (JIRA plugin) | No (JIRA plugin) |
| Pricing | Free tier | Paid only | Paid | Paid |
| JIRA integration | API | Built-in | Native | Native |
| CI/CD integration | API/webhooks | API | API | API |
| Learning curve | Low | Medium | Low (if you know JIRA) | Medium |
| Best for | Small-medium teams | Enterprise | JIRA-heavy teams | JIRA-heavy teams |

## Integration with CI/CD

Testiny can receive test results from automated pipelines:

```bash
# After pytest run, push results to Testiny via API
pytest tests/api/python/ --junitxml=results.xml
curl -X POST https://api.testiny.io/v1/test-runs/123/results \
    -H "Authorization: Bearer $TESTINY_TOKEN" \
    -F "file=@results.xml"
```

## Common Interview Questions

**Q: Why use a test management tool instead of spreadsheets?**
A: Test management tools provide traceability (link tests to requirements and bugs), execution history, dashboards, team collaboration, and CI/CD integration. Spreadsheets don't scale and lack audit trails.

**Q: How do you decide between Testiny, TestRail, and JIRA plugins?**
A: If the team already uses JIRA heavily, a JIRA plugin (Zephyr/Xray) keeps everything in one place. TestRail is the enterprise standard with rich reporting. Testiny is good for smaller teams wanting a clean, modern UI with a free tier.
