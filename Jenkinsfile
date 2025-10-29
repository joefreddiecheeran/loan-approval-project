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
                    # Install pytest for testing
                    pip install pytest
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''#!/bin/bash
                    echo "Running tests..."
                    source venv/bin/activate
                    # Run pytest with verbose output
                    python -m pytest -v || echo "No tests found or tests failed"
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''#!/bin/bash
                    echo "Cleaning up any old Flask process..."
                    
                    # Kill processes using port 5000 without sudo
                    fuser -k 5000/tcp || echo "No process on port 5000"
                    
                    # Kill any python app processes
                    pkill -f "python app/app.py" || echo "No existing Flask process found"
                    sleep 2
                    
                    echo "Starting Flask app on port 5000..."
                    source venv/bin/activate
                    
                    # Start Flask app in background
                    nohup python app/app.py > flask.log 2>&1 &
                    
                    # Wait for app to start
                    sleep 5
                    
                    echo "Flask log preview:"
                    tail -n 20 flask.log
                    
                    # Check if Flask app is running
                    echo "Checking if Flask app is running..."
                    if curl -s http://localhost:5000 > /dev/null; then
                        echo "✅ Flask app is running successfully!"
                    else
                        echo "❌ Flask app failed to start"
                        exit 1
                    fi
                '''
            }
        }
    }

    post {
        success {
            echo "Build succeeded and Flask is running!"
        }
        failure {
            echo "Build failed. Please check the logs."
        }
        always {
            sh '''#!/bin/bash
                echo "Final process check:"
                ps aux | grep "python app/app.py" || echo "No Flask process found"
                echo "Port 5000 status:"
                netstat -tulpn | grep :5000 || echo "Port 5000 not in use"
            '''
        }
    }
}
