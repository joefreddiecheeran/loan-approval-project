pipeline {
    agent any

    environment {
        // Define variables. These should be configured as credentials in Jenkins.
        AZURE_CREDENTIALS_ID = 'your-azure-credentials-id' // The ID of your Azure Service Principal credential in Jenkins
        RESOURCE_GROUP = 'rg-loanapp-dev' // Must match what Terraform creates
        WEB_APP_NAME = '' // This will be set dynamically by Terraform
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Get code from your Git repository
                checkout scm
            }
        }

        stage('Build & Prepare Artifact') {
            steps {
                script {
                    echo "Creating deployment artifact..."
                    // Create a zip file containing only the application code
                    // Exclude files not needed for deployment
                    zip zipFile: 'artifact.zip', dir: 'app', archive: true
                    
                    // Stash the artifact to use in a later stage
                    stash name: 'app-artifact', includes: 'artifact.zip'
                }
            }
        }

        stage('Terraform Provision') {
            steps {
                dir('terraform') {
                    script {
                        // Use Azure credentials configured in Jenkins
                        withCredentials([azureServicePrincipal(credentialsId: AZURE_CREDENTIALS_ID,
                                                               subscriptionId: env.AZURE_SUBSCRIPTION_ID, // Jenkins global variable
                                                               tenantId: env.AZURE_TENANT_ID)]) { // Jenkins global variable
                            
                            echo "Initializing Terraform..."
                            sh 'terraform init -input=false'

                            echo "Planning infrastructure changes..."
                            sh 'terraform plan -out=tfplan -input=false'

                            // Optional: Add a manual approval step before applying
                            // input "Apply infrastructure changes?"

                            echo "Applying Terraform plan..."
                            sh 'terraform apply -auto-approve tfplan'

                            // Capture the web app name from Terraform output for the deploy stage
                            env.WEB_APP_NAME = sh(script: "terraform output -raw web_app_name", returnStdout: true).trim()
                            echo "Azure Web App Name: ${env.WEB_APP_NAME}"
                        }
                    }
                }
            }
        }
        
        stage('Deploy to Azure Web App') {
            steps {
                script {
                    // Retrieve the artifact from the build stage
                    unstash 'app-artifact'
                    
                    withCredentials([azureServicePrincipal(credentialsId: AZURE_CREDENTIALS_ID,
                                                               subscriptionId: env.AZURE_SUBSCRIPTION_ID,
                                                               tenantId: env.AZURE_TENANT_ID)]) {
                        
                        echo "Deploying artifact.zip to ${env.WEB_APP_NAME}..."
                        // Use the Azure CLI to deploy the zipped artifact
                        sh "az webapp deploy --resource-group ${env.RESOURCE_GROUP} --name ${env.WEB_APP_NAME} --src-path artifact.zip --type zip"
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Clean up workspace
            cleanWs()
            deleteDir()
        }
    }
}