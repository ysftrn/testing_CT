"""
Test Cases: Portfolio Management
Maps to: TC-011 through TC-020
"""

import requests


class TestAddPortfolio:
    """Tests for POST /api/portfolio"""

    def test_add_crypto_to_portfolio(self, base_url, auth_header):
        """TC-011: Successfully add a cryptocurrency to portfolio."""
        resp = requests.post(
            f"{base_url}/api/portfolio",
            json={"symbol": "BTC", "amount": 1.5},
            headers=auth_header,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["symbol"] == "BTC"
        assert data["amount"] == 1.5
        assert "id" in data
        assert "user_id" in data
        assert "created_at" in data

    def test_add_empty_symbol_rejected(self, base_url, auth_header):
        """TC-012: Adding cryptocurrency rejected when symbol is empty."""
        resp = requests.post(
            f"{base_url}/api/portfolio",
            json={"symbol": "", "amount": 1.0},
            headers=auth_header,
        )
        assert resp.status_code == 400
        assert "symbol is required" in resp.json()["error"]

    def test_symbol_auto_uppercase(self, base_url, auth_header):
        """TC-013: Symbol is automatically converted to uppercase."""
        resp = requests.post(
            f"{base_url}/api/portfolio",
            json={"symbol": "eth", "amount": 5.0},
            headers=auth_header,
        )
        assert resp.status_code == 201
        assert resp.json()["symbol"] == "ETH"

    def test_zero_amount_rejected(self, base_url, auth_header):
        """TC-014: Adding cryptocurrency rejected when amount is zero."""
        resp = requests.post(
            f"{base_url}/api/portfolio",
            json={"symbol": "BTC", "amount": 0},
            headers=auth_header,
        )
        assert resp.status_code == 400
        assert "amount must be positive" in resp.json()["error"]

    def test_negative_amount_rejected(self, base_url, auth_header):
        """TC-015: Adding cryptocurrency rejected when amount is negative."""
        resp = requests.post(
            f"{base_url}/api/portfolio",
            json={"symbol": "BTC", "amount": -5},
            headers=auth_header,
        )
        assert resp.status_code == 400
        assert "amount must be positive" in resp.json()["error"]


class TestGetPortfolio:
    """Tests for GET /api/portfolio"""

    def test_view_portfolio(self, base_url, auth_header):
        """TC-016: Successfully retrieve user's portfolio."""
        # Add an item first
        requests.post(
            f"{base_url}/api/portfolio",
            json={"symbol": "SOL", "amount": 100},
            headers=auth_header,
        )

        resp = requests.get(f"{base_url}/api/portfolio", headers=auth_header)
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1

        # Verify item structure
        item = data[0]
        assert "id" in item
        assert "user_id" in item
        assert "symbol" in item
        assert "amount" in item
        assert "created_at" in item

    def test_empty_portfolio_returns_empty_array(self, base_url):
        """TC-017: Empty portfolio returns empty array."""
        # Register and login a fresh user with no portfolio
        import random, string
        suffix = "".join(random.choices(string.ascii_lowercase, k=8))
        username = f"emptyuser_{suffix}"

        requests.post(
            f"{base_url}/api/register",
            json={"username": username, "password": "test123456"},
        )
        login_resp = requests.post(
            f"{base_url}/api/login",
            json={"username": username, "password": "test123456"},
        )
        token = login_resp.json()["token"]

        resp = requests.get(
            f"{base_url}/api/portfolio",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        assert resp.json() == []


class TestDeletePortfolio:
    """Tests for DELETE /api/portfolio/{id}"""

    def test_delete_portfolio_item(self, base_url, auth_header):
        """TC-018: Successfully delete a portfolio item."""
        # Add an item
        add_resp = requests.post(
            f"{base_url}/api/portfolio",
            json={"symbol": "ADA", "amount": 500},
            headers=auth_header,
        )
        item_id = add_resp.json()["id"]

        # Delete it
        del_resp = requests.delete(
            f"{base_url}/api/portfolio/{item_id}",
            headers=auth_header,
        )
        assert del_resp.status_code == 200
        assert del_resp.json()["message"] == "item deleted"

        # Verify it's gone
        portfolio = requests.get(
            f"{base_url}/api/portfolio", headers=auth_header
        ).json()
        item_ids = [item["id"] for item in portfolio]
        assert item_id not in item_ids

    def test_delete_nonexistent_item(self, base_url, auth_header):
        """TC-019: Deleting non-existent item returns error."""
        resp = requests.delete(
            f"{base_url}/api/portfolio/99999",
            headers=auth_header,
        )
        assert resp.status_code == 404
        assert "item not found" in resp.json()["error"]

    def test_cannot_delete_other_users_item(self, base_url, auth_header):
        """TC-020: User cannot delete another user's portfolio item."""
        import random, string

        # Add item as session_user (via auth_header)
        add_resp = requests.post(
            f"{base_url}/api/portfolio",
            json={"symbol": "DOT", "amount": 50},
            headers=auth_header,
        )
        item_id = add_resp.json()["id"]

        # Register and login a different user
        suffix = "".join(random.choices(string.ascii_lowercase, k=8))
        other_user = f"other_{suffix}"
        requests.post(
            f"{base_url}/api/register",
            json={"username": other_user, "password": "other123456"},
        )
        login_resp = requests.post(
            f"{base_url}/api/login",
            json={"username": other_user, "password": "other123456"},
        )
        other_token = login_resp.json()["token"]

        # Try to delete session_user's item with other_user's token
        del_resp = requests.delete(
            f"{base_url}/api/portfolio/{item_id}",
            headers={"Authorization": f"Bearer {other_token}"},
        )
        assert del_resp.status_code == 404  # Should not find it (belongs to another user)

        # Verify original user's item still exists
        portfolio = requests.get(
            f"{base_url}/api/portfolio", headers=auth_header
        ).json()
        item_ids = [item["id"] for item in portfolio]
        assert item_id in item_ids
