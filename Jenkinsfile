pipeline {
    agent any

    environment {
        DOCKER_BUILDKIT = '1'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Generate .env') {
            steps {
                withCredentials([
                    string(credentialsId: 'budget-api-db-host', variable: 'DB_HOST'),
                    string(credentialsId: 'budget-api-db-user', variable: 'DB_USER'),
                    string(credentialsId: 'budget-api-db-password', variable: 'DB_PASSWORD'),
                    string(credentialsId: 'budget-api-db-port', variable: 'DB_PORT'),
                    string(credentialsId: 'budget-api-db-name', variable: 'DB_NAME'),
                    string(credentialsId: 'budget-api-jwt-secret', variable: 'JWT_SECRET_KEY'),
                    string(credentialsId: 'budget-api-jwt-algorithm', variable: 'JWT_ALGORITHM'),
                    string(credentialsId: 'budget-api-jwt-expiration', variable: 'JWT_EXPIRATION_MINUTES'),
                    string(credentialsId: 'budget-api-url-cors', variable: 'URL_CORS'),
                    string(credentialsId: 'budget-api-asaas-key', variable: 'ASAAS_API_KEY'),
                    string(credentialsId: 'budget-api-asaas-env', variable: 'ASAAS_ENVIRONMENT')
                ]) {
                    writeFile file: '.env', text: """
DB_HOST='${DB_HOST}'
DB_USER='${DB_USER}'
DB_PASSWORD='${DB_PASSWORD}'
DB_PORT='${DB_PORT}'
DB_NAME='${DB_NAME}'
DATABASE_URL='mysql+aiomysql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}'
JWT_SECRET_KEY='${JWT_SECRET_KEY}'
JWT_ALGORITHM='${JWT_ALGORITHM}'
JWT_EXPIRATION_MINUTES='${JWT_EXPIRATION_MINUTES}'
URL_CORS='${URL_CORS}'
ASAAS_API_KEY='${ASAAS_API_KEY}'
ASAAS_ENVIRONMENT='${ASAAS_ENVIRONMENT}'
"""
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t budget-api:latest .'
            }
        }

        stage('Tests') {
            steps {
                sh """
                    mkdir -p reports
                    docker run --rm -v ${WORKSPACE}:/app -w /app budget-api:latest \
                    sh -c "ls -R /app && pytest budget-api/tests -v --cov=app --cov-report=xml --junitxml=reports/junit.xml"
                """
            }
            post {
                always {
                    junit 'reports/junit.xml'
                    publishHTML(target: [
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }

        stage('Deploy') {
            steps {
                sh 'docker compose down'
                sh 'docker compose up -d'
            }
        }

        stage('Cleanup') {
            steps {
                sh 'rm -f .env'
            }
        }
    }

    post {
        failure {
            sh 'rm -f .env'
        }
    }
}