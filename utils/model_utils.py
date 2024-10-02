import os
import joblib

def load_model():
    model_path = os.path.join('models', 'iris_model.pkl')
    if not os.path.exists(model_path):
        raise FileNotFoundError("Le modèle Iris n'a pas été trouvé.")
    return joblib.load(model_path)
