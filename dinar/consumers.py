import json
import re
import asyncio
import os
from channels.generic.websocket import AsyncWebsocketConsumer
from functools import lru_cache


@lru_cache(maxsize=None)
def parse_log_entry(log_entry):
    log_dict = {}
    pattern = r'(\w+)="([^"]*)"|(\w+)=([^\s]+)'
    for match in re.finditer(pattern, log_entry):
        key = match.group(1) or match.group(3)
        value = match.group(2) or match.group(4)
        if value.isdigit():
            value = int(value)
        elif value.replace('.', '', 1).isdigit():
            value = float(value)
        log_dict[key] = value
    return log_dict


class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.keep_streaming = True
        self.log_task = asyncio.create_task(self.stream_logs())

    async def disconnect(self, close_code):
        self.keep_streaming = False
        if self.log_task:
            self.log_task.cancel()
            try:
                await self.log_task
            except asyncio.CancelledError:
                pass

    async def receive(self, text_data):
        print("Received from frontend:", text_data)

    async def stream_logs(self):
        log_file_path = "/home/wadii/code/python/dj-test-slaff/dinar/logs/test.txt"  # 👈 Your log file path
        if not os.path.exists(log_file_path):
            await self.send(text_data=json.dumps({"error": "Log file not found"}))
            return

        # Keep track of where we last read
        with open(log_file_path, "r") as f:
            f.seek(0, os.SEEK_END)  # Move to end of file

            while self.keep_streaming:
                line = f.readline()
                if not line:
                    print("Waiting for new log lines...")
                    await asyncio.sleep(1)  # Wait for new lines
                    #await self.send(text_data=json.dumps({"heartbeat": "still alive"}))
                    continue
                print(f"New line: {line.strip()}")  # 👈 Debug output
                log_dict = parse_log_entry(line.strip())
                await self.send(text_data=json.dumps(log_dict))
