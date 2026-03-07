# Software Requirements Specification (SRS)
## CryptoTracker v1.0

| Field | Value |
|-------|-------|
| Document ID | SRS-CT-001 |
| Version | 1.0 |
| Date | 2026-03-06 |
| Author | Yusuf Torun |
| Status | Approved |

---

## 1. Introduction

### 1.1 Purpose
This document defines the functional and non-functional requirements for CryptoTracker, a web-based cryptocurrency portfolio tracking application.

### 1.2 Scope
CryptoTracker allows users to register, authenticate, manage a personal cryptocurrency portfolio, and view market prices through a web interface and REST API.

### 1.3 Definitions
| Term | Definition |
|------|-----------|
| SUT | System Under Test |
| API | Application Programming Interface |
| CRUD | Create, Read, Update, Delete |
| Token | A string used for session authentication |

---

## 2. Functional Requirements

### 2.1 User Registration

| Req ID | Requirement | Priority |
|--------|------------|----------|
| FR-001 | The system shall allow users to create an account with a username and password. | High |
| FR-002 | The system shall enforce a minimum username length of 3 characters. | High |
| FR-003 | The system shall enforce a minimum password length of 6 characters. | High |
| FR-004 | The system shall not allow duplicate usernames. | High |
| FR-005 | The system shall store passwords in hashed form (bcrypt). | High |

### 2.2 User Authentication

| Req ID | Requirement | Priority |
|--------|------------|----------|
| FR-006 | The system shall authenticate users with username and password. | High |
| FR-007 | The system shall return a Bearer token upon successful login. | High |
| FR-008 | The system shall reject login attempts with invalid credentials. | High |
| FR-009 | The system shall require a valid Bearer token for protected endpoints. | High |
| FR-010 | The system shall return HTTP 401 for requests with missing or invalid tokens. | High |

### 2.3 Portfolio Management

| Req ID | Requirement | Priority |
|--------|------------|----------|
| FR-011 | The system shall allow authenticated users to add a cryptocurrency to their portfolio. | High |
| FR-012 | The system shall validate that the cryptocurrency symbol is not empty. | Medium |
| FR-013 | The system shall automatically convert symbols to uppercase. | Low |
| FR-014 | The system shall validate that the amount is a positive number. | High |
| FR-015 | The system shall allow authenticated users to view their portfolio. | High |
| FR-016 | The system shall return an empty list for users with no portfolio items. | Medium |
| FR-017 | The system shall allow authenticated users to delete a portfolio item by ID. | High |
| FR-018 | The system shall return an error when deleting a non-existent portfolio item. | Medium |
| FR-019 | The system shall prevent users from deleting another user's portfolio items. | High |

### 2.4 Market Prices

| Req ID | Requirement | Priority |
|--------|------------|----------|
| FR-020 | The system shall provide current cryptocurrency prices. | Medium |
| FR-021 | The system shall include 24-hour price change percentage. | Low |
| FR-022 | The prices endpoint shall be accessible without authentication. | Medium |

### 2.5 Health Check

| Req ID | Requirement | Priority |
|--------|------------|----------|
| FR-023 | The system shall provide a health check endpoint. | High |
| FR-024 | The health check shall return the application name and status. | Medium |

### 2.6 Web Interface

| Req ID | Requirement | Priority |
|--------|------------|----------|
| FR-025 | The system shall provide a web UI for registration and login. | Medium |
| FR-026 | The system shall display market prices in a table on the dashboard. | Medium |
| FR-027 | The system shall display the user's portfolio in a table on the dashboard. | Medium |
| FR-028 | The system shall provide UI controls to add and delete portfolio items. | Medium |
| FR-029 | The system shall display success and error messages to the user. | Medium |
| FR-030 | The system shall provide a logout function that clears the session. | Medium |

---

## 3. Non-Functional Requirements

| Req ID | Requirement | Category | Priority |
|--------|------------|----------|----------|
| NFR-001 | The API shall respond within 500ms under normal load. | Performance | Medium |
| NFR-002 | The system shall handle at least 100 concurrent users. | Performance | Low |
| NFR-003 | All API responses shall be in JSON format. | Interoperability | High |
| NFR-004 | The API shall use standard HTTP status codes. | Interoperability | High |
| NFR-005 | The system shall run on Linux, macOS, and Windows. | Portability | Medium |
| NFR-006 | The system shall use SQLite for data persistence. | Maintainability | Medium |
| NFR-007 | Passwords shall never be returned in API responses. | Security | High |

---

## 4. API Specification

| Method | Endpoint | Auth | Request Body | Success Code |
|--------|----------|:----:|-------------|:------------:|
| GET | /api/health | No | — | 200 |
| POST | /api/register | No | `{"username","password"}` | 201 |
| POST | /api/login | No | `{"username","password"}` | 200 |
| GET | /api/portfolio | Yes | — | 200 |
| POST | /api/portfolio | Yes | `{"symbol","amount"}` | 201 |
| DELETE | /api/portfolio/{id} | Yes | — | 200 |
| GET | /api/prices | No | — | 200 |
