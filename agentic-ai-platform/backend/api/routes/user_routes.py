"""
API routes for user management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from models.user_model import User
from schemas.user_schema import UserCreate, UserResponse, UserUpdate
from services.user_service import UserService
from utils.security import get_current_user

router = APIRouter()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    user_service = UserService()
    user = await user_service.create_user(user_data)
    return user


@router.get("/", response_model=List[UserResponse])
async def get_users(current_user: User = Depends(get_current_user)):
    user_service = UserService()
    users = await user_service.get_users()
    return users


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, current_user: User = Depends(get_current_user)):
    user_service = UserService()
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str, user_data: UserUpdate, current_user: User = Depends(get_current_user)
):
    # Only allow users to update their own data or admin users
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this user",
        )

    user_service = UserService()
    updated_user = await user_service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str, current_user: User = Depends(get_current_user)):
    # Only allow users to delete their own account
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this user",
        )

    user_service = UserService()
    deleted = await user_service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return None
