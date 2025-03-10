from core.models import PyObjectId, PaginationInfoModel
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict, List


class AddressModel(BaseModel):
    street: str = Field(..., example="123 Main St")
    city: str = Field(..., example="Mumbai")
    state: str = Field(..., example="Maharashtra")
    country: str = Field(..., example="India")
    postal_code: str = Field(..., example="400001")


class DoctorBaseModel(BaseModel):
    username: str = Field(..., min_length=1, max_length=50, example="username")
    name: str = Field(..., min_length=1, max_length=50, example="Dr. Akash")
    email: EmailStr = Field(..., example="akash@example.com")
    role: str = Field(..., min_length=1, max_length=20, example="admin")
    phone: Optional[str] = Field(..., min_length=10, max_length=50, example="9988776655")
    is_active: Optional[bool] = Field(True, description="Indicates if the doctor is active")
    address: Optional[AddressModel] = Field(
        ...,
        example={
            "street": "123 Main St",
            "city": "Mumbai",
            "state": "Maharashtra",
            "country": "India",
            "postal_code": "400001",
        },
    )
    doctor_info: Optional[Dict[str, Optional[str | int | float]]] = Field(
        ...,
        example={
            "specialization": "Cardiology",
            "experience": 10,
            "rating": 4.5,
        },
        description="Additional doctor details like specialization, experience, etc.",
    )

    class Config:
        arbitrary_types_allowed = True


class DoctorCreateModel(DoctorBaseModel):
    password: str = Field(..., min_length=4, example="password")

class DoctorResponseModel(DoctorBaseModel):
    id: PyObjectId = Field(..., alias="_id", description="Unique identifier")


class PaginatedResponseModel(BaseModel):
    data: List[DoctorResponseModel] = Field(..., description="List of doctors on the current page")
    pagination: PaginationInfoModel = Field(..., description="Pagination metadata")
