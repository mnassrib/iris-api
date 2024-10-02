import pytest
import json
from app import app

@pytest.fixture
def client():
    # Crée une instance de l'application Flask pour les tests
    with app.test_client() as client:
        yield client

def test_predict_valid_data(client):
    # Test avec des données valides
    response = client.post('/predict', json={'features': [5.1, 3.5, 1.4, 0.2]})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'prediction' in data

def test_predict_missing_features(client):
    # Test sans la clé 'features'
    response = client.post('/predict', json={})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == "Les données doivent contenir la clé 'features'."

def test_predict_invalid_features(client):
    # Test avec des 'features' invalides (nombre incorrect d'éléments)
    response = client.post('/predict', json={'features': [5.1, 3.5]})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == "Les 'features' doivent être une liste de 4 éléments."

def test_predict_non_numeric_features(client):
    # Test avec des 'features' non numériques
    response = client.post('/predict', json={'features': ['a', 'b', 'c', 'd']})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert data['error'] == "Les 'features' doivent être des valeurs numériques."

def test_welcome_page(client):
    # Test de la page d'accueil
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['message'] == "Bienvenue sur l'API de prédiction Iris"
