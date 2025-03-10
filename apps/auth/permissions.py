from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from core.config import SIMPLE_JWT
import jwt

security = HTTPBearer()

def is_authenticated(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Extracts and verifies JWT from Authorization header"""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SIMPLE_JWT['SECRETE_KEY'], algorithms=[SIMPLE_JWT['JWT_ALGORITHM']])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def role_required(required_role: list):
    def check_role(user_data: dict = Depends(is_authenticated)):
        """Check if the user has the required role"""
        user_role = user_data.get("role")
        if user_role not in required_role:
            raise HTTPException(status_code=403, detail="Access denied: Insufficient permissions")
        return user_data
    return check_role
