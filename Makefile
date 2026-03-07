.PHONY: run build test clean

# Run the server locally
run:
	go run ./sample-app/cmd/server/

# Build the binary
build:
	go build -o bin/cryptotracker ./sample-app/cmd/server/

# Run Go tests
test:
	go test -v ./...

# Clean build artifacts and database
clean:
	rm -f bin/cryptotracker cryptotracker.db
