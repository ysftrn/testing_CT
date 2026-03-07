/*
 * Jenkins Declarative Pipeline for CryptoTracker.
 *
 * Stages:
 *   1. Checkout       — pull source from Git
 *   2. Build          — compile Go binary
 *   3. Unit Tests     — run Go tests
 *   4. API Tests      — start server, run Pytest
 *   5. SonarQube      — static code analysis
 *   6. Archive        — save binary as build artifact
 *
 * Requirements:
 *   - Jenkins plugins: Pipeline, Git
 *   - SonarQube server configured in Jenkins > Manage > System > SonarQube (optional)
 */

pipeline {
    agent any

    environment {
        GO111MODULE = 'on'
        CGO_ENABLED = '1'
        GOROOT      = "${JENKINS_HOME}/.go"
        GOPATH      = "${JENKINS_HOME}/.gopath"
        GOCACHE     = "${JENKINS_HOME}/.cache/go-build"
        GOMODCACHE  = "${JENKINS_HOME}/.gopath/pkg/mod"
        PATH        = "${JENKINS_HOME}/.go/bin:${JENKINS_HOME}/.gopath/bin:${env.PATH}"
        SONAR_HOST  = 'http://sonarqube:9000'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Go') {
            steps {
                sh '''
                    if [ ! -f "$GOROOT/bin/go" ]; then
                        echo "=== Installing Go ==="
                        mkdir -p "$GOROOT"
                        curl -sL https://go.dev/dl/go1.24.1.linux-amd64.tar.gz -o /tmp/go.tar.gz
                        tar -C "$JENKINS_HOME" -xzf /tmp/go.tar.gz
                        mv "$JENKINS_HOME/go"/* "$GOROOT/"
                        rm -rf "$JENKINS_HOME/go" /tmp/go.tar.gz
                    fi
                    go version
                    gcc --version | head -1
                    python3 --version
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    echo "=== Building CryptoTracker ==="
                    go build -o bin/cryptotracker ./sample-app/cmd/server/
                    ls -la bin/cryptotracker
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    echo "=== Running Go Tests ==="
                    go test -v -coverprofile=coverage.out ./sample-app/internal/service/
                    go tool cover -func=coverage.out
                '''
            }
            post {
                always {
                    // Archive coverage report
                    archiveArtifacts artifacts: 'coverage.out', allowEmptyArchive: true
                }
            }
        }

        stage('API Tests') {
            steps {
                sh '''
                    echo "=== Starting server on port 9090 (8080 is used by Jenkins) ==="
                    PORT=9090 ./bin/cryptotracker &
                    SERVER_PID=$!

                    # Wait for server to be ready
                    for i in $(seq 1 30); do
                        curl -s http://localhost:9090/api/health && break
                        sleep 1
                    done

                    echo "=== Installing Python dependencies ==="
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install -q requests pytest

                    echo "=== Running Pytest API Tests ==="
                    CRYPTOTRACKER_URL=http://localhost:9090 pytest tests/api/python/ -v --tb=short --junitxml=pytest-results.xml

                    echo "=== Running unittest Tests ==="
                    CRYPTOTRACKER_URL=http://localhost:9090 python -m pytest tests/unittest/ -v --tb=short --junitxml=unittest-results.xml

                    # Cleanup
                    kill $SERVER_PID 2>/dev/null || true
                    rm -f cryptotracker.db
                '''
            }
            post {
                always {
                    junit '*-results.xml'
                }
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('SonarQube') {  // Name configured in Jenkins
                    sh '''
                        echo "=== Running SonarQube Scanner ==="
                        sonar-scanner \
                            -Dsonar.projectKey=cryptotracker \
                            -Dsonar.sources=sample-app/ \
                            -Dsonar.tests=sample-app/internal/service/ \
                            -Dsonar.test.inclusions=**/*_test.go \
                            -Dsonar.go.coverage.reportPaths=coverage.out \
                            -Dsonar.python.version=3
                    '''
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Archive') {
            steps {
                archiveArtifacts artifacts: 'bin/cryptotracker', fingerprint: true
            }
        }
    }

    post {
        always {
            // Clean up any leftover server processes
            sh 'pkill -f cryptotracker || true'
            sh 'rm -f cryptotracker.db'
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs above.'
        }
    }
}
