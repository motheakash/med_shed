from apps.doctors.repository import DoctorRepository
from .models import LoginRequestModel
from fastapi import HTTPException
from core.utils import generate_access_token, is_valid_password

class LoginService:
    def __init__(self):
        self.repository = DoctorRepository()

    async def validate_login(self, user_obj: LoginRequestModel):

        doctor = await self.repository.find_by_username(user_obj.username)

        if not doctor:
            raise HTTPException(status_code=404, detail="member not found")
        
        if not is_valid_password(user_obj.password, doctor['password']):
            raise HTTPException(status_code=401, detail="invalid password")

        access_token = generate_access_token(member=doctor)

        return doctor, access_token

