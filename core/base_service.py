from typing import List, Optional, Type, TypeVar
from bson import ObjectId
from pymongo.collection import Collection
from datetime import datetime

# Create a type variable for model
T = TypeVar("T")

class BaseService:
    def __init__(self, collection: Collection):
        self.collection = collection

    def _get_collection(self):
        return self.collection

    async def insert_one(self, data: dict) -> dict:
        """Insert a new document into the collection."""
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        data["deleted_at"] = None
        result = await self.collection.insert_one(data)
        return {**data, "_id": result.inserted_id}

    async def aggregate(self, pipeline: list) -> list:
        deleted_filter = {"$match": {"deleted_at": None}}
        pipeline.insert(0, deleted_filter)
        cursor = self.collection.aggregate(pipeline)
        return await cursor.to_list(length=None)

    async def find_one(self, object_id: str) -> Optional[dict]:
        """Fetch a document by its ObjectId."""
        obj = await self.collection.find_one({"_id": ObjectId(object_id)})
        return obj

    async def update_one(self, object_id: str, data: dict) -> Optional[dict]:
        """Update an existing document."""
        data["updated_at"] = datetime.utcnow()
        result = await self.collection.update_one({"_id": ObjectId(object_id)}, {"$set": data})
        if result.modified_count > 0:
            return await self.get(object_id)
        return None

    async def soft_delete_one(self, object_id: str) -> bool:
        """Soft delete a document by updating `deleted_at` field."""
        result = await self.collection.update_one(
            {"_id": ObjectId(object_id)}, {"$set": {"deleted_at": datetime.utcnow()}}
        )
        return result.modified_count > 0

    async def list(self, skip: int = 0, limit: int = 10) -> List[dict]:
        """Fetch multiple documents with pagination."""
        cursor = self.collection.find().skip(skip).limit(limit)
        return await cursor.to_list(length=limit)
