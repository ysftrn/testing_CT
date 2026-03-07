package service

import (
	"database/sql"
	"os"
	"testing"

	"github.com/yusuftorun/testing-portfolio/sample-app/internal/repository"

	_ "github.com/mattn/go-sqlite3"
)

// testService creates a Service with a temporary in-memory database.
// This is the Go equivalent of a Pytest fixture.
func testService(t *testing.T) *Service {
	t.Helper()
	db, err := sql.Open("sqlite3", ":memory:")
	if err != nil {
		t.Fatalf("open db: %v", err)
	}
	t.Cleanup(func() { db.Close() })

	repo := repository.New(db)
	if err := repo.InitDB(); err != nil {
		t.Fatalf("init db: %v", err)
	}
	return New(repo)
}

// --- Registration Tests ---

func TestRegister_Success(t *testing.T) {
	svc := testService(t)

	err := svc.Register("testuser", "secure123")
	if err != nil {
		t.Fatalf("expected no error, got: %v", err)
	}
}

func TestRegister_ShortUsername(t *testing.T) {
	svc := testService(t)

	err := svc.Register("ab", "secure123")
	if err == nil {
		t.Fatal("expected error for short username, got nil")
	}
}

func TestRegister_ShortPassword(t *testing.T) {
	svc := testService(t)

	err := svc.Register("testuser", "abc")
	if err == nil {
		t.Fatal("expected error for short password, got nil")
	}
}

func TestRegister_DuplicateUsername(t *testing.T) {
	svc := testService(t)

	err := svc.Register("testuser", "secure123")
	if err != nil {
		t.Fatalf("first registration failed: %v", err)
	}

	err = svc.Register("testuser", "different456")
	if err == nil {
		t.Fatal("expected error for duplicate username, got nil")
	}
}

// --- Login Tests ---

func TestLogin_Success(t *testing.T) {
	svc := testService(t)

	_ = svc.Register("loginuser", "pass123456")

	token, err := svc.Login("loginuser", "pass123456")
	if err != nil {
		t.Fatalf("expected no error, got: %v", err)
	}
	if token == "" {
		t.Fatal("expected non-empty token")
	}
}

func TestLogin_WrongPassword(t *testing.T) {
	svc := testService(t)

	_ = svc.Register("loginuser", "pass123456")

	_, err := svc.Login("loginuser", "wrongpassword")
	if err == nil {
		t.Fatal("expected error for wrong password, got nil")
	}
}

func TestLogin_NonexistentUser(t *testing.T) {
	svc := testService(t)

	_, err := svc.Login("ghostuser", "any123")
	if err == nil {
		t.Fatal("expected error for nonexistent user, got nil")
	}
}

// --- Token Validation Tests ---

func TestValidateToken_Valid(t *testing.T) {
	svc := testService(t)

	_ = svc.Register("tokenuser", "pass123456")
	token, _ := svc.Login("tokenuser", "pass123456")

	userID, err := svc.ValidateToken(token)
	if err != nil {
		t.Fatalf("expected valid token, got error: %v", err)
	}
	if userID == 0 {
		t.Fatal("expected non-zero user ID")
	}
}

func TestValidateToken_Invalid(t *testing.T) {
	svc := testService(t)

	_, err := svc.ValidateToken("fakefakefake")
	if err == nil {
		t.Fatal("expected error for invalid token, got nil")
	}
}

// --- Portfolio Tests ---

func TestAddToPortfolio_Success(t *testing.T) {
	svc := testService(t)

	_ = svc.Register("portfoliouser", "pass123456")
	token, _ := svc.Login("portfoliouser", "pass123456")
	userID, _ := svc.ValidateToken(token)

	item, err := svc.AddToPortfolio(userID, "btc", 1.5)
	if err != nil {
		t.Fatalf("expected no error, got: %v", err)
	}
	if item.Symbol != "BTC" {
		t.Errorf("expected symbol BTC, got %s", item.Symbol)
	}
	if item.Amount != 1.5 {
		t.Errorf("expected amount 1.5, got %f", item.Amount)
	}
}

func TestAddToPortfolio_EmptySymbol(t *testing.T) {
	svc := testService(t)

	_, err := svc.AddToPortfolio(1, "", 1.0)
	if err == nil {
		t.Fatal("expected error for empty symbol, got nil")
	}
}

