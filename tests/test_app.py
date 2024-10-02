import pytest
import json
from app import app

@pytest.fixture
def client():
    # Crée une instance de l'application Flask pour les tests
    with app.test_client() as client:
        yield client

def test_predict(client):
    # Simule une requête POST avec des données valides pour tester l'endpoint /predict
    response = client.post('/predict', json={
        'features': [5.1, 3.5, 1.4, 0.2]
    })
    
    # Vérifie que le statut de la réponse est 200 (succès)
    assert response.status_code == 200
    
    # Vérifie que la réponse contient bien une prédiction
    data = json.loads(response.data)
    assert 'prediction' in data
