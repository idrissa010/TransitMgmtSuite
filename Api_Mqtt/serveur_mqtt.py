#Ce serveur est sub (abonné) à la file mqtt er reçoit les données du QR_code ou du badge
#il demande ensuite à l'api mqtt si le QR_code ou le badge est valide
#Si l'api lui dit que les données sont valides, il envoit avec le protocol coap un ok pour ouvrir la porte
from flask import Flask, send_file
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
import json
import paho.mqtt.client as mqtt
import requests

# Envoyer les données à l'API Flask
api_url = "http://localhost:5000"

def on_message(client, userdata, message):
    payload = message.payload.decode()
    json_data = json.loads(payload)
    nom = json_data.get("nom")
    prenom = json_data.get("prenom")
    print(nom)
    print(prenom)
    #print(f"Message reçu sur le sujet {message.topic}: {payload}")
    data = {"nom": nom, "prenom": prenom}
    response = requests.post(api_url + "/verif_qrcode", json=data)

    if response.ok:
        # Récupérer la réponse JSON
        api_response = response.json()
        print("Réponse de l'API:", api_response)
        status = api_response.get("status")
        if status == "success":
            #Bon, il faut envoyer la réponse positive avec le protocole coap
            print("ok")
        else:
            #envoyer la réponse négative avec le protocole coap
            print ("ok")
    else:
        print("erreur de connexion")



if __name__ == '__main__':
    # Configuration du client MQTT
    #config de mosquitto
    mqtt_broker_address = "localhost"
    mqtt_broker_port = 1883
    mqtt_topic = "topic/qr_data"
    mqtt_client = mqtt.Client()
    mqtt_client.connect(mqtt_broker_address, mqtt_broker_port)
    mqtt_client.subscribe(mqtt_topic)
    mqtt_client.loop_start()
    mqtt_client.on_message = on_message
    mqtt_client.loop_forever()