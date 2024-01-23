#!/usr/bin/python3
import logging
import asyncio

import aiocoap
import aiocoap.numbers.codes as codes

logging.basicConfig(level=logging.INFO)

async def main():
    protocol = await aiocoap.Context.create_client_context()
    #Le b avant une chaîne de caractères en Python indique 
    #que la chaîne est de type "bytes". C'est nécessaire pour coap
    payload = b"bonjour"
    request = aiocoap.Message(code=codes.GET, uri='coap://localhost:5683/',payload=payload) 
    #5183 est le port par defaut
    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s\n%r'%(response.code, response.payload))

if __name__ == "__main__":
    asyncio.run(main()) 