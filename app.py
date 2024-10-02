from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
import numpy as np
from utils.model_utils import load_model
from utils.validation import validate_input

# Initialiser Flask
app = Flask(__name__)

# Configurer Swagger
swagger = Swagger(app)

# Charger le modèle
model = load_model()

@app.route('/predict', methods=['POST'])
@swag_from('swagger/predict.yml')
def predict():
    """
    Endpoint pour faire une prédiction avec le modèle Iris.
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
@swag_from('swagger/index.yml')
def index():
    """
    Page d'accueil de l'API Iris.
    """
    return jsonify({"message": "Bienvenue sur l'API de prédiction Iris"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
