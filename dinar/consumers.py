import asyncio
import json
import os
from channels.generic.websocket import AsyncWebsocketConsumer
from core.mongo import collection
from dinar.scripts.flous import parse_log_entry  # assuming you use this function

class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.keep_streaming = True
        await self.accept()
        asyncio.create_task(self.stream_logs())

    async def disconnect(self, close_code):
        self.keep_streaming = False

    async def stream_logs(self):
        log_file_path = "/home/wadii/code/python/dj-test-slaff/dinar/logs/test.txt"

        with open(log_file_path, "r") as f:
            # Go to the end of the file
            f.seek(0, os.SEEK_END)

            while self.keep_streaming:
                position = f.tell()
                line = f.readline()

                if not line:
                    await asyncio.sleep(0.5)
                    f.seek(position)  # go back to the last position
                    continue

                log_dict = parse_log_entry(line.strip())

                # Insert into MongoDB without blocking
                result = await asyncio.to_thread(collection.insert_one, log_dict)
                
                log_dict["_id"] = str(result.inserted_id)

                # Send to frontend
                await self.send(text_data=json.dumps(log_dict))
