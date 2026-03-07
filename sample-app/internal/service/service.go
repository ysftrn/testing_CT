package service

import (
	"crypto/rand"
	"encoding/hex"
	"fmt"
	"strings"

	"github.com/yusuftorun/testing-portfolio/sample-app/internal/models"
	"github.com/yusuftorun/testing-portfolio/sample-app/internal/repository"
	"golang.org/x/crypto/bcrypt"
)

// Service contains the business logic for CryptoTracker.
// This layer sits between the HTTP handlers and the repository.
// It's where validation, authentication, and business rules live.
type Service struct {
	repo   *repository.Repository
	tokens map[string]int // token -> userID (simple in-memory token store)
}

// New creates a new Service.
func New(repo *repository.Repository) *Service {
	return &Service{
		repo:   repo,
		tokens: make(map[string]int),
	}
}

// Register creates a new user account.
func (s *Service) Register(username, password string) error {
	if len(username) < 3 {
		return fmt.Errorf("username must be at least 3 characters")
	}
	if len(password) < 6 {
		return fmt.Errorf("password must be at least 6 characters")
	}

	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)
	if err != nil {
		return fmt.Errorf("hash password: %w", err)
	}

	_, err = s.repo.CreateUser(username, string(hashedPassword))
	return err
}

// Login authenticates a user and returns a session token.
func (s *Service) Login(username, password string) (string, error) {
	user, err := s.repo.GetUserByUsername(username)
	if err != nil {
		return "", fmt.Errorf("invalid credentials")
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password)); err != nil {
		return "", fmt.Errorf("invalid credentials")
	}

	token, err := generateToken()
	if err != nil {
		return "", fmt.Errorf("generate token: %w", err)
	}

	s.tokens[token] = user.ID
	return token, nil
}

// ValidateToken checks if a token is valid and returns the associated user ID.
func (s *Service) ValidateToken(token string) (int, error) {
	userID, ok := s.tokens[token]
	if !ok {
		return 0, fmt.Errorf("invalid or expired token")
	}
	return userID, nil
}

// AddToPortfolio adds a crypto holding to the user's portfolio.
func (s *Service) AddToPortfolio(userID int, symbol string, amount float64) (*models.PortfolioItem, error) {
	symbol = strings.ToUpper(strings.TrimSpace(symbol))

	if symbol == "" {
		return nil, fmt.Errorf("symbol is required")
	}
	if amount <= 0 {
		return nil, fmt.Errorf("amount must be positive")
	}

	return s.repo.AddPortfolioItem(userID, symbol, amount)
}

// GetPortfolio returns all portfolio items for a user.
func (s *Service) GetPortfolio(userID int) ([]models.PortfolioItem, error) {
	return s.repo.GetPortfolio(userID)
}

// DeleteFromPortfolio removes a portfolio item.
func (s *Service) DeleteFromPortfolio(itemID, userID int) error {
	return s.repo.DeletePortfolioItem(itemID, userID)
}

// GetPrices returns mock crypto prices.
// In a real app, this would call a crypto exchange API.
func (s *Service) GetPrices() []models.CryptoPrice {
	return []models.CryptoPrice{
		{Symbol: "BTC", Price: 67432.50, Change: 2.3},
		{Symbol: "ETH", Price: 3521.80, Change: -1.1},
		{Symbol: "SOL", Price: 142.65, Change: 5.7},
		{Symbol: "ADA", Price: 0.45, Change: -0.3},
		{Symbol: "DOT", Price: 7.82, Change: 1.8},
	}
}

func generateToken() (string, error) {
	bytes := make([]byte, 32)
	if _, err := rand.Read(bytes); err != nil {
		return "", err
	}
	return hex.EncodeToString(bytes), nil
}
