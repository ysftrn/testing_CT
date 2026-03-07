"""
Python unittest Tests for CryptoTracker API.

Demonstrates the unittest framework (Python's built-in test framework)
alongside the Pytest tests in tests/api/python/.

Key differences from Pytest:
- Tests must be methods in a class that inherits unittest.TestCase
- Uses self.assert* methods instead of bare assert
- setUp/tearDown instead of fixtures
- No automatic test discovery by function name — needs unittest runner or pytest
"""

import json
import os
import random
import string
import unittest
from urllib import request, error


BASE_URL = os.environ.get("CRYPTOTRACKER_URL", "http://localhost:8080")


def _random_username():
    suffix = "".join(random.choices(string.ascii_lowercase, k=8))
    return f"ut_{suffix}"


def _api(method, path, body=None, token=None):
    """Helper: send JSON request, return (status_code, parsed_body)."""
    url = f"{BASE_URL}{path}"
    data = json.dumps(body).encode() if body else None
    req = request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        resp = request.urlopen(req)
        return resp.status, json.loads(resp.read())
    except error.HTTPError as e:
        return e.code, json.loads(e.read())


class TestHealthEndpoint(unittest.TestCase):
    """Tests for GET /api/health."""

    def test_health_returns_200(self):
        status, body = _api("GET", "/api/health")
        self.assertEqual(status, 200)

    def test_health_status_field(self):
        status, body = _api("GET", "/api/health")
        self.assertIn("status", body)
        self.assertEqual(body["status"], "healthy")


class TestRegistration(unittest.TestCase):
    """Tests for POST /api/register."""

    def test_register_success(self):
        username = _random_username()
        status, body = _api("POST", "/api/register", {
            "username": username, "password": "secure123"
        })
        self.assertEqual(status, 201)
        self.assertIn("message", body)

    def test_register_short_username(self):
        status, body = _api("POST", "/api/register", {
            "username": "ab", "password": "secure123"
        })
        self.assertNotEqual(status, 201)

    def test_register_short_password(self):
        status, body = _api("POST", "/api/register", {
            "username": _random_username(), "password": "abc"
        })
        self.assertNotEqual(status, 201)

    def test_register_duplicate_username(self):
        username = _random_username()
        _api("POST", "/api/register", {
            "username": username, "password": "secure123"
        })
        status, body = _api("POST", "/api/register", {
            "username": username, "password": "different456"
        })
        self.assertNotEqual(status, 201)

    def test_register_empty_body(self):
        status, body = _api("POST", "/api/register", {})
        self.assertNotEqual(status, 201)


class TestLogin(unittest.TestCase):
    """Tests for POST /api/login."""

    def setUp(self):
        """Register a user before each login test — like a Pytest fixture."""
        self.username = _random_username()
        self.password = "secure123"
        _api("POST", "/api/register", {
            "username": self.username, "password": self.password
        })

    def test_login_success(self):
        status, body = _api("POST", "/api/login", {
            "username": self.username, "password": self.password
        })
        self.assertEqual(status, 200)
        self.assertIn("token", body)
        self.assertTrue(len(body["token"]) > 0)

    def test_login_wrong_password(self):
        status, body = _api("POST", "/api/login", {
            "username": self.username, "password": "wrongpassword"
        })
        self.assertNotEqual(status, 200)

    def test_login_nonexistent_user(self):
        status, body = _api("POST", "/api/login", {
            "username": "ghost_user_xyz", "password": "any123"
        })
        self.assertNotEqual(status, 200)


