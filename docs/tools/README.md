# Testing Tools

Documentation for testing and project management tools used in the software testing industry.

## Tool Categories

### Project Management & Tracking
| Tool | Type | Documentation |
|------|------|:------------:|
| **JIRA** | Issue tracking, sprint management | [jira-confluence.md](jira-confluence.md) |
| **Confluence** | Documentation wiki | [jira-confluence.md](jira-confluence.md) |

### Test Management
| Tool | Type | Documentation |
|------|------|:------------:|
| **Testiny** | Test case management, test runs | [testiny.md](testiny.md) |

### Test Automation Platforms
| Tool | Type | Documentation |
|------|------|:------------:|
| **Katalon Studio** | All-in-one (Web, API, Mobile) | [katalon.md](katalon.md) |
| **Zebrunner** | Reporting, Selenium Grid, AI analysis | [zebrunner.md](zebrunner.md) |

### Version Control
| Tool | Type | Documentation |
|------|------|:------------:|
| **Git / GitHub** | Source control, collaboration | [git.md](git.md) |

## Tools Used Hands-On in This Project

| Tool | Where Used |
|------|-----------|
| Pytest | `tests/api/python/` — 42 API tests |
| Python unittest | `tests/unittest/` — 22 unit tests |
| Go testing | `sample-app/internal/service/service_test.go` — 25 tests |
| Selenium WebDriver | `tests/selenium/` — 23 UI tests (Chrome headless) |
| Postman / Newman | `tests/api/postman/` — 14 requests, 31 assertions |
| Locust | `tests/performance/locust/` — load testing |
| JMeter | `tests/performance/jmeter/` — test plan |
| Jenkins | `Jenkinsfile` — CI/CD pipeline |
| GitHub Actions | `.github/workflows/ci.yml` — CI pipeline |
| SonarQube | `ci-cd/sonarqube/` — static analysis config |
| Git | Entire project — version control |

## Tools Documented (Awareness Level)

These tools are documented to demonstrate knowledge, even without hands-on usage in this specific project:

- **JIRA** — mapped our defect reports and test cases to JIRA structure
- **Confluence** — mapped our documentation to Confluence page hierarchy
- **Testiny** — mapped our test cases and test runs to Testiny's model
- **Katalon** — showed equivalent test code for our Selenium/API tests
- **Zebrunner** — showed integration with our Pytest and Selenium setup
- **SoapUI** — documented in `tests/api/soapui/`
- **BrowserStack** — documented in `tests/selenium/README.md`
