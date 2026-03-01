---
name: refactor
description: "Safely refactor code with test verification"
---

# Safe Refactoring

Refactor: $ARGUMENTS

## ⚠️ Pre-Refactoring Checklist

Before ANY refactoring:

1. **Verify test coverage exists**
   ```bash
   pytest --cov=$TARGET --cov-fail-under=70 tests/
   ```
   If coverage < 70%, generate tests first with `/test $ARGUMENTS`

2. **Ensure tests pass**
   ```bash
   pytest tests/ -x
   ```
   
3. **Create restore point**
   ```bash
   git stash push -m "pre-refactor-$(date +%s)"
   ```

## Refactoring Patterns

### 1. Extract Function

**When:** Code block is reused or does a distinct thing

```python
# Before
def process_order(order):
    # Validate
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")
    # Process
    ...

# After  
def validate_order(order):
    """Validate order has items and valid total."""
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")

def process_order(order):
    validate_order(order)
    # Process
    ...
```

### 2. Extract Class

**When:** A group of functions operate on the same data

```python
# Before: Functions scattered around
def send_email(to, subject, body): ...
def send_email_with_template(to, template, data): ...
def validate_email(email): ...

# After: Cohesive class
class EmailService:
    def send(self, to, subject, body): ...
    def send_template(self, to, template, data): ...
    def validate(self, email): ...
```

### 3. Simplify Conditionals

**When:** Complex if/else chains

```python
# Before
def get_discount(user):
    if user.is_premium:
        if user.years > 5:
            return 0.25
        else:
            return 0.15
    else:
        if user.years > 5:
            return 0.10
        else:
            return 0.05

# After
DISCOUNT_MATRIX = {
    (True, True): 0.25,   # premium, 5+ years
    (True, False): 0.15,  # premium, <5 years
    (False, True): 0.10,  # standard, 5+ years
    (False, False): 0.05, # standard, <5 years
}

def get_discount(user):
    key = (user.is_premium, user.years > 5)
    return DISCOUNT_MATRIX[key]
```

### 4. Remove Duplication (DRY)

**When:** Same code appears multiple times

```python
# Before
def create_user(data):
    user = User()
    user.name = data['name']
    user.email = data['email']
    user.created_at = datetime.now()
    user.updated_at = datetime.now()
    db.add(user)
    db.commit()
    return user

def update_user(user, data):
    user.name = data['name']
    user.email = data['email']
    user.updated_at = datetime.now()
    db.commit()
    return user

# After
def _apply_user_data(user, data):
    user.name = data['name']
    user.email = data['email']
    user.updated_at = datetime.now()

def create_user(data):
    user = User()
    _apply_user_data(user, data)
    user.created_at = datetime.now()
    db.add(user)
    db.commit()
    return user

def update_user(user, data):
    _apply_user_data(user, data)
    db.commit()
    return user
```

### 5. Dependency Injection

**When:** Hard to test due to tight coupling

```python
# Before: Tight coupling
class OrderService:
    def __init__(self):
        self.db = Database()  # Hard to test!
        self.email = EmailClient()  # Hard to test!

# After: Dependency injection
class OrderService:
    def __init__(self, db: Database, email: EmailClient):
        self.db = db
        self.email = email

# Easy to test with mocks
service = OrderService(mock_db, mock_email)
```

## Execution Flow

### Step 1: Analyze Target
- Read the file/function to refactor
- Identify code smells and opportunities
- Plan the refactoring steps

### Step 2: Verify Safety
- Check test coverage
- Run existing tests
- Create git checkpoint

### Step 3: Incremental Refactoring
- Make ONE small change
- Run tests
- If pass, continue
- If fail, revert and reassess

### Step 4: Final Verification
- Run full test suite
- Check coverage didn't drop
- Review changes

## Output

```
🔧 Refactoring: src/services/order.py
══════════════════════════════════════════════════════════

Pre-flight:
  ✅ Test coverage: 85%
  ✅ All tests passing
  ✅ Git checkpoint created

Refactoring Plan:
  1. Extract validate_order() function
  2. Extract calculate_total() function  
  3. Add dependency injection for EmailService
  4. Simplify discount calculation

Progress:
  ✅ Step 1: Extract validate_order() - tests pass
  ✅ Step 2: Extract calculate_total() - tests pass
  ✅ Step 3: Add DI for EmailService - tests pass
  ✅ Step 4: Simplify discounts - tests pass

Results:
  - Lines of code: 245 → 198 (-19%)
  - Cyclomatic complexity: 12 → 7 (-42%)
  - Test coverage: 85% → 88% (+3%)

Changes:
  M src/services/order.py
  A src/services/validators.py
  M tests/test_order.py

══════════════════════════════════════════════════════════
```

## Options

`/refactor src/file.py` - Refactor specific file
`/refactor src/file.py:function_name` - Refactor specific function
`/refactor --dry-run` - Show plan without changes
`/refactor --aggressive` - More extensive refactoring
`/refactor --preserve-api` - Keep public API unchanged

## Safety Rules

- ✅ Always run tests after each change
- ✅ Make small, incremental changes
- ✅ Preserve public API unless explicitly changing
- ✅ Keep git history clean (atomic commits)
- ❌ Never refactor without test coverage
- ❌ Don't combine refactoring with new features
