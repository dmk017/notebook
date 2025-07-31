pipeline {
    agent any
    
    environment {
        DOCKER_COMPOSE_FILE = 'docker-compose.dev.yml'
        FRONTEND_DIR = 'apps/fb/web'
    }

    parameters {
        booleanParam(name: 'DEPLOY_FB_WEB', defaultValue: true, description: 'Deploy fb-web')
        booleanParam(name: 'DEPLOY_FB_API', defaultValue: true, description: 'Deploy fb-api')
        booleanParam(name: 'DEPLOY_FB_BOT', defaultValue: true, description: 'Deploy fb-bot')
    }

    stages {
        stage("Start...") {
            steps {
                git branch: "dev", credentialsId: '4tuna', url: 'https://gitlab.com/billysmalldefend/fortuna.git'
            }
        }
        stage("Build...") {
            steps {
                sh 'docker ps'
                sh 'docker network ls'
                script {
                    def networkId = sh(script: "docker network ls | grep fb-web | tr -s ' ' | cut -d ' ' -f 1", returnStdout: true).trim()
                    def containerId = sh(script: "docker ps | grep fb-api | tr -s ' ' | cut -d ' ' -f 1", returnStdout: true).trim()
        
                    echo "NETWORK ID: ${networkId}"
                    echo "CONTAINER ID: ${containerId}"
                }
            }
        }
        stage('Testing...') {
            steps {
                sh '''
                    cd ./services/fb
                    ./run-test.sh
                '''
            }
        }
        stage("Deploy fb-web") {
            when {
                expression { params.DEPLOY_FB_WEB }
            }
            steps {
                sh 'docker compose down fb-web'
                sh 'docker compose up fb-web -d'
            }
        }
        stage("Deploy fb-api") {
            when {
                expression { params.DEPLOY_FB_API }
            }
            steps {
                sh 'docker compose down fb-api'
                sh 'docker compose up fb-api -d'
            }
        }
        stage("Deploy fb-bot") {
            when {
                expression { params.DEPLOY_FB_BOT }
            }
            steps {
                sh 'docker compose down fb-bot'
                sh 'docker compose up fb-bot -d'
            }
        }
        stage("Adding containers to the same network") {
            steps {
                sh 'docker ps -a'
                sh 'docker network ls'
                script {
                    def networkId = sh(script: "docker network ls | grep fb-web | tr -s ' ' | cut -d ' ' -f 1", returnStdout: true).trim()
                    def containerId = sh(script: "docker ps -a | grep fortuna-fb-api | tr -s ' ' | cut -d ' ' -f 1", returnStdout: true).trim()
        
                    echo "NETWORK ID: ${networkId}"
                    echo "CONTAINER ID: ${containerId}"

                    sh "docker network connect ${networkId} ${containerId}"
                }
            }
        }
    }
}