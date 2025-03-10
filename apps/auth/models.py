from pydantic import BaseModel, Field
from apps.doctors.models import DoctorResponseModel



class LoginRequestModel(BaseModel):
    username: str = Field(..., examples="myusername")
    password: str = Field(..., examples="mypassword")

class LoginResponseModel(BaseModel):
    member: DoctorResponseModel
    access_token: str