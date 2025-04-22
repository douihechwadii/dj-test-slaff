# myapp/mongo.py
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["fortigate_logs"]
collection = db["logs"]
