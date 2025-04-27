from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("logs_group", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("logs_group", self.channel_name)

    async def send_log(self, event):
        log = event['log']
        await self.send(text_data=json.dumps(log))