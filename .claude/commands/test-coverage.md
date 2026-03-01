---
name: test-coverage
description: "Analyze test coverage and generate tests for uncovered code"
---

# Test Coverage Analysis & Improvement

Analyze and improve test coverage for: $ARGUMENTS

## Execution Flow

### Step 1: Run Coverage Analysis

**Python:**
```bash
pytest --cov=src --cov-report=term-missing --cov-report=html tests/
```

**JavaScript/TypeScript:**
```bash
npm test -- --coverage --coverageReporters=text
```

**Go:**
```bash
go test -coverprofile=coverage.out ./...
go tool cover -func=coverage.out
```

### Step 2: Parse Coverage Report

Identify:
- Files with < 80% coverage
- Specific uncovered lines/functions
- Critical paths missing tests (error handlers, edge cases)

### Step 3: Prioritize by Risk

High Priority (test first):
1. Public API endpoints
2. Authentication/authorization logic
3. Data validation functions
4. Payment/transaction handlers
5. Error handling paths

Medium Priority:
1. Business logic in services
2. Data transformation utilities
3. Integration points

Low Priority:
1. Simple getters/setters
2. Configuration loading
3. Logging statements

### Step 4: Generate Missing Tests

For each uncovered section:
1. Understand what the code does
2. Determine why it might be untested (hard to test? edge case?)
3. Create appropriate test with proper mocking
4. Verify the test actually covers the target lines

### Step 5: Report

```
📊 Coverage Report
══════════════════════════════════════
Before: 65%  →  After: 84%  (+19%)

Files Improved:
  ✅ src/auth.py: 45% → 92%
  ✅ src/api/users.py: 70% → 88%
  ⚠️ src/legacy.py: 30% → 45% (needs manual review)

New Tests Created:
  - tests/test_auth.py (8 tests)
  - tests/test_users.py (5 tests)

Remaining Gaps:
  - src/legacy.py:45-67 (complex branching)
  - src/utils.py:12-15 (dead code?)
══════════════════════════════════════
```

## Coverage Targets

| Category | Target | Minimum |
|----------|--------|---------|
| Overall | 80% | 70% |
| Critical paths | 95% | 90% |
| New code | 90% | 80% |
| Utilities | 70% | 60% |

## Options

`/test-coverage` - Full analysis and improvement
`/test-coverage --report` - Report only, no changes
`/test-coverage src/auth.py` - Focus on specific file
`/test-coverage --critical` - Only critical paths
