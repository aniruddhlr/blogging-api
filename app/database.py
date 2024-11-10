from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_URI, DATABASE_NAME

client = AsyncIOMotorClient(MONGO_URI)
database = client[DATABASE_NAME]

async def get_collection(collection_name: str):
    return database[collection_name]
