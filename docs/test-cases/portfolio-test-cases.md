# Test Cases: Portfolio Management
## CryptoTracker v1.0

| Field | Value |
|-------|-------|
| Document ID | TC-CT-PORT |
| Version | 1.0 |
| Date | 2026-03-06 |
| Author | Yusuf Torun |
| Related Requirements | FR-011 through FR-019 |

---

## TC-011: Add Cryptocurrency to Portfolio

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-011 |
| **Title** | Successfully add a cryptocurrency to portfolio |
| **Priority** | High |
| **Type** | Functional / Positive |
| **Related Req** | FR-011 |
| **Preconditions** | Server is running. User is authenticated (valid token obtained). |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send POST to `/api/portfolio` with `Authorization: Bearer <token>` and body `{"symbol":"BTC","amount":1.5}` | HTTP 201 response |
| 2 | Verify response contains `id`, `user_id`, `symbol`, `amount`, `created_at` | All fields present with correct values |
| 3 | Verify `symbol` is "BTC" and `amount` is 1.5 | Values match request |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-012: Add Cryptocurrency with Empty Symbol

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-012 |
| **Title** | Adding cryptocurrency rejected when symbol is empty |
| **Priority** | Medium |
| **Type** | Functional / Negative |
| **Related Req** | FR-012 |
| **Preconditions** | Server is running. User is authenticated. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send POST to `/api/portfolio` with body `{"symbol":"","amount":1.0}` | HTTP 400 response |
| 2 | Verify response body | `{"error":"symbol is required"}` |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-013: Symbol Auto-Uppercase Conversion

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-013 |
| **Title** | Symbol is automatically converted to uppercase |
| **Priority** | Low |
| **Type** | Functional / Positive |
| **Related Req** | FR-013 |
| **Preconditions** | Server is running. User is authenticated. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send POST to `/api/portfolio` with body `{"symbol":"eth","amount":5.0}` | HTTP 201 response |
| 2 | Verify the `symbol` field in response is "ETH" (uppercase) | Symbol converted to uppercase |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-014: Add Cryptocurrency with Zero Amount

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-014 |
| **Title** | Adding cryptocurrency rejected when amount is zero |
| **Priority** | High |
| **Type** | Functional / Negative |
| **Related Req** | FR-014 |
| **Preconditions** | Server is running. User is authenticated. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send POST to `/api/portfolio` with body `{"symbol":"BTC","amount":0}` | HTTP 400 response |
| 2 | Verify response body | `{"error":"amount must be positive"}` |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-015: Add Cryptocurrency with Negative Amount

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-015 |
| **Title** | Adding cryptocurrency rejected when amount is negative |
| **Priority** | High |
| **Type** | Functional / Negative |
| **Related Req** | FR-014 |
| **Preconditions** | Server is running. User is authenticated. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send POST to `/api/portfolio` with body `{"symbol":"BTC","amount":-5}` | HTTP 400 response |
| 2 | Verify response body | `{"error":"amount must be positive"}` |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-016: View Portfolio

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-016 |
| **Title** | Successfully retrieve user's portfolio |
| **Priority** | High |
| **Type** | Functional / Positive |
| **Related Req** | FR-015 |
| **Preconditions** | Server is running. User is authenticated. User has at least one portfolio item. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Add a portfolio item (BTC, 1.0) | Item added successfully |
| 2 | Send GET to `/api/portfolio` with valid token | HTTP 200 response |
| 3 | Verify response is a JSON array containing the added item | Array with at least one item |
| 4 | Verify each item has `id`, `user_id`, `symbol`, `amount`, `created_at` | All fields present |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-017: View Empty Portfolio

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-017 |
| **Title** | Empty portfolio returns empty array |
| **Priority** | Medium |
| **Type** | Functional / Positive |
| **Related Req** | FR-016 |
| **Preconditions** | Server is running. User is authenticated. User has no portfolio items. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send GET to `/api/portfolio` with valid token | HTTP 200 response |
| 2 | Verify response body is `[]` | Empty JSON array |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-018: Delete Portfolio Item

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-018 |
| **Title** | Successfully delete a portfolio item |
| **Priority** | High |
| **Type** | Functional / Positive |
| **Related Req** | FR-017 |
| **Preconditions** | Server is running. User is authenticated. User has a portfolio item with known ID. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Add a portfolio item and note the returned `id` | Item created, ID obtained |
| 2 | Send DELETE to `/api/portfolio/{id}` with valid token | HTTP 200 response |
| 3 | Verify response body | `{"message":"item deleted"}` |
| 4 | Send GET to `/api/portfolio` | The deleted item is no longer in the list |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-019: Delete Non-existent Portfolio Item

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-019 |
| **Title** | Deleting non-existent item returns error |
| **Priority** | Medium |
| **Type** | Functional / Negative |
| **Related Req** | FR-018 |
| **Preconditions** | Server is running. User is authenticated. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Send DELETE to `/api/portfolio/99999` with valid token | HTTP 404 response |
| 2 | Verify response body | `{"error":"item not found"}` |

| **Actual Result** | |
| **Status** | Not Executed |

---

## TC-020: Cannot Delete Another User's Portfolio Item

| Field | Value |
|-------|-------|
| **Test Case ID** | TC-020 |
| **Title** | User cannot delete another user's portfolio item |
| **Priority** | High |
| **Type** | Security / Negative |
| **Related Req** | FR-019 |
| **Preconditions** | Server is running. Two users are registered (User A and User B). User A has a portfolio item. |

| Step | Action | Expected Result |
|:----:|--------|----------------|
| 1 | Login as User A and add a portfolio item. Note the item ID. | Item created |
| 2 | Login as User B | Token obtained for User B |
| 3 | Send DELETE to `/api/portfolio/{User A's item ID}` with User B's token | HTTP 404 response |
| 4 | Verify User A's item still exists by logging in as User A and listing portfolio | Item is still present |

| **Actual Result** | |
| **Status** | Not Executed |
