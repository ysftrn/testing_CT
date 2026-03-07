# UI Testing (Web / Mobile)

## What Is It?
UI testing verifies that the **user interface** looks correct, behaves correctly, and provides a good user experience. It tests what the user actually sees and interacts with — forms, buttons, tables, messages, navigation.

It answers: **"Does the interface work correctly from the user's perspective?"**

## When Is It Used?
- After API/backend testing confirms the backend works
- When UI changes are made (new pages, redesigns)
- Before release (final visual/functional check)
- Cross-browser/cross-device validation

## What to Test in a Web UI

| Category | What to Check | Example |
|----------|--------------|---------|
| **Layout** | Elements are visible and positioned correctly | Login form is centered, buttons are clickable |
| **Input** | Fields accept/reject correct data | Username field enforces minlength |
| **Navigation** | Page transitions work | Login → Dashboard, Logout → Login |
| **Display** | Data renders correctly | Prices show with $ sign, portfolio lists items |
| **Messages** | Feedback shown to user | "Registered!" in green, errors in red |
| **State** | UI reflects application state | Dashboard hidden until logged in |
| **Responsive** | Works on different screen sizes | (Not in scope for v1.0) |

## CryptoTracker UI Test Cases

### UI-001: Login Form Validation

| Step | Action | Expected |
|:----:|--------|----------|
| 1 | Open http://localhost:8080 | Login form visible with Username, Password fields |
| 2 | Click "Login" with empty fields | Browser shows HTML5 validation ("Please fill out this field") |
| 3 | Enter 2-char username, valid password, click "Login" | Browser shows minlength validation |
| 4 | Enter valid credentials, click "Login" | Dashboard appears, login form disappears |

### UI-002: Dashboard Display After Login

| Step | Action | Expected |
|:----:|--------|----------|
| 1 | Login with valid credentials | Dashboard section becomes visible |
| 2 | Check market prices table | 5 rows: BTC, ETH, SOL, ADA, DOT |
| 3 | Check price formatting | Prices show as "$67,432.5" with commas |
| 4 | Check 24h change colors | Positive changes in green, negative in red |
| 5 | Check portfolio table | Shows "No items yet" or existing items |

### UI-003: Add Portfolio Item via UI

| Step | Action | Expected |
|:----:|--------|----------|
| 1 | Enter "BTC" in symbol field | Field accepts input |
| 2 | Enter "0.5" in amount field | Field accepts decimal |
| 3 | Click "Add" | "Added BTC!" message appears in green |
| 4 | Check portfolio table | New row with BTC, 0.5, Delete button |

### UI-004: Delete Portfolio Item via UI

| Step | Action | Expected |
|:----:|--------|----------|
| 1 | Verify an item exists in portfolio table | At least one row visible |
| 2 | Click "Delete" button on the item | Item removed from table |
| 3 | Refresh page and re-login | Item still gone (persisted) |

### UI-005: Error Message Display

| Step | Action | Expected |
|:----:|--------|----------|
| 1 | Try to login with wrong password | Error message appears in red |
| 2 | Try to register with existing username | Error message appears in red |
| 3 | Try to add item with empty symbol | Browser validation prevents submission |

### UI-006: Logout

| Step | Action | Expected |
|:----:|--------|----------|
| 1 | While logged in, click "Logout" | Dashboard disappears, login form reappears |
| 2 | Username and password fields are empty | Fields cleared |
| 3 | Try accessing portfolio (manually via URL/console) | Should fail without token |

## Manual vs Automated UI Testing

| Aspect | Manual | Automated (Selenium) |
|--------|--------|---------------------|
| **Speed** | Slow | Fast after setup |
| **Visual bugs** | Humans are better | Can't detect visual issues |
| **Repeatability** | Inconsistent | Perfectly consistent |
| **Cost** | Low setup, high running | High setup, low running |
| **Best for** | Exploratory, usability | Regression, repetitive checks |

## Tools

| Tool | Type | Used For |
|------|------|----------|
| **Selenium WebDriver** | Browser automation | Automated UI test execution |
| **Selenium Grid** | Distributed testing | Run tests on multiple browsers/machines |
| **BrowserStack** | Cloud testing | Cross-browser testing without local setup |
| **Chrome DevTools** | Manual inspection | Debug layout, network, console errors |

We'll implement automated Selenium UI tests in **Phase 5**.

## Common Interview Questions
- **Q: How do you handle dynamic elements in UI testing?**
  A: Use stable selectors (ID, data-testid attributes) instead of fragile ones (CSS classes, XPath by position). Wait for elements to be present/visible before interacting.
- **Q: What's the biggest challenge in UI test automation?**
  A: Flakiness — tests that sometimes pass and sometimes fail due to timing, animation, or dynamic content. Solved with proper waits and stable selectors.
- **Q: Should you automate all UI tests?**
  A: No. Automate repetitive regression tests. Keep exploratory and usability testing manual.
