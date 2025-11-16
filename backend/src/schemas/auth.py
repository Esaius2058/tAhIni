from pydantic import BaseModel, EmailStr, Field
from src.db.models import UserType

class RegisterUserRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: UserType = UserType.STUDENT

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jean Dawson",
                "email": "jean@gmail.com",
                "password": "jnjkavlko939",
                "role": "student"
            }
        }

class RegisterUserResponse(BaseModel):
    id: str
    email: EmailStr
    role: UserType

    class Config:
        json_schema_extra = {
            "example": {
                "id": "a4f9f1bc-0d5e-4d8d-8b9a-c9f84a4a13f4",
                "email": "jean@example.com",
                "role": "student"
            }
        }

class LoginUserRequest(BaseModel):
    email: EmailStr = Field(..., example="isaiah@example.com")
    password: str = Field(..., min_length=6, example="StrongPass123")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "jane@gmail.com",
                "password": "jrkls234k"
            }
        }

class LoginUserResponse(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(default="bearer", example="bearer")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class AuthenticatedUser(BaseModel):
    id: str = Field(..., example="a4f9f1bc-0d5e-4d8d-8b9a-c9f84a4a13f4")
    name: str = Field(..., example="Isaiah Maina")
    email: EmailStr = Field(..., example="isaiah@example.com")
    role: UserType = Field(..., example="student")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "a4f9f1bc-0d5e-4d8d-8b9a-c9f84a4a13f4",
                "name": "Isaiah Maina",
                "email": "isaiah@example.com",
                "role": "student"
            }
        }