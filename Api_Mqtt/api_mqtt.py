#elle communiquera avec la base de donnée mangoDB
#elle communiuera avec le serveur (en code python aussi)
from flask import Flask, send_file, request, jsonify
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
import json
import paho.mqtt.client as mqtt
import pymongo

from flask import Flask


api_mqtt = Flask(__name__)

# Configuration de MongoDB
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["RT_0707"]
collection = db["user"]

@api_mqtt.route("/verif_qrcode", methods=['POST'])
def verif_qrcode():
    data = request.json
    nom = data.get('nom')
    prenom = data.get('prenom')
    print(f"Nom reçu: {nom}")
    print(f"Prénom reçu: {prenom}")
    # Faire ce que vous avez besoin de faire avec les données reçues
    # Vérification dans la base de données MongoDB
    query = {"nom": nom, "prenom": prenom}
    result = collection.find_one(query)

    if result:
         # Les données sont présentes dans la base de données
        print("Données trouvées dans la base de données MongoDB.")
        response = {"status": "success", "message": "Données trouvées dans la base de données MongoDB."} 
    else:
        # Les données ne sont pas présentes dans la base de données
        print("Données non trouvées dans la base de données MongoDB.")
        response = {"status": "error", "message": "Données non trouvées dans la base de données MongoDB."}
    
    return jsonify(response)

if __name__ == '__main__':
    api_mqtt.run(debug=True, port=5000)
