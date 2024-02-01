import logging
import asyncio

from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():
    protocol = await Context.create_client_context()

    payload_data = "ouverte".encode('utf-8')

    request = Message(code=GET,payload=payload_data,uri='coap://localhost/lecteur')

    try:
        response = await protocol.request(request).response
    except Exception as e:
        print('Failed to fetch resource:')
        print(e)
    else:
        print('Result: %s'%(response.payload))

if __name__ == "__main__":
    asyncio.run(main())