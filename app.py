from flask import Flask, request, jsonify  # Framework principal pour créer l'API
from flasgger import Swagger, swag_from  # Pour la documentation Swagger de l'API
import numpy as np  # Utilisé pour manipuler les tableaux de données d'entrée
from utils.model_utils import load_model  # Pour charger le modèle pré-entraîné
from utils.validation import validate_input  # Pour valider les données d'entrée
from utils.swagger_config import swagger_template  # Importer le template Swagger
import json # Pour encoder et décoder des données JSON

# Initialiser Flask
app = Flask(__name__)

# Configurer Swagger pour la documentation API avec un template
swagger = Swagger(app, template=swagger_template)

# Charger le modèle au démarrage de l'application
model = load_model()

@app.before_request
def configure_swagger():
    """
    Configure dynamiquement le schéma (http/https) et l'hôte pour Swagger.
    Cette fonction est appelée avant chaque requête pour garantir que l'hôte et le schéma sont définis correctement.
    """
    scheme = request.scheme  # HTTP ou HTTPS
    host = request.host  # Hôte (localhost:5000 ou hôte de production)
    swagger_template['schemes'] = [scheme]
    swagger_template['host'] = host
    app.config['SWAGGER'] = swagger_template  # Mettre à jour la configuration Swagger

@app.route('/predict', methods=['POST'])
@swag_from('swagger/predict.yml')  # Documentation Swagger pour l'endpoint /predict
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
        # Faire une prédiction avec le modèle chargé
        prediction = model.predict(features)
        return jsonify({'prediction': int(prediction[0])}), 200
    except ValueError as e:
        # Erreur liée aux données (par exemple, mauvaise forme d'entrée)
        return jsonify({"error": f"Erreur dans les données d'entrée: {str(e)}"}), 400
    except Exception as e:
        # Erreur interne du serveur
        app.logger.error(f"Erreur interne: {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

@app.route('/')
@swag_from('swagger/index.yml')  # Documentation Swagger pour la page d'accueil
def index():
    """
    Page d'accueil de l'API Iris.
    """
    response = {"message": "Bienvenue sur l'API de prédiction Iris"}
    return app.response_class(
        response=json.dumps(response, ensure_ascii=False),
        mimetype='application/json'
    ), 200

if __name__ == '__main__':
    # Configurations pour l'exécution de l'application
    app.run(host='0.0.0.0', port=5000)
