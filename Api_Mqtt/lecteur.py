#Lis le qr_code ou le badge
#envoie ensuite par fil mqtt les donnée du qr_code au serveur
#recoit par le protocole coap la réponse du serveur, si c'est OK, il envoit avec le protocole coap ok à la porte
from flask import Flask, send_file
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode
import json
import paho.mqtt.client as mqtt
from flask import Flask

#config de mosquitto
mqtt_broker_address = "localhost"
mqtt_broker_port = 1883
mqtt_topic = "topic/qr_data"
mqtt_client = mqtt.Client()
mqtt_client.connect(mqtt_broker_address, mqtt_broker_port)

lecteur = Flask(__name__)

@lecteur.route('/recois_qr')
def lecture_qr_code():
    img = qrcode.make('{"nom" : "olivier", "prenom" : "flauzac"}')
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
    return send_file("qr1.png", mimetype="image/png")

if __name__ == '__main__':
    lecteur.run(debug=True, port=3000)
    
