import pymongo
from pymongo import MongoClient
import dotenv
import os

dotenv.load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB = os.getenv("MONGODB_DB")

def connectDB():
    client = MongoClient(MONGODB_URI)
    db = client.get_database("webchat-app")
    return db