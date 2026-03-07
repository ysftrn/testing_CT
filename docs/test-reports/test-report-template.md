# Software Test Report (STR)
## CryptoTracker v1.0

| Field | Value |
|-------|-------|
| Document ID | STR-CT-001 |
| Version | 1.1 |
| Date | 2026-03-07 |
| Author | Yusuf Torun |
| Test Cycle | Cycle 1 |
| Status | Completed |
| Test Tools | Pytest, Python unittest, Go testing, Selenium WebDriver (Chrome headless) |
| Execution Time | ~17 seconds (all suites) |

---

## 1. Summary

| Metric | Value |
|--------|-------|
| Total Test Cases | 25 |
| Executed | 25 |
| Passed | 25 |
| Failed | 0 |
| Blocked | 0 |
| Not Executed | 0 |
| Pass Rate | 100% |

---

## 2. Test Execution Results

### 2.1 Authentication Tests (TC-001 to TC-010)

| TC ID | Title | Status | Defect |
|-------|-------|:------:|--------|
| TC-001 | Successful registration | PASS | — |
| TC-002 | Short username rejected | PASS | — |
| TC-003 | Short password rejected | PASS | — |
| TC-004 | Duplicate username rejected | PASS | — |
| TC-005 | Empty body rejected | PASS | — |
| TC-006 | Successful login | PASS | — |
| TC-007 | Wrong password rejected | PASS | — |
| TC-008 | Non-existent user rejected | PASS | — |
| TC-009 | No token returns 401 | PASS | — |
| TC-010 | Invalid token returns 401 | PASS | — |

### 2.2 Portfolio Tests (TC-011 to TC-020)

| TC ID | Title | Status | Defect |
|-------|-------|:------:|--------|
| TC-011 | Add crypto to portfolio | PASS | — |
| TC-012 | Empty symbol rejected | PASS | — |
| TC-013 | Symbol auto-uppercase | PASS | — |
| TC-014 | Zero amount rejected | PASS | — |
| TC-015 | Negative amount rejected | PASS | — |
| TC-016 | View portfolio | PASS | — |
| TC-017 | Empty portfolio returns [] | PASS | — |
| TC-018 | Delete portfolio item | PASS | — |
| TC-019 | Delete non-existent item | PASS | — |
| TC-020 | Cannot delete other user's item | PASS | — |

### 2.3 Prices & Health Tests (TC-021 to TC-025)

| TC ID | Title | Status | Defect |
|-------|-------|:------:|--------|
| TC-021 | Get market prices | PASS | — |
| TC-022 | Health check | PASS | — |
| TC-023 | JSON content-type | PASS | — |
| TC-024 | Correct HTTP status codes | PASS | — |
| TC-025 | Password not in responses | PASS | — |

---

## 3. Defect Summary

| Severity | Open | Fixed | Closed | Total |
|----------|:----:|:-----:|:------:|:-----:|
| Critical | 0 | 0 | 0 | 0 |
| High | 0 | 0 | 0 | 0 |
| Medium | 1 | 0 | 0 | 1 |
| Low | 0 | 0 | 0 | 0 |

**Known Defects:**
- DR-001 (Medium): Registration accepts whitespace-only username. Intentionally deferred.

---

## 4. Exit Criteria Evaluation

| Criteria | Target | Actual | Met? |
|----------|--------|--------|:----:|
| All High priority TCs executed | 100% | 100% | YES |
| Test case pass rate | >= 95% | 100% | YES |
| No open Critical defects | 0 | 0 | YES |
| No open High defects | 0 | 0 | YES |

---

## 5. Test Suite Summary

| Suite | Framework | Tests | Status |
|-------|-----------|:-----:|:------:|
| API Tests | Pytest (Python) | 42 | ALL PASS |
| Unit Tests | Go `testing` | 25 | ALL PASS |
| Unit Tests | Python `unittest` | 22 | ALL PASS |
| UI Tests | Selenium (Chrome headless) | 23 | ALL PASS |
| **Total** | | **112** | **ALL PASS** |

## 6. Recommendations


1. **DR-001 (whitespace username):** Schedule fix for next sprint. Low risk but should be resolved before production.
2. **Additional test coverage:** Consider adding boundary tests for very long inputs (username, symbol) and concurrent access scenarios.
3. **Performance testing:** Recommended before production deployment (Phase 7).
4. **CI/CD integration:** Automate test execution on every commit via Jenkins (Phase 8).
5. **Browser matrix:** Currently tested on Chrome headless only. Extend to Firefox and Safari via Selenium Grid or BrowserStack for cross-browser coverage.

---

## 7. Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test Lead | Yusuf Torun | | 2026-03-07 |
| Project Manager | | | |
