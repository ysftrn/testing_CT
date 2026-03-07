package models

import "time"

// User represents a registered user in the system.
type User struct {
	ID        int       `json:"id"`
	Username  string    `json:"username"`
	Password  string    `json:"-"` // "-" means this field is NEVER included in JSON responses (security)
	CreatedAt time.Time `json:"created_at"`
}

// PortfolioItem represents a cryptocurrency holding in a user's portfolio.
type PortfolioItem struct {
	ID        int       `json:"id"`
	UserID    int       `json:"user_id"`
	Symbol    string    `json:"symbol"`    // e.g. "BTC", "ETH"
	Amount    float64   `json:"amount"`    // how much they hold
	CreatedAt time.Time `json:"created_at"`
}

// CryptoPrice represents the current price of a cryptocurrency.
type CryptoPrice struct {
	Symbol string  `json:"symbol"`
	Price  float64 `json:"price"`
	Change float64 `json:"change_24h"` // 24h change percentage
}

// --- Request/Response types ---

type RegisterRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

type LoginRequest struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

type LoginResponse struct {
	Token   string `json:"token"`
	Message string `json:"message"`
}

type AddPortfolioRequest struct {
	Symbol string  `json:"symbol"`
	Amount float64 `json:"amount"`
}

type ErrorResponse struct {
	Error string `json:"error"`
}

type SuccessResponse struct {
	Message string `json:"message"`
}
