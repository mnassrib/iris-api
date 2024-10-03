import pytest
import json
from app import app

@pytest.fixture
def client():
    """
    Crée une instance de l'application Flask pour les tests.
    """
    with app.test_client() as client:
        yield client

def test_predict_valid_data(client):
    """
    Test de l'endpoint /predict avec des données valides.
    Vérifie si une prédiction est renvoyée avec succès.
    """
    response = client.post('/predict', json={'features': [5.1, 3.5, 1.4, 0.2]})
    assert response.status_code == 200, "Le statut devrait être 200 pour des données valides."
    data = json.loads(response.data)
    assert 'prediction' in data, "La réponse devrait contenir une clé 'prediction'."

def test_predict_missing_features(client):
    """
    Test de l'endpoint /predict avec des données manquantes.
    Vérifie si une erreur est renvoyée lorsqu'il manque la clé 'features'.
    """
    response = client.post('/predict', json={})
    assert response.status_code == 400, "Le statut devrait être 400 lorsque la clé 'features' est manquante."
    data = json.loads(response.data)
    assert 'error' in data, "La réponse devrait contenir une clé 'error'."
    assert data['error'] == "Les données doivent contenir la clé 'features'.", \
        "Le message d'erreur ne correspond pas."

def test_predict_invalid_features(client):
    """
    Test de l'endpoint /predict avec un nombre incorrect de 'features'.
    Vérifie si une erreur est renvoyée lorsque la liste de 'features' est incorrecte.
    """
    response = client.post('/predict', json={'features': [5.1, 3.5]})
    assert response.status_code == 400, "Le statut devrait être 400 pour un nombre incorrect de 'features'."
    data = json.loads(response.data)
    assert 'error' in data, "La réponse devrait contenir une clé 'error'."
    assert data['error'] == "Les 'features' doivent être une liste de 4 éléments.", \
        "Le message d'erreur ne correspond pas."

def test_predict_non_numeric_features(client):
    """
    Test de l'endpoint /predict avec des 'features' non numériques.
    Vérifie si une erreur est renvoyée lorsque les 'features' contiennent des valeurs non numériques.
    """
    response = client.post('/predict', json={'features': ['a', 'b', 'c', 'd']})
    assert response.status_code == 400, "Le statut devrait être 400 pour des 'features' non numériques."
    data = json.loads(response.data)
    assert 'error' in data, "La réponse devrait contenir une clé 'error'."
    assert data['error'] == "Les 'features' doivent être des valeurs numériques.", \
        "Le message d'erreur ne correspond pas."

def test_welcome_page(client):
    """
    Test de l'endpoint racine /.
    Vérifie si la page d'accueil renvoie le message attendu.
    """
    response = client.get('/')
    assert response.status_code == 200, "Le statut devrait être 200 pour la page d'accueil."
    data = json.loads(response.data)
    assert 'message' in data, "La réponse devrait contenir une clé 'message'."
    assert data['message'] == "Bienvenue sur l'API de prédiction Iris", \
        "Le message de bienvenue ne correspond pas."
