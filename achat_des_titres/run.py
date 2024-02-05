import os
from flask import Flask, render_template, redirect, request, url_for, session, jsonify
import requests
from functools import wraps

# Créer une instance de l'application Flask
app = Flask(__name__)

# Obtenez le chemin absolu du répertoire des modèles
template_dir = os.path.abspath('templates')
app.template_folder = template_dir

# Configurez le dossier statique
static_dir = os.path.abspath('static')
app.static_folder = static_dir
app.static_url_path = '/static'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
