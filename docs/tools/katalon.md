# Katalon Studio

## What is Katalon?

Katalon Studio is an all-in-one test automation platform that supports Web, API, Mobile, and Desktop testing. It provides both a visual (codeless) and scripted (Groovy) approach.

## Key Features

| Feature | Description |
|---------|-------------|
| **Web Testing** | Built on Selenium — uses the same locators and concepts |
| **API Testing** | Built-in REST/SOAP client (like Postman + automation) |
| **Mobile Testing** | Built on Appium for iOS/Android |
| **Record & Playback** | Record browser actions, generate test scripts |
| **Dual Mode** | Visual (drag-and-drop) + Script (Groovy code) |
| **Object Repository** | Central store for UI element locators |
| **Data-Driven** | Read test data from Excel, CSV, databases |
| **CI/CD** | CLI runner, Jenkins/GitHub Actions integration |

## Katalon vs Our Current Setup

| Capability | Our Approach | Katalon Equivalent |
|-----------|-------------|-------------------|
| API testing | Pytest + requests | Built-in API testing |
| UI testing | Selenium + Python | Built-in Web testing (Selenium under the hood) |
| Test management | Markdown test cases | Katalon TestOps |
| CI/CD | Jenkins/GitHub Actions | Katalon CLI + TestOps |
| Reporting | JUnit XML + manual | Built-in reports + TestOps dashboard |

## How Katalon Works

### Test Case Structure

```groovy
// Katalon uses Groovy scripts
// This is equivalent to our Pytest test_auth.py

import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.webservice.keyword.WSBuiltInKeywords as WS

// API Test: Register a new user
def response = WS.sendRequest(findTestObject('API/Register', [
    ('username'): 'testuser',
    ('password'): 'secure123'
]))

WS.verifyResponseStatusCode(response, 201)
WS.verifyElementPropertyValue(response, 'message', 'Registered successfully')
```

### Web Test (equivalent to our Selenium tests)

```groovy
import static com.kms.katalon.core.testobject.ObjectRepository.findTestObject
import com.kms.katalon.core.webui.keyword.WebUiBuiltInKeywords as WebUI

// Open browser and navigate
WebUI.openBrowser('http://localhost:8080')

// Login (like our logged_in_driver fixture)
WebUI.setText(findTestObject('Page/username_field'), 'testuser')
WebUI.setText(findTestObject('Page/password_field'), 'secure123')
WebUI.click(findTestObject('Page/login_button'))

// Verify dashboard is visible
WebUI.verifyElementVisible(findTestObject('Page/dashboard_section'))

// Close browser
WebUI.closeBrowser()
```

### Object Repository

Instead of hardcoding locators in tests, Katalon stores them centrally:

```
Object Repository/
├── API/
│   ├── Register        (POST /api/register)
│   ├── Login           (POST /api/login)
│   ├── GetPortfolio    (GET /api/portfolio)
│   └── GetPrices       (GET /api/prices)
└── Page/
    ├── username_field   (id="username")
    ├── password_field   (id="password")
    ├── login_button     (id="login-btn")
    └── dashboard_section (id="dashboard-section")
```

This is similar to the **Page Object Model** pattern — separating locators from test logic.

## Katalon TestOps

TestOps is Katalon's cloud platform for:
- **Test planning** — organize tests into releases and builds
- **Execution scheduling** — run tests on schedule or on trigger
- **Results dashboard** — pass rates, trends, flaky test detection
- **Integration** — JIRA, Slack, CI/CD pipelines

## When to Use Katalon

| Scenario | Recommended? |
|----------|:------------:|
| Team with mixed skill levels (some non-coders) | Yes |
| Need API + Web + Mobile in one tool | Yes |
| Already invested in Selenium + Pytest | Not necessary |
| Enterprise wanting vendor support | Yes |
| Open-source / full control needed | No (Katalon is proprietary) |

## Common Interview Questions

**Q: What is Katalon Studio?**
A: An all-in-one test automation platform supporting Web (Selenium-based), API (REST/SOAP), Mobile (Appium-based), and Desktop testing. It offers both codeless (record & playback) and coded (Groovy) approaches.

**Q: How does Katalon compare to Selenium?**
A: Katalon is built *on top of* Selenium for web testing. It adds an IDE, object repository, built-in reporting, and data-driven testing. Pure Selenium gives more flexibility and is free/open-source, while Katalon adds convenience at the cost of vendor lock-in.

**Q: What is the Object Repository in Katalon?**
A: A centralized store for test object definitions (locators). Instead of hardcoding `By.ID("username")` in every test, you define it once in the repository and reference it by name. This is similar to the Page Object Model pattern.
