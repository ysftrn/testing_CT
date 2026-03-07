# Software Test Plan (STP)
## CryptoTracker v1.0

| Field | Value |
|-------|-------|
| Document ID | STP-CT-001 |
| Version | 1.0 |
| Date | 2026-03-06 |
| Author | Yusuf Torun |
| Status | Draft |
| Referenced SRS | SRS-CT-001 v1.0 |

---

## 1. Introduction

### 1.1 Purpose
This Software Test Plan defines the test strategy, scope, approach, resources, and schedule for testing the CryptoTracker application. It follows the structure defined in MIL-STD-498 (STP) and ISO/IEC/IEEE 29119-3.

### 1.2 Scope
This plan covers all functional and non-functional testing activities for CryptoTracker v1.0, including:
- API endpoint testing
- Web UI testing
- Security testing (authentication)
- Performance testing
- Integration testing

### 1.3 References
| Document | ID | Version |
|----------|----|---------|
| Software Requirements Specification | SRS-CT-001 | 1.0 |
| ISO/IEC/IEEE 29119-3:2021 | — | — |
| MIL-STD-498 | — | — |

### 1.4 Definitions and Acronyms
| Term | Definition |
|------|-----------|
| STP | Software Test Plan (MIL-STD-498) |
| STD | Software Test Description (MIL-STD-498) |
| STR | Software Test Report (MIL-STD-498) |
| SUT | System Under Test |
| RTM | Requirements Traceability Matrix |
| UAT | User Acceptance Testing |
| E2E | End-to-End |

---

## 2. Test Strategy

### 2.1 Test Levels

| Level | Scope | Tools | Responsibility |
|-------|-------|-------|----------------|
| Unit Testing | Individual functions and methods | Go `testing` package | Developer/Tester |
| Integration Testing | Component interactions, DB operations | Go tests, Pytest | Tester |
| API Testing | REST endpoint behavior | Postman, Python requests | Tester |
| UI Testing | Web interface functionality | Selenium WebDriver | Tester |
| System Testing | End-to-end application behavior | Selenium, Postman | Tester |
| Performance Testing | Load and response time | JMeter | Tester |

### 2.2 Test Types

| Type | Description | When Applied |
|------|-------------|-------------|
| Smoke Testing | Verify critical functionality works after deployment | After each build |
| Functional Testing | Verify features meet requirements (SRS) | Each sprint/iteration |
| Regression Testing | Verify existing features after code changes | After bug fixes, new features |
| Exploratory Testing | Unscripted testing to find unexpected defects | Mid-sprint, before release |
| Negative Testing | Test with invalid inputs and error conditions | During functional testing |

### 2.3 Test Design Techniques
- **Equivalence Partitioning** — Divide inputs into valid/invalid classes
- **Boundary Value Analysis** — Test at the edges of input ranges
- **Decision Table Testing** — Test combinations of conditions
- **Error Guessing** — Based on experience and intuition

---

## 3. Test Environment

### 3.1 Hardware
| Component | Specification |
|-----------|--------------|
| Development Machine | macOS, Apple Silicon |
| Test Server | DigitalOcean Droplet (Ubuntu 22.04/24.04 LTS, 2-4 GB RAM) |

### 3.2 Software
| Component | Version | Purpose |
|-----------|---------|---------|
| Go | 1.26+ | Application runtime |
| Python | 3.14+ | Test automation scripts |
| Selenium WebDriver | Latest | UI test automation |
| Postman | Latest | API testing |
| JMeter | Latest | Performance testing |
| Jenkins | Latest | CI/CD pipeline |
| SonarQube | Latest | Code quality analysis |
| Git | Latest | Version control |
| SQLite | 3.x | Application database |

### 3.3 Test Data
- Test users will be created at the start of each test run.
- Portfolio items will use standard crypto symbols (BTC, ETH, SOL).
- Database will be reset between test suites to ensure clean state.

---

## 4. Features to be Tested

| Feature Area | Requirements | Priority |
|-------------|-------------|----------|
| User Registration | FR-001 through FR-005 | High |
| User Authentication | FR-006 through FR-010 | High |
| Portfolio Management | FR-011 through FR-019 | High |
| Market Prices | FR-020 through FR-022 | Medium |
| Health Check | FR-023, FR-024 | High |
| Web Interface | FR-025 through FR-030 | Medium |
| Performance | NFR-001, NFR-002 | Medium |
| Security | NFR-007 | High |
| API Standards | NFR-003, NFR-004 | High |

---

## 5. Features Not to be Tested

| Feature | Reason |
|---------|--------|
| Third-party SQLite engine | Vendor responsibility |
| Browser rendering / CSS | Not in scope for v1.0 |
| Mobile responsiveness | Not in scope for v1.0 |

---

## 6. Entry and Exit Criteria

### 6.1 Entry Criteria
- SRS document is approved (SRS-CT-001).
- Application builds successfully.
- Test environment is configured and accessible.
- Test data is prepared.
- Health check endpoint returns `{"status":"healthy"}`.

### 6.2 Exit Criteria
- All High priority test cases are executed.
- At least 95% of test cases pass.
- No open Critical or High severity defects.
- All test reports are generated and reviewed.
- RTM shows full coverage of High priority requirements.

### 6.3 Suspension Criteria
- Application cannot be deployed to test environment.
- More than 30% of test cases fail in a single test cycle.
- Critical defect blocks further testing.

### 6.4 Resumption Criteria
- Blocking defect is resolved and verified.
- Application is redeployed successfully.
- Smoke test passes.

---

## 7. Test Schedule

| Phase | Activity | Duration |
|-------|----------|----------|
| 1 | Test Planning & Design | Week 1 |
| 2 | Test Case Development | Week 1-2 |
| 3 | Test Environment Setup | Week 2 |
| 4 | Smoke Testing | Week 2 |
| 5 | Functional Testing (API) | Week 2-3 |
| 6 | Functional Testing (UI) | Week 3 |
| 7 | Integration Testing | Week 3 |
| 8 | Performance Testing | Week 4 |
| 9 | Regression Testing | Week 4 |
| 10 | Test Reporting & Closure | Week 4 |

---

## 8. Roles and Responsibilities

| Role | Person | Responsibilities |
|------|--------|-----------------|
| Test Lead | Yusuf Torun | Test planning, strategy, reporting |
| Test Engineer | Yusuf Torun | Test case design, execution, automation |
| Developer | Yusuf Torun | Bug fixes, unit tests |

---

## 9. Risks and Mitigations

| Risk | Probability | Impact | Mitigation |
|------|:-----------:|:------:|-----------|
| Test environment unavailable | Low | High | Maintain local test environment as backup |
| Requirements change mid-cycle | Medium | Medium | Use agile approach, update test cases incrementally |
| Insufficient test data | Low | Medium | Automate test data generation in setup scripts |
| Single tester bottleneck | High | Medium | Prioritize critical paths, automate where possible |

---

## 10. Test Deliverables

| Deliverable | Document ID | Description |
|-------------|------------|-------------|
| Software Test Plan | STP-CT-001 | This document |
| Test Cases | TC-CT-xxx | Individual test case specifications |
| Test Scenarios | TS-CT-xxx | High-level test scenarios |
| Test Scripts | Automated | Selenium, Postman, Pytest scripts |
| Test Report | STR-CT-001 | Test execution results |
| Defect Reports | DR-CT-xxx | Individual bug reports |
| Traceability Matrix | RTM-CT-001 | Requirements-to-tests mapping |

---

## 11. Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Test Lead | Yusuf Torun | | |
| Project Manager | | | |
| Stakeholder | | | |
