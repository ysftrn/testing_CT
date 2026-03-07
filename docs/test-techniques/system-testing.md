# System Testing

## What Is It?
System testing validates the **complete, integrated system** against the Software Requirements Specification (SRS). Unlike E2E testing (which follows user journeys), system testing methodically checks **every requirement** — both functional and non-functional.

It answers: **"Does the system meet ALL its specified requirements?"**

## When Is It Used?
- After integration testing is complete
- Before User Acceptance Testing (UAT)
- It's the last level of testing before the software is handed to the customer/stakeholders
- Performed in an environment as close to production as possible

## Where It Fits in the V-Model

```
Requirements  ←──────────────→  System Testing
  ↓                                    ↑
High-Level Design ←────────→  Integration Testing
  ↓                                    ↑
Detailed Design ←──────────→  Unit Testing
  ↓                                    ↑
    Implementation (Coding)
```

System testing is paired with the **Requirements** phase — it validates that what was specified is what was built.

## How It Differs from E2E

| Aspect | System Testing | E2E Testing |
|--------|---------------|-------------|
| **Driven by** | Requirements (SRS) | User scenarios |
| **Coverage** | Every requirement | Critical user flows |
| **Includes** | Functional + Non-functional | Mainly functional |
| **Goal** | Full requirements coverage | Workflow validation |

## CryptoTracker System Test Approach

We go through the SRS requirement by requirement:

### Functional Requirements Check

| Req ID | Requirement | How to Verify | Test Case |
|--------|------------|---------------|-----------|
| FR-001 | Registration with username/password | API call with valid data | TC-001 |
| FR-002 | Username >= 3 chars | Try 2 chars, 3 chars | TC-002 |
| FR-003 | Password >= 6 chars | Try 5 chars, 6 chars | TC-003 |
| ... | ... | ... | ... |
| FR-030 | Logout clears session | Click logout, verify state | (UI test) |

### Non-Functional Requirements Check

| Req ID | Requirement | How to Verify |
|--------|------------|---------------|
| NFR-001 | Response within 500ms | Measure response times with JMeter |
| NFR-002 | 100 concurrent users | Load test with JMeter |
| NFR-003 | All responses JSON | Check Content-Type header on every endpoint |
| NFR-004 | Standard HTTP codes | Verify 200, 201, 400, 401, 404 used correctly |
| NFR-005 | Cross-platform | Build and run on Linux, macOS, Windows |
| NFR-006 | SQLite persistence | Restart server, verify data persists |
| NFR-007 | Passwords never in responses | Inspect every API response |

## System Test Execution

The system test is typically documented in a matrix:

| # | Req ID | Test Description | Expected | Actual | Pass/Fail |
|:-:|--------|-----------------|----------|--------|:---------:|
| 1 | FR-001 | Register new user | 201, success message | — | — |
| 2 | FR-002 | Register with 2-char username | 400, error | — | — |
| 3 | FR-003 | Register with 5-char password | 400, error | — | — |
| ... | ... | ... | ... | ... | ... |
| 37 | NFR-007 | Check no password in any response | No password field | — | — |

This matrix becomes part of the **Test Report (STR)**.

## Common Interview Questions
- **Q: What's the difference between system testing and integration testing?**
  A: Integration testing checks how components work together. System testing checks the complete system against all requirements.
- **Q: Who performs system testing?**
  A: Usually a dedicated QA/test team, independent from the development team. This independence reduces bias.
- **Q: Can system testing be automated?**
  A: Functional parts can be automated (API tests, UI tests). Non-functional parts (performance, usability) often require specialized tools or manual evaluation.
