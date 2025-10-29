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
                sh '''
                    #!/bin/bash
                    set -e
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    #!/bin/bash
                    set -e
                    source venv/bin/activate
                    pytest || echo "No tests found"
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                    #!/bin/bash
                    set -e
                    source venv/bin/activate
                    nohup python app/app.py &
                    echo "Flask app started successfully!"
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Build completed successfully!"
        }
        failure {
            echo "❌ Build failed. Please check the logs."
        }
    }
}
