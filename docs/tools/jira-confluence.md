# JIRA & Confluence

## JIRA — Issue & Project Tracking

JIRA is the industry-standard tool for managing software projects. Testers use it to track bugs, test tasks, and sprint progress.

### How Testers Use JIRA

| Activity | JIRA Feature |
|----------|-------------|
| Report bugs | Create Issue (type: Bug) |
| Track test tasks | Create Issue (type: Task/Story) |
| Link bugs to test cases | Issue Links |
| Track defect lifecycle | Workflow (Open → In Progress → Fixed → Verified → Closed) |
| Sprint planning | Scrum/Kanban boards |
| Filter test-related work | JQL queries |
| Dashboard metrics | Gadgets (bug count, burndown, velocity) |

### Bug Report in JIRA

A typical bug report maps directly to our defect report template (DR-001):

```
Project:     CRYPTO
Issue Type:  Bug
Summary:     Registration accepts whitespace-only username
Priority:    Medium
Severity:    Medium (custom field)
Assignee:    Backend Developer

Description:
  Steps to Reproduce:
  1. POST /api/register with body {"username": "   ", "password": "secure123"}
  2. Observe response

  Expected Result: 400 Bad Request
  Actual Result:   201 Created — user registered with blank name

  Environment: macOS, Go 1.22, SQLite

Labels:       validation, security
Components:   API, Auth
Sprint:       Sprint 3
Linked Issues: TC-001 (Test Case), SRS FR-001 (Requirement)
Attachments:  screenshot.png, api-response.json
```

### JQL (JIRA Query Language)

JQL lets you filter and search issues. Essential queries for testers:

```sql
-- All open bugs assigned to me
project = CRYPTO AND type = Bug AND status != Closed AND assignee = currentUser()

-- High/Critical bugs in current sprint
project = CRYPTO AND type = Bug AND priority in (High, Critical) AND sprint in openSprints()

-- Bugs found this week
project = CRYPTO AND type = Bug AND created >= startOfWeek()

-- All issues linked to a test case
issue in linkedIssues("TC-001")

-- Bugs by component
project = CRYPTO AND type = Bug AND component = "API"

-- Reopened bugs (regression indicators)
project = CRYPTO AND type = Bug AND status changed to "Reopened"
```

### JIRA Workflow for Bugs

```
     ┌─────────────────────────────────────────────────┐
     │                                                 │
Open ──► In Progress ──► Fixed ──► In Testing ──► Closed
                           │            │
                           │            └──► Reopened ──► In Progress
                           │
                           └──► Won't Fix ──► Closed
```

### JIRA + CryptoTracker Mapping

| CryptoTracker Artifact | JIRA Equivalent |
|----------------------|----------------|
| SRS requirements (FR-001) | Epic or Story |
| Test cases (TC-001) | Test type issue or linked to Story |
| Defect report (DR-001) | Bug issue |
| Test plan | Confluence page (linked from Epic) |
| Sprint test tasks | Sub-tasks under Stories |

---

## Confluence — Documentation & Knowledge Base

Confluence is Atlassian's wiki tool, used alongside JIRA for test documentation.

### What Testers Store in Confluence

| Document | CryptoTracker Equivalent |
|----------|-------------------------|
| Test Plan | `docs/test-plan/test-plan.md` |
| Test Strategy | Part of test plan |
| Test Cases | `docs/test-cases/*.md` |
| RTM | `docs/traceability-matrix/RTM.md` |
| Test Reports | `docs/test-reports/test-report-template.md` |
| Release Notes | Summary of test results per release |
| Onboarding Guide | How to set up and run the test suite |

### Confluence Page Structure

```
CryptoTracker Space
├── Project Overview
├── Requirements
│   └── SRS v1.0
├── Test Documentation
│   ├── Test Plan
│   ├── Test Cases
│   │   ├── Auth Test Cases (TC-001 to TC-010)
│   │   ├── Portfolio Test Cases (TC-011 to TC-020)
│   │   └── Prices/Health Test Cases (TC-021 to TC-025)
│   ├── Traceability Matrix
│   └── Test Techniques
├── Test Reports
│   ├── Sprint 1 Report
│   ├── Sprint 2 Report
│   └── Release 1.0 Report
├── Defects
│   └── Known Issues
└── CI/CD
    ├── Pipeline Setup Guide
    └── SonarQube Configuration
```

### JIRA + Confluence Integration

- Confluence pages can embed JIRA issue lists (live filters)
- JIRA issues can link to Confluence pages
- Example: Test Plan page has a live JIRA macro showing all open bugs
- Sprint retrospective pages pull velocity charts from JIRA

---

## Common Interview Questions

**Q: How do you manage test cases in JIRA?**
A: Either use JIRA's built-in test management (with plugins like Zephyr/Xray), or link test cases from a dedicated tool (Testiny, TestRail) to JIRA stories. Each test case links to the requirement it verifies and any bugs it discovers.

**Q: How do you track test progress in a sprint?**
A: Create a JIRA dashboard with gadgets: test execution status (pass/fail/blocked), open bugs by priority, burn-down chart. Use JQL filters to show sprint-specific metrics.

**Q: What's the relationship between Confluence and JIRA?**
A: Confluence is for documentation (test plans, guides, reports), JIRA is for tracking (bugs, tasks, sprints). They integrate: Confluence pages embed live JIRA data, and JIRA issues link to Confluence docs.
