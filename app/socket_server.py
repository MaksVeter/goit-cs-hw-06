import asyncio
from datetime import datetime
import logging
import websockets
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from pymongo import MongoClient
import os
import json

logging.basicConfig(level=logging.INFO)

mongo_client = MongoClient(os.getenv('MONGO_URI'))
db = mongo_client['messages_db']
messages_collection = db['messages']


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        self.clients.add(ws)
        logging.info(f'{ws.remote_address} connects')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects')

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distribute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distribute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            try:
                data = json.loads(message)
                message_to_store = {
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                    "username": data["username"],
                    "message": data["message"]
                }
                messages_collection.insert_one(message_to_store)
                logging.info(f"Збережено повідомлення: {data}")
                response = {
                    "username": data["username"],
                    "message": data["message"]
                }
                await self.send_to_clients(json.dumps(response))
            except json.JSONDecodeError:
                logging.error("Помилка при декодуванні повідомлення")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, '0.0.0.0', 5000):
        await asyncio.Future() 

if __name__ == '__main__':
    asyncio.run(main())
