pipeline {
    agent any

    environment {
        REPO_DIR = "/home/ubuntu/mydockerapp/APP/mydockerapp"
        APP_SERVER = "ubuntu@3.254.104.246"
        GIT_BRANCH = "APP"
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Deploy to App Server') {
            steps {
                sshagent (credentials: ['jenkins-ssh']) {
                    sh """
                        ssh -o StrictHostKeyChecking=no $APP_SERVER '
                            cd $REPO_DIR &&
                            git reset --hard &&
                            git checkout $GIT_BRANCH &&
                            git pull origin $GIT_BRANCH &&
                            docker-compose down &&
                            docker-compose up -d --build
                        '
                    """
                }
            }
        }
    }
}
