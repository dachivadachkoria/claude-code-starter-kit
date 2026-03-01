---
name: monitor
description: "Monitor repository health, track issues, and identify maintenance tasks"
---

# Repository Health Monitor

Analyze repository health and identify maintenance tasks.

## Target: $ARGUMENTS (default: full repository scan)

## Health Checks

### 1. Dependency Health

```bash
# Check for outdated dependencies
# Python
pip list --outdated 2>/dev/null | head -20

# JavaScript  
npm outdated 2>/dev/null | head -20

# Go
go list -u -m all 2>/dev/null | grep '\[' | head -20
```

**Assess:**
- Major version updates available
- Security patches needed
- Deprecated packages in use
- Unused dependencies

### 2. Code Quality Metrics

```bash
# Line count and complexity
find . -name "*.py" -o -name "*.js" -o -name "*.go" | head -100 | xargs wc -l 2>/dev/null | tail -1

# TODO/FIXME count
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.py" --include="*.js" --include="*.go" . 2>/dev/null | wc -l
```

**Track:**
- Files over 500 lines (candidates for splitting)
- Functions over 50 lines (complexity concern)
- Cyclomatic complexity hotspots
- Code duplication

### 3. Test Health

```bash
# Test count
find . -name "test_*.py" -o -name "*.test.js" -o -name "*_test.go" | wc -l

# Recent test failures (if CI logs available)
```

**Assess:**
- Test coverage percentage
- Flaky test patterns
- Missing test directories
- Test execution time trends

### 4. Documentation Status

**Check:**
- README.md completeness
- API documentation currency
- Docstring coverage
- Changelog updates

### 5. Git Health

```bash
# Large files
git rev-list --objects --all | git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | awk '/^blob/ {print $3, $4}' | sort -rn | head -10

# Stale branches
git branch -r --merged origin/main | grep -v main | head -10

# Recent commit activity
git log --oneline --since="30 days ago" | wc -l
```

**Track:**
- Large files that shouldn't be in git
- Stale branches to clean up
- Commit frequency trends
- Contributors activity

### 6. Security Posture

**Quick checks:**
- `.env` files in `.gitignore`
- No hardcoded secrets in recent commits
- Dependency vulnerabilities
- Security headers in configs

## Output Report

```
📊 Repository Health Report
══════════════════════════════════════════════════════════
Generated: [timestamp]
Repository: [name]

## Overall Health: 🟢 Good | 🟡 Needs Attention | 🔴 Critical

### Summary
┌─────────────────────┬───────────┬────────┐
│ Category            │ Status    │ Score  │
├─────────────────────┼───────────┼────────┤
│ Dependencies        │ 🟡        │ 7/10   │
│ Code Quality        │ 🟢        │ 9/10   │
│ Test Coverage       │ 🟢        │ 8/10   │
│ Documentation       │ 🟡        │ 6/10   │
│ Git Hygiene         │ 🟢        │ 9/10   │
│ Security            │ 🟢        │ 8/10   │
└─────────────────────┴───────────┴────────┘

### 🔴 Critical Issues (0)
None! 🎉

### 🟡 Needs Attention (3)

1. **Outdated Dependencies** (2 major updates)
   - django 3.2 → 4.2 (security patches)
   - requests 2.25 → 2.31 (bug fixes)
   
2. **Low Documentation Coverage**
   - 45% of public functions lack docstrings
   - API docs not updated since [date]
   
3. **TODO Debt** (23 items)
   - 5 marked as FIXME (higher priority)
   - Oldest TODO: 6 months old

### 🟢 Healthy Areas

- Test coverage at 85%
- No security vulnerabilities in dependencies
- Active development (42 commits in last 30 days)
- Clean git history

### 📋 Recommended Actions

Priority 1 (This Week):
- [ ] Update django to 4.2 (security)
- [ ] Address 5 FIXME items

Priority 2 (This Sprint):
- [ ] Add docstrings to core modules
- [ ] Update API documentation
- [ ] Clean up 3 stale branches

Priority 3 (Backlog):
- [ ] Reduce complexity in src/legacy.py
- [ ] Address remaining TODOs
- [ ] Add missing integration tests

### 📈 Trends (Last 30 Days)

- Commits: 42 (↑ 15% from previous period)
- Test coverage: 85% (↑ 3%)
- Open issues: 12 (↓ 4)
- Dependencies updated: 5

══════════════════════════════════════════════════════════
```

## Options

`/monitor` - Full health scan
`/monitor --deps` - Dependencies only
`/monitor --tests` - Test health only
`/monitor --security` - Security focus
`/monitor --quick` - Quick summary only
`/monitor --fix` - Generate fix tasks

## Automation

Consider running weekly via CI:

```yaml
# .github/workflows/health-check.yml
name: Weekly Health Check
on:
  schedule:
    - cron: '0 9 * * 1'  # Monday 9am
  workflow_dispatch:

jobs:
  health-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run health check
        run: |
          # Your monitoring script here
          npm outdated || true
          pip list --outdated || true
      - name: Create issue if needed
        uses: actions/github-script@v7
        with:
          script: |
            // Create issue with findings
```
