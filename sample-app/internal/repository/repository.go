package repository

import (
	"database/sql"
	"fmt"
	"time"

	"github.com/yusuftorun/testing-portfolio/sample-app/internal/models"
)

// Repository handles all database operations.
// In testing terminology, this is our "Data Access Layer" — a common target for integration tests.
type Repository struct {
	db *sql.DB
}

// New creates a new Repository with the given database connection.
func New(db *sql.DB) *Repository {
	return &Repository{db: db}
}

// InitDB creates the required tables if they don't exist.
func (r *Repository) InitDB() error {
	queries := []string{
		`CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT UNIQUE NOT NULL,
			password TEXT NOT NULL,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP
		)`,
		`CREATE TABLE IF NOT EXISTS portfolio_items (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_id INTEGER NOT NULL,
			symbol TEXT NOT NULL,
			amount REAL NOT NULL,
			created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (user_id) REFERENCES users(id)
		)`,
	}

	for _, q := range queries {
		if _, err := r.db.Exec(q); err != nil {
			return fmt.Errorf("init db: %w", err)
		}
	}
	return nil
}

// --- User operations ---

func (r *Repository) CreateUser(username, password string) (*models.User, error) {
	result, err := r.db.Exec(
		"INSERT INTO users (username, password) VALUES (?, ?)",
		username, password,
	)
	if err != nil {
		return nil, fmt.Errorf("create user: %w", err)
	}

	id, _ := result.LastInsertId()
	return &models.User{
		ID:        int(id),
		Username:  username,
		CreatedAt: time.Now(),
	}, nil
}

func (r *Repository) GetUserByUsername(username string) (*models.User, error) {
	user := &models.User{}
	err := r.db.QueryRow(
		"SELECT id, username, password, created_at FROM users WHERE username = ?",
		username,
	).Scan(&user.ID, &user.Username, &user.Password, &user.CreatedAt)
	if err != nil {
		return nil, fmt.Errorf("get user: %w", err)
	}
	return user, nil
}

// --- Portfolio operations ---

func (r *Repository) AddPortfolioItem(userID int, symbol string, amount float64) (*models.PortfolioItem, error) {
	result, err := r.db.Exec(
		"INSERT INTO portfolio_items (user_id, symbol, amount) VALUES (?, ?, ?)",
		userID, symbol, amount,
	)
	if err != nil {
		return nil, fmt.Errorf("add portfolio item: %w", err)
	}

	id, _ := result.LastInsertId()
	return &models.PortfolioItem{
		ID:        int(id),
		UserID:    userID,
		Symbol:    symbol,
		Amount:    amount,
		CreatedAt: time.Now(),
	}, nil
}

func (r *Repository) GetPortfolio(userID int) ([]models.PortfolioItem, error) {
	rows, err := r.db.Query(
		"SELECT id, user_id, symbol, amount, created_at FROM portfolio_items WHERE user_id = ?",
		userID,
	)
	if err != nil {
		return nil, fmt.Errorf("get portfolio: %w", err)
	}
	defer rows.Close()

	var items []models.PortfolioItem
	for rows.Next() {
		var item models.PortfolioItem
		if err := rows.Scan(&item.ID, &item.UserID, &item.Symbol, &item.Amount, &item.CreatedAt); err != nil {
			return nil, fmt.Errorf("scan portfolio item: %w", err)
		}
		items = append(items, item)
	}
	return items, nil
}

func (r *Repository) DeletePortfolioItem(id, userID int) error {
	result, err := r.db.Exec(
		"DELETE FROM portfolio_items WHERE id = ? AND user_id = ?",
		id, userID,
	)
	if err != nil {
		return fmt.Errorf("delete portfolio item: %w", err)
	}

	rows, _ := result.RowsAffected()
	if rows == 0 {
		return fmt.Errorf("item not found")
	}
	return nil
}
