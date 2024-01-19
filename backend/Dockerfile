# Utilisez une image de base Ubuntu 20.04
FROM ubuntu:20.04
FROM python:3.9

# Installez Python et pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Créez et définissez le répertoire de travail
WORKDIR /app

# Copiez le fichier requirements.txt et installez les dépendances
COPY requirements.txt /app/
RUN pip3 install --no-cache-dir -r requirements.txt

# Copiez le reste de l'application
COPY . /app/
# Exposez le port sur lequel l'application Flask écoute
EXPOSE 8000

# Commande par défaut pour lancer l'application Flask
CMD ["python3", "app/app.py"]