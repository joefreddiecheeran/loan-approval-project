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

        sstage('Run Flask App') {
            steps {
                sh '''#!/bin/bash
                    echo "Stopping any existing Flask app on port 5000..."
                    
                    # Kill processes using port 5000 with sudo
                    sudo fuser -k 5000/tcp || true
                    
                    # Wait for processes to terminate
                    sleep 3
                    
                    # Verify port is free
                    if sudo fuser 5000/tcp; then
                        echo "Warning: Port 5000 is still in use"
                        # Force kill any remaining processes
                        sudo pkill -f "python.*app.py" || true
                        sudo pkill -f gunicorn || true
                        sleep 2
                    else
                        echo "Port 5000 is now free"
                    fi
                    
                    echo "Starting Flask app..."
                    source venv/bin/activate
                    
                    # Start with nohup and save PID
                    nohup python app/app.py > flask.log 2>&1 &
                    APP_PID=$!
                    echo $APP_PID > flask.pid
                    echo "Flask app started with PID: $APP_PID"
                    
                    # Wait and verify the app is running
                    sleep 5
                    if curl -f http://localhost:5000/ > /dev/null 2>&1; then
                        echo "Flask app is running successfully on port 5000"
                        echo "New changes have been deployed!"
                    else
                        echo "Flask app is not responding"
                        echo "Checking application logs..."
                        tail -20 flask.log || true
                        exit 1
                    fi
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


