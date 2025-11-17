FROM python:3.12-slim


WORKDIR /app

# Copier ton code serveur (adapter le chemin si nécessaire)
COPY gophub.py /app/gophub.py

# Installer les dépendances
RUN pip install --no-cache-dir fastapi uvicorn requests websocket-client pyjwt chromadb

EXPOSE 8000

CMD ["uvicorn", "gophub:app", "--host", "0.0.0.0", "--port", "8000"]
