from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings

# MongoDB Configuration
MONGO_URI = settings.MONGO_URI
DATABASE_NAME = settings.DATABASE_NAME

# Synchronous MongoDB Client (rarely used)
mongo_client = MongoClient(MONGO_URI)
sync_db = mongo_client[DATABASE_NAME]

# Asynchronous MongoDB Client
async_client = AsyncIOMotorClient(MONGO_URI)
db = async_client[DATABASE_NAME]
async_db = db

def get_collection(collection_name: str):
    """
    Utility function to get a specific MongoDB collection.
    :param collection_name: The name of the collection to retrieve.
    :return: MongoDB collection object.
    """
    return db[collection_name]
