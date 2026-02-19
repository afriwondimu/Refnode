from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime
import re

class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = True
    
    @validator('username')
    def validate_username(cls, v):
        if v:
            if not re.match("^[a-zA-Z0-9_.-]+$", v):
                raise ValueError('Username can only contain letters, numbers, dots, underscores and hyphens')
        return v

class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str = Field(..., min_length=8)
    referral_code: Optional[str] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime
    reward_points: int
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginRequest(BaseModel):
    username: str
    password: str