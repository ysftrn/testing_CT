# API Testing

## What Is It?
API testing validates the application's **programming interface directly**, bypassing the UI. You send HTTP requests to endpoints and verify the responses — status codes, body content, headers, response time.

It answers: **"Does the API behave correctly according to its contract?"**

## Why API Testing Matters
- **Faster than UI testing** — no browser rendering, no UI interaction
- **More reliable** — no flaky selectors or timing issues
- **Earlier detection** — test backend logic before the UI is even built
- **Better coverage** — test edge cases that are hard to trigger via UI
- In modern architectures (microservices, SPAs), the API IS the product

## What to Verify

| Aspect | What to Check | Example |
|--------|--------------|---------|
| **Status Code** | Correct HTTP code returned | 201 for creation, 401 for unauthorized |
| **Response Body** | Correct data structure and values | JSON has "token" field after login |
| **Headers** | Content-Type, CORS, caching | Content-Type is application/json |
| **Authentication** | Protected endpoints reject unauthenticated requests | 401 without Bearer token |
| **Error Handling** | Meaningful error messages | "username must be at least 3 characters" |
| **Data Integrity** | Created data can be retrieved correctly | POST then GET returns same data |
| **Idempotency** | Repeated calls behave correctly | Double-delete returns 404 on second call |

## HTTP Methods & REST Conventions

| Method | Purpose | Idempotent? | Example |
|--------|---------|:-----------:|---------|
| GET | Read data | Yes | Get portfolio |
| POST | Create data | No | Register user, add item |
| PUT | Replace data | Yes | (Not used in CryptoTracker) |
| PATCH | Partial update | No | (Not used in CryptoTracker) |
| DELETE | Remove data | Yes | Delete portfolio item |

## CryptoTracker API Test Examples

### Positive Tests

```bash
# Health check
curl -s http://localhost:8080/api/health
# Assert: status=200, body contains "healthy"

# Registration
curl -s -w "\nHTTP_CODE:%{http_code}" -X POST http://localhost:8080/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"apitest","password":"test123456"}'
# Assert: status=201, body contains "user registered successfully"

# Login
curl -s -w "\nHTTP_CODE:%{http_code}" -X POST http://localhost:8080/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"apitest","password":"test123456"}'
# Assert: status=200, body contains "token" (non-empty string)
```

### Negative Tests

```bash
# Missing Content-Type
curl -s -w "\nHTTP_CODE:%{http_code}" -X POST http://localhost:8080/api/register \
  -d '{"username":"test","password":"test123"}'
# Assert: status=400

# Invalid JSON
curl -s -w "\nHTTP_CODE:%{http_code}" -X POST http://localhost:8080/api/register \
  -H "Content-Type: application/json" \
  -d 'not json'
# Assert: status=400

# Wrong HTTP method
curl -s -w "\nHTTP_CODE:%{http_code}" -X GET http://localhost:8080/api/register
# Assert: status=405 Method Not Allowed
```

### Chained Tests (Data Flow)

```bash
# Create → Read → Delete → Read (verify deletion)
TOKEN="..."

# 1. Create
ID=$(curl -s -X POST http://localhost:8080/api/portfolio \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"symbol":"DOT","amount":100}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

# 2. Read - verify item exists
curl -s http://localhost:8080/api/portfolio -H "Authorization: Bearer $TOKEN"
# Assert: contains DOT with amount 100

# 3. Delete
curl -s -X DELETE "http://localhost:8080/api/portfolio/$ID" \
  -H "Authorization: Bearer $TOKEN"
# Assert: status=200

# 4. Read again - verify item is gone
curl -s http://localhost:8080/api/portfolio -H "Authorization: Bearer $TOKEN"
# Assert: does NOT contain DOT
```

## Tools Comparison

| Tool | Type | Strengths | Weaknesses |
|------|------|-----------|------------|
| **Postman** | GUI | Visual, easy to learn, collections | Not great for CI/CD |
| **curl** | CLI | Available everywhere, scriptable | Verbose, no assertions |
| **Python requests** | Code | Full programming power, CI-friendly | Requires coding |
| **SoapUI** | GUI | SOAP + REST, data-driven testing | Heavy, complex |
| **Pytest + requests** | Code | Best for CI/CD, rich assertions | Requires Python knowledge |

We'll use **Postman** (Phase 4) and **Pytest** (Phase 6) to automate these tests.

## Common Interview Questions
- **Q: What's the difference between API testing and unit testing?**
  A: Unit testing tests internal functions in isolation. API testing tests the external interface (HTTP endpoints) as a black box — you don't see the code, just the inputs and outputs.
- **Q: How do you test an API that requires authentication?**
  A: First call the login endpoint to get a token, then include that token in the Authorization header of subsequent requests. In test frameworks, this is typically done in a setup/fixture function.
- **Q: What is contract testing?**
  A: Verifying that the API's actual behavior matches its documented specification (OpenAPI/Swagger). If the spec says a field is required, the API must actually require it.
