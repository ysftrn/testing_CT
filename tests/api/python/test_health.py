"""
Test Cases: Health Check & General API behavior
Maps to: TC-022, TC-023, TC-024
"""

import requests


class TestHealthCheck:
    """TC-022: Health check endpoint returns healthy status."""

    def test_health_returns_200(self, base_url):
        resp = requests.get(f"{base_url}/api/health")
        assert resp.status_code == 200

    def test_health_returns_healthy_status(self, base_url):
        resp = requests.get(f"{base_url}/api/health")
        data = resp.json()
        assert data["status"] == "healthy"

    def test_health_returns_app_name(self, base_url):
        resp = requests.get(f"{base_url}/api/health")
        data = resp.json()
        assert data["app"] == "CryptoTracker"

    def test_health_content_type_is_json(self, base_url):
        """TC-023: API responses have Content-Type application/json."""
        resp = requests.get(f"{base_url}/api/health")
        assert "application/json" in resp.headers["Content-Type"]
