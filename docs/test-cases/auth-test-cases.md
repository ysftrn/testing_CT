# Test Cases: Authentication
## CryptoTracker v1.0

| Field | Value |
|-------|-------|
| Document ID | TC-CT-AUTH |
| Version | 1.0 |
| Date | 2026-03-06 |
| Author | Yusuf Torun |
| Related Requirements | FR-001 through FR-010 |

---

## TC-001: Successful User Registration

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-001 |
| **Title** | Successful user registration with valid credentials |
| **Priority** | High |
| **Type** | Functional / Positive |
| **Related Req** | FR-001 |
| **Preconditions** | Server is running. Username "newuser" does not exist in the database. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send POST to `/api/register` with body `{"username":"newuser","password":"secure123"}` | HTTP 201 response |
| 2 | Verify response body | `{"message":"user registered successfully"}` |
| 3 | Attempt to login with the registered credentials | Login succeeds, token is returned |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-002: Registration with Short Username

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-002 |
| **Title** | Registration rejected when username is less than 3 characters |
| **Priority** | High |
| **Type** | Functional / Negative |
| **Related Req** | FR-002 |
| **Preconditions** | Server is running. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send POST to `/api/register` with body `{"username":"ab","password":"secure123"}` | HTTP 400 response |
| 2 | Verify response body | `{"error":"username must be at least 3 characters"}` |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-003: Registration with Short Password

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-003 |
| **Title** | Registration rejected when password is less than 6 characters |
| **Priority** | High |
| **Type** | Functional / Negative |
| **Related Req** | FR-003 |
| **Preconditions** | Server is running. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send POST to `/api/register` with body `{"username":"testuser","password":"abc"}` | HTTP 400 response |
| 2 | Verify response body | `{"error":"password must be at least 6 characters"}` |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-004: Registration with Duplicate Username

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-004 |
| **Title** | Registration rejected when username already exists |
| **Priority** | High |
| **Type** | Functional / Negative |
| **Related Req** | FR-004 |
| **Preconditions** | Server is running. User "existinguser" is already registered. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Register a user with username "existinguser" | HTTP 201, registration succeeds |
| 2 | Send POST to `/api/register` with the same username "existinguser" | HTTP 400 response |
| 3 | Verify response body contains an error about duplicate username | Error message returned |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-005: Registration with Empty Body

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-005 |
| **Title** | Registration rejected when request body is empty or invalid JSON |
| **Priority** | Medium |
| **Type** | Functional / Negative |
| **Related Req** | FR-001 |
| **Preconditions** | Server is running. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send POST to `/api/register` with empty body | HTTP 400 response |
| 2 | Verify response body | `{"error":"invalid request body"}` |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-006: Successful Login

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-006 |
| **Title** | Successful login with valid credentials |
| **Priority** | High |
| **Type** | Functional / Positive |
| **Related Req** | FR-006, FR-007 |
| **Preconditions** | Server is running. User "loginuser" is registered with password "pass123456". |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send POST to `/api/login` with body `{"username":"loginuser","password":"pass123456"}` | HTTP 200 response |
| 2 | Verify response contains a "token" field | Token is a non-empty string |
| 3 | Verify response contains `"message":"login successful"` | Message field present |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-007: Login with Wrong Password

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-007 |
| **Title** | Login rejected with incorrect password |
| **Priority** | High |
| **Type** | Functional / Negative |
| **Related Req** | FR-008 |
| **Preconditions** | Server is running. User "loginuser" is registered. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send POST to `/api/login` with body `{"username":"loginuser","password":"wrongpass"}` | HTTP 401 response |
| 2 | Verify response body | `{"error":"invalid credentials"}` |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-008: Login with Non-existent Username

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-008 |
| **Title** | Login rejected when user does not exist |
| **Priority** | High |
| **Type** | Functional / Negative |
| **Related Req** | FR-008 |
| **Preconditions** | Server is running. User "ghostuser" is NOT registered. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send POST to `/api/login` with body `{"username":"ghostuser","password":"any123"}` | HTTP 401 response |
| 2 | Verify response body | `{"error":"invalid credentials"}` |
| 3 | Verify error message does NOT reveal whether the username or password was wrong | Same generic error for both cases |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-009: Access Protected Endpoint Without Token

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-009 |
| **Title** | Protected endpoint returns 401 when no Authorization header is provided |
| **Priority** | High |
| **Type** | Security / Negative |
| **Related Req** | FR-009, FR-010 |
| **Preconditions** | Server is running. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send GET to `/api/portfolio` without Authorization header | HTTP 401 response |
| 2 | Verify response body | `{"error":"authorization header required"}` |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-010: Access Protected Endpoint With Invalid Token

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-010 |
| **Title** | Protected endpoint returns 401 when token is invalid |
| **Priority** | High |
| **Type** | Security / Negative |
| **Related Req** | FR-009, FR-010 |
| **Preconditions** | Server is running. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send GET to `/api/portfolio` with header `Authorization: Bearer invalidtoken123` | HTTP 401 response |
| 2 | Verify response body | `{"error":"invalid or expired token"}` |

| **Actual Result** | |
| **Status** | Not Executed |
