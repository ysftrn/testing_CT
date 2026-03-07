# SDLC & STLC

## Software Development Life Cycle (SDLC)

The SDLC defines the phases a software product goes through from concept to retirement.

### SDLC Models

#### Waterfall
Sequential phases. Each phase completes before the next begins.

```
Requirements → Design → Implementation → Testing → Deployment → Maintenance
```

- Testing happens late — bugs found late are expensive to fix
- Works for: well-defined requirements, regulatory/compliance projects
- Risks: changes are costly, no working software until late

#### V-Model
Extension of Waterfall. Each development phase has a corresponding test phase.

```
Requirements  ──────────────────────────  Acceptance Testing
    Design  ──────────────────────────  System Testing
        Architecture  ──────────────  Integration Testing
            Coding  ────────────  Unit Testing
```

- Test planning starts early (left side), execution happens on the right
- Works for: safety-critical systems, medical devices
- Our RTM follows V-Model thinking: requirements ↔ test cases

#### Agile (Scrum)
Iterative development in short sprints (1-4 weeks). Testing is continuous.

```
Sprint 1          Sprint 2          Sprint 3
┌─────────┐      ┌─────────┐      ┌─────────┐
│ Plan     │      │ Plan     │      │ Plan     │
│ Develop  │      │ Develop  │      │ Develop  │
│ Test     │ ──►  │ Test     │ ──►  │ Test     │
│ Review   │      │ Review   │      │ Review   │
│ Retro    │      │ Retro    │      │ Retro    │
└─────────┘      └─────────┘      └─────────┘
    Shippable         Shippable         Shippable
    Increment         Increment         Increment
```

- Testing integrated throughout — not a separate phase
- Works for: most modern software projects
- This is the model CryptoTracker follows

#### Kanban
Continuous flow. No fixed sprints. Work items move through columns.

```
Backlog → In Progress → Testing → Done
```

- WIP (Work In Progress) limits prevent overload
- Works for: support teams, maintenance, ops

---

## Software Testing Life Cycle (STLC)

The STLC defines the testing phases within the SDLC.

### STLC Phases

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│  1. Requirement    2. Test         3. Test              │
│     Analysis          Planning        Case Design       │
│     ↓                 ↓               ↓                 │
│  4. Environment   5. Test         6. Test Cycle         │
│     Setup             Execution       Closure           │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### CryptoTracker STLC Mapping

| STLC Phase | What We Did | Artifacts |
|-----------|------------|-----------|
| **1. Requirement Analysis** | Reviewed SRS, identified testable requirements | `docs/requirements/SRS.md` |
| **2. Test Planning** | Defined strategy, scope, entry/exit criteria | `docs/test-plan/test-plan.md` |
| **3. Test Case Design** | Wrote 25 test cases using EP, BVA, Decision Tables | `docs/test-cases/*.md` |
| **4. Environment Setup** | Set up Go server, Python venv, Selenium, Locust | `Makefile`, `conftest.py` files |
| **5. Test Execution** | Ran all test suites (112 automated tests) | `docs/test-reports/test-report-template.md` |
| **6. Test Cycle Closure** | Documented results, known defects, recommendations | Test report, `docs/defect-reports/` |

---

## Testing in Agile/Scrum

### Scrum Roles & Testing

| Role | Testing Responsibility |
|------|----------------------|
| **Product Owner** | Defines acceptance criteria (what to test) |
| **Scrum Master** | Removes blockers, ensures testing time in sprint |
| **Developer** | Writes unit tests, fixes bugs |
| **Tester/QA** | Test planning, test case design, execution, automation |

### Sprint Ceremonies & Testing

| Ceremony | Tester's Role |
|----------|--------------|
| **Sprint Planning** | Estimate test effort, identify test cases for stories |
| **Daily Standup** | Report test progress, blockers, bugs found |
| **Sprint Review** | Demo test results, coverage metrics |
| **Retrospective** | Suggest process improvements (flaky tests, slow CI) |
| **Backlog Refinement** | Review upcoming stories for testability |

### Definition of Done (DoD)

A user story is "Done" when:

