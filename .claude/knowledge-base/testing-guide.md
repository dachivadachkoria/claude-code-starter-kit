# Testing Guide

This guide documents the testing philosophy and patterns for this project.

## Testing Pyramid

```
         /\
        /  \        E2E Tests (few)
       /----\       - Critical user flows
      /      \      - Slow, expensive
     /--------\     Integration Tests (some)
    /          \    - API endpoints
   /------------\   - Database operations
  /              \  Unit Tests (many)
 /----------------\ - Fast, isolated
                    - Core logic
```

## Unit Testing

### Principles

1. **Fast** - Each test < 100ms
2. **Isolated** - No external dependencies
3. **Repeatable** - Same result every time
4. **Self-validating** - Pass or fail, no manual inspection
5. **Timely** - Written alongside code

### Structure (AAA Pattern)

```python
def test_calculate_discount_premium_user_gets_twenty_percent():
    # Arrange - Set up test data
    user = User(tier="premium", years_active=3)
    order = Order(total=100.00)
    
    # Act - Execute the code under test
    discount = calculate_discount(user, order)
    
    # Assert - Verify the result
    assert discount == 20.00
```

### Naming Convention

```
test_<function>_<scenario>_<expected_result>

Examples:
- test_login_valid_credentials_returns_token
- test_login_invalid_password_raises_auth_error
- test_calculate_total_empty_cart_returns_zero
```

### What to Test

✅ **DO Test:**
- Public functions and methods
- Business logic
- Edge cases (empty, null, boundary values)
- Error handling
- State changes

❌ **DON'T Test:**
- Private implementation details
- Simple getters/setters
- Third-party library code
- Configuration loading

## Mocking

### When to Mock

Mock external dependencies:
- HTTP APIs
- Databases
- File systems
- Time/dates
- Random number generation
- Email/SMS services

### Mock Examples

```python
# Python with pytest-mock
def test_sends_notification(mocker):
    mock_email = mocker.patch('services.email.send')
    
    create_order(order_data)
    
    mock_email.assert_called_once()


# Python with responses (HTTP mocking)
@responses.activate
def test_fetches_weather():
    responses.add(
        responses.GET,
        "https://api.weather.com/current",
        json={"temp": 72, "unit": "F"},
        status=200
    )
    
    result = get_weather("NYC")
    
    assert result["temp"] == 72
```

### Anti-Patterns

❌ **Don't mock the thing you're testing:**
```python
# BAD - Testing nothing!
def test_user_service(mocker):
    mocker.patch.object(UserService, 'create_user', return_value=User())
    result = UserService().create_user(data)  # Testing the mock!
```

❌ **Don't verify mock calls without behavior:**
```python
# BAD - What does this actually test?
def test_process_order(mock_db):
    process_order(order)
    mock_db.save.assert_called()  # So what?
```

## Fixtures

### Shared Test Data

```python
# conftest.py
import pytest

@pytest.fixture
def sample_user():
    return User(
        id=1,
        email="test@example.com",
        name="Test User"
    )

@pytest.fixture
def authenticated_client(client, sample_user):
    token = create_token(sample_user)
    client.headers["Authorization"] = f"Bearer {token}"
    return client
```

### Fixture Scopes

```python
@pytest.fixture(scope="session")
def database():
    """Created once per test session."""
    db = setup_test_database()
    yield db
    db.teardown()

@pytest.fixture(scope="function")  # Default
def clean_state(database):
    """Fresh state for each test."""
    database.clear_all()
    yield
    database.clear_all()
```

## Parameterized Tests

```python
@pytest.mark.parametrize("input,expected", [
    (0, "zero"),
    (1, "one"),
    (-1, "negative"),
    (100, "hundred"),
])
def test_number_to_word(input, expected):
    assert number_to_word(input) == expected
```

## Async Testing

```python
import pytest

@pytest.mark.asyncio
async def test_fetch_user_async():
    result = await fetch_user(user_id=123)
    assert result.id == 123

# With async fixtures
@pytest.fixture
async def async_client():
    async with AsyncClient() as client:
        yield client
```

## Coverage

### Running Coverage

```bash
# Python
pytest --cov=src --cov-report=html --cov-fail-under=80

# JavaScript
npm test -- --coverage --coverageThreshold='{"global":{"lines":80}}'

# Go
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

### Coverage Goals

| Category | Target | Minimum |
|----------|--------|---------|
| Overall | 80% | 70% |
| New code | 90% | 80% |
| Critical paths | 95% | 90% |

### What Coverage Doesn't Tell You

- Quality of assertions
- Meaningful test scenarios
- Edge case coverage
- Error handling adequacy

## Test Organization

```
tests/
├── conftest.py          # Shared fixtures
├── unit/                # Unit tests
│   ├── test_auth.py
│   └── test_users.py
├── integration/         # Integration tests
│   └── test_api.py
└── e2e/                 # End-to-end tests
    └── test_flows.py
```

## CI Integration

```yaml
# Run tests on every push
test:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Run tests
      run: pytest --cov --cov-fail-under=80
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```
