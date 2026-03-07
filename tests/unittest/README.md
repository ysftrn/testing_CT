# Python unittest Tests

Python's built-in test framework. These tests cover the same CryptoTracker API as the Pytest tests in `tests/api/python/`, but use `unittest.TestCase` style.

## Run

```bash
# Requires the server running on localhost:8080
python -m unittest tests/unittest/test_service.py -v

# Or run with pytest (pytest can discover unittest-style tests too)
pytest tests/unittest/test_service.py -v
```

## unittest vs Pytest comparison

| Feature | unittest | Pytest |
|---|---|---|
| Assertions | `self.assertEqual(a, b)` | `assert a == b` |
| Setup | `setUp()` / `tearDown()` methods | `@pytest.fixture` |
| Test discovery | Class-based, `test_` prefix | Function or class, `test_` prefix |
| Subtests | `self.subTest()` | `@pytest.mark.parametrize` |
| Output | Basic | Rich diffs, colors |
| Plugins | Limited | Huge ecosystem |
| Built-in | Yes (stdlib) | Requires `pip install` |

## Key patterns demonstrated

- **`unittest.TestCase`** — all tests inherit from this base class
- **`setUp()`** — runs before each test (like a per-test fixture)
- **`self.assert*()`** — assertion methods (`assertEqual`, `assertIn`, `assertNotEqual`, etc.)
- **`subTest()`** — table-driven tests, equivalent to Go's `t.Run()`
- **`if __name__ == "__main__"`** — allows running with `python test_service.py`
