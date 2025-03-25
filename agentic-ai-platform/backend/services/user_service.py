"""
User service for handling user-related operations.
"""

from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from models.user_model import User
from schemas.user_schema import UserCreate, UserUpdate
from db.mongodb import get_database
from utils.security import get_password_hash


class UserService:
    def __init__(self):
        self.db = get_database()
        self.collection = self.db.users

    async def create_user(self, user_data: UserCreate) -> User:
        # Check if user with the same email already exists
        existing_user = await self.collection.find_one({"email": user_data.email})
        if existing_user:
            raise ValueError("User with this email already exists")

        # Check if user with the same username already exists
        existing_user = await self.collection.find_one({"username": user_data.username})
        if existing_user:
            raise ValueError("User with this username already exists")

        # Create new user
        user_dict = user_data.dict()

        # Hash the password
        user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))

        # Add timestamps
        now = datetime.now()
        user_dict["created_at"] = now
        user_dict["updated_at"] = now

        # Insert into database
        result = await self.collection.insert_one(user_dict)

        # Get the created user
        created_user = await self.collection.find_one({"_id": result.inserted_id})

        return User(**created_user)

    async def get_users(self) -> List[User]:
        users = []
        async for user in self.collection.find():
            users.append(User(**user))
        return users

    async def get_user(self, user_id: str) -> Optional[User]:
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return User(**user)
        return None

    async def get_user_by_email(self, email: str) -> Optional[User]:
        user = await self.collection.find_one({"email": email})
        if user:
            return User(**user)
        return None

    async def get_user_by_username(self, username: str) -> Optional[User]:
        user = await self.collection.find_one({"username": username})
        if user:
            return User(**user)
        return None

    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            return None

        # Update user data
        update_data = user_data.dict(exclude_unset=True)

        # Hash the password if provided
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(
                update_data.pop("password")
            )

        # Update timestamp
        update_data["updated_at"] = datetime.now()

        # Update in database
        await self.collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )

        # Get the updated user
        updated_user = await self.collection.find_one({"_id": ObjectId(user_id)})

        return User(**updated_user)

    async def delete_user(self, user_id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
