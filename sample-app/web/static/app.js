let token = "";

function showMessage(elementId, text, isError) {
    const el = document.getElementById(elementId);
    el.textContent = text;
    el.className = "message " + (isError ? "error" : "success");
}

async function register() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const res = await fetch("/api/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error);
        showMessage("auth-message", "Registered! You can now login.", false);
    } catch (err) {
        showMessage("auth-message", err.message, true);
    }
}

async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
        const res = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error);

        token = data.token;
        document.getElementById("auth-section").style.display = "none";
        document.getElementById("dashboard-section").style.display = "block";
        loadPrices();
        loadPortfolio();
    } catch (err) {
        showMessage("auth-message", err.message, true);
    }
}

function logout() {
    token = "";
    document.getElementById("auth-section").style.display = "block";
    document.getElementById("dashboard-section").style.display = "none";
    document.getElementById("username").value = "";
    document.getElementById("password").value = "";
}

async function loadPrices() {
    try {
        const res = await fetch("/api/prices");
        const prices = await res.json();
        const tbody = document.getElementById("prices-body");
        tbody.innerHTML = prices
            .map(
                (p) => `<tr>
                <td>${p.symbol}</td>
                <td>$${p.price.toLocaleString()}</td>
                <td class="${p.change_24h >= 0 ? "positive" : "negative"}">
                    ${p.change_24h >= 0 ? "+" : ""}${p.change_24h}%
                </td>
            </tr>`
            )
            .join("");
    } catch (err) {
        showMessage("dashboard-message", "Failed to load prices", true);
    }
}

async function loadPortfolio() {
    try {
        const res = await fetch("/api/portfolio", {
            headers: { Authorization: "Bearer " + token },
        });
        const items = await res.json();
        const tbody = document.getElementById("portfolio-body");

        if (items.length === 0) {
            tbody.innerHTML =
                '<tr><td colspan="3">No items yet. Add your first crypto!</td></tr>';
            return;
        }

        tbody.innerHTML = items
            .map(
                (item) => `<tr>
                <td>${item.symbol}</td>
                <td>${item.amount}</td>
                <td><button class="delete-btn" onclick="deleteItem(${item.id})">Delete</button></td>
            </tr>`
            )
            .join("");
    } catch (err) {
        showMessage("dashboard-message", "Failed to load portfolio", true);
    }
}

async function addToPortfolio() {
    const symbol = document.getElementById("symbol").value;
    const amount = parseFloat(document.getElementById("amount").value);

    try {
        const res = await fetch("/api/portfolio", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: "Bearer " + token,
            },
            body: JSON.stringify({ symbol, amount }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error);

        document.getElementById("symbol").value = "";
        document.getElementById("amount").value = "";
        showMessage("dashboard-message", `Added ${symbol.toUpperCase()}!`, false);
        loadPortfolio();
    } catch (err) {
        showMessage("dashboard-message", err.message, true);
    }
}

async function deleteItem(id) {
    try {
        const res = await fetch(`/api/portfolio/${id}`, {
            method: "DELETE",
            headers: { Authorization: "Bearer " + token },
        });
        if (!res.ok) {
            const data = await res.json();
            throw new Error(data.error);
        }
        loadPortfolio();
    } catch (err) {
        showMessage("dashboard-message", err.message, true);
    }
}
