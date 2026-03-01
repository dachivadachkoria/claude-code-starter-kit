---
name: docs
description: "Generate or update documentation for code"
---

# Documentation Generator

Generate documentation for: $ARGUMENTS

## Target Selection

**If `$ARGUMENTS` is empty:**
- Generate/update README.md
- Update API documentation
- Check for missing docstrings

**If `$ARGUMENTS` is a file:**
- Generate docstrings for all public functions/classes
- Create/update corresponding docs

**If `$ARGUMENTS` is `--api`:**
- Generate API endpoint documentation
- Create OpenAPI/Swagger spec if applicable

## Documentation Types

### 1. Function/Method Docstrings

**Python (Google style):**
```python
def process_payment(amount: float, currency: str = "USD") -> PaymentResult:
    """Process a payment transaction.

    Args:
        amount: The payment amount in the smallest currency unit.
        currency: ISO 4217 currency code. Defaults to "USD".

    Returns:
        PaymentResult containing transaction ID and status.

    Raises:
        PaymentError: If the payment fails.
        ValidationError: If amount is negative.

    Example:
        >>> result = process_payment(1000, "EUR")
        >>> print(result.transaction_id)
        'txn_abc123'
    """
```

**TypeScript (JSDoc):**
```typescript
/**
 * Process a payment transaction.
 * 
 * @param amount - The payment amount in cents
 * @param currency - ISO 4217 currency code
 * @returns Promise resolving to PaymentResult
 * @throws {PaymentError} If the payment fails
 * 
 * @example
 * const result = await processPayment(1000, 'EUR');
 * console.log(result.transactionId);
 */
```

**Go:**
```go
// ProcessPayment handles a payment transaction.
//
// It accepts the amount in the smallest currency unit and an optional
// currency code (defaults to "USD").
//
// Returns a PaymentResult or an error if the payment fails.
func ProcessPayment(amount int64, currency string) (*PaymentResult, error) {
```

### 2. Class/Module Documentation

```python
"""User authentication and session management.

This module provides:
- User login/logout functionality
- Session token generation and validation  
- Password hashing and verification

Typical usage:
    from auth import AuthService
    
    auth = AuthService()
    token = auth.login(username, password)
    user = auth.validate_token(token)

Security Notes:
    - Tokens expire after 24 hours
    - Failed logins are rate-limited
    - Passwords are hashed with bcrypt
"""
```

### 3. API Documentation

```markdown
## POST /api/users

Create a new user account.

### Request

```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

### Response

**201 Created**
```json
{
  "id": "usr_abc123",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2024-01-15T10:30:00Z"
}
```

**400 Bad Request**
```json
{
  "error": "validation_error",
  "details": [
    {"field": "email", "message": "Invalid email format"}
  ]
}
```
```

### 4. README Structure

```markdown
# Project Name

Brief description of what the project does.

## Features

- Feature 1
- Feature 2

## Installation

\`\`\`bash
pip install project-name
\`\`\`

## Quick Start

\`\`\`python
from project import main
main.run()
\`\`\`

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | Your API key | Required |

## API Reference

[Link to detailed API docs]

## Contributing

[Link to CONTRIBUTING.md]

## License

MIT
```

## Execution Flow

1. **Scan** - Find undocumented public APIs
2. **Analyze** - Understand what each function does
3. **Generate** - Create appropriate documentation
4. **Format** - Match project's doc style
5. **Verify** - Ensure docs are accurate

## Output

```
📚 Documentation Report
══════════════════════════════════════════════════════════

Generated/Updated:
  ✅ src/auth.py - Added 5 docstrings
  ✅ src/api/users.py - Added 3 docstrings
  ✅ docs/api.md - Updated API reference
  ✅ README.md - Updated installation section

Coverage:
  Before: 45% documented
  After:  89% documented

Missing (optional):
  - src/utils.py:helper_func (private, skip?)
  - src/internal.py (internal module)

══════════════════════════════════════════════════════════
```

## Options

`/docs` - Update all documentation
`/docs src/file.py` - Document specific file
`/docs --api` - API documentation only
`/docs --readme` - Update README only
`/docs --check` - Report missing docs without changes
