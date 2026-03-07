# Zebrunner

## What is Zebrunner?

Zebrunner is a test automation reporting and infrastructure platform. It aggregates test results from multiple frameworks (Pytest, Selenium, JUnit, TestNG) into a single dashboard with analytics, AI-powered failure analysis, and Selenium Grid management.

## Core Components

| Component | Purpose |
|-----------|---------|
| **Zebrunner Reporting** | Centralized dashboard for all test results |
| **Zebrunner Selenium Grid** | Managed browser infrastructure (like Selenium Grid + BrowserStack) |
| **Zebrunner Agent** | SDK that sends test results from your framework to Zebrunner |
| **AI Failure Analysis** | Groups similar failures, suggests root causes |

## How It Fits Our Stack

```
Our Test Suites                    Zebrunner
─────────────────                  ──────────────────────
Pytest (42 tests)    ──agent──►    ┌──────────────────┐
unittest (22 tests)  ──agent──►    │  Zebrunner       │
Go tests (25 tests)  ──agent──►    │  Dashboard       │
Selenium (23 tests)  ──agent──►    │                  │
Locust (perf tests)  ──────────    │  - Pass/fail     │
                                   │  - Trends        │
Jenkins/GH Actions   ──webhook──►  │  - Screenshots   │
                                   │  - AI analysis   │
                                   └──────────────────┘
```

## Zebrunner Agent for Pytest

```python
# Install: pip install zebrunner-pytest

# pytest.ini or pyproject.toml
# [tool:pytest]
# zebrunner =
#   enabled = true
#   service_url = https://your-instance.zebrunner.com
#   access_token = YOUR_TOKEN
#   project_key = CRYPTO

# That's it — Zebrunner agent hooks into pytest automatically.
# Every test run sends results to the dashboard.
```

### What Gets Reported

For each test run, Zebrunner captures:

| Data | Source |
|------|--------|
| Test name & status | Pytest/unittest results |
| Duration | Start/end timestamps |
| Failure message | Exception + traceback |
| Screenshots | Selenium WebDriver (on failure) |
| Browser/OS info | WebDriver capabilities |
| Build info | CI/CD environment variables |
| Tags/labels | Pytest markers |

## Zebrunner Selenium Grid

Instead of running your own Selenium Grid (Docker containers), Zebrunner provides managed browser infrastructure:

```python
# Connect to Zebrunner's Grid instead of local Grid
from selenium import webdriver

options = webdriver.ChromeOptions()
options.set_capability("zebrunner:options", {
    "enableVideo": True,       # Record test execution video
    "enableLog": True,         # Capture browser logs
    "projectKey": "CRYPTO",
})

driver = webdriver.Remote(
    command_executor="https://grid.zebrunner.com/wd/hub",
    options=options,
)
```

Features:
- **Video recording** of every test execution
- **Browser logs** captured automatically
- **Multiple browsers/versions** available on demand
- **Parallel execution** without local infrastructure

## Dashboard Features

| Feature | Description |
|---------|-------------|
| **Test Run Summary** | Pass/fail/skip counts per run |
| **Trend Analysis** | Pass rate over time (detect regressions) |
| **Flaky Test Detection** | Tests that flip between pass/fail |
| **Failure Grouping** | AI groups tests that fail for the same reason |
| **Environment Matrix** | Results by browser, OS, device |
| **Integration** | JIRA (auto-create bugs), Slack (notifications) |

## Zebrunner vs Similar Tools

| Feature | Zebrunner | ReportPortal | Allure TestOps |
|---------|-----------|-------------|----------------|
| Reporting | Yes | Yes | Yes |
| Selenium Grid | Yes | No | No |
| AI analysis | Yes | ML-based | No |
| Video recording | Yes | No | No |
| Self-hosted | Yes | Yes | Yes |
| Cloud option | Yes | No | Yes |
| Free tier | Yes | Open source | Limited |

## Common Interview Questions

**Q: What is Zebrunner used for?**
A: Zebrunner is a test automation reporting platform that aggregates results from multiple test frameworks into one dashboard. It also provides managed Selenium Grid infrastructure with video recording and AI-powered failure analysis.

**Q: How does Zebrunner differ from Allure reports?**
A: Allure generates static HTML reports per test run. Zebrunner is a platform — it stores historical data, shows trends, detects flaky tests, groups failures by root cause, and manages browser infrastructure. Allure is a report format; Zebrunner is a reporting + infrastructure service.

**Q: How do you integrate Zebrunner with your test framework?**
A: Install the Zebrunner agent for your framework (e.g., `zebrunner-pytest`), configure the server URL and access token, and run tests normally. The agent automatically sends results to the Zebrunner dashboard — no changes to test code needed.
