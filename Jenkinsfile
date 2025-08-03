pipeline {
    agent any

    stages {
        stage('Load Credentials') {
            steps {
                echo 'Loading environment variables and SSH key from Jenkins credentials'
                withCredentials([
                    file(credentialsId: 'JEC_ENV_FILE', variable: 'ENV_FILE'),
                    file(credentialsId: 'JEC_GCP_FILE', variable: 'GCP_FILE'),
                    file(credentialsId: 'JEC_SSH_FILE', variable: 'SSH_FILE')
                ]) {
                    sh 'cp "$ENV_FILE" "$WORKSPACE/.env"'
                    sh 'cp "$GCP_FILE" "$WORKSPACE/gcp_key.json"'
                    sh 'cp "$SSH_FILE" "$WORKSPACE/id_ed25519"'
                    sh 'chmod 600 "$WORKSPACE/id_ed25519"'
                }
            }
        }

        stage('Environment Check') {
            steps {
                echo 'Version check: python3'
                sh 'python3 --version'
                echo 'Version check: gradle'
                sh 'gradle --version'
                echo 'Version check: maven'
                sh 'mvn -version'
                echo 'Version check: node'
                sh 'node --version'
            }
        }

        stage('Build Java Services') {
            parallel {
                stage('Account Service') {
                    steps {
                        dir('Backend/Workspace/Service_Account/Service_Account_Backend') {
                            sh 'chmod +x ./gradlew'
                            sh './gradlew clean build -x test'
                        }
                    }
                }
                stage('Manager Service') {
                    steps {
                        dir('Backend/Workspace/Service_Manager') {
                            sh 'chmod +x ./mvnw'
                            sh './mvnw clean install -DskipTests'
                        }
                    }
                }
                stage('Catalog Service') {
                    steps {
                        dir('Backend/Workspace/Service_Catalog/Service_Catalog_Backend') {
                            sh 'chmod +x ./gradlew'
                            sh './gradlew clean build -x test'
                        }
                    }
                }
            }
        }

        stage('Build Node Services') {
            parallel {
                stage('API Gateway') {
                    steps {
                        dir('Backend/Workspace/API_Gateway/api-gateway') {
                            echo 'This service doesn not need to be built'
                        }
                    }
                }
                stage('Cart Order Service') {
                    steps {
                        dir('Backend/Workspace/Service_Cart_Order/Service_Cart_Order_Backend') {
                            echo 'This service doesn not need to be built'
                        }
                    }
                }
            }
        }

        stage('Build Python Services') {
            steps {
                dir('Backend/Workspace/Service_Chatbot/Service_Chatbot_Python') {
                    echo 'This service doesn not need to be built'
                }
            }
        }

        stage('Build Frontend') {
            parallel {
                stage('Container') {
                    steps {
                        dir('Frontend/Workspace/Container/container-vite') {
                            sh '''
                                npm install
                                npm run build
                            '''
                        }
                    }
                }
                stage('Frontend Services') {
                    steps {
                        script {
                            def frontendServices = [
                                'Service_Account/service-account-vite',
                                'Service_Manager/service-manager-vite',
                                'Service_Catalog/service-catalog-vite',
                                'Service_Cart_Order/service-cart-order-vite'
                            ]

                            frontendServices.each { service ->
                                dir("Frontend/Workspace/${service}") {
                                    sh '''
                                        npm install
                                        npm run build
                                    '''
                                }
                            }
                        }
                    }
                }
            }
        }

        stage('Deploy to VM') {
            steps {
                echo 'Deploying to GCP VM at 34.9.78.197'
                sh '''
                    set +x
                    # Load environment variables
                    set -a
                    cat "$WORKSPACE/.env" | tr -d '\r' | sed 's/[[:space:]]*$//' > "$WORKSPACE/.env.clean"
                    . "$WORKSPACE/.env.clean"
                    set +a

                    # SSH connection details
                    VM_HOST="${VITE_BACKEND_HOST}"
                    SSH_USER="ray"
                    SSH_KEY="$WORKSPACE/id_ed25519"

                    echo "Connecting to VM: $SSH_USER@$VM_HOST"

                    # SSH into VM and deploy
                    ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SSH_USER@$VM_HOST" << 'EOF'
                        echo "Connected to VM successfully"

                        # Navigate to home directory
                        cd ~

                        # Remove existing project if exists
                        if [ -d "Microservices_Jewelry_eCommerce" ]; then
                            echo "Removing existing project directory"
                            sudo docker-compose -f Microservices_Jewelry_eCommerce/docker-compose.yml down || true
                            rm -rf Microservices_Jewelry_eCommerce
                        fi

                        # Clone repository with submodules
                        echo "Cloning repository with submodules"
                        git clone --recurse-submodules https://github.com/Zennisch/Microservices_Jewelry_eCommerce.git

                        # Navigate to project directory
                        cd Microservices_Jewelry_eCommerce

                        # Initialize and update submodules
                        git submodule update --init --recursive

                        echo "Repository cloned successfully"
EOF

                    # Copy .env file to VM
                    echo "Copying .env file to VM"
                    scp -i "$SSH_KEY" -o StrictHostKeyChecking=no "$WORKSPACE/.env.clean" "$SSH_USER@$VM_HOST:~/Microservices_Jewelry_eCommerce/.env"

                    # Start services with docker-compose
                    ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SSH_USER@$VM_HOST" << 'EOF'
                        cd ~/Microservices_Jewelry_eCommerce

                        echo "Starting services with docker-compose"
                        sudo docker-compose up -d --build

                        echo "Waiting for services to start..."
                        sleep 30

                        echo "Checking running containers:"
                        sudo docker-compose ps

                        echo "Deployment completed successfully"
EOF
                '''
            }
        }

        stage('Health Check') {
            steps {
                echo 'Performing health check on deployed services'
                sh '''
                    set -a
                    . "$WORKSPACE/.env.clean"
                    set +a

                    VM_HOST="${VITE_BACKEND_HOST}"
                    API_PORT="${VITE_BACKEND_PORT}"
                    FRONTEND_PORT="${VITE_FRONTEND_PORT}"

                    echo "Checking API Gateway health at http://$VM_HOST:$API_PORT"
                    for i in {1..10}; do
                        if curl -s -f "http://$VM_HOST:$API_PORT/health" > /dev/null 2>&1; then
                            echo "API Gateway is healthy"
                            break
                        else
                            echo "Attempt $i: API Gateway not ready, waiting..."
                            sleep 10
                        fi
                        if [ $i -eq 10 ]; then
                            echo "Warning: API Gateway health check failed after 10 attempts"
                        fi
                    done

                    echo "Checking Frontend health at http://$VM_HOST:$FRONTEND_PORT"
                    for i in {1..5}; do
                        if curl -s -f "http://$VM_HOST:$FRONTEND_PORT" > /dev/null 2>&1; then
                            echo "Frontend is healthy"
                            break
                        else
                            echo "Attempt $i: Frontend not ready, waiting..."
                            sleep 10
                        fi
                        if [ $i -eq 5 ]; then
                            echo "Warning: Frontend health check failed after 5 attempts"
                        fi
                    done
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up credentials files'
            sh '''
                rm -f "$WORKSPACE/.env" || true
                rm -f "$WORKSPACE/.env.clean" || true
                rm -f "$WORKSPACE/gcp_key.json" || true
                rm -f "$WORKSPACE/id_ed25519" || true
            '''
        }
        success {
            echo 'Pipeline completed successfully'
            sh '''
                set -a
                . "$WORKSPACE/.env.clean" 2>/dev/null || true
                set +a
                echo "✅ Deployment successful!"
                echo "🌐 Frontend: http://${VITE_BACKEND_HOST:-34.9.78.197}:${VITE_FRONTEND_PORT:-3000}"
                echo "🔧 API Gateway: http://${VITE_BACKEND_HOST:-34.9.78.197}:${VITE_BACKEND_PORT:-8000}"
            '''
        }
        failure {
            echo 'Pipeline execution failed'
            echo 'Attempting to collect logs from VM for debugging'
            sh '''
                set -a
                . "$WORKSPACE/.env.clean" 2>/dev/null || true
                set +a

                VM_HOST="${VITE_BACKEND_HOST:-34.9.78.197}"
                SSH_USER="ray"
                SSH_KEY="$WORKSPACE/id_ed25519"

                if [ -f "$SSH_KEY" ]; then
                    ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SSH_USER@$VM_HOST" << 'EOF' || true
                        cd ~/Microservices_Jewelry_eCommerce
                        echo "=== Docker Compose Status ==="
                        sudo docker-compose ps
                        echo "=== Container Logs ==="
                        sudo docker-compose logs --tail=50
EOF
                fi
            '''
        }
    }
}
