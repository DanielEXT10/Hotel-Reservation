pipeline {
    agent any

    environment {
        VENV_DIR ='venv'
    }


    stages {
        stage('Cloning Github Repo to Jenkins'){
            steps{
                script{
                    echo 'Cloning Github Repo to Jenkins'
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/DanielEXT10/Hotel-Reservation.git']])
                }

            }
        }

        stage('Setting up our virtual Environment and Installing dependencies'){
            steps{
                script{
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
    }
}