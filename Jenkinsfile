pipeline {
    agent any

    stages {
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
                            sh '''
                                npm install
                                npm run build
                            '''
                        }
                    }
                }
                stage('Cart Order Service') {
                    steps {
                        dir('Backend/Workspace/Service_Cart_Order/Service_Cart_Order_Backend') {
                            sh '''
                                npm install
                                npm run build
                            '''
                        }
                    }
                }
            }
        }
        stage('Build Python Services') {
            steps {
                dir('Backend/Workspace/Service_Chatbot/Service_Chatbot_Python') {
                    sh '''
                        pip install -r requirements.txt
                        python -m pytest tests/ || true
                    '''
                }
            }
        }
        stage('Build Frontend') {
            parallel {
                stage('Container') {
                    steps {
                        dir('Frontend/Workspace/Container/container-vite') {
                            sh '''
                                npm ci
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
                                        npm ci
                                        npm run build
                                    '''
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
