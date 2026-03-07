# Selenium UI Tests

Automated browser tests for CryptoTracker's web interface using Selenium WebDriver.

## Browser Choice

Tests run in **Chrome headless** by default. Chrome was chosen over Safari because:
- Safari only allows one WebDriver session at a time, causing frequent pairing errors
- Safari has no headless mode (always opens a visible window)
- Chrome headless is the industry standard for CI/CD pipelines
- ChromeDriver is auto-managed by `selenium-manager` (no manual driver installs)

The test suite auto-detects available browsers (Chrome, Firefox, Safari) and can be overridden with `--browser`.

## Setup

```bash
# Activate the virtual environment
source tests/api/python/.venv/bin/activate

# Install dependencies (if not already installed)
pip install selenium requests pytest

# Install Chrome (macOS)
brew install --cask google-chrome
```

## Running Tests

```bash
# Start the server with a clean database
rm -f cryptotracker.db
./server &

# Run all Selenium tests (auto-detects Chrome)
pytest tests/selenium/ -v

# Run with a specific browser
pytest tests/selenium/ -v --browser=chrome
pytest tests/selenium/ -v --browser=firefox
pytest tests/selenium/ -v --browser=safari

# Run a specific test file
pytest tests/selenium/test_login_page.py -v
```

> **Note:** Selenium tests need a clean database. If tests fail with stale data, stop the server, delete `cryptotracker.db`, and restart.

## Test Structure

| File | Tests | What It Covers |
|------|:-----:|----------------|
| `conftest.py` | — | Browser setup, login fixture |
| `test_login_page.py` | 10 | Page elements, registration UI, login UI, error messages |
| `test_dashboard.py` | 10 | Prices table, add/delete portfolio items |
| `test_logout.py` | 3 | Logout button, state transition |

## Key Selenium Concepts Used

### Element Locators
```python
driver.find_element(By.ID, "username")              # by HTML id
driver.find_element(By.CSS_SELECTOR, "#prices-body") # by CSS selector
driver.find_element(By.TAG_NAME, "h1")               # by tag name
driver.find_elements(By.CSS_SELECTOR, ".delete-btn") # multiple elements
```

### Waits
```python
# Implicit wait: set once, applies to all find_element calls
driver.implicitly_wait(5)

# Explicit wait: wait for a specific condition
WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.ID, "dashboard-section"))
)
```

### Interactions
```python
element.send_keys("text")    # type into a field
element.click()              # click a button/link
element.text                 # get visible text
element.get_attribute("value")  # get input field value
element.is_displayed()       # check visibility
```

## Browser Auto-Detection

The `conftest.py` auto-detects which browser is installed, trying Chrome first, then Firefox, then Safari. Override with the `--browser` flag:

```bash
pytest tests/selenium/ --browser=firefox
```

Chrome runs in headless mode (`--headless=new`). Firefox also runs headless. Safari always runs with a visible window (no headless support).

## Selenium Grid

Selenium Grid lets you run tests on **multiple browsers/machines in parallel**.

### Architecture
```
                    ┌──── Node 1 (Chrome, Linux)
Test Script ──▶ Hub ├──── Node 2 (Firefox, Linux)
                    ├──── Node 3 (Safari, macOS)
                    └──── Node 4 (Chrome, Windows)
```

### Setup with Docker
```bash
# Start Grid Hub
docker run -d -p 4442-4444:4442-4444 --name selenium-hub selenium/hub

# Start Chrome node
docker run -d --link selenium-hub:hub selenium/node-chrome

# Start Firefox node
docker run -d --link selenium-hub:hub selenium/node-firefox
```

### Connect Tests to Grid
```python
driver = webdriver.Remote(
    command_executor="http://localhost:4444/wd/hub",
    options=webdriver.ChromeOptions()
)
```

## BrowserStack Integration

BrowserStack provides cloud-based cross-browser testing — no local browser/driver setup needed.

### How It Works
```
Your Tests ──▶ BrowserStack Cloud ──▶ Real browsers on real devices
                                      (Chrome, Firefox, Safari, Edge,
                                       iOS Safari, Android Chrome)
```

### Configuration
```python
from selenium import webdriver

options = webdriver.ChromeOptions()
options.set_capability("browserName", "Chrome")
options.set_capability("browserVersion", "latest")
options.set_capability("bstack:options", {
    "os": "Windows",
    "osVersion": "11",
    "buildName": "CryptoTracker UI Tests",
    "sessionName": "Login Page Tests",
})

driver = webdriver.Remote(
    command_executor="https://USERNAME:ACCESS_KEY@hub-cloud.browserstack.com/wd/hub",
    options=options,
)
```

### When to Use BrowserStack
- Cross-browser compatibility testing (Chrome, Firefox, Safari, Edge)
- Testing on operating systems you don't have (Windows from macOS)
- Mobile browser testing (iOS Safari, Android Chrome)
- CI/CD pipeline integration (no browser installation on CI server)

### Free Tier
BrowserStack offers limited free access for open-source projects. For this portfolio, documentation and configuration examples demonstrate the knowledge.
