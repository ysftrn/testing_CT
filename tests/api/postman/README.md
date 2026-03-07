# Postman API Tests

## Setup

1. Open Postman
2. Click **Import** and select `CryptoTracker.postman_collection.json`
3. Import the environment: `CryptoTracker.postman_environment.json`
4. Select **CryptoTracker Local** environment from the dropdown

## Running in Postman

- Open the collection and run requests individually, or
- Click **Run Collection** to execute all requests in order

The collection uses **pre-request scripts** to generate unique usernames and **test scripts** to validate responses and chain requests (e.g., login token is saved and reused).

## Running with Newman (CLI)

Newman is Postman's CLI runner, ideal for CI/CD pipelines:

```bash
# Install Newman
npm install -g newman

# Run the collection
newman run CryptoTracker.postman_collection.json -e CryptoTracker.postman_environment.json

# Run with HTML report
npm install -g newman-reporter-html
newman run CryptoTracker.postman_collection.json \
  -e CryptoTracker.postman_environment.json \
  -r html --reporter-html-export report.html
```

## Collection Structure

| Folder | Requests | Tests |
|--------|:--------:|:-----:|
| Health | 1 | 3 |
| Authentication | 6 | 12 |
| Portfolio | 6 | 12 |
| Prices | 1 | 4 |
| **Total** | **14** | **31** |
