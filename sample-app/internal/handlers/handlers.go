package handlers

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strconv"
	"strings"

	"github.com/yusuftorun/testing-portfolio/sample-app/internal/models"
	"github.com/yusuftorun/testing-portfolio/sample-app/internal/service"
)

// Handler holds all HTTP handler functions.
// Each method corresponds to an API endpoint that we'll test.
type Handler struct {
	svc *service.Service
}

// New creates a new Handler.
func New(svc *service.Service) *Handler {
	return &Handler{svc: svc}
}

// RegisterRoutes sets up all API routes.
func (h *Handler) RegisterRoutes(mux *http.ServeMux) {
	mux.HandleFunc("POST /api/register", h.Register)
	mux.HandleFunc("POST /api/login", h.Login)
	mux.HandleFunc("GET /api/portfolio", h.GetPortfolio)
	mux.HandleFunc("POST /api/portfolio", h.AddPortfolio)
	mux.HandleFunc("DELETE /api/portfolio/{id}", h.DeletePortfolio)
	mux.HandleFunc("GET /api/prices", h.GetPrices)
	mux.HandleFunc("GET /api/health", h.HealthCheck)

	// Serve static files for the web frontend
	mux.Handle("GET /", http.FileServer(http.Dir("sample-app/web")))
}

// HealthCheck is a simple endpoint to verify the server is running.
// This is the first thing smoke tests check.
func (h *Handler) HealthCheck(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, map[string]string{
		"status": "healthy",
		"app":    "CryptoTracker",
	})
}

func (h *Handler) Register(w http.ResponseWriter, r *http.Request) {
	var req models.RegisterRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, models.ErrorResponse{Error: "invalid request body"})
		return
	}

	if err := h.svc.Register(req.Username, req.Password); err != nil {
		writeJSON(w, http.StatusBadRequest, models.ErrorResponse{Error: err.Error()})
		return
	}

	writeJSON(w, http.StatusCreated, models.SuccessResponse{Message: "user registered successfully"})
}

func (h *Handler) Login(w http.ResponseWriter, r *http.Request) {
	var req models.LoginRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, models.ErrorResponse{Error: "invalid request body"})
		return
	}

	token, err := h.svc.Login(req.Username, req.Password)
	if err != nil {
		writeJSON(w, http.StatusUnauthorized, models.ErrorResponse{Error: err.Error()})
		return
	}

	writeJSON(w, http.StatusOK, models.LoginResponse{Token: token, Message: "login successful"})
}

func (h *Handler) GetPortfolio(w http.ResponseWriter, r *http.Request) {
	userID, err := h.authenticate(r)
	if err != nil {
		writeJSON(w, http.StatusUnauthorized, models.ErrorResponse{Error: err.Error()})
		return
	}

	items, err := h.svc.GetPortfolio(userID)
	if err != nil {
		writeJSON(w, http.StatusInternalServerError, models.ErrorResponse{Error: "failed to get portfolio"})
		return
	}

	if items == nil {
		items = []models.PortfolioItem{}
	}
	writeJSON(w, http.StatusOK, items)
}

func (h *Handler) AddPortfolio(w http.ResponseWriter, r *http.Request) {
	userID, err := h.authenticate(r)
	if err != nil {
		writeJSON(w, http.StatusUnauthorized, models.ErrorResponse{Error: err.Error()})
		return
	}

	var req models.AddPortfolioRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		writeJSON(w, http.StatusBadRequest, models.ErrorResponse{Error: "invalid request body"})
		return
	}

	item, err := h.svc.AddToPortfolio(userID, req.Symbol, req.Amount)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, models.ErrorResponse{Error: err.Error()})
		return
	}

	writeJSON(w, http.StatusCreated, item)
}

func (h *Handler) DeletePortfolio(w http.ResponseWriter, r *http.Request) {
	userID, err := h.authenticate(r)
	if err != nil {
		writeJSON(w, http.StatusUnauthorized, models.ErrorResponse{Error: err.Error()})
		return
	}

	idStr := r.PathValue("id")
	id, err := strconv.Atoi(idStr)
	if err != nil {
		writeJSON(w, http.StatusBadRequest, models.ErrorResponse{Error: "invalid item id"})
		return
	}

	if err := h.svc.DeleteFromPortfolio(id, userID); err != nil {
		writeJSON(w, http.StatusNotFound, models.ErrorResponse{Error: err.Error()})
		return
	}

	writeJSON(w, http.StatusOK, models.SuccessResponse{Message: "item deleted"})
}

func (h *Handler) GetPrices(w http.ResponseWriter, r *http.Request) {
	prices := h.svc.GetPrices()
	writeJSON(w, http.StatusOK, prices)
}

// --- Helper functions ---

// authenticate extracts the Bearer token from the Authorization header
// and validates it. Returns the user ID if valid.
func (h *Handler) authenticate(r *http.Request) (int, error) {
	auth := r.Header.Get("Authorization")
	if auth == "" {
		return 0, fmt.Errorf("authorization header required")
	}

	token := strings.TrimPrefix(auth, "Bearer ")
	return h.svc.ValidateToken(token)
}

func writeJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}
