# Guide pour Déployer une API de Prédiction Iris avec un Pipeline CI/CD sur Render

Ce projet implémente une API Flask permettant de prédire la classe d'une fleur Iris à partir de ses caractéristiques, accompagnée d'une documentation Swagger. Le projet inclut également un pipeline CI/CD complet utilisant GitHub Actions pour automatiser les tests et le déploiement de l'application sur Render, avec une image Docker hébergée sur Docker Hub.

## Table des matières

1. [Introduction et description du projet](#introduction-et-description-du-projet)
2. [Fonctionnalités](#fonctionnalités)
3. [Prérequis](#prérequis)
4. [Installation](#installation)
5. [Structure du projet](#structure-du-projet)
6. [Utilisation](#utilisation)
7. [Tester l'image Docker localement](#tester-limage-docker-localement)
8. [Déploiement via un Pipeline CI/CD avec GitHub Actions](#déploiement-via-un-pipeline-cicd-avec-github-actions)
9. [Importance du CI/CD](#importance-du-cicd)
10. [Tester l'API en production](#tester-lapi-en-production)
11. [Améliorations futures](#améliorations-futures)

## Introduction et description du projet

Ce projet a pour but de démontrer une approche complète de développement d'une API de prédiction utilisant le modèle `RandomForestClassifier` de scikit-learn, avec une intégration complète de CI/CD (Continuous Integration/Continuous Deployment). 

Grâce à cette API, vous pourrez prédire la classe d'une fleur Iris à partir de ses caractéristiques florales (longueur et largeur des sépales et des pétales). L'API est documentée via Swagger UI pour faciliter l'interaction avec les différents endpoints.

Un pipeline CI/CD est mis en place avec GitHub Actions pour automatiser les tests, la construction d'une image Docker, et le déploiement de l'application sur la plateforme Render. Ce pipeline permet une gestion fluide des déploiements en production tout en garantissant la qualité grâce à des tests automatisés.

## Fonctionnalités

- **Prédiction** : Fournit la classe prédite (Setosa, Versicolor, Virginica) d'une fleur Iris à partir de 4 caractéristiques.
- **Documentation Swagger** : Swagger UI est intégré pour documenter les endpoints disponibles.
- **CI/CD Automatisé** : Tests unitaires, construction d'une image Docker, et déploiement automatisé sur Render via GitHub Actions.
- **Validation des données** : Validation des données d'entrée avant la prédiction pour s'assurer que les entrées sont correctes.
- **Modularité** : Organisation modulaire du code pour une meilleure maintenabilité.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants :

- **Python 3.12**
- **GitHub et un dépôt Git**
- **Compte Render** (pour héberger l'application)
- **Compte Docker Hub** (pour héberger l'image Docker de l'application)

## Installation

1. **Cloner le dépôt Git** :
   ```bash
   git clone https://github.com/mnassrib/iris-api.git
   cd iris-api
   ```

2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

3. **Entraîner le modèle (si le modèle n'est pas encore disponible dans le dossier `models`)** :
   ```bash
   python train_model.py
   ```

## Structure du projet

La structure du projet est la suivante :

```
iris-api
├── app.py
├── train_model.py
├── models
│   └── iris_model.pkl
├── utils
│   ├── model_utils.py
│   └── validation.py
├── swagger
│   ├── index.yml
│   └── predict.yml
├── tests
│   └── test_app.py
├── Dockerfile
├── requirements.txt
├── .gitignore
├── README.md
└── .github
    └── workflows
        └── ci-cd.yml
```

### Explication des fichiers principaux :

- **`app.py`** : Fichier principal de l'API. Il contient les routes pour les prédictions et la page d'accueil.
- **`train_model.py`** : Script pour entraîner le modèle `RandomForestClassifier` et le sauvegarder.
- **`models/iris_model.pkl`** : Modèle pré-entraîné utilisé pour faire des prédictions.
- **`utils/model_utils.py`** : Contient la fonction de chargement du modèle.
- **`utils/validation.py`** : Contient la fonction de validation des données d'entrée.
- **`swagger/`** : Contient les fichiers YAML définissant la documentation Swagger pour les différents endpoints.
- **`tests/test_app.py`** : Tests unitaires pour valider le bon fonctionnement de l'API.
- **`.gitignore`** : Fichier pour exclure certains fichiers ou répertoires du suivi de version Git, tels que les fichiers générés automatiquement ou les données sensibles.
- **`.github/workflows/ci-cd.yml`** : Pipeline CI/CD pour exécuter les tests et déployer l'application sur Render.

## Utilisation

1. **Lancer l'application localement** :
   ```bash
   python app.py
   ```

   L'application sera disponible à l'adresse `http://127.0.0.1:5000`.

2. **Tester l'API avec une requête curl** :
   ```bash
   curl -X POST http://localhost:5000/predict \
   -H "Content-Type: application/json" \
   -d "{\"features\": [5.1, 3.5, 1.4, 0.2]}"

   ```

   Vous recevrez une réponse JSON avec la classe prédite :
   ```json
   {
     "prediction": 0
   }
   ```

3. **Accéder à la documentation Swagger** :
   Accédez à `http://127.0.0.1:5000/apidocs/` pour voir la documentation complète de l'API générée automatiquement via Swagger.

4. **Tests** :
    Pour exécuter les tests unitaires :

    ```bash
    pytest
    ```

    Les tests se trouvent dans le répertoire `tests/` et couvrent les fonctionnalités principales de l'API.

## Tester l'image Docker localement

1. **Construire l'image Docker** :
   ```bash
   docker build -t iris-api .
   ```

2. **Lancer le conteneur Docker** :
   ```bash
   docker run -p 5000:5000 iris-api
   ```

   L'application sera disponible à `http://127.0.0.1:5000`.

3. **Tester l'API avec une requête curl** :
   ```bash
   curl -X POST http://localhost:5000/predict \
   -H "Content-Type: application/json" \
   -d "{\"features\": [5.1, 3.5, 1.4, 0.2]}"
   ```

4. **Accéder à la documentation Swagger** :
   Accédez à `http://127.0.0.1:5000/apidocs/` pour voir la documentation complète de l'API générée automatiquement via Swagger.

5. **Tests** :
    Pour exécuter les tests unitaires :

    ```bash
    pytest
    ```

## Déploiement via un Pipeline CI/CD avec GitHub Actions

Ce projet est configuré avec un pipeline CI/CD dans le fichier `.github/workflows/ci-cd.yml`. Le pipeline effectue les actions suivantes :

1. **Installation des dépendances** : Installe les dépendances définies dans `requirements.txt`.
2. **Exécution des tests** : Exécute les tests unitaires via `pytest`.
3. **Création et déploiement de l'image Docker** : Si les tests sont réussis, le pipeline crée une image Docker et la pousse sur Docker Hub.
4. **Déclenchement du déploiement sur Render** : Une fois l'image Docker prête, le déploiement est déclenché sur Render via un webhook. **Notez qu'il est important de désactiver l'option Auto-Deploy sur Render pour que le déploiement suive uniquement le workflow GitHub Actions et ne se déclenche qu'après validation complète du pipeline CI/CD**.

### Secrets dans CI/CD

Les secrets pour Docker Hub et Render doivent être ajoutés dans les secrets GitHub de votre dépôt. Pour ce faire :

1. **Ajouter les secrets GitHub** :
   - `DOCKER_USERNAME` : Votre nom d'utilisateur Docker Hub.
   - `DOCKER_PASSWORD` : Votre mot de passe Docker Hub.
   - `RENDER_DEPLOY_HOOK` : URL du webhook Render pour déployer l'application.

2. Allez dans les paramètres de votre dépôt GitHub, puis dans la section **Secrets and variables** > **Actions** pour ajouter ces secrets.

## Importance du CI/CD

### Qu'est-ce que le CI/CD ?

Le CI/CD, ou **Continuous Integration/Continuous Deployment**, est une pratique de développement logiciel qui automatise les processus de test, d'intégration et de déploiement des applications. Cette approche permet d'intégrer les nouvelles modifications dans le code source de manière continue, de tester ces modifications automatiquement, et de déployer rapidement et de manière fiable les nouvelles versions de l'application.

### Pourquoi est-il important ?

L'importance du CI/CD réside dans les bénéfices suivants :
- **Automatisation** : Le CI/CD permet d'automatiser des processus fastidieux comme les tests et les déploiements. Cela réduit les erreurs humaines et garantit des processus fiables et reproductibles.
- **Rapidité** : En automatisant les tests et les déploiements, les développeurs peuvent itérer plus rapidement et mettre à

 jour leurs applications plus fréquemment, avec des retours immédiats en cas de problèmes.
- **Qualité** : Grâce à des tests automatisés exécutés à chaque modification du code, le CI/CD améliore la qualité du code en détectant rapidement les régressions ou les bugs.
- **Confiance** : En s'appuyant sur des pipelines bien configurés, les développeurs peuvent déployer en production avec confiance, sachant que les tests ont été effectués et que les étapes de déploiement sont automatisées.

### Application dans ce projet

Dans ce projet, le pipeline CI/CD assure que chaque modification du code est correctement testée avant d'être déployée en production. Voici comment le pipeline est appliqué :

1. **Test automatique** : À chaque push sur la branche principale du dépôt GitHub, le pipeline CI/CD teste le code avec `pytest`.
2. **Création de l'image Docker** : Si les tests réussissent, une image Docker est créée.
3. **Déploiement automatique** : Enfin, l'image est déployée sur Render, garantissant que la dernière version de l'application est toujours en production.

## Tester l'API en production

L'API de ce projet est déployée sur Render et est disponible à l'adresse suivante :

**[https://iris-api-7cbf.onrender.com](https://iris-api-7cbf.onrender.com)**

### Tester l'API en production

Vous pouvez tester l'API en envoyant une requête POST à l'endpoint `/predict` :

```bash
curl -X POST https://iris-api-7cbf.onrender.com/predict \
-H "Content-Type: application/json" \
-d "{\"features\": [5.1, 3.5, 1.4, 0.2]}"
```

Vous recevrez une réponse JSON avec la classe prédite. Par exemple :

```json
{
  "prediction": 0
}
```

### Consulter la documentation de l'API

Vous pouvez également accéder à la documentation Swagger de l'API en production à l'adresse suivante :

**[https://iris-api-7cbf.onrender.com/apidocs/](https://iris-api-7cbf.onrender.com/apidocs/)**

## Améliorations futures

- Ajouter des tests supplémentaires pour améliorer la couverture.
- Optimiser la gestion des erreurs pour plus de robustesse.
- Implémenter un système de cache pour les prédictions.
- Ajouter des fonctionnalités de monitoring et de logging pour la production.

---

Ce guide est conçu pour vous fournir un aperçu complet du projet, de l'installation à l'utilisation, en passant par les tests, le déploiement et l'importance du CI/CD dans ce projet.