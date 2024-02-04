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

class PorteResource(resource.Resource):
    
    async def render_get(self, request):
        resultat = request.payload.decode('utf-8')
        print("dans le get : ",resultat)
        payload = "Messsage de serveur_coap redner get".encode('utf-8')
        return aiocoap.Message(payload=payload)

    async def render_put(self, request):
        payload = "Messsage de serveur_coap render put".encode('utf-8')
        return aiocoap.Message(payload=payload)


async def main():
    # Resource tree creation
    root = resource.Site()
    root.add_resource(['porte'], PorteResource())
    await aiocoap.Context.create_server_context(root)
    # Run forever
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())