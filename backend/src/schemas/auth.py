from pydantic import BaseModel, EmailStr, Field, ConfigDict
from src.db.models import UserType
from datetime import datetime
from uuid import UUID

class RegisterUserRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "name": "Jean Dawson",
                "email": "jean@gmail.com",
                "password": "jnjkavlko939",
                "type": "student"
            }
        })

    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    type: UserType = UserType.STUDENT


class RegisterUserResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "a4f9f1bc-0d5e-4d8d-8b9a-c9f84a4a13f4",
                "email": "jean@example.com",
                "type": "student"
            }
        })

    id: UUID
    email: EmailStr
    type: UserType

class LoginUserRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "jane@gmail.com",
                "password": "jrkls234k"
            }
        })

    email: EmailStr = Field(..., example="isaiah@example.com")
    password: str = Field(..., min_length=6, example="StrongPass123")


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: EmailStr
    type: UserType
    created_at: datetime

class LoginUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    access_token: str
    token_type: str
    user: UserOut

class AuthenticatedUser(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra = {
            "example": {
                "id": "a4f9f1bc-0d5e-4d8d-8b9a-c9f84a4a13f4",
                "name": "Isaiah Maina",
                "email": "isaiah@example.com",
                "type": "student"
            }
        })

    id: UUID = Field(..., example="a4f9f1bc-0d5e-4d8d-8b9a-c9f84a4a13f4")
    name: str = Field(..., example="Isaiah Maina")
    email: EmailStr = Field(..., example="isaiah@example.com")
    type: UserType = Field(..., example="student")
