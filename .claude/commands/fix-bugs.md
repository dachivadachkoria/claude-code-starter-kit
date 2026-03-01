---
name: fix-bugs
description: "Detect and fix common bugs, anti-patterns, and code issues"
---

# Bug Detection & Auto-Fix

Scan and fix issues in: $ARGUMENTS (default: changed files)

## Detection Categories

### 1. Common Bugs

**Null/Undefined Handling**
```python
# Bug: AttributeError if user is None
user.name  

# Fix: Safe navigation
user.name if user else None
# Or: getattr(user, 'name', None)
```

**Off-by-One Errors**
```python
# Bug: Misses last element
for i in range(len(items) - 1):

# Fix: Include last element
for i in range(len(items)):
```

**Resource Leaks**
```python
# Bug: File handle not closed on error
f = open('file.txt')
data = f.read()
f.close()

# Fix: Context manager
with open('file.txt') as f:
    data = f.read()
```

### 2. Async Issues

**Missing await**
```python
# Bug: Returns coroutine, not result
async def get_user():
    return fetch_user(id)  # Missing await!

# Fix
async def get_user():
    return await fetch_user(id)
```

**Blocking in async context**
```python
# Bug: Blocks event loop
async def process():
    time.sleep(1)  # Blocking!

# Fix: Use async sleep
async def process():
    await asyncio.sleep(1)
```

### 3. Logic Errors

**Boolean Expression Bugs**
```python
# Bug: Always True
if x == 1 or 2:

# Fix
if x == 1 or x == 2:
# Or: if x in (1, 2):
```

**Mutable Default Arguments**
```python
# Bug: Shared list across calls
def add_item(item, items=[]):
    items.append(item)
    return items

# Fix: Use None default
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### 4. Type Issues

**Type Coercion Problems**
```javascript
// Bug: String concatenation instead of addition
const total = "5" + 3;  // "53"

// Fix: Explicit conversion
const total = Number("5") + 3;  // 8
```

### 5. Security Issues

**Injection Vulnerabilities**
```python
# Bug: SQL Injection
query = f"SELECT * FROM users WHERE id = {user_id}"

# Fix: Parameterized query
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))
```

## Execution Flow

### Step 1: Identify Targets

```bash
# Default: Changed files
git diff --name-only HEAD~1 | grep -E '\.(py|js|ts|go)$'

# Or scan specific path
$ARGUMENTS
```

### Step 2: Static Analysis

Run available linters:
```bash
# Python
ruff check . --output-format=json 2>/dev/null || pylint --output-format=json . 2>/dev/null

# JavaScript
npx eslint . --format=json 2>/dev/null

# Go
go vet ./... 2>&1
staticcheck ./... 2>/dev/null || true
```

### Step 3: Pattern Matching

Scan for known bug patterns (see categories above)

### Step 4: Categorize & Prioritize

| Priority | Fix Automatically |
|----------|-------------------|
| 🔴 Security bugs | ⚠️ With review |
| 🟠 Logic errors | ⚠️ With review |
| 🟡 Style issues | ✅ Auto-fix |
| 🟢 Minor issues | ✅ Auto-fix |

### Step 5: Apply Fixes

Safe auto-fixes (applied immediately):
- Formatting issues
- Unused imports
- Simple type fixes
- Resource leak fixes (context managers)

Fixes requiring review:
- Logic changes
- Security fixes
- API changes

### Step 6: Verify

```bash
# Run tests to ensure fixes don't break anything
pytest tests/ -x -q
```

## Output

```
🐛 Bug Fix Report
══════════════════════════════════════════════════════════

Scanned: 12 files
Issues Found: 8
Auto-Fixed: 5
Needs Review: 3

## Auto-Fixed ✅

1. src/utils.py:23 - Added missing await
2. src/utils.py:45 - Fixed mutable default argument  
3. src/api.py:12 - Added context manager for file
4. src/models.py:8 - Removed unused import
5. src/models.py:34 - Fixed off-by-one error

## Needs Review ⚠️

1. src/db.py:56 - Potential SQL injection
   Suggested fix shown, please review before applying.
   
2. src/auth.py:23 - Missing null check
   Multiple valid fixes possible.
   
3. src/api.py:89 - Logic error in condition
   Verify business logic is correct.

## Commands

Apply reviewed fixes:
  /fix-bugs --apply src/db.py:56

Skip an issue:
  /fix-bugs --skip src/auth.py:23
══════════════════════════════════════════════════════════
```

## Options

`/fix-bugs` - Scan changed files
`/fix-bugs src/` - Scan specific directory
`/fix-bugs --all` - Scan entire codebase
`/fix-bugs --dry-run` - Report only, no changes
`/fix-bugs --auto` - Auto-fix all safe issues
`/fix-bugs --apply <location>` - Apply specific fix
