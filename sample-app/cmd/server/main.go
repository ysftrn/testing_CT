package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/yusuftorun/testing-portfolio/sample-app/internal/handlers"
	"github.com/yusuftorun/testing-portfolio/sample-app/internal/repository"
	"github.com/yusuftorun/testing-portfolio/sample-app/internal/service"

	_ "github.com/mattn/go-sqlite3" // SQLite driver
)

func main() {
	// Determine port (default 8080, or from environment variable)
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	// Open SQLite database
	db, err := sql.Open("sqlite3", "./cryptotracker.db")
	if err != nil {
		log.Fatalf("Failed to open database: %v", err)
	}
	defer db.Close()

	// Initialize layers: Repository -> Service -> Handlers
	// This is a common pattern called "layered architecture" or "clean architecture"
	repo := repository.New(db)
	if err := repo.InitDB(); err != nil {
		log.Fatalf("Failed to initialize database: %v", err)
	}

	svc := service.New(repo)
	handler := handlers.New(svc)

	// Register routes
	mux := http.NewServeMux()
	handler.RegisterRoutes(mux)

	// Start server
	addr := fmt.Sprintf(":%s", port)
	log.Printf("CryptoTracker server starting on http://localhost%s", addr)
	if err := http.ListenAndServe(addr, mux); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}
