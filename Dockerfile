# Utiliser une image de base Python
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier uniquement le fichier requirements.txt
COPY requirements.txt requirements.txt

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier les fichiers et dossiers nécessaires à l'application
COPY app.py app.py
COPY utils/ utils/
COPY swagger/ swagger/
COPY models/ models/
COPY tests/ tests/  

# Exécuter les tests
RUN pytest tests/

# Exposer le port 5000 pour l'application Flask
EXPOSE 5000

# Lancer l'application avec Gunicorn pour la production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
