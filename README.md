### Guide pour Déployer une Application de Prédiction d’Iris avec un Pipeline CI/CD sur Render

#### Introduction
Ce guide vous présente un projet d'application Flask de prédiction de l'espèce d'Iris, utilisant un modèle de machine learning entraîné avec scikit-learn. L'application est automatiquement déployée sur Render grâce à un pipeline CI/CD configuré avec GitHub Actions.

#### Définition du CI/CD

Le CI/CD (Intégration Continue/Déploiement Continu) est un ensemble de pratiques visant à automatiser les processus de développement logiciel, depuis l'intégration des modifications de code jusqu'à leur déploiement en production. Il permet de minimiser les erreurs humaines, d'accélérer les livraisons, et d'améliorer la qualité du code en s'appuyant sur des tests automatisés. 

- **Intégration Continue (CI)** : Chaque modification de code est automatiquement testée et intégrée dans la branche principale du projet après avoir passé des tests.
- **Déploiement Continu (CD)** : Une fois les tests validés, le code est automatiquement déployé dans un environnement de production.

### Prérequis

1. **Python 3.12**
2. **GitHub et un dépôt Git**
3. **Compte Render** (Pour héberger l'application)
4. **Docker Hub** (Pour héberger l'image Docker de votre application)

### Structure du Projet

```
iris-api
├── app.py
├── train_model.py
├── models
│   └── iris_model.pkl
├── tests
│   └── __init__.py
│   └── test_app.py
├── Dockerfile
├── requirements.txt
├── README.md
└── .github
    └── workflows
        └── ci-cd.yml
```

### Étape 1: Entraîner le Modèle

Le fichier `train_model.py` charge le dataset Iris, entraîne un modèle `RandomForestClassifier`, puis sauvegarde ce modèle dans un fichier pickle sous `models/iris_model.pkl`.

```python
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# Charger le dataset Iris
iris = datasets.load_iris()
X = iris.data
y = iris.target

# Séparer les données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner le modèle
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Sauvegarder le modèle
joblib.dump(model, 'models/iris_model.pkl')
```

### Étape 2: Créer l'API avec Flask

L'application Flask dans `app.py` expose un endpoint `/predict` qui reçoit un JSON avec les caractéristiques d'une fleur et retourne la prédiction de l'espèce d'Iris.

```python
from flask import Flask, request, jsonify
import joblib
import os

# Initialiser Flask
app = Flask(__name__)

# Charger le modèle
model_path = os.path.join('models', 'iris_model.pkl')
model = joblib.load(model_path)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    prediction = model.predict([data['features']])
    return jsonify({'prediction': int(prediction[0])})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

### Étape 3: Tester l'Application

Les tests se trouvent dans `tests/test_app.py`. Nous utilisons `pytest` pour exécuter des tests unitaires sur l'application. Le test simule une requête POST à l'endpoint `/predict` et vérifie que la réponse contient une prédiction.

```python
import pytest
import json
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_predict(client):
    response = client.post('/predict', json={
        'features': [5.1, 3.5, 1.4, 0.2]
    })
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'prediction' in data
```

### Étape 4: Dockeriser l'Application

Le fichier `Dockerfile` est utilisé pour containeriser l'application Flask. Cela permet de créer une image Docker qui sera déployée sur Render.

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py app.py
COPY models/ models/
COPY tests/ tests/  

RUN pytest tests/

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

### Étape 5: Configurer le Pipeline CI/CD

Le pipeline CI/CD est défini dans `.github/workflows/ci-cd.yml`. Ce fichier configure les étapes pour exécuter les tests, construire l'image Docker, la pousser sur Docker Hub, et déclencher le déploiement automatique sur Render.

#### Secrets dans GitHub Actions

Pour sécuriser les informations sensibles comme les identifiants Docker et les hooks de déploiement, nous utilisons les **Secrets** de GitHub. Vous pouvez les ajouter dans la section *Settings* du dépôt GitHub, sous *Secrets and variables*.

Secrets nécessaires :

- **DOCKER_USERNAME** : Votre nom d'utilisateur Docker Hub.
- **DOCKER_PASSWORD** : Votre mot de passe Docker Hub.
- **RENDER_DEPLOY_HOOK** : Le hook de déploiement Render (Optionnel si vous n’utilisez pas l’Auto-Deploy).

```yaml
jobs:
  # Job de construction, de test et de déploiement
  build_and_deploy:
    runs-on: ubuntu-latest

    steps:
      # Étape 1: Récupérer le code du dépôt GitHub
      - name: Checkout code
        uses: actions/checkout@v3

      # Étape 2: Configurer Python 3.12
      - name: Set up Python 3.12
        uses: actions/setup-python@v3
        with:
          python-version: '3.12'

      # Étape 3: Mettre en cache les dépendances Python pour accélérer les builds
      - name: Cache pip dependencies
        uses: actions/cache@v2
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-

      # Étape 4: Installer les dépendances définies dans le fichier requirements.txt
      - name: Install Python dependencies
        run: |
          pip install -r requirements.txt

      # Étape 5: Exécuter les tests avec pytest
      - name: Run tests
        run: |
          pytest --maxfail=5 --disable-warnings

      # Étape 6: Créer une image Docker seulement si les tests réussissent
      - name: Build Docker image
        if: success()
        run: |
          docker build -t iris-api .

      # Étape 7: Se connecter à Docker Hub (ou un registre Docker privé)
      - name: Log in to Docker Hub
        if: success()
        run: |
          echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin

      # Étape 8: Taguer et pousser l'image Docker sur Docker Hub
      - name: Push Docker image to Docker Hub
        if: success()
        run: |
          docker tag iris-api:latest ${{ secrets.DOCKER_USERNAME }}/iris-api:latest
          docker push ${{ secrets.DOCKER_USERNAME }}/iris-api:latest

      # Étape 9: Déclencher le déploiement avec le webhook
      - name: Trigger Render Deploy Hook
        if: success()
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }}
```

### Étape 6: Tester Localement l'API

Vous pouvez tester localement l'API avant de la déployer en utilisant `curl` :

```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d "{\"features\": [5.1, 3.5, 1.4, 0.2]}"
```

Cela devrait retourner une prédiction dans la réponse JSON.

### Conclusion

Ce projet vous permet d'automatiser le déploiement d'une application de machine learning sur Render tout en vous assurant de la qualité grâce à un pipeline CI/CD. En intégrant des tests automatisés, des images Docker, et un déploiement continu, vous garantissez un développement rapide et fiable, tout en maintenant une haute qualité de code.
