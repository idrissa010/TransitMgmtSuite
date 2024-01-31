#!/usr/bin/python3
import logging
import asyncio
import aiocoap
import aiocoap.numbers.codes as codes
import aiocoap.resource as resource
from aiocoap import Message, Context
from concurrent.futures import ThreadPoolExecutor

from flask import Flask

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# Variable partagée pour stocker le message CoAP
coap_message = None

class CoAPResource(resource.Resource):
    def __init__(self):
        super().__init__()



def run_flask():
    app.run(port=5000)

async def coap_server():
        protocol = await aiocoap.Context.create_client_context()
        #Le b avant une chaîne de caractères en Python indique 
        #que la chaîne est de type "bytes". C'est nécessaire pour coap
        payload = b"bonjour"
        request = aiocoap.Message(code=codes.GET, uri='coap://localhost:5683/',payload=payload) 
        #5183 est le port par defaut
        global coap_message
        try:
            coap_message = await protocol.request(request).response
        except Exception as e:
            print('Failed to fetch resource:')
            print(e)
        else:
            print('Result: %s\n%r'%(coap_message.code, coap_message.payload))

async def run_coap_server():
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, coap_server)

@app.route('/')
def Hello_world():
    #global coap_message
    #return f"coap_message : {coap_message.payload}"
    return "hello world"

async def main():
    with ThreadPoolExecutor() as executor:
        await asyncio.gather(
            asyncio.get_running_loop().run_in_executor(executor, run_flask),
            run_coap_server()
        )
        
if __name__ == "__main__":
    asyncio.run(main()) 