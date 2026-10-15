pipeline {
    agent any

    options {
        timestamps()
        timeout(time: 15, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    environment {
        IMAGE_NAME     = 'taskboard'
        CONTAINER_NAME = 'taskboard'
        APP_PORT       = '8000'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'git log -1 --pretty=format:"Commit: %h | %s | %an"'
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    python3 -m venv .venv
                    . .venv/bin/activate
                    pip install --quiet -r requirements-dev.txt
                    flake8 app tests
                '''
            }
        }

        stage('Unit tests') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pytest --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Build image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
                sh 'docker images ${IMAGE_NAME}:${BUILD_NUMBER}'
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([string(credentialsId: 'taskboard-database-url', variable: 'DATABASE_URL')]) {
                    sh '''
                        docker rm -f ${CONTAINER_NAME} || true
                        docker run -d --name ${CONTAINER_NAME} --restart unless-stopped \
                            -p ${APP_PORT}:8000 \
                            -e DATABASE_URL="$DATABASE_URL" \
                            ${IMAGE_NAME}:${BUILD_NUMBER}
                    '''
                }
                sh '''
                    for i in $(seq 1 15); do
                        if curl -fsS http://localhost:${APP_PORT}/health; then
                            echo
                            echo "Deployment healthy"
                            exit 0
                        fi
                        sleep 3
                    done
                    echo "App did not become healthy in time"
                    docker logs --tail 50 ${CONTAINER_NAME}
                    exit 1
                '''
                script {
                    currentBuild.description = "Deployed ${IMAGE_NAME}:${BUILD_NUMBER}"
                }
            }
        }
    }

    post {
        success {
            echo "RESULT: SUCCESS | build #${env.BUILD_NUMBER} | image ${env.IMAGE_NAME}:${env.BUILD_NUMBER} is live"
        }
        failure {
            echo "RESULT: FAILED | build #${env.BUILD_NUMBER} | open Stage View to see which stage failed"
        }
        always {
            echo "Build duration: ${currentBuild.durationString}"
        }
    }
}
