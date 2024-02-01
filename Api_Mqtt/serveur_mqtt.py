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
import asyncio
import aiocoap.resource as resource
import aiocoap
from aiocoap import Context, Message
import aiocoap
import logging
import asyncio

from aiocoap import *


# Envoyer les données à l'API Flask
api_url = "http://localhost:5000"
lecteur_url = "http://localhost:3000"


async def handle_get(request):
    print("Requête CoAP reçue")
    payload = b"OK"
    return aiocoap.Message(payload=payload)

async def send_coap_request(status):
    #await asyncio.sleep(3)
    print("status is ",status)
    # Faire une requête get au serveur CoAP
    payload_data = status.encode('utf-8')
    protocol = await Context.create_client_context()
    request = Message(code=GET,payload = payload_data, uri='coap://localhost/lecteur')
    try:
         response = await asyncio.wait_for(protocol.request(request).response, timeout=2)
    except asyncio.TimeoutError:
        # Handle timeout (server did not respond within the specified time)
        print('Timeout: Server did not respond within 2 seconds')
    
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    
    else:
        print('Result: %s'%(response.payload))
    return 

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
            resultat = "ouverte"
            print("porte ouverte")
            #await send_coap_request("ouvert")
        else:
            #envoyer la réponse négative avec le protocole coap
            resultat = "fermé"
            print ("porte fermé")
            #await send_coap_request("fermé")
    else:
        print("erreur de connexion")
    asyncio.run(send_coap_request(resultat))

async def mqtt_handler():
    mqtt_broker_address = "localhost"
    mqtt_broker_port = 1883
    mqtt_topic = "topic/qr_data"
    mqtt_client = mqtt.Client()

    mqtt_client.on_message = on_message
    mqtt_client.connect(mqtt_broker_address, mqtt_broker_port)
    mqtt_client.subscribe(mqtt_topic)
    mqtt_client.loop_start()

class ServeurResource(resource.Resource):

    async def render_get(self, request):
        payload = "Messsage de serveur_coap redner get".encode('utf-8')
        return aiocoap.Message(payload=payload)
    
    async def render_put(self, request):
        payload = "Messsage de serveur_coap render put".encode('utf-8')
        return aiocoap.Message(payload=payload)

async def coap_server():
    root = resource.Site()
    root.add_resource(['serveur'], ServeurResource())
    await aiocoap.Context.create_server_context(root)
    # Run forever
    await asyncio.get_running_loop().create_future()

async def main():
    await asyncio.gather(coap_server(), mqtt_handler())

if __name__ == '__main__':
    asyncio.run(main())