from channels.generic.websocket import AsyncWebsocketConsumer

import json


class PriceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "crypto_feed"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        print("Websocket connected")

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def price_update(self, event):
        data = event["data"]
        # send data to websocket
        await self.send(text_data=json.dumps(data))
