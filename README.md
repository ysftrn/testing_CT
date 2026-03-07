# Software Testing Portfolio

A comprehensive software testing portfolio demonstrating testing methodologies, tools, documentation, and automation skills. Built around **CryptoTracker** — a Go-based cryptocurrency portfolio tracker used as the System Under Test (SUT).

---

## Project Structure

```
Testing_CT/
|
|-- sample-app/                         # CryptoTracker - System Under Test
|   |-- cmd/server/                     # Go API server entry point
|   |-- internal/
|   |   |-- handlers/                   # HTTP handlers (REST API)
|   |   |-- models/                     # Data models
|   |   |-- repository/                 # Database layer (SQLite)
|   |   +-- service/                    # Business logic & auth
|   +-- web/                            # Frontend (HTML/JS/CSS)
|
|-- docs/                               # Test documentation
|   |-- requirements/                   # Software Requirements Specification
|   |-- test-plan/                      # Test Plan (MIL-STD-498 / ISO 29119)
|   |-- test-cases/                     # Detailed test cases (25 cases)
|   |-- test-techniques/               # 10 testing technique guides
|   |-- test-reports/                   # Test execution reports
|   |-- defect-reports/                # Bug reports
|   |-- traceability-matrix/           # Requirements Traceability Matrix
|   +-- tools/                         # Tool documentation (JIRA, Testiny, etc.)
|
|-- tests/                              # Test automation
|   |-- api/
|   |   |-- postman/                   # Postman collections
|   |   |-- python/                    # Python/Pytest API tests
|   |   +-- soapui/                    # SoapUI project
|   |-- selenium/                      # Selenium WebDriver UI tests
|   |-- pytest/                        # Pytest test suites
|   |-- unittest/                      # Python unittest examples
|   |-- go/                            # Go native tests
|   +-- performance/                   # Performance testing
|       |-- locust/                    # Locust load tests (Python)
|       +-- jmeter/                   # JMeter test plans
|
|-- ci-cd/                             # CI/CD pipeline configuration
|   |-- docker-compose.yml            # Jenkins + SonarQube stack
|   +-- sonarqube/                     # SonarQube config
|
|-- .github/workflows/ci.yml          # GitHub Actions CI pipeline
|-- Jenkinsfile                        # Jenkins declarative pipeline
|
+-- sdlc-docs/                         # SDLC/STLC process documentation
```

## System Under Test: CryptoTracker

A REST API + web application for managing a cryptocurrency portfolio.

**Tech stack:** Go, SQLite, HTML/JS

**API Endpoints:**

| Method | Endpoint | Auth | Description |
|--------|----------|:----:|-------------|
| `GET` | `/api/health` | No | Health check |
| `POST` | `/api/register` | No | User registration |
| `POST` | `/api/login` | No | Authentication (returns Bearer token) |
| `GET` | `/api/portfolio` | Yes | List portfolio items |
| `POST` | `/api/portfolio` | Yes | Add cryptocurrency holding |
| `DELETE` | `/api/portfolio/{id}` | Yes | Remove portfolio item |
| `GET` | `/api/prices` | No | Market prices |

See [sample-app/README.md](sample-app/README.md) for full details.

## Test Documentation

All documentation follows **MIL-STD-498** and **ISO/IEC/IEEE 29119** standards.

| Document | Description |
|----------|-------------|
| [Software Requirements Specification](docs/requirements/SRS.md) | 30 functional + 7 non-functional requirements |
| [Test Plan (STP)](docs/test-plan/test-plan.md) | Strategy, scope, schedule, entry/exit criteria |
| [Test Cases](docs/test-cases/) | 25 detailed test cases (positive, negative, security) |
| [Traceability Matrix (RTM)](docs/traceability-matrix/RTM.md) | Bidirectional mapping: Requirements <-> Design <-> Tests |
| [Test Report Template](docs/test-reports/test-report-template.md) | Execution results and exit criteria evaluation |
| [Defect Report](docs/defect-reports/defect-report-template.md) | Sample bug report with severity/priority classification |

## Test Techniques

Guides for each technique with definitions, CryptoTracker examples, and interview Q&A.

| Technique | Key Concepts |
|-----------|-------------|
| [Functional Testing](docs/test-techniques/functional-testing.md) | Equivalence Partitioning, Boundary Value Analysis, Decision Tables |
| [Regression Testing](docs/test-techniques/regression-testing.md) | Impact Analysis, test selection strategies |
| [Smoke Testing](docs/test-techniques/smoke-testing.md) | Build Verification Test, critical path validation |
| [Exploratory Testing](docs/test-techniques/exploratory-testing.md) | Session-Based Test Management, charter & session reports |
| [E2E Testing](docs/test-techniques/e2e-testing.md) | User journeys, testing pyramid |
| [System Testing](docs/test-techniques/system-testing.md) | V-Model, full SRS verification |
| [Integration Testing](docs/test-techniques/integration-testing.md) | Top-down, bottom-up, stubs vs mocks |
| [UI Testing](docs/test-techniques/ui-testing.md) | Manual vs automated, selectors, cross-browser |
| [API Testing](docs/test-techniques/api-testing.md) | REST conventions, tools comparison, contract testing |
| [Performance Testing](docs/test-techniques/performance-testing.md) | Load, stress, spike, soak testing, metrics, tools |

