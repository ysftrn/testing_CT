"""
Test Cases: Authentication (Registration & Login)
Maps to: TC-001 through TC-010
"""

import requests


class TestRegistration:
    """Tests for POST /api/register"""

    def test_successful_registration(self, base_url, unique_username):
        """TC-001: Successful user registration with valid credentials."""
        resp = requests.post(
            f"{base_url}/api/register",
            json={"username": unique_username, "password": "secure123"},
        )
        assert resp.status_code == 201
        assert resp.json()["message"] == "user registered successfully"

    def test_registration_short_username(self, base_url):
        """TC-002: Registration rejected when username < 3 characters."""
        resp = requests.post(
            f"{base_url}/api/register",
            json={"username": "ab", "password": "secure123"},
        )
        assert resp.status_code == 400
        assert "username must be at least 3 characters" in resp.json()["error"]

    def test_registration_short_password(self, base_url):
        """TC-003: Registration rejected when password < 6 characters."""
        resp = requests.post(
            f"{base_url}/api/register",
            json={"username": "testuser", "password": "abc"},
        )
        assert resp.status_code == 400
        assert "password must be at least 6 characters" in resp.json()["error"]

    def test_registration_duplicate_username(self, base_url, unique_username):
        """TC-004: Registration rejected when username already exists."""
        # First registration should succeed
        resp1 = requests.post(
            f"{base_url}/api/register",
            json={"username": unique_username, "password": "secure123"},
        )
        assert resp1.status_code == 201

        # Second registration with same username should fail
        resp2 = requests.post(
            f"{base_url}/api/register",
            json={"username": unique_username, "password": "secure123"},
        )
        assert resp2.status_code == 400

    def test_registration_empty_body(self, base_url):
        """TC-005: Registration rejected when request body is empty."""
        resp = requests.post(
            f"{base_url}/api/register",
            data="",
            headers={"Content-Type": "application/json"},
        )
        assert resp.status_code == 400
        assert "invalid request body" in resp.json()["error"]

    def test_registration_boundary_username_3_chars(self, base_url):
        """Boundary Value: Username with exactly 3 characters should succeed."""
        resp = requests.post(
            f"{base_url}/api/register",
            json={"username": "abc", "password": "secure123"},
        )
        # Might fail if "abc" already exists, but status should not be 400 for length
        assert resp.status_code in (201, 400)
        if resp.status_code == 400:
            # If it fails, it should be for duplicate, not length
            assert "at least 3 characters" not in resp.json()["error"]

    def test_registration_boundary_password_6_chars(self, base_url, unique_username):
        """Boundary Value: Password with exactly 6 characters should succeed."""
        resp = requests.post(
            f"{base_url}/api/register",
            json={"username": unique_username, "password": "abcdef"},
        )
        assert resp.status_code == 201


class TestLogin:
    """Tests for POST /api/login"""

    def test_successful_login(self, base_url, session_user):
        """TC-006: Successful login with valid credentials."""
        resp = requests.post(
            f"{base_url}/api/login",
            json={
                "username": session_user["username"],
                "password": session_user["password"],
            },
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "token" in data
        assert len(data["token"]) > 0
        assert data["message"] == "login successful"

    def test_login_wrong_password(self, base_url, session_user):
        """TC-007: Login rejected with incorrect password."""
        resp = requests.post(
            f"{base_url}/api/login",
            json={
                "username": session_user["username"],
                "password": "wrongpassword",
            },
        )
        assert resp.status_code == 401
        assert resp.json()["error"] == "invalid credentials"

    def test_login_nonexistent_user(self, base_url):
        """TC-008: Login rejected when user does not exist."""
        resp = requests.post(
            f"{base_url}/api/login",
            json={"username": "ghostuser_nonexistent", "password": "any123"},
        )
        assert resp.status_code == 401
        assert resp.json()["error"] == "invalid credentials"

    def test_login_error_does_not_reveal_which_field_is_wrong(self, base_url, session_user):
        """TC-008 (security): Same error message for wrong username vs wrong password."""
        # Wrong username
        resp1 = requests.post(
            f"{base_url}/api/login",
            json={"username": "nonexistent_user_xyz", "password": "any123"},
        )
        # Wrong password
        resp2 = requests.post(
            f"{base_url}/api/login",
            json={
                "username": session_user["username"],
                "password": "wrongpassword",
            },
        )
        # Both should return the same generic error
        assert resp1.json()["error"] == resp2.json()["error"] == "invalid credentials"


class TestTokenAuth:
    """Tests for token-based authentication on protected endpoints."""

    def test_no_token_returns_401(self, base_url):
        """TC-009: Protected endpoint returns 401 without Authorization header."""
        resp = requests.get(f"{base_url}/api/portfolio")
        assert resp.status_code == 401
        assert "authorization header required" in resp.json()["error"]

    def test_invalid_token_returns_401(self, base_url):
        """TC-010: Protected endpoint returns 401 with invalid token."""
        resp = requests.get(
            f"{base_url}/api/portfolio",
            headers={"Authorization": "Bearer invalidtoken123"},
        )
        assert resp.status_code == 401
        assert "invalid or expired token" in resp.json()["error"]
