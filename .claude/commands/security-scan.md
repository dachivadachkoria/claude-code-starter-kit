---
name: security-scan
description: "Scan for security vulnerabilities in code and dependencies"
---

# Security Vulnerability Scanner

Perform security audit on: $ARGUMENTS (default: entire project)

## Scan Categories

### 1. Dependency Vulnerabilities

**Python:**
```bash
pip-audit --desc 2>/dev/null || pip install pip-audit && pip-audit --desc
safety check 2>/dev/null || true
```

**JavaScript:**
```bash
npm audit --json
npx audit-ci --moderate
```

**Go:**
```bash
govulncheck ./...
```

### 2. Code Security Issues

Scan for these patterns:

**🔴 Critical**
- Hardcoded secrets/API keys
- SQL injection vulnerabilities
- Command injection (os.system, exec, eval)
- Path traversal (../ in file operations)
- Insecure deserialization
- XXE vulnerabilities

**🟠 High**
- Missing input validation
- Insecure cryptography (MD5, SHA1 for passwords)
- Sensitive data in logs
- Missing authentication checks
- CORS misconfiguration
- Open redirects

**🟡 Medium**
- Missing rate limiting
- Verbose error messages
- Missing security headers
- Insecure random number generation
- Session fixation risks

**🟢 Low**
- Debug mode enabled
- Unnecessary dependencies
- Outdated but non-vulnerable packages

### 3. Secret Detection

Scan for exposed secrets:
```bash
# Check for common secret patterns
grep -rn "password\s*=" --include="*.py" --include="*.js" --include="*.go" .
grep -rn "api_key\s*=" --include="*.py" --include="*.js" --include="*.go" .
grep -rn "secret\s*=" --include="*.py" --include="*.js" --include="*.go" .
```

Patterns to detect:
- AWS access keys: `AKIA[0-9A-Z]{16}`
- GitHub tokens: `ghp_[a-zA-Z0-9]{36}`
- Generic API keys: `[aA][pP][iI]_?[kK][eE][yY].*['\"][a-zA-Z0-9]{20,}['\"]`
- Private keys: `-----BEGIN (RSA|EC|OPENSSH) PRIVATE KEY-----`
- JWT tokens: `eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*`

### 4. Configuration Security

Check:
- `.env` files not in `.gitignore`
- Debug/development settings in production configs
- Default credentials
- Overly permissive CORS
- Missing HTTPS enforcement

## Output Report

```
🛡️ Security Scan Report
══════════════════════════════════════════════════════════

🔴 CRITICAL (2)
───────────────
1. SQL Injection - src/db/queries.py:45
   Issue: User input directly in SQL query
   Fix: Use parameterized queries
   
2. Hardcoded Secret - src/config.py:12
   Issue: API key exposed in source code
   Fix: Move to environment variable

🟠 HIGH (3)
───────────────
1. Missing Auth Check - src/api/admin.py:23
   Issue: Admin endpoint lacks authentication
   Fix: Add @require_auth decorator

[... more items ...]

📦 Dependency Issues (5)
───────────────
- requests 2.25.0 → 2.31.0 (CVE-2023-32681)
- lodash 4.17.20 → 4.17.21 (Prototype pollution)

📊 Summary
───────────────
Critical: 2  |  High: 3  |  Medium: 5  |  Low: 8
Dependencies: 5 vulnerable

🔧 Auto-fixable: 6 issues
   Run /security-fix to apply safe fixes
══════════════════════════════════════════════════════════
```

## Options

`/security-scan` - Full scan
`/security-scan --deps` - Dependencies only
`/security-scan --code` - Code patterns only
`/security-scan --secrets` - Secret detection only
`/security-scan src/api/` - Specific directory
`/security-scan --fix` - Scan and auto-fix safe issues

## Safe Auto-Fixes

These can be fixed automatically:
- ✅ Dependency updates (non-breaking)
- ✅ Adding .gitignore entries
- ✅ Replacing insecure hash functions
- ✅ Adding input sanitization

These require manual review:
- ⚠️ Authentication changes
- ⚠️ Database query modifications
- ⚠️ API endpoint changes
- ⚠️ Configuration changes
