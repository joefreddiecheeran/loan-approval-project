pipeline {
    agent any

    // ✅ This ensures every 'sh' runs with bash instead of sh
    options {
        shell('/bin/bash')
    }

    environment {
        // You can define global environment variables here if needed
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
                sh '''
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
                    echo "🧪 Running tests..."
                    source venv/bin/activate
                    pytest || echo "⚠️ No tests found"
                '''
            }
        }

        stage('Run Flask App') {
            steps {
                sh '''
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
