import asyncio
import json
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from api_app.nomenclators import TipoPrograma
from api_app.models import Medio, Movimiento
from channels.consumer import AsyncConsumer


class Consumer(AsyncConsumer):

    async def websocket_connect(self, event):
        self.connected = True
        self.first = True
        # print("connected", event)

        # indica que se acepta la conexion
        await self.send({
            "type": "websocket.accept"
        })

        while self.connected:
            if not self.first:
                await asyncio.sleep(10)  # continuar cada 3 segundos

            # ERROR Exception inside application: You cannot call this
            # from an async context - use a thread or sync_to_async.
            programs = await database_sync_to_async(self.get_total_programs)()
            mediums = await database_sync_to_async(self.get_total_mediums)()
            moves = await database_sync_to_async(self.get_total_moves)()
            users = await database_sync_to_async(self.get_total_users)()

            await self.send({
                'type': 'websocket.send',
                'text': json.dumps({
                    "programs": programs,
                    "mediums": mediums,
                    "moves": moves,
                    "users": users}),
            })
            self.first = False

    def  get_total_programs(self):
        return TipoPrograma.objects.count()

    def  get_total_mediums(self):
        return Medio.objects.count()

    def  get_total_moves(self):
        return Movimiento.objects.count()

    def  get_total_users(self):
        # return random.randint(0, 10)
        return User.objects.count()

    async def disconnect(self, close_code):
        self.connected = False
 
