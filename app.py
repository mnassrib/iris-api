from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
import joblib
import os
import numpy as np

# Initialiser Flask
app = Flask(__name__)

# Configurer Swagger
swagger = Swagger(app)

# Charger le modèle au démarrage de l'application
def load_model():
    model_path = os.path.join('models', 'iris_model.pkl')
    if not os.path.exists(model_path):
        raise FileNotFoundError("Le modèle Iris n'a pas été trouvé.")
    return joblib.load(model_path)

model = load_model()

# Fonction pour valider les données d'entrée
def validate_input(data):
    if not data or 'features' not in data:
        return False, "Les données doivent contenir la clé 'features'."
    
    features = data['features']
    
    if not isinstance(features, list) or len(features) != 4:
        return False, "Les 'features' doivent être une liste de 4 éléments."
    
    try:
        # Convertir en tableau numpy pour s'assurer qu'il n'y a que des valeurs numériques
        np.array(features, dtype=float)
    except ValueError:
        return False, "Les 'features' doivent être des valeurs numériques."
    
    return True, None

@app.route('/predict', methods=['POST'])
@swag_from({
    'summary': "Faire une prédiction avec le modèle Iris",
    'description': "Prend les caractéristiques de la fleur Iris en entrée et retourne la classe prédite.",
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': "Les caractéristiques de la fleur sous forme de liste",
            'schema': {
                'type': 'object',
                'properties': {
                    'features': {
                        'type': 'array',
                        'items': {'type': 'number'},
                        'example': [5.1, 3.5, 1.4, 0.2]
                    }
                },
            }
        }
    ],
    'responses': {
        200: {
            'description': "La classe prédite pour la fleur Iris",
            'schema': {
                'type': 'object',
                'properties': {
                    'prediction': {
                        'type': 'integer',
                        'example': 0
                    }
                }
            }
        },
        400: {
            'description': "Erreur dans les données envoyées",
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {
                        'type': 'string',
                        'example': "Les données doivent contenir la clé 'features'."
                    }
                }
            }
        }
    }
})
def predict():
    """
    Endpoint pour faire une prédiction avec le modèle Iris.
    ---
    tags:
      - Prédictions
    """
    data = request.get_json()
    
    # Validation des données d'entrée
    is_valid, error_message = validate_input(data)
    if not is_valid:
        return jsonify({"error": error_message}), 400
    
    features = np.array([data['features']])
    
    try:
        prediction = model.predict(features)
        return jsonify({'prediction': int(prediction[0])}), 200
    except Exception as e:
        return jsonify({"error": "Erreur interne du serveur"}), 500

@app.route('/')
def index():
    """
    Page d'accueil de l'API Iris.
    ---
    tags:
      - Accueil
    responses:
      200:
        description: "Bienvenue sur l'API de prédiction Iris"
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Bienvenue sur l'API de prédiction Iris"
    """
    return jsonify({"message": "Bienvenue sur l'API de prédiction Iris"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
