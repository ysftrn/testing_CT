# Test Cases: Prices & Health Check
## CryptoTracker v1.0

| Field | Value |
|-------|-------|
| Document ID | TC-CT-MISC |
| Version | 1.0 |
| Date | 2026-03-06 |
| Author | Yusuf Torun |
| Related Requirements | FR-020 through FR-024 |

---

## TC-021: Get Market Prices

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-021 |
| **Title** | Successfully retrieve cryptocurrency prices |
| **Priority** | Medium |
| **Type** | Functional / Positive |
| **Related Req** | FR-020, FR-021, FR-022 |
| **Preconditions** | Server is running. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send GET to `/api/prices` without any authentication | HTTP 200 response |
| 2 | Verify response is a JSON array | Array of price objects |
| 3 | Verify each object has `symbol`, `price`, `change_24h` | All fields present |
| 4 | Verify `price` values are positive numbers | No zero or negative prices |
| 5 | Verify known symbols are present (BTC, ETH) | Expected symbols in response |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-022: Health Check Returns Healthy Status

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-022 |
| **Title** | Health check endpoint returns healthy status |
| **Priority** | High |
| **Type** | Smoke Test |
| **Related Req** | FR-023, FR-024 |
| **Preconditions** | Server is running. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send GET to `/api/health` | HTTP 200 response |
| 2 | Verify response contains `"status":"healthy"` | Status is healthy |
| 3 | Verify response contains `"app":"CryptoTracker"` | App name is correct |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-023: API Responses Use JSON Content-Type

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-023 |
| **Title** | All API responses have Content-Type application/json |
| **Priority** | High |
| **Type** | Functional / Positive |
| **Related Req** | NFR-003 |
| **Preconditions** | Server is running. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send GET to `/api/health` | Response header `Content-Type` is `application/json` |
| 2 | Send GET to `/api/prices` | Response header `Content-Type` is `application/json` |
| 3 | Send POST to `/api/register` with valid body | Response header `Content-Type` is `application/json` |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-024: API Uses Correct HTTP Status Codes

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-024 |
| **Title** | API returns appropriate HTTP status codes for different scenarios |
| **Priority** | High |
| **Type** | Functional / Positive |
| **Related Req** | NFR-004 |
| **Preconditions** | Server is running. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Successful registration | 201 Created |
| 2 | Successful login | 200 OK |
| 3 | Failed login (wrong password) | 401 Unauthorized |
| 4 | Invalid request body | 400 Bad Request |
| 5 | Access without token | 401 Unauthorized |
| 6 | Delete non-existent item | 404 Not Found |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-025: Password Not Exposed in API Responses

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-025 |
| **Title** | Password is never returned in any API response |
| **Priority** | High |
| **Type** | Security |
| **Related Req** | NFR-007 |
| **Preconditions** | Server is running. A user is registered. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Register a new user, inspect full response | No "password" field in response |
| 2 | Login, inspect full response | No "password" field in response |
| 3 | Get portfolio, inspect full response | No "password" field in response |

| **Actual Result** | |
| **Status** | Not Executed |
