"""
Test Cases: Prices, HTTP Standards, Security
Maps to: TC-021, TC-023, TC-024, TC-025
"""

import requests


class TestPrices:
    """Tests for GET /api/prices"""

    def test_get_prices_returns_200(self, base_url):
        """TC-021: Successfully retrieve cryptocurrency prices."""
        resp = requests.get(f"{base_url}/api/prices")
        assert resp.status_code == 200

    def test_prices_returns_array(self, base_url):
        """TC-021: Response is a non-empty array."""
        resp = requests.get(f"{base_url}/api/prices")
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_prices_have_required_fields(self, base_url):
        """TC-021: Each price object has symbol, price, change_24h."""
        resp = requests.get(f"{base_url}/api/prices")
        for item in resp.json():
            assert "symbol" in item
            assert "price" in item
            assert "change_24h" in item

    def test_prices_values_are_valid(self, base_url):
        """TC-021: Price values are positive numbers."""
        resp = requests.get(f"{base_url}/api/prices")
        for item in resp.json():
            assert isinstance(item["price"], (int, float))
            assert item["price"] > 0

    def test_prices_include_known_symbols(self, base_url):
        """TC-021: Known symbols BTC and ETH are present."""
        resp = requests.get(f"{base_url}/api/prices")
        symbols = [item["symbol"] for item in resp.json()]
        assert "BTC" in symbols
        assert "ETH" in symbols

    def test_prices_accessible_without_auth(self, base_url):
        """TC-021/FR-022: Prices endpoint does not require authentication."""
        resp = requests.get(f"{base_url}/api/prices")
        assert resp.status_code == 200  # No 401


class TestHTTPStandards:
    """TC-023, TC-024: API follows HTTP standards."""

    def test_json_content_type_on_health(self, base_url):
        """TC-023: Health endpoint returns JSON content type."""
        resp = requests.get(f"{base_url}/api/health")
        assert "application/json" in resp.headers["Content-Type"]

    def test_json_content_type_on_prices(self, base_url):
        """TC-023: Prices endpoint returns JSON content type."""
        resp = requests.get(f"{base_url}/api/prices")
        assert "application/json" in resp.headers["Content-Type"]

    def test_json_content_type_on_register(self, base_url):
        """TC-023: Register endpoint returns JSON content type."""
        resp = requests.post(
            f"{base_url}/api/register",
            json={"username": "x", "password": "x"},
        )
        assert "application/json" in resp.headers["Content-Type"]

    def test_201_on_successful_creation(self, base_url, auth_header):
        """TC-024: Successful creation returns 201."""
        resp = requests.post(
            f"{base_url}/api/portfolio",
            json={"symbol": "XRP", "amount": 1},
            headers=auth_header,
        )
        assert resp.status_code == 201

    def test_400_on_bad_request(self, base_url):
        """TC-024: Invalid input returns 400."""
        resp = requests.post(
            f"{base_url}/api/register",
            json={"username": "ab", "password": "secure123"},
        )
        assert resp.status_code == 400

    def test_401_on_unauthorized(self, base_url):
        """TC-024: Missing auth returns 401."""
        resp = requests.get(f"{base_url}/api/portfolio")
        assert resp.status_code == 401


class TestSecurity:
    """TC-025: Password is never exposed in API responses."""

    def test_register_response_has_no_password(self, base_url):
        """TC-025: Registration response does not contain password."""
        import random, string
        suffix = "".join(random.choices(string.ascii_lowercase, k=8))
        resp = requests.post(
            f"{base_url}/api/register",
            json={"username": f"sec_{suffix}", "password": "secret123"},
        )
        body = resp.text
        assert "secret123" not in body
        assert "password" not in body.lower() or '"password"' not in body

    def test_login_response_has_no_password(self, base_url, session_user):
        """TC-025: Login response does not contain password."""
        resp = requests.post(
            f"{base_url}/api/login",
            json={
                "username": session_user["username"],
                "password": session_user["password"],
            },
        )
        body = resp.text
        assert session_user["password"] not in body

    def test_portfolio_response_has_no_password(self, base_url, auth_header):
        """TC-025: Portfolio response does not contain password."""
        resp = requests.get(f"{base_url}/api/portfolio", headers=auth_header)
        assert "password" not in resp.text.lower()
