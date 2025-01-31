from core.base_service import BaseService
from .models import DoctorCreateModel, DoctorBaseModel, DoctorResponseModel
from core.database import async_db
from datetime import datetime
from typing import Optional, List, Tuple
from passlib.context import CryptContext



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str:
    """Hash the given password."""
    return pwd_context.hash(password)

class DoctorService(BaseService):
    def __init__(self):
        super().__init__(async_db["Doctors"])

    async def create_doctor(self, doctor_data: DoctorCreateModel | dict) -> dict:
        doctor_data['is_active'] = False   # without email varification it should be false
        doctor_data['password'] = hash_password(doctor_data['password'])
        if not isinstance(doctor_data, DoctorCreateModel):
            doctor_data = DoctorCreateModel(**doctor_data)

        doctor_dict = doctor_data.dict(by_alias=True, exclude_unset=True)
        return await self.insert_one(doctor_dict)


    async def get_doctor(self, doctor_id: str) -> Optional[DoctorBaseModel]:
        """
        Retrieve a doctor by ID.
        """
        doctor = await self.find_one(doctor_id)  
        if doctor:
            return DoctorBaseModel(**doctor)  
        return None
    
    async def get_all_doctors(self, page: int = 1, limit: int = 10) -> Tuple[List[DoctorResponseModel], int]:
        skip = (page - 1) * limit
        
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
        
        result  = await self.aggregate(pipeline)
        
        doctors = result[0].get("doctors", [])
        total_count = result[0].get("total_count", [{"count": 0}])[0].get("count", 0)
        
        return doctors, total_count

    async def update_doctor(self, doctor_id: str, doctor_data: DoctorCreateModel) -> Optional[DoctorCreateModel]:
        """
        Update a doctor's information.
        """
        updated_data = doctor_data.dict(by_alias=True, exclude_unset=True)  
        updated_data["updated_at"] = datetime.utcnow()
        updated_doc = await self.update(doctor_id, updated_data)  
        if updated_doc:
            return DoctorBaseModel(**updated_doc)
        return None

    async def delete_doctor(self, doctor_id: str) -> bool:
        """
        Soft delete a doctor by marking the `deleted_at` field.
        """
        updated_doc = await self.update(doctor_id, {"deleted_at": datetime.utcnow()})  
        return bool(updated_doc)  


