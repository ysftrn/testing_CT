# Integration Testing

## What Is It?
Integration testing verifies that **different modules or components work correctly together**. Individual units may pass their unit tests, but they can still fail when combined due to interface mismatches, data format issues, or incorrect assumptions.

It answers: **"Do these components communicate correctly?"**

## When Is It Used?
- After unit testing is complete
- Before system testing
- When new modules are integrated
- When APIs or database schemas change

## Integration Approaches

### Top-Down
Start from the highest-level module and work down, using **stubs** for lower modules not yet integrated.

```
Handler (real)
    ↓
Service (stub) → returns hardcoded values
```

### Bottom-Up
Start from the lowest-level module and work up, using **drivers** to call the lower modules.

```
Test Driver → calls Repository directly
    ↓
Repository (real)
    ↓
SQLite (real)
```

### Big Bang
Integrate everything at once and test. Simple but hard to debug when things fail.

### Sandwich (Hybrid)
Combine top-down and bottom-up — test from both ends toward the middle.

## Stubs vs Mocks

| | Stub | Mock |
|---|------|------|
| **Purpose** | Provides predefined responses | Verifies interactions |
| **Example** | Fake repository that returns hardcoded users | Verify that `Register()` calls `CreateUser()` exactly once |
| **Checks** | Output correctness | Behavior correctness |

## CryptoTracker Integration Points

Our app has 3 integration boundaries:

```
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────┐
│  Handlers  │────▶│  Service   │────▶│ Repository │────▶│ SQLite │
└────────────┘     └────────────┘     └────────────┘     └────────┘
     ↑ Integration 1      ↑ Integration 2      ↑ Integration 3
```

### Integration Test 1: Handler → Service

Does the HTTP handler correctly parse the request and call the right service method?

```go
// Test: POST /api/register with valid JSON calls service.Register()
func TestRegisterHandler_CallsService(t *testing.T) {
    // Create a real service with a test database
    // Send HTTP request to the handler
    // Verify the response status and body
    // Verify the user was actually created in the database
}
```

### Integration Test 2: Service → Repository

Does the service layer correctly interact with the database layer?

```go
// Test: service.Register() stores hashed password via repository
func TestRegister_StoresHashedPassword(t *testing.T) {
    // Call service.Register("testuser", "plaintext")
    // Query the database directly
    // Verify password is NOT "plaintext" (it should be a bcrypt hash)
}
```

### Integration Test 3: Repository → SQLite

Does the repository correctly execute SQL and handle database responses?

```go
// Test: CreateUser then GetUserByUsername returns the same user
func TestCreateAndGetUser(t *testing.T) {
    // Create user via repository
    // Retrieve user via repository
    // Compare: username matches, ID is assigned, timestamp is set
}
```

### Full Stack Integration Test

Test the complete chain via HTTP:

```bash
# Register a user via HTTP, then verify they exist in the database
curl -X POST http://localhost:8080/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"inttest","password":"test123456"}'

# Login to prove the full chain works:
# HTTP → Handler → Service (password verify) → Repository (user lookup) → SQLite
curl -X POST http://localhost:8080/api/login \
  -H "Content-Type: application/json" \
  -d '{"username":"inttest","password":"test123456"}'
# If token is returned, all integration points work.
```

## Common Interview Questions
- **Q: What's the difference between unit testing and integration testing?**
  A: Unit tests isolate a single function using mocks/stubs. Integration tests verify that real components work together correctly.
- **Q: What approach do you prefer: top-down or bottom-up?**
  A: It depends on the project. Bottom-up is practical when low-level components (like database) are ready first. Top-down works when the UI/API is defined first. Many teams use sandwich approach.
- **Q: What's the hardest part of integration testing?**
  A: Test environment setup — you need real databases, real network connections, and clean test data for each run.
