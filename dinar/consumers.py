import json
from channels.generic.websocket import AsyncWebsocketConsumer

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({"message": "Connected to WebSocket!"}))

    async def disconnect(self, close_code):
        print(f"connection closed: {close_code}")

    async def receive(self, text_data):
        data = json.loads(text_data)
        response = {"message": f"Received: {data['message']}"}
        await self.send(text_data=json.dumps(response))
