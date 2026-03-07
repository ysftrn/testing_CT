# Regression Testing

## What Is It?
Regression testing is re-running existing tests after a code change to ensure that the change didn't break anything that was previously working.

The word "regression" means "going backward" — you're checking that the software didn't regress (go back to a broken state).

## When Is It Used?
- After a bug fix
- After adding a new feature
- After refactoring code
- After merging branches
- Before every release

## How to Decide What to Retest: Impact Analysis

This is the key skill. You don't always rerun ALL tests — that's expensive. Instead, you analyze what the code change might affect.

### Impact Analysis Process

1. **Identify what changed** — which files, functions, modules
2. **Identify dependencies** — what other code calls or uses the changed code
3. **Map to features** — which user-facing features are affected
4. **Select test cases** — pick tests that cover the affected features

### CryptoTracker Example

**Scenario:** We fix bug DR-001 (whitespace username). The fix is in `service.Register()` — we add `strings.TrimSpace(username)` before the length check.

**Impact Analysis:**

```
Changed: service.Register()
    ↓
Called by: handlers.Register()
    ↓
Affects: POST /api/register endpoint
    ↓
Also consider: Does the trimmed username affect login?
    → Yes! service.Login() searches by username
    → If we store "john" but they type " john", login might fail
    ↓
Regression test selection:
    - TC-001: Successful registration ← MUST RETEST
    - TC-002: Short username ← MUST RETEST (boundary changed)
    - TC-003: Short password ← skip (unrelated)
    - TC-004: Duplicate username ← MUST RETEST (trimming affects uniqueness)
    - TC-006: Successful login ← MUST RETEST (username matching)
    - TC-007: Wrong password ← skip (password logic unchanged)
    - TC-011 to TC-020: Portfolio tests ← skip (unrelated module)
```

**Result:** We retest 4 out of 25 test cases instead of all 25.

## Regression Test Selection Strategies

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| **Retest All** | Run every test case | Small projects, before major releases |
| **Priority-based** | Run High priority tests first, then Medium if time allows | Time-constrained sprints |
| **Risk-based** | Focus on areas with highest risk of breaking | Large codebases, critical systems |
| **Change-based** | Only test areas affected by the change (impact analysis) | Bug fixes, small changes |

## Relationship to CI/CD
In a CI/CD pipeline, regression tests run **automatically** on every commit:

```
Developer pushes code → CI server detects change → Runs regression suite → Reports results
```

This is why test automation is valuable — manual regression testing doesn't scale.

## Common Interview Questions
- **Q: How do you decide which tests to include in regression?**
  A: Impact analysis — trace the code change to affected features, select tests that cover those features.
- **Q: What's the difference between regression testing and retesting?**
  A: Retesting verifies that a specific bug is fixed. Regression testing verifies that the fix didn't break other things.
- **Q: When would you do a full regression?**
  A: Before a major release, after large refactoring, or when the change affects shared components (database schema, authentication, etc.).
