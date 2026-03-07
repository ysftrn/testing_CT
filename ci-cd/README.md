# CI/CD Pipeline

Continuous Integration and Continuous Delivery configuration for CryptoTracker.

## Pipeline Overview

```
Push to Git
    |
    v
+-------------------+
| 1. Checkout       |  Pull source code
+-------------------+
    |
    v
+-------------------+
| 2. Build          |  go build → bin/cryptotracker
+-------------------+
    |
    v
+-------------------+
| 3. Unit Tests     |  go test (25 tests) + coverage report
+-------------------+
    |
    v
+-------------------+
| 4. API Tests      |  Start server → Pytest (42) + unittest (22)
+-------------------+
    |
    v
+-------------------+
| 5. SonarQube      |  Static analysis, code quality gate
+-------------------+
    |
    v
+-------------------+
| 6. Archive        |  Save binary as build artifact
+-------------------+
```

## Tools

| Tool | Purpose | Config File |
|------|---------|-------------|
| **Jenkins** | CI/CD orchestration | `Jenkinsfile` (project root) |
| **GitHub Actions** | CI/CD (GitHub-native) | `.github/workflows/ci.yml` |
| **SonarQube** | Static code analysis | `ci-cd/sonarqube/sonar-project.properties` |
| **Docker Compose** | Run Jenkins + SonarQube | `ci-cd/docker-compose.yml` |

## Live Instances

Jenkins and SonarQube are deployed on a Digital Ocean droplet alongside the CryptoTracker app:

| Service | URL |
|---------|-----|
| **Jenkins** | http://178.128.250.129:8081 |
| **SonarQube** | http://178.128.250.129:9000 (login: admin/admin) |
| **CryptoTracker** | http://178.128.250.129:8080 |

## Quick Start (Docker)

To run locally or on your own server:

```bash
# Start Jenkins + SonarQube
cd ci-cd/
docker compose up -d

# Jenkins:   http://localhost:8081
# SonarQube: http://localhost:9000 (login: admin/admin)
```

### First-time Jenkins setup

1. Get the initial admin password:
   ```bash
   docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
   ```
2. Open http://localhost:8081 (or http://178.128.250.129:8081 for the live server), paste the password
3. Install suggested plugins + Pipeline, Git, SonarQube Scanner
4. Create a Pipeline job pointing to this repo's `Jenkinsfile`

### First-time SonarQube setup

1. Open http://localhost:9000 (or http://178.128.250.129:9000 for the live server), login with admin/admin
2. Change the default password when prompted
3. Create a project: key = `cryptotracker`
4. Generate a token → copy it
5. In Jenkins: Manage Jenkins > System > SonarQube > add server URL + token

## GitHub Actions

The `.github/workflows/ci.yml` runs automatically on push/PR to main. No setup needed — GitHub provides the runners.

What it does:
1. Checks out code
2. Sets up Go 1.22 + Python 3.12
3. Builds the binary
4. Runs Go unit tests with coverage
5. Starts the server, runs Pytest + unittest
6. Uploads test results as artifacts

## Jenkinsfile Explained

```groovy
pipeline {
    agent any                    // Run on any available Jenkins agent

    stages {
        stage('Build') { ... }  // Compile Go binary
        stage('Unit Tests') {   // Go tests + coverage
            post {
                always { archiveArtifacts 'coverage.out' }
            }
        }
        stage('API Tests') {    // Start server, run Pytest
            post {
                always { junit '*-results.xml' }  // Publish test results
            }
        }
        stage('SonarQube') {    // Static analysis
            steps {
                withSonarQubeEnv('SonarQube') { ... }
            }
        }
        stage('Quality Gate') { // Fail if quality gate fails
            steps {
                waitForQualityGate abortPipeline: true
            }
        }
    }
}
```

### Key Jenkins Concepts

| Concept | Description |
|---------|-------------|
| **Declarative Pipeline** | Pipeline-as-code in Groovy DSL (`Jenkinsfile`) |
| **Stage** | A logical phase (Build, Test, Deploy) |
| **Step** | A single action within a stage (`sh`, `junit`, `archiveArtifacts`) |
| **Agent** | The machine/container that runs the pipeline |
| **Post** | Actions after stage/pipeline (always, success, failure) |
| **Tools** | Auto-installed build tools (Go, JDK, Maven) |
| **Environment** | Variables available to all stages |
| **withSonarQubeEnv** | Injects SonarQube server URL and token |
| **waitForQualityGate** | Blocks until SonarQube returns pass/fail |

## SonarQube

### What it analyzes

- **Bugs** — code that is demonstrably wrong
- **Vulnerabilities** — security issues (SQL injection, XSS, etc.)
- **Code smells** — maintainability issues (long methods, complexity)
- **Duplication** — copy-pasted code blocks
- **Coverage** — % of code exercised by tests

### Quality Gate (default)

| Condition | Threshold |
|-----------|-----------|
| New bugs | 0 |
| New vulnerabilities | 0 |
| New code coverage | > 80% |
| Duplication on new code | < 3% |

If any condition fails, the pipeline aborts (Quality Gate stage).

### Running manually

```bash
# Generate Go coverage
go test -coverprofile=coverage.out ./sample-app/internal/service/

# Run scanner (requires sonar-scanner CLI)
sonar-scanner \
    -Dsonar.host.url=http://localhost:9000 \
    -Dsonar.login=<your-token> \
    -Dsonar.projectKey=cryptotracker
```

## Jenkins vs GitHub Actions

| Feature | Jenkins | GitHub Actions |
|---------|---------|----------------|
| Hosting | Self-hosted (your server) | GitHub cloud |
| Config | `Jenkinsfile` (Groovy) | `.yml` files |
| Cost | Free (server cost only) | Free for public repos |
| Plugins | 1800+ plugins | Marketplace actions |
| Flexibility | Full control | Simpler, less control |
| Best for | Enterprise, complex pipelines | Open-source, GitHub repos |

This project includes both to demonstrate knowledge of each approach.
