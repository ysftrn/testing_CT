"""
Shared test fixtures for CryptoTracker API tests.

Fixtures are Pytest's way of providing reusable setup/teardown logic.
Any test function can request a fixture by including it as a parameter.
"""

import random
import string

import pytest
import requests

BASE_URL = "http://localhost:8080"


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the API. Scope='session' means it's created once for the entire test run."""
    return BASE_URL


@pytest.fixture(scope="session")
def session_user(base_url):
    """
    Register a unique user for the test session.
    Returns a dict with username, password, and auth token.
    This user is shared across all tests that need authentication.
    """
    suffix = "".join(random.choices(string.ascii_lowercase, k=8))
    username = f"testuser_{suffix}"
    password = "testpass123"

    # Register
    resp = requests.post(
        f"{base_url}/api/register",
        json={"username": username, "password": password},
    )
    assert resp.status_code == 201, f"Setup failed: could not register user: {resp.text}"

    # Login
    resp = requests.post(
        f"{base_url}/api/login",
        json={"username": username, "password": password},
    )
    assert resp.status_code == 200, f"Setup failed: could not login: {resp.text}"
    token = resp.json()["token"]

    return {"username": username, "password": password, "token": token}


@pytest.fixture
def auth_header(session_user):
    """Convenience fixture: returns the Authorization header dict."""
    return {"Authorization": f"Bearer {session_user['token']}"}


@pytest.fixture
def unique_username():
    """Generate a unique username for tests that need a fresh user."""
    suffix = "".join(random.choices(string.ascii_lowercase, k=8))
    return f"user_{suffix}"
