from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import Dict, List

from .models import DoctorBaseModel, DoctorCreateModel, DoctorResponseModel, PaginatedResponseModel
from .services import DoctorService
from core.utils import PaginatedResponse


router = APIRouter()
# doctor_service = DoctorService()


@router.post("/signup", response_model=DoctorResponseModel)
async def signup_doctor(doctor: DoctorCreateModel, service_class=DoctorService):

    existing_doctor_by_username = await service_class().collection.find_one({"username": doctor.username})

    if existing_doctor_by_username:
        raise HTTPException(status_code=400, detail="Username already exists")

    existing_doctor_by_email = await service_class().collection.find_one({"email": doctor.email})

    if existing_doctor_by_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    created_doctor = await service_class().create_doctor(doctor.dict(by_alias=True))

    return DoctorResponseModel(**created_doctor)


@router.get("/get-doctors", response_model=PaginatedResponseModel)
async def get_doctor_api(
    service_class: DoctorService = Depends(DoctorService),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    limit: int = Query(10, le=100, description="Number of records per page")
):
    # Fetch doctors and total count with pagination
    doctors, total_count = await service_class.get_all_doctors(page=page, limit=limit)
    
    # Use the PaginatedResponse class to return paginated response
    response = PaginatedResponse(doctors, total_count, page, limit)
    return response.get_paginated_response()
