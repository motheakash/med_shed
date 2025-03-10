from fastapi import APIRouter, HTTPException
from .models import LoginRequestModel, LoginResponseModel, DoctorResponseModel
from .services import LoginService

router = APIRouter()

@router.post("/login", response_model=LoginResponseModel)
async def login(request: LoginRequestModel):
    service_class = LoginService()
    
    try:
        doctor, access_token = await service_class.validate_login(request)
        return LoginResponseModel(member=DoctorResponseModel(**doctor), access_token=access_token)
    except HTTPException as e:
        raise e  