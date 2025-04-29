pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = 'unique-rarity-456314-h2'
        GCLOUD_PATH = '/var/jenkins_home/google-cloud-sdk/bin'
    }

    stages {

        stage('Cloning Github Repo to Jenkins') {
            steps {
                script {
                    echo 'Cloning Github Repo to Jenkins'
                    checkout scmGit(
                        branches: [[name: '*/main']],
                        extensions: [],
                        userRemoteConfigs: [[
                            credentialsId: 'github-token',
                            url: 'https://github.com/DanielEXT10/Hotel-Reservation.git'
                        ]]
                    )
                }
            }
        }

        stage('Setting up our virtual Environment and Installing dependencies') {
            steps {
                script {
                    echo 'Setting up our virtual Environment and Installing dependencies'
                    sh '''
                        python -m venv ${VENV_DIR}
                        . ${VENV_DIR}/bin/activate
                        pip install --upgrade pip
                        pip install -e .
                    '''
                }
            }
        }

        stage('Building and pushing docker image into GCR') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    script {
                        echo 'Building and pushing docker image into GCR'
                        sh '''
                            export PATH=$PATH:${GCLOUD_PATH}

                            gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                            gcloud config set project ${GCP_PROJECT}
                            gcloud auth configure-docker --quiet

                            docker build -t gcr.io/${GCP_PROJECT}/hotel-reservation:latest .
                            docker push gcr.io/${GCP_PROJECT}/hotel-reservation:latest
                        '''
                    }
                }
            }
        }

    }
     post {
        success {
            echo '🎉 Build and deployment succeeded!'
            // Example: notify via Slack, email, or trigger another job
        }

        failure {
            echo '❌ Build failed.'
            // Example: send alert to email or logging system
        }

        always {
            echo '🧹 Running cleanup...'
            // Example: remove temporary files, Docker containers, etc.
        }

        aborted {
            echo '🚫 Build was aborted by user or system.'
        }

        unstable {
            echo '⚠️ Build is unstable (e.g., test failures).'
        }
    }
}