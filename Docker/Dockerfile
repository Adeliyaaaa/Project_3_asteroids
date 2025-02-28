FROM python:3.12.8-slim

WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances en premier pour optimiser le cache
COPY requirements.txt .

# Mettre à jour pip et installer les dépendances Python
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Installer mage-ai après requirements.txt
RUN pip install --no-cache-dir mage-ai

# Copier le reste des fichiers après l'installation des dépendances
COPY . .

CMD ["mage", "start"]