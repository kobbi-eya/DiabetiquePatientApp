pipeline {
    agent any

    environment {
        FRONTEND_PATH = "frontend"    // Dossier du front-end React
        BACKEND_PATH = "backend"      // Dossier du back-end Django
        VENV_PATH = "env"             // Dossier de l'environnement virtuel
    }

    stages {
        // Étape 1 : Préparation de l'environnement Python pour le back-end
        stage('Setup Python Environment') {
            steps {
                dir(BACKEND_PATH) {
                    echo 'Setting up Python virtual environment...'
                    sh 'python -m venv ../${VENV_PATH}' // Crée l'environnement virtuel
                    sh './../${VENV_PATH}/bin/activate && pip install -r requirements.txt' // Active l'environnement et installe les dépendances
                }
            }
        }

        // Étape 2 : Build du front-end (React)
        stage('Build Frontend') {
            steps {
                dir(FRONTEND_PATH) {
                    echo 'Building React application...'
                    sh 'npm install' // Installe les dépendances de React
                    sh 'npm run build' // Compile l’application React
                }
            }
        }


    }
}
