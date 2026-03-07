"""
Selenium UI Test Fixtures for CryptoTracker.

Fixtures provide:
- A browser instance (auto-detects: Chrome → Firefox → Safari)
- Base URL
- A pre-authenticated browser session for dashboard tests

Override browser with: pytest --browser=chrome|firefox|safari
"""

import os
import random
import string
import shutil
import sys

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


BASE_URL = os.environ.get("CRYPTOTRACKER_URL", "http://localhost:8080")


def pytest_addoption(parser):
    """Add --browser command line option."""
    parser.addoption(
        "--browser",
        default="auto",
        choices=["auto", "chrome", "firefox", "safari"],
        help="Browser to use for tests (default: auto-detect)",
    )


def _create_driver(browser_name):
    """Create a WebDriver instance for the given browser."""
    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome(options=options)

    if browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        return webdriver.Firefox(options=options)

    if browser_name == "safari":
        return webdriver.Safari()

    raise ValueError(f"Unknown browser: {browser_name}")


def _detect_browser():
    """Auto-detect which browser is available. Tries Chrome → Firefox → Safari."""
    chrome_paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
    ]
    if any(shutil.which(p) or __import__("os").path.exists(p) for p in chrome_paths):
        return "chrome"

    firefox_paths = [
        "/Applications/Firefox.app/Contents/MacOS/firefox",
        "/usr/bin/firefox",
    ]
    if any(shutil.which(p) or __import__("os").path.exists(p) for p in firefox_paths):
        return "firefox"

    if sys.platform == "darwin" and shutil.which("safaridriver"):
        return "safari"

    raise RuntimeError(
        "No supported browser found. Install Chrome, Firefox, or enable Safari WebDriver."
    )


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture(scope="session")
def browser_name(request):
    """Determine which browser to use."""
    choice = request.config.getoption("--browser")
    if choice == "auto":
        name = _detect_browser()
        print(f"\nAuto-detected browser: {name}")
        return name
    return choice


@pytest.fixture(scope="session")
def _shared_driver(browser_name):
    """
    Session-scoped browser instance. One browser for the entire test run.
    This is important for Safari which only allows one WebDriver session at a time.
    """
    driver = _create_driver(browser_name)
    driver.set_window_size(1280, 800)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.fixture
def driver(_shared_driver, base_url):
    """
    Per-test driver. Reuses the session-scoped browser but ensures
    a clean state (logged out, fresh page) before each test.
    """
    # Fresh page load clears all state
    _shared_driver.get(base_url)

    # If dashboard is visible, we're logged in — click logout
    try:
        dashboard = _shared_driver.find_element(By.ID, "dashboard-section")
        if dashboard.is_displayed():
            _shared_driver.find_element(By.ID, "logout-btn").click()
            WebDriverWait(_shared_driver, 5).until(
                EC.visibility_of_element_located((By.ID, "auth-section"))
            )
    except Exception:
        pass

    # Clear any leftover text in input fields
    for field_id in ("username", "password"):
        try:
            field = _shared_driver.find_element(By.ID, field_id)
            field.clear()
        except Exception:
            pass

    return _shared_driver


@pytest.fixture
def logged_in_driver(driver, base_url):
    """
    Provides a browser that is already logged in to CryptoTracker.
    Registers a fresh user via API, then logs in via the UI.
    """
    suffix = "".join(random.choices(string.ascii_lowercase, k=8))
    username = f"selenium_{suffix}"
    password = "testpass123"

    requests.post(
        f"{base_url}/api/register",
        json={"username": username, "password": password},
    )

    # Clear fields and type credentials
    username_field = driver.find_element(By.ID, "username")
    password_field = driver.find_element(By.ID, "password")
    username_field.clear()
    password_field.clear()
    username_field.send_keys(username)
    password_field.send_keys(password)
    driver.find_element(By.ID, "login-btn").click()

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "dashboard-section"))
    )

    return driver
