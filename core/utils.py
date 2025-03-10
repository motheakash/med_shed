from typing import List, Dict
from .config import SIMPLE_JWT
from datetime import datetime, timedelta, timezone
from apps.doctors.models import DoctorResponseModel
from passlib.context import CryptContext
import jwt
import bcrypt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class PaginatedResponse:
    def __init__(self, items: Dict, total_count: int, page: int, limit: int):
        self.items = items
        self.total_count = total_count
        self.page = page
        self.limit = limit

    def get_paginated_response(self) -> Dict:
        # Calculate pagination metadata
        total_pages = (self.total_count + self.limit - 1) // self.limit  # ceil division
        has_next = self.page < total_pages
        has_previous = self.page > 1

        return {
            "data": self.items,
            "pagination": {
                "total_count": self.total_count,
                "total_pages": total_pages,
                "page": self.page,
                "limit": self.limit,
                "has_next": has_next,
                "has_previous": has_previous
            }
        }


def hash_password(password: str) -> str:
    """Hash the given password."""
    return pwd_context.hash(password)

def generate_access_token(member:DoctorResponseModel) -> str:
    payload = {
        'username': member['username'],
        'email': member['email'],
        'role': member['role'],
        'exp': datetime.now(timezone.utc) + timedelta(minutes=SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']),  # Use timedelta for expiration
        'iat': datetime.now(timezone.utc),
    }
    encoded_jwt = jwt.encode(payload, SIMPLE_JWT['SECRETE_KEY'], algorithm=SIMPLE_JWT['JWT_ALGORITHM'])
    return encoded_jwt


def is_valid_password(provided_password:str, stored_hashed_password:str) -> bool:
    """
    Checks if the provided password matches the stored hashed password.
    """
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hashed_password.encode('utf-8'))