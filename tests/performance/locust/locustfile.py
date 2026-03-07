"""
Locust Performance Tests for CryptoTracker API.

Simulates realistic user behavior:
1. Register a new account
2. Login (get token)
3. Browse prices
4. Add portfolio items
5. View portfolio
6. Delete items

Run:
    locust -f tests/performance/locust/locustfile.py --host=http://localhost:8080

    # Headless mode (no web UI):
    locust -f tests/performance/locust/locustfile.py --host=http://localhost:8080 \
        --headless -u 50 -r 5 -t 60s

    # -u 50: 50 concurrent users
    # -r 5:  ramp up 5 users/second
    # -t 60s: run for 60 seconds
"""

import random
import string

from locust import HttpUser, task, between, tag


def _random_name():
    return "perf_" + "".join(random.choices(string.ascii_lowercase, k=8))


class CryptoTrackerUser(HttpUser):
    """
    Simulates a typical CryptoTracker user session.

    wait_time: each user waits 1-3 seconds between actions (realistic pacing).
    """

    wait_time = between(1, 3)

    def on_start(self):
        """Called once per simulated user. Register and login."""
        self.username = _random_name()
        self.password = "loadtest123"
        self.token = None
        self.portfolio_ids = []

        # Register
        resp = self.client.post("/api/register", json={
            "username": self.username,
            "password": self.password,
        })
        if resp.status_code != 201:
            return

        # Login
        resp = self.client.post("/api/login", json={
            "username": self.username,
            "password": self.password,
        })
        if resp.status_code == 200:
            self.token = resp.json().get("token")

    @property
    def _headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    # --- Tasks with weights ---
    # Higher weight = more frequent. Reflects real usage patterns:
    # users check prices often, add items sometimes, delete rarely.

    @task(5)
    @tag("read")
    def get_prices(self):
        """Most common action: check market prices."""
        self.client.get("/api/prices")

    @task(3)
    @tag("read")
    def get_portfolio(self):
        """View own portfolio."""
        self.client.get("/api/portfolio", headers=self._headers)

    @task(2)
    @tag("write")
    def add_to_portfolio(self):
        """Add a random crypto to portfolio."""
        symbols = ["BTC", "ETH", "ADA", "SOL", "DOT"]
        resp = self.client.post("/api/portfolio", json={
            "symbol": random.choice(symbols),
            "amount": round(random.uniform(0.1, 100), 2),
        }, headers=self._headers)

        if resp.status_code == 201:
            item_id = resp.json().get("id")
            if item_id:
                self.portfolio_ids.append(item_id)

    @task(1)
    @tag("write")
    def delete_from_portfolio(self):
        """Delete a random item from portfolio (least common action)."""
        if not self.portfolio_ids:
            return
        item_id = self.portfolio_ids.pop(random.randrange(len(self.portfolio_ids)))
        self.client.delete(f"/api/portfolio/{item_id}", headers=self._headers)

    @task(1)
    @tag("read")
    def health_check(self):
        """Periodic health check."""
        self.client.get("/api/health")
