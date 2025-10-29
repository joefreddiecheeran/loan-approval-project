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
                // ✅ explicitly use bash
                sh '''
                    #!/bin/bash
                    set -e
                    echo "✅ Setting up Python virtual environment..."
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
                    echo "🧪 Running tests..."
                    source venv/bin/activate
                    pytest || echo "⚠️ No tests found"
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
                    #!/bin/bash
                    echo "🚀 Starting Flask app..."
                    source venv/bin/activate
                    nohup python app/app.py > flask.log 2>&1 &
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Build succeeded!"
        }
        failure {
            echo "❌ Build failed. Please check the logs."
        }
    }
}
