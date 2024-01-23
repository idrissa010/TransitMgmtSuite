#il recoit des données du lecteur par protocole coap, si c'est ok print vert, si c'est ko print rouge.
import datetime
import asyncio
import logging
import aiocoap
import aiocoap.resource as resource

class Hello(resource.Resource):
    def __init__(self):
        super().__init__()

    async def render_get(self, request):
        payload = request.payload.decode()
        logging.info(f"Requête reçue avec payload : {payload}")

        if payload == "bonjour":
            msg = aiocoap.Message(payload=b"Bonjour toi")
        else:
            msg = aiocoap.Message(payload=b"Alors on dit pas bonjour")  
        return msg

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

async def main():
    root = resource.Site()
    root.add_resource([], Hello())
    #quand on  met root cela signifie que le serveur CoAP écoutera 
    #sur toutes les interfaces réseau de cet appareil. par defaut le port 5683
    await aiocoap.Context.create_server_context(root)
    await asyncio.get_running_loop().create_future()

if __name__ == "__main__":
    asyncio.run(main())