pipeline {
    agent any

    environment {
        FRONTEND_PATH = "frontend"    // Dossier du front-end React
        BACKEND_PATH = "backend"      // Dossier du back-end Django
        VENV_PATH = "env"             // Dossier de l'environnement virtuel
    }

    stages {
        stage('Setup Python Environment') {
            steps {
                dir(BACKEND_PATH) {
                    echo 'Setting up Python virtual environment...'
                    bat 'python -m venv ..\\${VENV_PATH}' // Crée l'environnement virtuel
                    bat '..\\${VENV_PATH}\\Scripts\\activate && pip install -r requirements.txt' // Active l'environnement et installe les dépendances
                }
            }
        }

        stage('Build Frontend') {
            steps {
                dir(FRONTEND_PATH) {
                    echo 'Building React application...'
                    bat 'npm install' // Installe les dépendances de React
                    bat 'npm run build' // Compile l’application React
                }
            }
        }
    }
}
