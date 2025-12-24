from pydantic import BaseModel, Field, EmailStr
from datetime import datetime
from src.db.models import UserType
from uuid import UUID
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class UserRead(UserBase):
    id: UUID
    type: UserType
    created_at: Optional[datetime]

class UpdateEmailRequest(BaseModel):
    email: EmailStr

class UpdateUserTypeRequest(BaseModel):
    type: UserType
