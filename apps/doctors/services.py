from datetime import datetime
from typing import Optional, List, Tuple
from passlib.context import CryptContext
from .models import DoctorCreateModel, DoctorBaseModel, DoctorResponseModel
from .repository import DoctorRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash the given password."""
    return pwd_context.hash(password)

class DoctorService:
    def __init__(self):
        self.repository = DoctorRepository()

    async def create_doctor(self, doctor_data: DoctorCreateModel | dict) -> dict:
        doctor_data['is_active'] = False
        doctor_data['password'] = hash_password(doctor_data['password'])

        if not isinstance(doctor_data, DoctorCreateModel):
            doctor_data = DoctorCreateModel(**doctor_data)

        doctor_dict = doctor_data.dict(by_alias=True, exclude_unset=True)
        return await self.repository.insert_doctor(doctor_dict)

    async def get_doctor(self, doctor_id: str) -> Optional[DoctorBaseModel]:
        doctor = await self.repository.find_by_id(doctor_id)
        return DoctorBaseModel(**doctor) if doctor else None

    async def get_all_doctors(self, page: int = 1, limit: int = 10) -> Tuple[List[DoctorResponseModel], int]:
        skip = (page - 1) * limit
        doctors, total_count = await self.repository.find_all_doctors(skip, limit)
        return doctors, total_count

    async def update_doctor(self, doctor_id: str, doctor_data: DoctorCreateModel) -> Optional[DoctorBaseModel]:
        updated_data = doctor_data.dict(by_alias=True, exclude_unset=True)
        updated_data["updated_at"] = datetime.utcnow()
        updated_doc = await self.repository.update_doctor(doctor_id, updated_data)
        return DoctorBaseModel(**updated_doc) if updated_doc else None

    async def delete_doctor(self, doctor_id: str) -> bool:
        return await self.repository.soft_delete_doctor(doctor_id)
