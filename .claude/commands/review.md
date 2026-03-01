---
name: review
description: "Perform AI-powered code review on changes or specific files"
---

# Code Review

Review code changes: $ARGUMENTS

## Target Selection

**If `$ARGUMENTS` is empty:**
```bash
# Review staged changes
git diff --cached
```

**If `$ARGUMENTS` is `--branch` or `--pr`:**
```bash
# Review all changes in current branch vs main
git diff main...HEAD
```

**If `$ARGUMENTS` is a file path:**
- Review that specific file

**If `$ARGUMENTS` is a PR number (e.g., `#123`):**
```bash
gh pr diff 123
```

## Review Checklist

### 🏗️ Architecture & Design

- [ ] Changes align with project architecture (see CLAUDE.md)
- [ ] No unnecessary coupling between modules
- [ ] Appropriate separation of concerns
- [ ] Follows existing patterns in the codebase

### 🐛 Correctness

- [ ] Logic is correct and handles all cases
- [ ] Edge cases are handled (null, empty, boundary values)
- [ ] Error handling is appropriate
- [ ] No off-by-one errors
- [ ] Async operations handled correctly

### 🛡️ Security

- [ ] No hardcoded secrets or credentials
- [ ] User input is validated and sanitized
- [ ] No SQL injection vulnerabilities
- [ ] Authentication/authorization checked where needed
- [ ] Sensitive data not logged

### ⚡ Performance

- [ ] No obvious N+1 queries
- [ ] Appropriate use of caching
- [ ] No unnecessary loops or iterations
- [ ] Large data sets handled efficiently
- [ ] No blocking operations in async code

### 📖 Readability & Maintainability

- [ ] Clear, descriptive variable/function names
- [ ] Complex logic has comments explaining "why"
- [ ] No magic numbers (use constants)
- [ ] Functions are focused (single responsibility)
- [ ] Code is not overly clever

### 🧪 Testing

- [ ] New code has corresponding tests
- [ ] Tests cover happy path and edge cases
- [ ] Tests are meaningful (not just coverage padding)
- [ ] No flaky tests introduced

### 📝 Documentation

- [ ] Public APIs have docstrings/JSDoc
- [ ] README updated if needed
- [ ] Breaking changes documented

## Output Format

```
📝 Code Review: src/api/users.py
══════════════════════════════════════════════════════════

✅ APPROVED with suggestions

## Summary
Good implementation of user CRUD operations. Clean separation 
of concerns. A few minor improvements suggested below.

## Issues Found

### 🟡 Medium: Missing input validation (line 45)
```python
# Current
def create_user(data: dict):
    user = User(**data)

# Suggested  
def create_user(data: UserCreateSchema):
    # Pydantic validates automatically
    user = User(**data.dict())
```
**Why:** Raw dict allows invalid data to reach the database.

### 🟢 Minor: Consider using constant (line 23)
```python
# Current
if len(password) < 8:

# Suggested
MIN_PASSWORD_LENGTH = 8
if len(password) < MIN_PASSWORD_LENGTH:
```
**Why:** Magic number; easier to maintain as a constant.

## What's Good 👍
- Clean async/await usage
- Good error messages
- Follows project patterns

## Checklist Results
✅ Architecture  ✅ Correctness  ✅ Security
⚠️ Performance (1 issue)  ✅ Readability  ⚠️ Testing (needs tests)

══════════════════════════════════════════════════════════
```

## Severity Levels

| Level | Action Required |
|-------|----------------|
| 🔴 **Blocker** | Must fix before merge |
| 🟠 **Major** | Should fix before merge |
| 🟡 **Medium** | Fix recommended |
| 🟢 **Minor** | Nice to have |
| 💡 **Suggestion** | Consider for future |

## Options

`/review` - Review staged changes
`/review --branch` - Review entire branch
`/review src/file.py` - Review specific file
`/review #123` - Review PR (requires gh CLI)
`/review --strict` - Stricter review criteria
