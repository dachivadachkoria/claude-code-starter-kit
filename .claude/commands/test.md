---
name: test
description: "Generate comprehensive unit tests for files. Use /test <file> or /test --changed"
---

# Unit Test Generation

Generate comprehensive unit tests for: $ARGUMENTS

## Execution Flow

### Step 1: Determine Target Files

**If `$ARGUMENTS` contains a file path:**
- Test that specific file

**If `$ARGUMENTS` is `--changed` or empty:**
- Run: `git diff --name-only HEAD~1 | grep -E '\.(py|js|ts|go)$'`
- Test all changed source files

**If `$ARGUMENTS` is `--staged`:**
- Run: `git diff --cached --name-only | grep -E '\.(py|js|ts|go)$'`
- Test all staged files

### Step 2: Analyze Source Code

For each target file:
1. Read the entire file
2. Identify all public functions/methods/classes
3. Note dependencies and imports
4. Check for existing tests

### Step 3: Generate Tests

For each function/method, create tests for:

**Happy Path**
- Normal inputs → expected outputs
- Multiple valid input variations

**Edge Cases**
- Empty inputs (null, empty string, empty array)
- Boundary values (0, -1, MAX_INT)
- Single element collections

**Error Handling**
- Invalid inputs
- Exception scenarios
- Network/IO failures (mocked)

**Async Behavior** (if applicable)
- Successful async operations
- Timeout handling
- Concurrent execution

### Step 4: Apply Project Conventions

Read `CLAUDE.md` and existing tests to match:
- Naming conventions
- File structure
- Assertion style
- Mocking patterns
- Fixture usage

### Step 5: Write and Verify

1. Create test file in appropriate location
2. Run the new tests
3. Fix any failures
4. Report coverage delta

## Output Format

```
📁 Generated: tests/test_<module>.py
✅ Tests: 12 passed
📊 Coverage: 87% (+15%)
```

## Language-Specific Patterns

### Python (pytest)
```python
import pytest
from unittest.mock import Mock, patch

class TestClassName:
    def test_method_success_returns_expected(self):
        # Arrange
        ...
        # Act
        result = function_under_test(input)
        # Assert
        assert result == expected
```

### JavaScript/TypeScript (jest)
```typescript
describe('ClassName', () => {
  describe('methodName', () => {
    it('should return expected when given valid input', () => {
      // Arrange
      ...
      // Act
      const result = functionUnderTest(input);
      // Assert
      expect(result).toEqual(expected);
    });
  });
});
```

### Go
```go
func TestFunctionName_Scenario_ExpectedBehavior(t *testing.T) {
    // Arrange
    ...
    // Act
    result := FunctionUnderTest(input)
    // Assert
    assert.Equal(t, expected, result)
}
```

## Important Guidelines

- ✅ Use existing fixtures from conftest.py / setupTests.js
- ✅ Mock all external dependencies (APIs, DB, cache)
- ✅ Each test should test ONE thing
- ✅ Tests must be deterministic (no random, no time-dependent)
- ❌ Don't test private/internal implementation details
- ❌ Don't mock the code under test
- ❌ Don't create tests that just verify mocks were called
