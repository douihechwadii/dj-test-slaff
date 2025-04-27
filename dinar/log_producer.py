import asyncio
import json
import os

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from pymongo import MongoClient

#! There's an error here preventing the logs from being sent and even redigtered in the database

# MongoDB setup
mongo_client = MongoClient("mongodb://localhost:27017/")
db = mongo_client["fortigate_logs"]
collection = db["logs"]

# File to read logs from
LOG_FILE_PATH = "/home/wadii/code/python/dj-test-slaff/dinar/logs/test.txt"

async def produce_logs():
    """Background task to read logs, insert to Mongo, and send to channel group."""
    channel_layer = get_channel_layer()

    while True:
        if not os.path.exists(LOG_FILE_PATH):
            await asyncio.sleep(1)
            continue

        with open(LOG_FILE_PATH, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Convert log line to dictionary
                log_dict = parse_log_line(line)

                # Insert into MongoDB
                result = collection.insert_one(log_dict)
                
                log_dict["_id"] = str(result.inserted_id)
                # Send to group
                await channel_layer.group_send(
                    "logs_group",
                    {
                        "type": "send_log",
                        "log": log_dict
                    }
                )
                await asyncio.sleep(1)  # slow down to simulate real-time logs
        await asyncio.sleep(1)

def parse_log_line(line):
    """Simple parser to convert log text to dict."""
    parts = line.split(" ")
    log_dict = {}
    for part in parts:
        if '=' in part:
            key, value = part.split('=', 1)
            log_dict[key] = value.strip('"')
    return log_dict

def start_log_producer():
    """Start the background async task."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(produce_logs())
