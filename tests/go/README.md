# Go Native Tests

Go's built-in `testing` package. The tests live alongside the source code (Go convention):

```
sample-app/internal/service/service_test.go
```

## Run

```bash
go test -v ./sample-app/internal/service/
```

## Go testing conventions

| Concept | Go | Pytest equivalent |
|---|---|---|
| Test file | `*_test.go` (same package) | `test_*.py` |
| Test function | `func TestXxx(t *testing.T)` | `def test_xxx():` |
| Setup/teardown | `t.Cleanup()` or `TestMain` | `@pytest.fixture` |
| Subtests | `t.Run("name", func(t *testing.T){})` | `@pytest.mark.parametrize` |
| Assertions | `t.Errorf()` / `t.Fatalf()` | `assert` |
| Table-driven | `[]struct{...}` + loop | list of tuples + parametrize |
| Runner | `go test` | `pytest` |

## Key patterns demonstrated

- **`t.Helper()`** — marks a function as a test helper (cleaner stack traces)
- **`t.Cleanup()`** — registers teardown (like a fixture finalizer)
- **`t.Run()`** — subtests for table-driven testing
- **`t.Fatalf()`** — fail and stop immediately
- **`t.Errorf()`** — fail but continue (non-fatal)
- **In-memory SQLite** — fast, isolated test database per test
