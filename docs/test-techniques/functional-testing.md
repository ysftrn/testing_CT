# Functional Testing

## What Is It?
Functional testing verifies that the software behaves according to its **requirements specification (SRS)**. You take each requirement, design test cases for it, execute them, and compare the actual result against the expected result.

It answers one question: **"Does the feature work as specified?"**

## When Is It Used?
- During every sprint/iteration in Agile
- After each build in Waterfall
- It is the most common type of testing — the core of a tester's daily work

## How It Works

### 1. Identify the requirement
> FR-002: The system shall enforce a minimum username length of 3 characters.

### 2. Design test cases using techniques

**Equivalence Partitioning (EP):**
Divide inputs into classes that should be treated the same.

| Class | Example Input | Expected |
|-------|:------------:|----------|
| Valid (3+ chars) | "john" | Registration succeeds |
| Invalid (< 3 chars) | "ab" | Error: username too short |
| Empty | "" | Error |

**Boundary Value Analysis (BVA):**
Test at the exact boundaries.

| Boundary | Input Length | Expected |
|----------|:-----------:|----------|
| Below minimum | 2 chars ("ab") | Rejected |
| At minimum | 3 chars ("abc") | Accepted |
| Above minimum | 4 chars ("abcd") | Accepted |

**Decision Table:**
Combine multiple conditions.

| Username Length | Password Length | Expected Result |
|:--------------:|:--------------:|----------------|
| >= 3 | >= 6 | Success |
| >= 3 | < 6 | Password error |
| < 3 | >= 6 | Username error |
| < 3 | < 6 | Username error (first validation) |

### 3. Execute and record results
Run the test, fill in "Actual Result" and "Status" in the test case document.

## CryptoTracker Example

Testing FR-014 (amount must be positive):

```bash
# Equivalence Partition: Valid
curl -X POST http://localhost:8080/api/portfolio \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"symbol":"BTC","amount":1.5}'
# Expected: 201 Created

# Equivalence Partition: Invalid (zero)
curl -X POST http://localhost:8080/api/portfolio \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"symbol":"BTC","amount":0}'
# Expected: 400 Bad Request

# Equivalence Partition: Invalid (negative)
curl -X POST http://localhost:8080/api/portfolio \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"symbol":"BTC","amount":-5}'
# Expected: 400 Bad Request

# Boundary: Smallest valid amount
curl -X POST http://localhost:8080/api/portfolio \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"symbol":"BTC","amount":0.00000001}'
# Expected: 201 Created
```

## Common Interview Questions
- **Q: What is the difference between functional and non-functional testing?**
  A: Functional tests check *what* the system does (features). Non-functional tests check *how well* it does it (performance, security, usability).
- **Q: Name three test design techniques.**
  A: Equivalence Partitioning, Boundary Value Analysis, Decision Table Testing.
- **Q: How do you decide which test cases to write?**
  A: Start from the SRS. Each requirement gets at least one positive and one negative test case. Use EP and BVA to determine specific values.
