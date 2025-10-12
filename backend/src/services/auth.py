from sqlalchemy.orm import Session
from fastapi import Depends
from backend.src.db.base import get_db
from backend.src.services.user import UserService

class AuthService:
    def __init__(self, user_service: UserService, jwt_handler, password_hasher):
        self.jwt_handler = jwt_handler
        self.password_hasher = password_hasher.PasswordHasher()
        self.user_service = user_service

    def register_user(self, name: str,email: str, password: str, role: str = "student"):
        existing_user = self.user_service.get_user_by_email(email)
        if existing_user:
            raise ConflictError("User already exists")

        hashed_pw = self.password_hasher.get_password_hash(password)
        user = self.user_service.create_user(name, email, hashed_pw, role)

        return {"id": user.id, "email": user.email, "role": user.role}

    def login_user(self, email: str, password: str):
        user = self.user_service.get_user_by_email(email)
        if not user:
            raise AuthError("Invalid credentials")

        if not self.password_hasher.verify_password(password, user.password):
            raise AuthError("Invalid credentials")

        token = self.jwt_handler.create_access_token({"user_id": user.id, "role": user.type})
        return {"access_token": token, "token_type": "bearer"}

    def verify_token(self, token: str):
        payload = self.jwt_handler.verify_token(token)
        if payload is None:
            raise AuthError("Invalid or expired token")

        user = self.user_service.get_user_by_id(payload["user_id"])
        if not user:
            raise AuthError("User not found")

        return user