func TestAddToPortfolio_ZeroAmount(t *testing.T) {
	svc := testService(t)

	_, err := svc.AddToPortfolio(1, "BTC", 0)
	if err == nil {
		t.Fatal("expected error for zero amount, got nil")
	}
}

func TestAddToPortfolio_NegativeAmount(t *testing.T) {
	svc := testService(t)

	_, err := svc.AddToPortfolio(1, "BTC", -5)
	if err == nil {
		t.Fatal("expected error for negative amount, got nil")
	}
}

func TestAddToPortfolio_SymbolUppercase(t *testing.T) {
	svc := testService(t)

	_ = svc.Register("upperuser", "pass123456")
	token, _ := svc.Login("upperuser", "pass123456")
	userID, _ := svc.ValidateToken(token)

	item, err := svc.AddToPortfolio(userID, "eth", 10)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if item.Symbol != "ETH" {
		t.Errorf("expected ETH, got %s", item.Symbol)
	}
}

func TestGetPortfolio_Empty(t *testing.T) {
	svc := testService(t)

	_ = svc.Register("emptyuser", "pass123456")
	token, _ := svc.Login("emptyuser", "pass123456")
	userID, _ := svc.ValidateToken(token)

	items, err := svc.GetPortfolio(userID)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if len(items) != 0 {
		t.Errorf("expected empty portfolio, got %d items", len(items))
	}
}

func TestDeleteFromPortfolio_Success(t *testing.T) {
	svc := testService(t)

	_ = svc.Register("deluser", "pass123456")
	token, _ := svc.Login("deluser", "pass123456")
	userID, _ := svc.ValidateToken(token)

	item, _ := svc.AddToPortfolio(userID, "ADA", 500)
	err := svc.DeleteFromPortfolio(item.ID, userID)
	if err != nil {
		t.Fatalf("expected no error, got: %v", err)
	}

	// Verify it's gone
	items, _ := svc.GetPortfolio(userID)
	for _, i := range items {
		if i.ID == item.ID {
			t.Fatal("item should have been deleted")
		}
	}
}

func TestDeleteFromPortfolio_WrongUser(t *testing.T) {
	svc := testService(t)

	_ = svc.Register("owner", "pass123456")
	_ = svc.Register("attacker", "pass123456")

	tokenOwner, _ := svc.Login("owner", "pass123456")
	tokenAttacker, _ := svc.Login("attacker", "pass123456")

	ownerID, _ := svc.ValidateToken(tokenOwner)
	attackerID, _ := svc.ValidateToken(tokenAttacker)

	item, _ := svc.AddToPortfolio(ownerID, "BTC", 1.0)

	err := svc.DeleteFromPortfolio(item.ID, attackerID)
	if err == nil {
		t.Fatal("expected error when deleting another user's item")
	}
}

// --- Prices Test ---

func TestGetPrices_ReturnsData(t *testing.T) {
	svc := testService(t)

	prices := svc.GetPrices()
	if len(prices) == 0 {
		t.Fatal("expected non-empty prices list")
	}

	// Check BTC exists
	found := false
	for _, p := range prices {
		if p.Symbol == "BTC" {
			found = true
			if p.Price <= 0 {
				t.Errorf("expected positive price for BTC, got %f", p.Price)
			}
		}
	}
	if !found {
		t.Fatal("expected BTC in prices list")
	}
}

// --- Table-Driven Test (Go idiom) ---

func TestRegister_Validation(t *testing.T) {
	// Table-driven tests are the Go convention for testing multiple inputs.
	// Each row is a test case with a name, inputs, and expected result.
	tests := []struct {
		name     string
		username string
		password string
		wantErr  bool
	}{
		{"valid", "gooduser", "secure123", false},
		{"short username", "ab", "secure123", true},
		{"short password", "gooduser", "abc", true},
		{"empty username", "", "secure123", true},
		{"empty password", "gooduser", "", true},
		{"boundary username 3 chars", "abc", "secure123", false},
		{"boundary password 6 chars", "defghi", "abcdef", false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			svc := testService(t)
			err := svc.Register(tt.username, tt.password)
			if (err != nil) != tt.wantErr {
				t.Errorf("Register(%q, %q) error = %v, wantErr = %v",
					tt.username, tt.password, err, tt.wantErr)
			}
		})
	}
}

// TestMain can be used for global setup/teardown.
// Here we just ensure cleanup of any test artifacts.
func TestMain(m *testing.M) {
	code := m.Run()
	os.Exit(code)
}
