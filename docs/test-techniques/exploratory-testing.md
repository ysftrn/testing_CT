# Exploratory Testing

## What Is It?
Exploratory testing is **simultaneous learning, test design, and test execution**. Unlike scripted testing (where you follow pre-written test cases), you explore the application freely, guided by your curiosity, intuition, and experience.

It's not random clicking — it's **structured improvisation**.

## When Is It Used?
- When requirements are incomplete or unclear
- When you want to find bugs that scripted tests miss
- Mid-sprint, to complement scripted testing
- When learning a new application
- Before writing formal test cases (to understand the system)

## How It Differs from Ad-hoc Testing

| | Exploratory Testing | Ad-hoc Testing |
|---|---|---|
| **Structure** | Charter, time-box, documented | None |
| **Goal** | Find specific types of issues | Find anything |
| **Notes** | Detailed session notes | None |
| **Reproducible** | Yes (notes enable reproduction) | Often not |

## Session-Based Test Management (SBTM)

The most common framework for exploratory testing. Each session has:

1. **Charter** — What area to explore and what to look for
2. **Time-box** — Fixed duration (usually 30-90 minutes)
3. **Session notes** — What you did, what you found, questions that arose

## CryptoTracker Example: Exploratory Session

### Session Report

| Field | Value |
|-------|-------|
| **Session ID** | ET-001 |
| **Charter** | Explore the registration feature with unusual inputs to find validation gaps |
| **Tester** | Yusuf Torun |
| **Duration** | 30 minutes |
| **Date** | 2026-03-06 |

### Test Notes

| Time | Action | Observation | Bug? |
|------|--------|-------------|:----:|
| 0:00 | Register with username "   " (3 spaces) | Accepted! Whitespace-only username created | YES → DR-001 |
| 0:05 | Register with username containing SQL: `' OR 1=1 --` | Rejected with generic error (safe) | No |
| 0:08 | Register with 10,000 character username | Accepted. No max length validation | Potential |
| 0:12 | Register with emoji username "🚀🌙💎" | Accepted. Works correctly with UTF-8 | No |
| 0:15 | Register with same username different case ("John" vs "john") | Both accepted as separate users | By design? |
| 0:18 | Send registration with Content-Type: text/plain | Returns "invalid request body" (correct) | No |
| 0:22 | Send registration with extra JSON fields `{"username":"x","password":"y","role":"admin"}` | Extra fields ignored (safe) | No |
| 0:25 | Register, then immediately register again in parallel | One succeeds, one gets duplicate error | No |
| 0:28 | Login with correct username, empty password | Returns "invalid credentials" (correct) | No |

### Session Summary
- **Bugs found:** 1 confirmed (DR-001: whitespace username)
- **Potential issues:** 1 (no max length for username)
- **Questions:** Should usernames be case-insensitive? (Design decision needed)
- **Areas for further exploration:** Login token behavior, portfolio with special characters

## Tips for Effective Exploratory Testing

1. **Think like a user who makes mistakes** — typos, wrong order of operations, back button
2. **Think like an attacker** — SQL injection, XSS, authentication bypass
3. **Think about boundaries** — empty, very long, zero, negative, special characters
4. **Think about state** — what happens if you do things out of order?
5. **Take notes constantly** — if you can't reproduce it, it didn't happen

## Common Interview Questions
- **Q: Is exploratory testing the same as random testing?**
  A: No. Exploratory testing is guided by charters, documented with session notes, and uses the tester's experience. Random testing has no structure.
- **Q: Can exploratory testing replace scripted testing?**
  A: No. They complement each other. Scripted tests ensure known requirements are covered. Exploratory tests find issues that scripted tests miss.
- **Q: How do you report exploratory testing results?**
  A: Through session reports — documenting the charter, duration, actions taken, observations, and bugs found.
