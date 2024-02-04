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

@app.route('/login', methods=['GET'])
def login_form():
    return render_template('login.html')

# Page de connexion (login)
@app.route('/login', methods=['POST'])
def login():
    # Récupérer les données du formulaire
    email = request.form.get('email')
    password = request.form.get('password')

    # Construire les données à envoyer à votre API
    data = {
        'email': email,
        'password': password
    }

    # URL de votre API de login
    api_url = 'http://10.11.5.97:8000/auth/login'

    try:
        # Envoyer la requête POST à l'API
        response = requests.post(api_url, json=data)

        # Traiter la réponse de l'API
        if response.status_code == 200:
            # Authentification réussie, récupérer les données de la réponse JSON
            response_data = response.json()
            # Stocker l'access_token et les informations de l'utilisateur dans la session
            session['access_token'] = response_data.get('access_token')
            session['user_info'] = response_data.get('user')
            
            # Rediriger vers la page souhaitée (index)
            return redirect(url_for('index'))
        else:
            # Authentification échouée, afficher un message d'erreur
            return render_template('login.html', error_message='Invalid credentials')
    except requests.RequestException as e:
        print(f"Error making request to API: {e}")
        return "Error making request to API", 500  # Réponse d'erreur interne du serveur


@app.route('/register', methods=['GET'])
def register_form():
    return render_template('register.html')


# Page de connexion (signin)
@app.route('/register', methods=['POST'])
def register():
    # Récupérer les données du formulaire
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # Construire les données à envoyer à votre API
    data = {
        'username': username,
        'email': email,
        'password': password
    }

    # URL de votre API de login
    api_url = 'http://10.11.5.97:8000/auth/login'

    try:
        # Envoyer la requête POST à l'API
        response = requests.post(api_url, json=data)

        # Traiter la réponse de l'API
        if response.status_code == 200:
            # Authentification réussie, récupérer les données de la réponse JSON
            response_data = response.json()
            # Stocker l'access_token et les informations de l'utilisateur dans la session
            session['access_token'] = response_data.get('access_token')
            session['user_info'] = response_data.get('user')
            
            # Rediriger vers la page souhaitée (index)
            return redirect(url_for('login'))
        else:
            # Authentification échouée, afficher un message d'erreur
            return render_template('register.html', error_message='Invalid credentials')
    except requests.RequestException as e:
        print(f"Error making request to API: {e}")
        return "Error making request to API", 500  # Réponse d'erreur interne du serveur


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
