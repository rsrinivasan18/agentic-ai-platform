"""
API routes for authentication.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Dict

from schemas.user_schema import UserCreate, UserResponse
from services.user_service import UserService
from utils.security import verify_password, create_access_token
from core.config import settings

router = APIRouter()


@router.post("/token", response_model=Dict[str, str])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user_service = UserService()

    # Try to authenticate by username
    user = await user_service.get_user_by_username(form_data.username)

    # If not found by username, try by email
    if not user:
        user = await user_service.get_user_by_email(form_data.username)

    # If still not found or password doesn't match, raise exception
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.JWT_EXPIRATION),
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(user_data: UserCreate):
    user_service = UserService()

    try:
        user = await user_service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return user
