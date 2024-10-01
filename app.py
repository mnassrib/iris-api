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
