pipeline {
    agent any
    
    environment {
        // Environment variables
        PYTHON_VERSION = '3.11'
        PIP_CACHE_DIR = "${WORKSPACE}/.pip-cache"
    }
    
    triggers {
        // Poll SCM every 2 minutes for changes
        pollSCM('H/2 * * * *')
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python environment...'
                script {
                    if (isUnix()) {
                        sh '''
                            python3 --version
                            # Install pip if not available
                            if ! command -v pip3 &> /dev/null; then
                                echo "Installing pip3..."
                                sudo dnf install -y python3-pip
                            fi
                            pip3 --version
                            pip3 install --user -r requirements.txt
                        '''
                    } else {
                        bat '''
                            python --version
                            pip --version
                            pip install -r requirements.txt
                        '''
                    }
                }
            }
        }
        
        stage('Compile') {
            steps {
                echo 'Compiling Python code...'
                script {
                    if (isUnix()) {
                        sh '''
                            # Try Maven first, fallback to Python compilation
                            if command -v mvn &> /dev/null; then
                                echo "Using Maven..."
                                mvn clean compile
                            elif [ -f "mvnw" ]; then
                                echo "Using Maven wrapper..."
                                chmod +x ./mvnw
                                ./mvnw clean compile
                            else
                                echo "Maven not available, using Python compilation..."
                                python3 -m py_compile hotel.py
                                echo "Python code compiled successfully"
                            fi
                        '''
                    } else {
                        bat '''
                            @echo off
                            where mvn >nul 2>&1
                            if %errorlevel% == 0 (
                                echo Using Maven...
                                mvn clean compile
                            ) else if exist mvnw.cmd (
                                echo Using Maven wrapper...
                                mvnw.cmd clean compile
                            ) else (
                                echo Maven not available, using Python compilation...
                                python -m py_compile hotel.py
                                echo Python code compiled successfully
                            )
                        '''
                    }
                }
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running unit tests...'
                script {
                    if (isUnix()) {
                        sh '''
                            # Try Maven first, fallback to direct pytest
                            if command -v mvn &> /dev/null; then
                                echo "Using Maven for testing..."
                                mvn test
                            elif [ -f "mvnw" ]; then
                                echo "Using Maven wrapper for testing..."
                                ./mvnw test
                            else
                                echo "Maven not available, using direct pytest..."
                                mkdir -p target/surefire-reports
                                python3 -m pytest tests/ -v --tb=short --junitxml=target/surefire-reports/pytest-results.xml
                                echo "Tests completed"
                            fi
                        '''
                    } else {
                        bat '''
                            @echo off
                            where mvn >nul 2>&1
                            if %errorlevel% == 0 (
                                echo Using Maven for testing...
                                mvn test
                            ) else if exist mvnw.cmd (
                                echo Using Maven wrapper for testing...
                                mvnw.cmd test
                            ) else (
                                echo Maven not available, using direct pytest...
                                mkdir target\\surefire-reports
                                python -m pytest tests/ -v --tb=short --junitxml=target/surefire-reports/pytest-results.xml
                                echo Tests completed
                            )
                        '''
                    }
                }
            }
            post {
                always {
                    // Publish test results
                    publishTestResults testResultsPattern: 'target/surefire-reports/*.xml'
                    
                    // Archive test reports if they exist
                    script {
                        if (fileExists('target/surefire-reports/pytest-results.xml')) {
                            archiveArtifacts artifacts: 'target/surefire-reports/*.xml', allowEmptyArchive: true
                        }
                    }
                }
            }
        }
        
        stage('Package') {
            steps {
                echo 'Creating deployable package...'
                script {
                    if (isUnix()) {
                        sh '''
                            # Try Maven first, fallback to direct packaging
                            if command -v mvn &> /dev/null; then
                                echo "Using Maven for packaging..."
                                mvn package
                            elif [ -f "mvnw" ]; then
                                echo "Using Maven wrapper for packaging..."
                                ./mvnw package
                            else
                                echo "Maven not available, using direct Python packaging..."
                                mkdir -p target/dist
                                python3 setup.py sdist --dist-dir target/dist
                                echo "Package created successfully"
                            fi
                        '''
                    } else {
                        bat '''
                            @echo off
                            where mvn >nul 2>&1
                            if %errorlevel% == 0 (
                                echo Using Maven for packaging...
                                mvn package
                            ) else if exist mvnw.cmd (
                                echo Using Maven wrapper for packaging...
                                mvnw.cmd package
                            ) else (
                                echo Maven not available, using direct Python packaging...
                                mkdir target\\dist
                                python setup.py sdist --dist-dir target/dist
                                echo Package created successfully
                            )
                        '''
                    }
                }
            }
            post {
                success {
                    // Archive the built artifacts
                    archiveArtifacts artifacts: 'target/dist/*.tar.gz, target/*.jar', allowEmptyArchive: true
                    echo 'Package created successfully!'
                }
            }
        }
        
        stage('Deploy Preparation') {
            steps {
                echo 'Preparing deployment artifacts...'
                script {
                    // Create deployment directory structure
                    if (isUnix()) {
                        sh '''
                            mkdir -p deployment
                            cp -r target/dist/* deployment/ || true
                            cp hotel.py deployment/
                            cp requirements.txt deployment/
                            echo "Deployment package prepared in deployment/ directory"
                        '''
                    } else {
                        bat '''
                            mkdir deployment
                            xcopy target\\dist\\* deployment\\ /E /I /Y
                            copy hotel.py deployment\\
                            copy requirements.txt deployment\\
                            echo "Deployment package prepared in deployment/ directory"
                        '''
                    }
                }
            }
        }
    }
    
    post {
        always {
            echo 'Pipeline execution completed.'
            // Clean up workspace if needed
            cleanWs(cleanWhenAborted: true, cleanWhenFailure: false, cleanWhenSuccess: true)
        }
        success {
            echo 'Pipeline executed successfully!'
            emailext (
                subject: "Jenkins Build Success: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: """
                    Build succeeded for job ${env.JOB_NAME}.
                    Build Number: ${env.BUILD_NUMBER}
                    Build URL: ${env.BUILD_URL}
                """,
                to: "${env.CHANGE_AUTHOR_EMAIL}",
                attachLog: true
            )
        }
        failure {
            echo 'Pipeline failed!'
            emailext (
                subject: "Jenkins Build Failed: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: """
                    Build failed for job ${env.JOB_NAME}.
                    Build Number: ${env.BUILD_NUMBER}
                    Build URL: ${env.BUILD_URL}
                    
                    Please check the build logs for more details.
                """,
                to: "${env.CHANGE_AUTHOR_EMAIL}",
                attachLog: true
            )
        }
    }
}
