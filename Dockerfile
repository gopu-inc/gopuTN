# Étape 1 : Image de base Python
FROM python:3.11-slim

# Étape 2 : Répertoire de travail
WORKDIR /app

COPY .. 
# Étape 3 : Installer ton paquet depuis PyPI
# Le token PyPI est injecté via --build-arg dans ton workflow CI/CD
ARG PYPI_TOKEN
RUN pip install --upgrade pip && \
    pip install gotn --extra-index-url https://__token__:${PYPI_TOKEN}@pypi.org/simple

# Étape 4 : Exposer le port (si ton CLI lance un serveur)
EXPOSE 8000

# Étape 5 : Commande par défaut
# Ici on lance ton CLI `gotn` directement
ENTRYPOINT ["gotn", "python3", "gotn/cli.py"]
