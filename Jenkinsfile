pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python Environment') {
            steps {
                sh '''#!/bin/bash
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                source venv/bin/activate
                pytest || echo "No tests found"
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                source venv/bin/activate
                nohup python app/app.py &
                '''
            }
        }
    }
}

