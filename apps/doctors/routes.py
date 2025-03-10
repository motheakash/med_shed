from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from typing import Dict, List

from .models import DoctorBaseModel, DoctorCreateModel, DoctorResponseModel, PaginatedResponseModel
from .services import DoctorService
from core.utils import PaginatedResponse
from apps.auth.permissions import is_authenticated, role_required


router = APIRouter()
# doctor_service = DoctorService()


@router.post("/", response_model=DoctorResponseModel, dependencies=[Depends(role_required(["doctor", "admin"]))])
async def signup_doctor(doctor: DoctorCreateModel, user: dict = Depends(is_authenticated)):
    service_class = DoctorService()

    created_doctor = await service_class.create_doctor(doctor)

    return DoctorResponseModel(**created_doctor)


@router.get("/", response_model=PaginatedResponseModel, dependencies=[Depends(role_required(["doctor", "admin"]))])
async def get_doctor_api(
    service_class: DoctorService = Depends(DoctorService),
    page: int = Query(1, ge=1, description="Page number, starting from 1"),
    limit: int = Query(10, le=100, description="Number of records per page"),
    user: dict = Depends(is_authenticated)
):
    doctors, total_count = await service_class.get_all_doctors(page=page, limit=limit)
    
    response = PaginatedResponse(doctors, total_count, page, limit)
    return response.get_paginated_response()
