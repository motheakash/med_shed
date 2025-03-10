from core.database import async_db
from datetime import datetime
from typing import Optional, List, Tuple
from .models import DoctorCreateModel, DoctorBaseModel

class DoctorRepository:
    def __init__(self):
        self.collection = async_db["Doctors"]

    async def find_by_username(self, username: str) -> Optional[dict]:
        return await self.collection.find_one({"username": username})

    async def find_by_email(self, email: str) -> Optional[dict]:
        return await self.collection.find_one({"email": email})

    async def insert_doctor(self, doctor_data: dict) -> dict:
        result = await self.collection.insert_one(doctor_data)
        doctor_data["_id"] = result.inserted_id
        return doctor_data

    async def find_by_id(self, doctor_id: str) -> Optional[dict]:
        return await self.collection.find_one({"_id": doctor_id})

    async def find_all_doctors(self, skip: int, limit: int) -> Tuple[List[dict], int]:
        pipeline = [
            {
                "$facet": {
                    "doctors": [
                        {"$skip": skip},
                        {"$limit": limit}
                    ],
                    "total_count": [
                        {"$count": "count"}
                    ]
                }
            }
        ]
        
        result = await self.collection.aggregate(pipeline).to_list(length=1)
        doctors = result[0].get("doctors", [])
        total_count = result[0].get("total_count", [{"count": 0}])[0].get("count", 0)
        
        return doctors, total_count

    async def update_doctor(self, doctor_id: str, updated_data: dict) -> Optional[dict]:
        result = await self.collection.find_one_and_update(
            {"_id": doctor_id}, 
            {"$set": updated_data},
            return_document=True
        )
        return result

    async def soft_delete_doctor(self, doctor_id: str) -> bool:
        result = await self.collection.find_one_and_update(
            {"_id": doctor_id},
            {"$set": {"deleted_at": datetime.utcnow()}},
            return_document=True
        )
        return result is not None
