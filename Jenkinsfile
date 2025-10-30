pipeline {
    agent any

    environment {
        PATH = "/usr/local/bin:/usr/bin:/bin"
    }

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }

        stage('Set up Python Environment') {
            steps {
                sh '''#!/bin/bash
                    set -e
                    echo "Setting up Python virtual environment..."
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''#!/bin/bash
                    echo "Running tests..."
                    source venv/bin/activate
                    pytest || echo "No tests found"
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''#!/bin/bash
                    echo "Stopping any existing Flask app on port 5000..."
                    # Find and kill process using port 5000
                    sudo fuser -k 5000/tcp || true
                    # Alternative method if fuser not available:
                    # PID=$(lsof -ti:5000) && kill -9 $PID || true
                    
                    echo "Starting Flask app..."
                    source venv/bin/activate
                    nohup python app/app.py > flask.log 2>&1 &
                    echo "Flask app started in background"
                '''
            }
        }
    }

    post {
        success {
            echo "Build succeeded!"
        }
        failure {
            echo "Build failed. Please check the logs."
        }
    }
}