- [ ] Code reviewed and merged
- [ ] Unit tests written and passing
- [ ] API tests updated/added
- [ ] UI tests updated (if UI changed)
- [ ] No open Critical/High bugs
- [ ] Test coverage > 80%
- [ ] SonarQube quality gate passed
- [ ] Documentation updated

### Example Sprint: CryptoTracker

```
Sprint 1: Authentication
├── Story: User Registration (FR-001, FR-002)
│   ├── Dev: Build POST /api/register
│   ├── Test: TC-001 to TC-005 (unit + API tests)
│   └── Done: 5/5 tests pass, no bugs
│
├── Story: User Login (FR-006, FR-007)
│   ├── Dev: Build POST /api/login
│   ├── Test: TC-006 to TC-010
│   └── Done: 5/5 tests pass, no bugs
│
└── Bug: DR-001 (whitespace username)
    ├── Found during exploratory testing
    ├── Severity: Medium, Priority: Medium
    └── Status: Deferred to Sprint 3

Sprint 2: Portfolio Management
├── Story: Add Crypto (FR-010 to FR-014)
├── Story: View Portfolio (FR-015, FR-016)
├── Story: Delete Item (FR-017 to FR-019)
└── Regression: Re-run Sprint 1 tests

Sprint 3: UI, Performance, CI/CD
├── Story: Selenium UI tests
├── Story: Locust performance tests
├── Story: Jenkins pipeline
└── Bug Fix: DR-001
```

---

## Entry & Exit Criteria

### Entry Criteria (start testing when...)

| Criteria | CryptoTracker Status |
|----------|:-------------------:|
| Requirements reviewed and approved | SRS signed off |
| Test plan approved | Test plan v1.0 |
| Test environment ready | Server compiles and runs |
| Test data available | SQLite in-memory DB |
| Build deployed to test environment | `./server` running |

### Exit Criteria (stop testing when...)

| Criteria | Target | Actual |
|----------|--------|--------|
| All test cases executed | 100% | 100% (25/25) |
| Pass rate | >= 95% | 100% |
| No open Critical bugs | 0 | 0 |
| No open High bugs | 0 | 0 |
| Test report delivered | Yes | Yes |
| Known defects documented | Yes | DR-001 |

---

## Test Levels in SDLC

```
                    ┌───────────────────┐
                    │  Acceptance Tests  │  ← User validates requirements
                    ├───────────────────┤
                 ┌──┤   System Tests    │  ← Full system (our Selenium tests)
                 │  ├───────────────────┤
              ┌──┤  │ Integration Tests │  ← Components together (our API tests)
              │  │  ├───────────────────┤
           ┌──┤  │  │   Unit Tests      │  ← Individual functions (our Go tests)
           │  │  │  └───────────────────┘
           │  │  │
         More  │  │   More expensive
         tests │  │   to fix bugs
         here  │  │   up here
```

- **Unit tests** (Go `testing`): fast, cheap, many — test individual functions
- **Integration tests** (Pytest API): test components working together
- **System tests** (Selenium): test the complete system end-to-end
- **Acceptance tests**: stakeholder validation against requirements

## Common Interview Questions

**Q: What's the difference between SDLC and STLC?**
A: SDLC covers the entire software lifecycle (requirements to retirement). STLC is the testing portion within SDLC — from requirement analysis through test closure. STLC is a subset of SDLC.

**Q: When does testing start in Agile?**
A: From day one. Testers participate in sprint planning, review stories for testability, write test cases during development, and execute tests continuously. Testing is not a separate phase — it's integrated throughout.

**Q: What is a Definition of Done?**
A: A checklist that defines when a user story is complete. It typically includes: code reviewed, unit tests passing, integration tests passing, no critical bugs, documentation updated, and quality gate passed.

**Q: How do you handle regression testing in Agile sprints?**
A: Automate regression tests (like our Pytest + Selenium suites) and run them in CI/CD on every commit. This gives immediate feedback without manual effort. Only add new manual exploratory tests for new features.

**Q: What's the testing pyramid?**
A: A model that recommends many unit tests (fast, cheap), fewer integration tests, and even fewer UI/E2E tests (slow, expensive). Our project follows this: 25 Go unit tests > 42+22 API tests > 23 Selenium tests.
