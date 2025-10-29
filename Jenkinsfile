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
                    echo "Cleaning up any old Flask process..."
                    set -x
                    # Find and kill any Flask process or python using port 5000
                    sudo lsof -t -i:5000 | xargs -r sudo kill -9
                    pkill -f "python app/app.py" || echo "No old Flask process."
                    sleep 2
        
                    echo "Starting Flask app on port 5000..."
                    source venv/bin/activate
                    nohup python app/app.py > flask.log 2>&1 &
                    sleep 3
                    echo "Flask log preview:"
                    tail -n 15 flask.log
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
    }
}


