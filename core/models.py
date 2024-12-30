from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, values=None, config=None):
        # You can ignore 'values' and 'config' by not using them
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)


class PaginationInfoModel(BaseModel):
    total_count: int = Field(..., description="Total number of records")
    total_pages: int = Field(..., description="Total number of pages")
    page: int = Field(..., description="Current page number")
    limit: int = Field(..., description="Number of records per page")
    has_next: bool = Field(..., description="Indicates if there are more pages")
    has_previous: bool = Field(..., description="Indicates if there are previous pages")
    
