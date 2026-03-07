# CryptoTracker - System Under Test

CryptoTracker is a simple cryptocurrency portfolio tracking web application built with Go. It serves as the **System Under Test (SUT)** for this software testing portfolio.

## Features

| Feature | Description |
|---------|-------------|
| User Registration | Create an account with username and password |
| User Login | Authenticate and receive a session token |
| Portfolio Management | Add and remove cryptocurrency holdings |
| Market Prices | View current cryptocurrency prices |
| Health Check | Verify server availability |

## Tech Stack

- **Language:** Go
- **Database:** SQLite
- **Frontend:** Vanilla HTML/CSS/JavaScript
- **Authentication:** Token-based (Bearer tokens)
- **Architecture:** Layered (Handlers → Service → Repository)

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────┐
│   Frontend   │────▶│   Handlers   │────▶│   Service    │────▶│   Repo   │──▶ SQLite
│  (HTML/JS)   │     │  (HTTP API)  │     │  (Business)  │     │  (Data)  │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────┘
```

- **Handlers** (`internal/handlers/`) — HTTP request/response handling, routing, JSON serialization
- **Service** (`internal/service/`) — Business logic, validation, authentication
- **Repository** (`internal/repository/`) — Database operations (CRUD)
- **Models** (`internal/models/`) — Data structures shared across layers

## API Endpoints

| Method | Endpoint | Auth Required | Description |
|--------|----------|:------------:|-------------|
| `GET` | `/api/health` | No | Server health check |
| `POST` | `/api/register` | No | Create a new user account |
| `POST` | `/api/login` | No | Authenticate and get token |
| `GET` | `/api/portfolio` | Yes | List user's portfolio items |
| `POST` | `/api/portfolio` | Yes | Add a cryptocurrency holding |
| `DELETE` | `/api/portfolio/{id}` | Yes | Remove a portfolio item |
| `GET` | `/api/prices` | No | Get cryptocurrency prices |

## Request/Response Examples

### Register
```bash
curl -X POST http://localhost:8080/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secret123"}'

# Response (201): {"message":"user registered successfully"}
```

### Login
```bash
curl -X POST http://localhost:8080/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"john","password":"secret123"}'

# Response (200): {"token":"abc123...","message":"login successful"}
```

### Add to Portfolio
```bash
curl -X POST http://localhost:8080/api/portfolio \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"symbol":"BTC","amount":0.5}'

# Response (201): {"id":1,"user_id":1,"symbol":"BTC","amount":0.5,"created_at":"..."}
```

### Get Portfolio
```bash
curl http://localhost:8080/api/portfolio \
  -H "Authorization: Bearer <token>"

# Response (200): [{"id":1,"user_id":1,"symbol":"BTC","amount":0.5,"created_at":"..."}]
```

### Delete from Portfolio
```bash
curl -X DELETE http://localhost:8080/api/portfolio/1 \
  -H "Authorization: Bearer <token>"

# Response (200): {"message":"item deleted"}
```

### Get Prices
```bash
curl http://localhost:8080/api/prices

# Response (200): [{"symbol":"BTC","price":67432.5,"change_24h":2.3}, ...]
```

## Validation Rules

| Field | Rule |
|-------|------|
| Username | Minimum 3 characters |
| Password | Minimum 6 characters |
| Symbol | Required, auto-converted to uppercase |
| Amount | Must be a positive number |

## Running

```bash
# From the project root directory
make run

# Or build and run the binary
make build
./bin/cryptotracker

# The server starts on http://localhost:8080
# Override port with: PORT=3000 ./bin/cryptotracker
```

## Notes

- Prices are currently mock data (hardcoded), not fetched from a live exchange API.
- Tokens are stored in-memory; they are lost when the server restarts.
- The SQLite database file (`cryptotracker.db`) is created in the working directory.