## Tools & Technologies

| Category | Tools |
|----------|-------|
| **Programming** | Go, Python, C++ |
| **API Testing** | Postman, Python requests, SoapUI, curl |
| **UI Automation** | Selenium WebDriver (Chrome headless), Selenium Grid, BrowserStack |
| **Test Frameworks** | Pytest, Python unittest, Go testing |
| **Performance** | Locust, JMeter |
| **CI/CD** | Jenkins, GitHub Actions, SonarQube, Docker |
| **Test Management** | Testiny, Katalon Studio, Zebrunner |
| **Project Tracking** | JIRA, Confluence |
| **Version Control** | Git, GitHub |
| **Process** | SDLC (Agile/Scrum), STLC, MIL-STD-498, ISO 29119 |

## Live Server

CryptoTracker is deployed on a Digital Ocean droplet and publicly accessible for testing:

```bash
# Quick test — hit the live health endpoint
curl http://178.128.250.129:8080/api/health
```

Jenkins and SonarQube are also running on the same server for CI/CD (not publicly listed for security).

## Running the Application

```bash
# Clone the repository
git clone https://github.com/yusuftorun/Testing_CT.git
cd Testing_CT

# Run the server
make run

# Or build and run the binary
make build
./bin/cryptotracker

# Server starts on http://localhost:8080
```

**Requirements:** Go 1.21+

## Running Tests

Tests default to `http://localhost:8080`. To run against the live server, set the `CRYPTOTRACKER_URL` environment variable:

```bash
export CRYPTOTRACKER_URL=http://<server-ip>:8080
```

```bash
# Start the server (required for API, UI, and unittest tests — skip if using the live server)
rm -f cryptotracker.db   # clean database
./server &

# Go unit tests (25 tests, no server needed)
go test -v ./sample-app/internal/service/

# Python API tests — Pytest (42 tests)
source tests/api/python/.venv/bin/activate
pytest tests/api/python/ -v

# Python unittest (22 tests)
python -m unittest tests/unittest/test_service.py -v

# Selenium UI tests (23 tests, Chrome headless)
pytest tests/selenium/ -v
pytest tests/selenium/ -v --browser=firefox   # override browser

# Postman collection (requires: npm install -g newman)
newman run tests/api/postman/CryptoTracker.postman_collection.json

# Performance tests against live server
locust -f tests/performance/locust/locustfile.py --host=http://<server-ip>:8080
```

**Total automated tests:** 112 (Go 25 + Pytest 42 + unittest 22 + Selenium 23)

## Performance Testing

Load and stress testing with real results.

| Tool | Config File | Description |
|------|------------|-------------|
| Locust | `tests/performance/locust/locustfile.py` | Python-based load tests (20 users, 291 req, 0 failures) |
| JMeter | `tests/performance/jmeter/CryptoTracker.jmx` | Importable test plan for GUI or CLI execution |

See [tests/performance/README.md](tests/performance/README.md) for details and results.

## CI/CD Pipeline

| Tool | Config File | Description |
|------|------------|-------------|
| Jenkins | `Jenkinsfile` | 6-stage pipeline (Build → Test → SonarQube → Archive) |
| GitHub Actions | `.github/workflows/ci.yml` | Auto-runs on push/PR to main |
| Docker Compose | `ci-cd/docker-compose.yml` | Jenkins + SonarQube stack |
| SonarQube | `ci-cd/sonarqube/sonar-project.properties` | Static code analysis config |

See [ci-cd/README.md](ci-cd/README.md) for setup guide.

## Tool Documentation

Guides for industry-standard testing and project management tools.

| Tool | Documentation |
|------|:------------:|
| JIRA & Confluence | [docs/tools/jira-confluence.md](docs/tools/jira-confluence.md) |
| Testiny | [docs/tools/testiny.md](docs/tools/testiny.md) |
| Katalon Studio | [docs/tools/katalon.md](docs/tools/katalon.md) |
| Zebrunner | [docs/tools/zebrunner.md](docs/tools/zebrunner.md) |
| Git & GitHub | [docs/tools/git.md](docs/tools/git.md) |

## SDLC/STLC Process

[sdlc-docs/sdlc-stlc.md](sdlc-docs/sdlc-stlc.md) — Covers SDLC models (Waterfall, V-Model, Agile, Kanban), STLC phases, testing in Scrum, sprint planning examples, entry/exit criteria, and the testing pyramid.

## Author

**Yusuf Torun**
- Background: Physics (BSc)
- Interests: Algorithmic crypto trading, music production, quantum computing
