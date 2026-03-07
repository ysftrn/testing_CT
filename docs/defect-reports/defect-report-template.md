# Defect Report Template
## CryptoTracker v1.0

---

## DR-001: [Sample] Registration Accepts Whitespace-Only Username

| Field | Value |
|-------|-------|
| **Defect ID** | DR-001 |
| **Title** | Registration accepts a username consisting only of spaces |
| **Reported By** | Yusuf Torun |
| **Date Reported** | 2026-03-06 |
| **Severity** | Medium |
| **Priority** | Medium |
| **Status** | Open |
| **Environment** | macOS, Go 1.26, SQLite 3.x, localhost:8080 |
| **Related Req** | FR-002 |
| **Related Test Case** | TC-002 |
| **Assigned To** | — |

### Description
When registering with a username that contains only whitespace characters (e.g., `"   "`), the system accepts the registration because the length check passes (3+ characters). However, a whitespace-only username is effectively invalid and should be rejected.

### Steps to Reproduce
1. Start the server.
2. Send POST to `/api/register` with body:
   ```json
   {"username": "   ", "password": "validpass123"}
   ```
3. Observe the response.

### Expected Result
HTTP 400 with error message: `"username must not be blank"`

### Actual Result
HTTP 201 with message: `"user registered successfully"`

### Severity Classification Guide
| Severity | Definition |
|----------|-----------|
| Critical | System crash, data loss, security breach |
| High | Major feature broken, no workaround |
| Medium | Feature partially broken, workaround exists |
| Low | Minor issue, cosmetic, no functional impact |

### Priority Classification Guide
| Priority | Definition |
|----------|-----------|
| Critical | Fix immediately (blocks release) |
| High | Fix in current sprint |
| Medium | Fix before next release |
| Low | Fix when time permits |

---

*Note: This is both a template and a real example. The whitespace username bug actually exists in the current CryptoTracker implementation and can be used to demonstrate defect lifecycle.*
