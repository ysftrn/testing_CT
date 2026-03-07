# Requirements Traceability Matrix (RTM)
## CryptoTracker v1.0

| Field | Value |
|-------|-------|
| Document ID | RTM-CT-001 |
| Version | 1.0 |
| Date | 2026-03-06 |
| Author | Yusuf Torun |

---

## 1. Purpose

The Requirements Traceability Matrix (RTM) maps each requirement from the SRS to:
- The design component that implements it
- The test case(s) that verify it

This ensures:
- **Forward traceability:** Every requirement has at least one test.
- **Backward traceability:** Every test traces back to a requirement.
- **Coverage visibility:** Stakeholders can see what is tested and what is not.

---

## 2. Functional Requirements Traceability

| Req ID | Requirement | Design Component | Test Case(s) | Status |
|--------|------------|-----------------|-------------|--------|
| FR-001 | User registration with username/password | `service.Register()`, `handlers.Register()` | TC-001, TC-005 | Covered |
| FR-002 | Username minimum 3 characters | `service.Register()` | TC-002 | Covered |
| FR-003 | Password minimum 6 characters | `service.Register()` | TC-003 | Covered |
| FR-004 | No duplicate usernames | `repository.CreateUser()` (UNIQUE constraint) | TC-004 | Covered |
| FR-005 | Passwords stored as bcrypt hash | `service.Register()` | TC-025 | Covered |
| FR-006 | Authenticate with username/password | `service.Login()` | TC-006 | Covered |
| FR-007 | Return Bearer token on login | `service.Login()`, `service.generateToken()` | TC-006 | Covered |
| FR-008 | Reject invalid credentials | `service.Login()` | TC-007, TC-008 | Covered |
| FR-009 | Require valid token for protected endpoints | `handlers.authenticate()` | TC-009, TC-010 | Covered |
| FR-010 | Return 401 for missing/invalid tokens | `handlers.authenticate()` | TC-009, TC-010 | Covered |
| FR-011 | Add crypto to portfolio | `service.AddToPortfolio()` | TC-011 | Covered |
| FR-012 | Validate symbol not empty | `service.AddToPortfolio()` | TC-012 | Covered |
| FR-013 | Auto-convert symbol to uppercase | `service.AddToPortfolio()` | TC-013 | Covered |
| FR-014 | Validate amount is positive | `service.AddToPortfolio()` | TC-014, TC-015 | Covered |
| FR-015 | View portfolio | `service.GetPortfolio()` | TC-016 | Covered |
| FR-016 | Empty portfolio returns empty list | `handlers.GetPortfolio()` | TC-017 | Covered |
| FR-017 | Delete portfolio item by ID | `service.DeleteFromPortfolio()` | TC-018 | Covered |
| FR-018 | Error on deleting non-existent item | `repository.DeletePortfolioItem()` | TC-019 | Covered |
| FR-019 | Cannot delete another user's item | `repository.DeletePortfolioItem()` (WHERE user_id=?) | TC-020 | Covered |
| FR-020 | Provide crypto prices | `service.GetPrices()` | TC-021 | Covered |
| FR-021 | Include 24h change percentage | `service.GetPrices()` | TC-021 | Covered |
| FR-022 | Prices accessible without auth | `handlers.RegisterRoutes()` | TC-021 | Covered |
| FR-023 | Health check endpoint | `handlers.HealthCheck()` | TC-022 | Covered |
| FR-024 | Health check returns app name and status | `handlers.HealthCheck()` | TC-022 | Covered |
| FR-025 | Web UI for registration/login | `web/index.html`, `app.js` | — | UI tests (Phase 5) |
| FR-026 | Display prices table on dashboard | `web/index.html`, `app.js` | — | UI tests (Phase 5) |
| FR-027 | Display portfolio table on dashboard | `web/index.html`, `app.js` | — | UI tests (Phase 5) |
| FR-028 | UI controls for add/delete | `web/index.html`, `app.js` | — | UI tests (Phase 5) |
| FR-029 | Display success/error messages | `web/index.html`, `app.js` | — | UI tests (Phase 5) |
| FR-030 | Logout function | `app.js logout()` | — | UI tests (Phase 5) |

---

## 3. Non-Functional Requirements Traceability

| Req ID | Requirement | Test Case(s) | Test Type | Status |
|--------|------------|-------------|-----------|--------|
| NFR-001 | API response within 500ms | — | Performance (Phase 7) | Planned |
| NFR-002 | Handle 100 concurrent users | — | Performance (Phase 7) | Planned |
| NFR-003 | All responses in JSON | TC-023 | Functional | Covered |
| NFR-004 | Standard HTTP status codes | TC-024 | Functional | Covered |
| NFR-005 | Cross-platform (Linux, macOS, Windows) | — | Environment (Phase 8) | Planned |
| NFR-006 | SQLite for persistence | — | Architecture | By design |
| NFR-007 | Passwords never in responses | TC-025 | Security | Covered |

---

## 4. Coverage Summary

| Category | Total Reqs | Covered | Planned | Gap |
|----------|:---------:|:-------:|:-------:|:---:|
| Registration (FR-001 to FR-005) | 5 | 5 | 0 | 0 |
| Authentication (FR-006 to FR-010) | 5 | 5 | 0 | 0 |
| Portfolio (FR-011 to FR-019) | 9 | 9 | 0 | 0 |
| Prices (FR-020 to FR-022) | 3 | 3 | 0 | 0 |
| Health (FR-023 to FR-024) | 2 | 2 | 0 | 0 |
| Web UI (FR-025 to FR-030) | 6 | 0 | 6 | 0 |
| Non-Functional (NFR-001 to NFR-007) | 7 | 3 | 3 | 0 |
| **Total** | **37** | **27** | **9** | **0** |

All requirements are either covered by existing test cases or planned for later phases.
