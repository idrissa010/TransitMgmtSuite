#Lis le qr_code ou le badge
#envoie ensuite par fil mqtt les donnée du qr_code au serveur
#recoit par le protocole coap la réponse du serveur, si c'est OK, il envoit avec le protocole coap ok à la porte
from flask import Flask, send_file
from pyzbar.pyzbar import decode
from PIL import Image
import requests
import qrcode
import json
import paho.mqtt.client as mqtt
from flask import Flask
import asyncio
import aiocoap.resource as resource
import aiocoap
import threading
from aiocoap import *
#config de mosquitto
mqtt_broker_address = "localhost"
mqtt_broker_port = 1883
mqtt_topic = "topic/qr_data"
mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker_address, mqtt_broker_port)

lecteur = Flask(__name__)

async def envoyer_message_coap(status):
    # Faire une requête get au serveur CoAP
    protocol = await Context.create_client_context()
    payload_data = status.encode('utf-8')
    request = Message(code=GET,payload = payload_data, uri='coap://localhost/porte')
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s'%(response.payload))

class LecteurResource(resource.Resource):

    async def render_get(self, request):
        resultat = request.payload.decode('utf-8')
        print("Porte : ",resultat)
        await envoyer_message_coap(resultat)
        payload = "Messsage du lecteur render get".encode('utf-8')
        return aiocoap.Message(payload=payload)
    
    async def render_put(self, request):
        payload = "Messsage du lecrteur render put".encode('utf-8')
        return aiocoap.Message(payload=payload)

async def coap_server_lecteur():
    root = resource.Site()
    root.add_resource(['lecteur'], LecteurResource())
    await aiocoap.Context.create_server_context(root)
    # Run forever
    await asyncio.get_running_loop().create_future()


@lecteur.route('/recevoir_message_coap')
async def recevoir_message_coap():
    # Faire une requête get au serveur CoAP
    protocol = await Context.create_client_context()
    request = Message(code=GET, uri='coap://localhost/serveur')
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s'%(response.payload))

@lecteur.route('/')
def hello_world():
    return "Hello world"

@lecteur.route('/recois_qr')
async def lecture_qr_code():
    img = qrcode.make('{"nom" : "Olivier", "prenom" : "Flauzac"}')
    type(img)
    img.save("qr1.png")
    img = decode(Image.open('./qr1.png'))
    print(img)
    json_data = json.loads(img[0].data.decode())
    nom = json_data["nom"]
    prenom = json_data["prenom"]
    print(nom)
    print (prenom)
        # Envoyer les données via MQTT*
    mqtt_client.publish(mqtt_topic, json.dumps({"nom": nom, "prenom": prenom}))
    await recevoir_message_coap()
    return send_file("qr1.png", mimetype="image/png")

def run_flask():
    lecteur.run(debug=True, port=3000, use_reloader=False)

"""async def run_coap_server_lecteur():
    await coap_server_lecteur()"""

"""async def main():
    # Lancer Flask dans un thread
    flask_thread = threading.Thread(target=lambda: asyncio.run(run_flask()))
    flask_thread.start()

    # Lancer le serveur CoAP dans un thread
    coap_thread = threading.Thread(target=lambda: asyncio.run(run_coap_server_lecteur()))
    coap_thread.start()

    # Attendre que les deux threads se terminent
    flask_thread.join()
    coap_thread.join()"""

async def main():
    # Lancer Flask dans un thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Lancer le serveur CoAP
    coap_task = asyncio.create_task(coap_server_lecteur())

    # Attendre que les deux tâches se terminent
    await asyncio.gather(coap_task)
    flask_thread.join()


if __name__ == '__main__':
    asyncio.run(main())