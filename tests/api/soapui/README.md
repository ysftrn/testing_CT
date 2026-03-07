# SoapUI API Testing

## What is SoapUI?

SoapUI is a widely-used API testing tool that supports both **SOAP** and **REST** APIs. It provides:

- GUI-based test creation
- Data-driven testing (load test data from files/databases)
- Assertions and validation
- Mock services
- Load testing (Pro version)

## When to Use SoapUI vs Postman

| Feature | Postman | SoapUI |
|---------|---------|--------|
| REST API testing | Excellent | Good |
| SOAP API testing | Limited | Excellent |
| Data-driven testing | Basic | Advanced |
| Mock services | Limited | Built-in |
| CI/CD integration | Newman (CLI) | testrunner (CLI) |
| Learning curve | Easy | Moderate |
| Enterprise features | Paid plans | SoapUI Pro |

**Use SoapUI when:**
- Testing SOAP/XML-based services (common in enterprise/banking)
- Need advanced data-driven testing
- Need to mock external services during integration testing

**Use Postman when:**
- Testing REST/JSON APIs (most modern applications)
- Quick ad-hoc testing
- Team collaboration on API collections

## Setting Up SoapUI for CryptoTracker

1. Download SoapUI from https://www.soapui.org/
2. Create a new REST project
3. Enter base URL: `http://localhost:8080`
4. Add each endpoint as a REST resource
5. Configure test suites with assertions

## Example Test Suite Structure

```
CryptoTracker REST Project
|-- TestSuite: Authentication
|   |-- TestCase: Registration
|   |   |-- Step: Register User (POST /api/register)
|   |   +-- Assertion: Status 201
|   +-- TestCase: Login
|       |-- Step: Login (POST /api/login)
|       |-- Assertion: Status 200
|       +-- Property Transfer: Extract token
|-- TestSuite: Portfolio
|   |-- TestCase: CRUD Operations
|   |   |-- Step: Add Item (POST /api/portfolio)
|   |   |-- Step: Get Portfolio (GET /api/portfolio)
|   |   +-- Step: Delete Item (DELETE /api/portfolio/{id})
+-- TestSuite: Prices
    +-- TestCase: Get Prices
        |-- Step: Request Prices (GET /api/prices)
        +-- Assertion: Contains BTC
```

## Running from CLI (CI/CD)

```bash
# SoapUI provides a testrunner for CLI execution
testrunner.sh -s "Authentication" -r -f /output CryptoTracker-soapui-project.xml
```

For this portfolio, we focus on Postman (REST) and Python/Pytest (automation). SoapUI knowledge is demonstrated here for completeness, as it remains prevalent in enterprise environments.
