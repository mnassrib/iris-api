swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "API de Prédiction Iris",
        "description": "Cette API prédit la classe d'une fleur Iris à partir de ses caractéristiques.",
        "version": "1.0.0",
        "termsOfService": "https://votre-site-web.com/terms",
        "contact": {
            "email": "votre-email@example.com"
        },
        "license": {
            "name": "MIT",
            "url": "https://opensource.org/licenses/MIT"
        },
    },
    "basePath": "/",  # Le chemin de base pour toutes les routes
    "tags": [
                {
            "name": "Accueil",
            "description": "Endpoint de la page d'accueil"
        },
        {
            "name": "Prédiction",
            "description": "Endpoint lié aux prédictions d'Iris"
        }
    ]
}
