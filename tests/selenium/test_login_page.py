"""
Selenium UI Tests: Login Page
Tests the authentication interface — form elements, registration, login, error handling.
"""

import random
import string

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLoginPageElements:
    """Verify the login page loads with all required elements."""

    def test_page_title(self, driver, base_url):
        """Page title contains CryptoTracker."""
        driver.get(base_url)
        assert "CryptoTracker" in driver.title

    def test_heading_visible(self, driver, base_url):
        """Main heading is displayed."""
        driver.get(base_url)
        heading = driver.find_element(By.TAG_NAME, "h1")
        assert heading.is_displayed()
        assert heading.text == "CryptoTracker"

    def test_username_field_exists(self, driver, base_url):
        """Username input field is present and visible."""
        driver.get(base_url)
        field = driver.find_element(By.ID, "username")
        assert field.is_displayed()
        assert field.get_attribute("placeholder") == "Username"

    def test_password_field_exists(self, driver, base_url):
        """Password input field is present and visible."""
        driver.get(base_url)
        field = driver.find_element(By.ID, "password")
        assert field.is_displayed()
        assert field.get_attribute("type") == "password"

    def test_login_button_exists(self, driver, base_url):
        """Login button is present and visible."""
        driver.get(base_url)
        btn = driver.find_element(By.ID, "login-btn")
        assert btn.is_displayed()
        assert btn.text == "Login"

    def test_register_button_exists(self, driver, base_url):
        """Register button is present and visible."""
        driver.get(base_url)
        btn = driver.find_element(By.ID, "register-btn")
        assert btn.is_displayed()
        assert btn.text == "Register"

    def test_dashboard_hidden_before_login(self, driver, base_url):
        """Dashboard section is not visible before login."""
        driver.get(base_url)
        dashboard = driver.find_element(By.ID, "dashboard-section")
        assert not dashboard.is_displayed()


class TestRegistrationUI:
    """Test user registration through the web interface."""

    def test_successful_registration_shows_message(self, driver, base_url):
        """Successful registration shows a success message."""
        suffix = "".join(random.choices(string.ascii_lowercase, k=8))
        driver.get(base_url)

        driver.find_element(By.ID, "username").send_keys(f"uitest_{suffix}")
        driver.find_element(By.ID, "password").send_keys("secure123")
        driver.find_element(By.ID, "register-btn").click()

        # Wait for success message text to appear
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element(
                (By.ID, "auth-message"), "Registered"
            )
        )
        msg = driver.find_element(By.ID, "auth-message")
        assert "Registered" in msg.text
        assert "success" in msg.get_attribute("class")


class TestLoginUI:
    """Test login functionality through the web interface."""

    def test_successful_login_shows_dashboard(self, driver, base_url):
        """Successful login hides auth section and shows dashboard."""
        # Register via API first
        suffix = "".join(random.choices(string.ascii_lowercase, k=8))
        username = f"loginui_{suffix}"
        requests.post(
            f"{base_url}/api/register",
            json={"username": username, "password": "secure123"},
        )

        driver.get(base_url)
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.ID, "password").send_keys("secure123")
        driver.find_element(By.ID, "login-btn").click()

        # Wait for dashboard
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "dashboard-section"))
        )

        # Auth section should be hidden
        auth = driver.find_element(By.ID, "auth-section")
        assert not auth.is_displayed()

        # Dashboard should be visible
        dashboard = driver.find_element(By.ID, "dashboard-section")
        assert dashboard.is_displayed()

    def test_failed_login_shows_error(self, driver, base_url):
        """Failed login shows error message."""
        driver.get(base_url)
        driver.find_element(By.ID, "username").send_keys("nonexistent_user")
        driver.find_element(By.ID, "password").send_keys("wrongpass")
        driver.find_element(By.ID, "login-btn").click()

        msg = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "auth-message"))
        )
        assert "invalid credentials" in msg.text.lower()
        assert "error" in msg.get_attribute("class")