class TestPortfolio(unittest.TestCase):
    """Tests for portfolio CRUD endpoints."""

    def setUp(self):
        """Register, login, and store token — reusable setup."""
        self.username = _random_username()
        self.password = "secure123"
        _api("POST", "/api/register", {
            "username": self.username, "password": self.password
        })
        _, body = _api("POST", "/api/login", {
            "username": self.username, "password": self.password
        })
        self.token = body["token"]

    def test_add_portfolio_item(self):
        status, body = _api("POST", "/api/portfolio", {
            "symbol": "BTC", "amount": 1.5
        }, token=self.token)
        self.assertEqual(status, 201)
        self.assertEqual(body["symbol"], "BTC")
        self.assertEqual(body["amount"], 1.5)

    def test_add_item_symbol_uppercased(self):
        status, body = _api("POST", "/api/portfolio", {
            "symbol": "eth", "amount": 10
        }, token=self.token)
        self.assertEqual(status, 201)
        self.assertEqual(body["symbol"], "ETH")

    def test_add_item_empty_symbol(self):
        status, body = _api("POST", "/api/portfolio", {
            "symbol": "", "amount": 1.0
        }, token=self.token)
        self.assertNotEqual(status, 201)

    def test_add_item_zero_amount(self):
        status, body = _api("POST", "/api/portfolio", {
            "symbol": "BTC", "amount": 0
        }, token=self.token)
        self.assertNotEqual(status, 201)

    def test_get_portfolio_empty(self):
        status, body = _api("GET", "/api/portfolio", token=self.token)
        self.assertEqual(status, 200)
        self.assertIsInstance(body, list)
        self.assertEqual(len(body), 0)

    def test_get_portfolio_after_add(self):
        _api("POST", "/api/portfolio", {
            "symbol": "ADA", "amount": 500
        }, token=self.token)
        status, body = _api("GET", "/api/portfolio", token=self.token)
        self.assertEqual(status, 200)
        self.assertEqual(len(body), 1)
        self.assertEqual(body[0]["symbol"], "ADA")

    def test_delete_portfolio_item(self):
        _, item = _api("POST", "/api/portfolio", {
            "symbol": "SOL", "amount": 25
        }, token=self.token)
        item_id = item["id"]

        status, _ = _api("DELETE", f"/api/portfolio/{item_id}",
                         token=self.token)
        self.assertEqual(status, 200)

        # Verify it's gone
        _, items = _api("GET", "/api/portfolio", token=self.token)
        ids = [i["id"] for i in items]
        self.assertNotIn(item_id, ids)

    def test_portfolio_requires_auth(self):
        status, _ = _api("GET", "/api/portfolio")
        self.assertNotEqual(status, 200)


class TestPrices(unittest.TestCase):
    """Tests for GET /api/prices."""

    def test_prices_returns_list(self):
        status, body = _api("GET", "/api/prices")
        self.assertEqual(status, 200)
        self.assertIsInstance(body, list)
        self.assertGreater(len(body), 0)

    def test_prices_contain_btc(self):
        _, body = _api("GET", "/api/prices")
        symbols = [p["symbol"] for p in body]
        self.assertIn("BTC", symbols)

    def test_prices_have_positive_values(self):
        _, body = _api("GET", "/api/prices")
        for price in body:
            self.assertGreater(price["price"], 0,
                               f"{price['symbol']} has non-positive price")


# --- Subtest example (unittest equivalent of Go table-driven tests) ---

class TestRegistrationValidation(unittest.TestCase):
    """
    Uses subTest() — Python's equivalent of Go's t.Run() for table-driven tests.
    Each case runs independently; one failure doesn't stop the rest.
    """

    def test_registration_validation_cases(self):
        cases = [
            ("valid", "gooduser", "secure123", True),
            ("short username", "ab", "secure123", False),
            ("short password", "gooduser", "abc", False),
            ("empty username", "", "secure123", False),
            ("empty password", "gooduser", "", False),
            ("boundary username 3 chars", "abc", "secure123", True),
            ("boundary password 6 chars", "defghi", "abcdef", True),
        ]

        for name, username, password, should_succeed in cases:
            with self.subTest(name=name):
                # Use unique username for success cases to avoid duplicates
                uname = f"{username}_{_random_username()}" if should_succeed and username else username
                status, _ = _api("POST", "/api/register", {
                    "username": uname, "password": password
                })
                if should_succeed:
                    self.assertEqual(status, 201,
                                     f"Expected success for '{name}'")
                else:
                    self.assertNotEqual(status, 201,
                                        f"Expected failure for '{name}'")


if __name__ == "__main__":
    unittest.main()
