# Security Checklist

Use this checklist for security reviews and audits.

## Input Validation

- [ ] All user inputs are validated
- [ ] Validation uses allowlists (not denylists)
- [ ] Input length limits are enforced
- [ ] File uploads validate type and size
- [ ] Query parameters are sanitized
- [ ] JSON schemas validate structure

## Authentication

- [ ] Passwords are hashed with bcrypt/argon2 (not MD5/SHA1)
- [ ] Password requirements are enforced (length, complexity)
- [ ] Account lockout after failed attempts
- [ ] Secure password reset flow
- [ ] Session tokens are random and unpredictable
- [ ] Sessions expire appropriately
- [ ] "Remember me" uses separate long-lived token

## Authorization

- [ ] Every endpoint checks permissions
- [ ] Default deny policy (explicit allow)
- [ ] Resource ownership verified
- [ ] Admin functions protected
- [ ] API keys have minimal required permissions
- [ ] RBAC/ABAC properly implemented

## Data Protection

- [ ] Sensitive data encrypted at rest
- [ ] TLS/HTTPS enforced
- [ ] Database connections encrypted
- [ ] Secrets in environment variables (not code)
- [ ] PII handling compliant with regulations
- [ ] Backup encryption enabled

## Injection Prevention

### SQL Injection
- [ ] Parameterized queries used everywhere
- [ ] ORM prevents raw SQL
- [ ] No string concatenation in queries

### XSS (Cross-Site Scripting)
- [ ] Output encoding applied
- [ ] Content Security Policy headers
- [ ] Template auto-escaping enabled
- [ ] Sanitization for rich text

### Command Injection
- [ ] No shell command execution with user input
- [ ] Subprocess uses arrays, not strings
- [ ] Input validation before system calls

### Path Traversal
- [ ] File paths validated
- [ ] No `../` allowed in paths
- [ ] Absolute paths checked against allowed directories

## API Security

- [ ] Rate limiting implemented
- [ ] API authentication required
- [ ] CORS configured correctly
- [ ] Sensitive data not in URLs
- [ ] Proper HTTP methods used
- [ ] Input validation on all endpoints
- [ ] Error messages don't leak info

## Session Management

- [ ] Session IDs regenerated on login
- [ ] Secure cookie flags (HttpOnly, Secure, SameSite)
- [ ] Session timeout implemented
- [ ] Logout invalidates session server-side
- [ ] Concurrent session handling

## Logging & Monitoring

- [ ] Security events logged
- [ ] Logs don't contain sensitive data
- [ ] Log integrity protected
- [ ] Alerts for suspicious activity
- [ ] Failed login attempts tracked

## Dependencies

- [ ] Dependencies regularly updated
- [ ] Vulnerability scanning automated
- [ ] No known vulnerable versions
- [ ] Dependency integrity verified (checksums)
- [ ] Minimal dependency footprint

## Configuration

- [ ] Debug mode disabled in production
- [ ] Error pages don't reveal stack traces
- [ ] Default credentials changed
- [ ] Unnecessary features disabled
- [ ] Security headers configured:
  - [ ] Content-Security-Policy
  - [ ] X-Content-Type-Options
  - [ ] X-Frame-Options
  - [ ] Strict-Transport-Security

## File Security

- [ ] Upload directory outside web root
- [ ] File execution disabled in upload directory
- [ ] File types validated (magic bytes, not extension)
- [ ] Uploaded files renamed
- [ ] Size limits enforced

## Cryptography

- [ ] Modern algorithms used (AES-256, RSA-2048+)
- [ ] No custom cryptography
- [ ] Secure random number generation
- [ ] Keys properly managed
- [ ] Certificates valid and not expiring

## Infrastructure

- [ ] Firewall rules minimized
- [ ] Unnecessary ports closed
- [ ] OS and services patched
- [ ] Principle of least privilege
- [ ] Network segmentation

## Incident Response

- [ ] Incident response plan exists
- [ ] Contact information current
- [ ] Backup restoration tested
- [ ] Security team notified of issues

---

## Quick Checks

### Find Hardcoded Secrets
```bash
grep -rn "password\s*=" --include="*.py" --include="*.js" .
grep -rn "api_key\s*=" --include="*.py" --include="*.js" .
grep -rn "secret\s*=" --include="*.py" --include="*.js" .
```

### Check .gitignore
```bash
# Should contain:
# .env
# *.pem
# *.key
# secrets.*
```

### Verify HTTPS
```bash
curl -I https://yourdomain.com | grep -i strict-transport
```

### Check Dependencies
```bash
# Python
pip-audit

# JavaScript
npm audit

# Go
govulncheck ./...
```
