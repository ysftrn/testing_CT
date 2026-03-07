# SDLC/STLC Documentation

Process documentation demonstrating understanding of software development and testing lifecycles.

## Contents

| Document | Topics Covered |
|----------|---------------|
| [sdlc-stlc.md](sdlc-stlc.md) | SDLC models (Waterfall, V-Model, Agile, Kanban), STLC phases, testing in Scrum, entry/exit criteria, test levels, sprint examples, interview Q&A |

## How This Maps to CryptoTracker

| Process Concept | Our Implementation |
|----------------|-------------------|
| SDLC Model | Agile (iterative phases) |
| Requirements | `docs/requirements/SRS.md` |
| Test Planning | `docs/test-plan/test-plan.md` |
| Test Case Design | `docs/test-cases/*.md` (25 cases) |
| Test Execution | 112 automated tests across 4 frameworks |
| Defect Management | `docs/defect-reports/` (DR-001) |
| Test Reporting | `docs/test-reports/test-report-template.md` |
| CI/CD | `Jenkinsfile`, `.github/workflows/ci.yml` |
| Traceability | `docs/traceability-matrix/RTM.md` |
