"""
Selenium UI Tests: Dashboard
Tests the main dashboard — prices table, portfolio management, add/delete items.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestPricesTable:
    """Verify the market prices table on the dashboard."""

    def test_prices_table_visible(self, logged_in_driver):
        """Prices table is displayed after login."""
        table = logged_in_driver.find_element(By.ID, "prices-table")
        assert table.is_displayed()

    def test_prices_table_has_rows(self, logged_in_driver):
        """Prices table has 5 cryptocurrency rows."""
        rows = logged_in_driver.find_elements(
            By.CSS_SELECTOR, "#prices-body tr"
        )
        assert len(rows) == 5

    def test_prices_table_contains_btc(self, logged_in_driver):
        """Prices table includes BTC."""
        body = logged_in_driver.find_element(By.ID, "prices-body")
        assert "BTC" in body.text

    def test_prices_table_contains_eth(self, logged_in_driver):
        """Prices table includes ETH."""
        body = logged_in_driver.find_element(By.ID, "prices-body")
        assert "ETH" in body.text

    def test_positive_change_has_green_class(self, logged_in_driver):
        """Positive price changes are styled with the 'positive' class."""
        positive_cells = logged_in_driver.find_elements(
            By.CSS_SELECTOR, "#prices-body .positive"
        )
        assert len(positive_cells) > 0

    def test_negative_change_has_red_class(self, logged_in_driver):
        """Negative price changes are styled with the 'negative' class."""
        negative_cells = logged_in_driver.find_elements(
            By.CSS_SELECTOR, "#prices-body .negative"
        )
        assert len(negative_cells) > 0


class TestPortfolioManagement:
    """Test adding and deleting portfolio items through the UI."""

    def test_add_form_elements_visible(self, logged_in_driver):
        """Add form has symbol field, amount field, and Add button."""
        symbol = logged_in_driver.find_element(By.ID, "symbol")
        amount = logged_in_driver.find_element(By.ID, "amount")
        add_btn = logged_in_driver.find_element(By.ID, "add-btn")

        assert symbol.is_displayed()
        assert amount.is_displayed()
        assert add_btn.is_displayed()

    def test_add_item_appears_in_table(self, logged_in_driver):
        """Adding an item makes it appear in the portfolio table."""
        driver = logged_in_driver

        driver.find_element(By.ID, "symbol").send_keys("BTC")
        driver.find_element(By.ID, "amount").send_keys("1.5")
        driver.find_element(By.ID, "add-btn").click()

        # Wait for success message
        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element(
                (By.ID, "dashboard-message"), "Added BTC"
            )
        )

        # Verify BTC appears in portfolio table
        portfolio_body = driver.find_element(By.ID, "portfolio-body")
        assert "BTC" in portfolio_body.text
        assert "1.5" in portfolio_body.text

    def test_add_item_clears_form(self, logged_in_driver):
        """After adding an item, the input fields are cleared."""
        driver = logged_in_driver

        driver.find_element(By.ID, "symbol").send_keys("ETH")
        driver.find_element(By.ID, "amount").send_keys("10")
        driver.find_element(By.ID, "add-btn").click()

        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element(
                (By.ID, "dashboard-message"), "Added ETH"
            )
        )

        assert driver.find_element(By.ID, "symbol").get_attribute("value") == ""
        assert driver.find_element(By.ID, "amount").get_attribute("value") == ""

    def test_delete_item_removes_from_table(self, logged_in_driver):
        """Clicking delete removes the item from the portfolio table."""
        driver = logged_in_driver

        # Add an item first
        driver.find_element(By.ID, "symbol").send_keys("ADA")
        driver.find_element(By.ID, "amount").send_keys("500")
        driver.find_element(By.ID, "add-btn").click()

        WebDriverWait(driver, 5).until(
            EC.text_to_be_present_in_element(
                (By.ID, "dashboard-message"), "Added ADA"
            )
        )

        # Verify ADA is in the table
        portfolio_body = driver.find_element(By.ID, "portfolio-body")
        assert "ADA" in portfolio_body.text

        # Click the last delete button (the one for ADA)
        delete_buttons = driver.find_elements(By.CSS_SELECTOR, ".delete-btn")
        delete_buttons[-1].click()

        # Wait for ADA to disappear from the table
        WebDriverWait(driver, 5).until_not(
            EC.text_to_be_present_in_element(
                (By.ID, "portfolio-body"), "ADA"
            )
        )
