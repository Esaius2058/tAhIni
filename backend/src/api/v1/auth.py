import logging
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends, HTTPException, status
from src.db.database import get_db
from sqlalchemy.orm import Session
from src.schemas.auth import (RegisterUserRequest, RegisterUserResponse, LoginUserRequest, LoginUserResponse,
                              AuthenticatedUser)
from src.utils.jwt_handler import JWTHandler
from src.utils.password_hasher import PasswordHasher
from src.services.auth import AuthService
from src.services.user import UserService

class AuthRouter:
    def __init__(self):
        self.logger = logging.getLogger("Auth Router")
        self.oauth2_scheme = OAuth2PasswordBearer(token_url="/v1/auth/login")
        self.router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

        self.router.add_api_route(
            "/register",
            self.register_user,
            response_model=RegisterUserResponse,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"]
        )
        self.router.add_api_route(
            "/login",
            self.login_user,
            response_model=LoginUserResponse,
            status_code=status.HTTP_200_OK,
            methods=["POST"]
        )
        self.router.add_api_route(
            "/me",
            self.verify_token,
            response_model=AuthenticatedUser,
            status_code=status.HTTP_200_OK,
            methods=["GET"]
        )

    def get_auth_service(self, db: Session) -> AuthService:
        user_service = UserService(db)
        jwt_handler = JWTHandler()
        password_hasher = PasswordHasher()
        return AuthService(user_service, jwt_handler, password_hasher)

    async def register_user(
        self,
        payload: RegisterUserRequest,
        db: Session=Depends(get_db),
    ):
        service = self.get_auth_service(db)
        try:
            user = service.register_user(payload.name, payload.email, payload.password, payload.role)
            return user
        except Exception as e:
            self.logger.error(f"Failed to register user: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    async def login_user(
        self,
        payload: LoginUserRequest,
        db: Session=Depends(get_db),
    ):
        service = self.get_auth_service(db)
        try:
            session = service.login_user(payload.email, payload.password)
            return session
        except Exception as e:
            self.logger.error(f"Failed to log in user: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    async def verify_token(
        self,
        token: str = Depends(OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")),
        db: Session=Depends(get_db),
    ):
        service = self.get_auth_service(db)
        try:
            user = service.verify_token(token)
            if not user:
                raise HTTPException(status_code=status. HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
            return user
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to verify user: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
