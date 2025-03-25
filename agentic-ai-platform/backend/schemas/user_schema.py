"""
User schemas for API requests and responses.
"""

from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    disabled: Optional[bool] = None


class UserResponse(UserBase):
    id: str
    disabled: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
