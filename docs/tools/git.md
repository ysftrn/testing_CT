# Git & GitHub for Testers

## Why Testers Need Git

- Version control test scripts alongside application code
- Track changes to test plans and documentation
- Collaborate with developers via pull requests
- Trigger CI/CD pipelines on push/merge
- Review code changes to identify what needs testing (impact analysis)

## Essential Git Commands

### Daily workflow

```bash
git status                    # What files changed?
git diff                      # What exactly changed?
git add <file>                # Stage changes
git commit -m "message"       # Save a snapshot
git push                      # Upload to remote
git pull                      # Download latest changes
```

### Branching

```bash
git branch feature/add-tests  # Create a branch
git checkout feature/add-tests # Switch to it
git checkout -b feature/x     # Create + switch (shortcut)
git merge feature/add-tests   # Merge branch into current
git branch -d feature/x       # Delete merged branch
```

### Investigating changes (for impact analysis)

```bash
git log --oneline -20         # Recent commit history
git log --oneline -- path/    # History for specific files
git diff main..feature        # What changed on a branch?
git blame <file>              # Who changed each line?
git show <commit>             # Full details of a commit
```

## Git Workflow for Testing Teams

### Feature Branch Workflow

```
main ─────────────────────────────────────────────►
       \                              /
        \── feature/auth-tests ──────/  (PR + merge)
       \                                      /
        \── feature/portfolio-tests ─────────/
```

1. Developer creates feature branch
2. Tester reviews PR → identifies test impact
3. Tester creates their own branch for new tests
4. Tests pass in CI → PR approved → merge to main

### What Testers Review in PRs

| Look For | Why |
|----------|-----|
| Changed API endpoints | Need new/updated API tests |
| Changed validation logic | Need boundary/negative tests |
| Changed database schema | Need data integrity tests |
| New dependencies | Need integration tests |
| Changed UI components | Need Selenium test updates |
| Security-related changes | Need security test review |

## GitHub Features for Testers

| Feature | Testing Use |
|---------|------------|
| **Issues** | Bug reports (like JIRA) |
| **Pull Requests** | Code review + CI check gates |
| **Actions** | Automated test execution |
| **Projects** | Kanban boards for test tasks |
| **Wiki** | Test documentation (like Confluence) |
| **Releases** | Tag tested versions |

## CryptoTracker Git History

```bash
# Our commit history shows the project evolution:
git log --oneline

# Each phase was committed as a logical unit:
# Phase 1: "initial commit" (app code)
# Phase 2-8: "updates" (docs, tests, CI/CD)
```

## Common Interview Questions

**Q: How do you use Git as a tester?**
A: I version-control test scripts, review PRs to assess test impact, create branches for new test suites, and use CI/CD integration to run tests automatically on push.

**Q: What do you look for when reviewing a PR?**
A: Changed endpoints, validation logic, database queries, and UI components — anything that affects existing test cases or requires new ones. I also check for security issues and missing error handling.

**Q: What's the difference between `git merge` and `git rebase`?**
A: Merge creates a merge commit preserving full history. Rebase replays commits on top of the target branch for a linear history. Teams typically merge feature branches and rebase to keep up with main.
