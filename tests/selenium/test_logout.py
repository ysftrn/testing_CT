"""
Selenium UI Tests: Logout
Tests the logout functionality — button visibility, state transition.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestLogout:
    """Test logout functionality through the web interface."""

    def test_logout_button_visible(self, logged_in_driver):
        """Logout button is visible on the dashboard."""
        btn = logged_in_driver.find_element(By.ID, "logout-btn")
        assert btn.is_displayed()
        assert btn.text == "Logout"

    def test_logout_returns_to_login_page(self, logged_in_driver):
        """Clicking logout hides dashboard and shows login form."""
        driver = logged_in_driver

        driver.find_element(By.ID, "logout-btn").click()

        # Wait for auth section to reappear
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "auth-section"))
        )

        # Auth section visible
        assert driver.find_element(By.ID, "auth-section").is_displayed()

        # Dashboard hidden
        assert not driver.find_element(By.ID, "dashboard-section").is_displayed()

    def test_logout_clears_input_fields(self, logged_in_driver):
        """After logout, username and password fields are empty."""
        driver = logged_in_driver

        driver.find_element(By.ID, "logout-btn").click()

        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, "auth-section"))
        )

        assert driver.find_element(By.ID, "username").get_attribute("value") == ""
        assert driver.find_element(By.ID, "password").get_attribute("value") == ""
