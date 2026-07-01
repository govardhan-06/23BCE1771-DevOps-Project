pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    triggers {
        // Works even when Jenkins is local and cannot receive a GitHub webhook.
        pollSCM('H/2 * * * *')
    }

    environment {
        IMAGE_NAME = '23bce1771-devops-project'
        IMAGE_TAG = "${BUILD_NUMBER}"
        CONTAINER_NAME = 'portfolio-jenkins-deployment'
        APP_PORT = '8090'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Maven Build') {
            steps {
                sh 'mvn -B clean package'
            }
        }

        stage('Validate Build Output') {
            steps {
                sh '''
                  test -f target/classes/static/index.html
                  test -f target/online-portfolio.jar
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Automated Docker Deployment') {
            steps {
                sh '''
                  docker rm -f ${CONTAINER_NAME} 2>/dev/null || true
                  docker run -d \
                    --name ${CONTAINER_NAME} \
                    --restart unless-stopped \
                    -p ${APP_PORT}:80 \
                    ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                  for attempt in 1 2 3 4 5; do
                    if curl --fail --silent http://localhost:${APP_PORT}/health; then
                      exit 0
                    fi
                    sleep 3
                  done
                  echo "Application health check failed"
                  docker logs ${CONTAINER_NAME} || true
                  exit 1
                '''
            }
        }
    }

    post {
        success {
            echo 'Build, containerization, deployment, and health check completed successfully.'
        }
        always {
            archiveArtifacts artifacts: 'target/*.jar', fingerprint: true, allowEmptyArchive: true
        }
    }
}
