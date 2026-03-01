# Project: [YOUR PROJECT NAME]

> ⚠️ **Customize this file** for your specific project. This is the most important file for Claude Code to understand your codebase.

## Overview

[Brief description of what your project does]

## Tech Stack

- **Language**: [Python 3.11+ / TypeScript / Go / etc.]
- **Framework**: [FastAPI / Express / Gin / etc.]
- **Database**: [PostgreSQL / MongoDB / etc.]
- **Cache**: [Redis / Memcached / etc.]
- **Testing**: [pytest / jest / go test / etc.]

## Project Structure

```
src/                    # Source code
├── api/               # API endpoints/routes
├── services/          # Business logic
├── models/            # Data models
├── utils/             # Utilities
tests/                  # Test files (mirrors src/ structure)
├── conftest.py        # Shared fixtures (Python)
├── unit/              # Unit tests
└── integration/       # Integration tests
docs/                   # Documentation
```

## Development Commands

```bash
# Install dependencies
[pip install -r requirements.txt / npm install / go mod download]

# Run tests
[pytest tests/ -v / npm test / go test ./...]

# Run with coverage
[pytest --cov=src / npm test -- --coverage / go test -cover ./...]

# Lint
[ruff check . / npm run lint / golangci-lint run]

# Format
[black . && isort . / npm run format / gofmt -w .]

# Start dev server
[uvicorn main:app --reload / npm run dev / go run main.go]
```

## Testing Conventions

### File Naming
- Test files: `test_<module>.py` or `<module>.test.ts` or `<module>_test.go`
- Located in `tests/` directory, mirroring `src/` structure

### Test Structure
```python
# Python example
def test_<function>_<scenario>_<expected_result>():
    # Arrange
    ...
    # Act
    ...
    # Assert
    ...
```

### Mocking Guidelines
- Mock external services (APIs, databases, cache)
- Use fixtures for common setup
- Never mock the code under test

### What to Test
- ✅ Public functions and methods
- ✅ Edge cases and error handling
- ✅ Business logic in services
- ⚠️ Integration points (with mocks)
- ❌ Private implementation details
- ❌ Third-party library internals

## Code Style

### General
- [Your style guide - PEP 8 / Airbnb / Google / etc.]
- Max line length: [80/100/120]
- Use type hints/annotations

### Naming
- Functions: `snake_case` / `camelCase`
- Classes: `PascalCase`
- Constants: `SCREAMING_SNAKE_CASE`
- Files: `snake_case` / `kebab-case`

### Error Handling
- Always handle errors explicitly
- Use custom exception classes
- Log errors with context

## Security Requirements

### Sensitive Data
- Never log PII or secrets
- Use environment variables for config
- Sanitize user input

### Authentication
- [Your auth approach]

### Dependencies
- Keep dependencies updated
- Review security advisories

## AI Assistant Guidelines

### When Generating Tests
1. Read existing tests in `tests/` for patterns
2. Use fixtures from `conftest.py` when available
3. Mock external dependencies
4. Aim for meaningful assertions, not just coverage
5. Include edge cases and error scenarios

### When Fixing Bugs
1. Write a failing test first
2. Make minimal changes to fix
3. Ensure all existing tests pass
4. Document the fix in commit message

### When Refactoring
1. Ensure test coverage exists first
2. Make incremental changes
3. Run tests after each change
4. Preserve public API unless explicitly changing

### Off-Limits (Always Ask First)
- Authentication/authorization changes
- Database schema changes
- Environment configuration
- Deployment scripts
- Security-critical code

## Common Patterns

### [Pattern 1 - e.g., API Response Format]
```python
# Example pattern used in this project
```

### [Pattern 2 - e.g., Error Handling]
```python
# Example pattern used in this project
```

## Known Issues / Tech Debt

- [ ] [Issue 1]
- [ ] [Issue 2]

## Team Contacts

- **Lead**: [Name]
- **Security**: [Name]

---

*Last updated: [DATE]*
