from sqlalchemy.orm import Session
import logging
from src.utils.exceptions import AuthError, ConflictError, ServiceError, NotFoundError
from src.services.user import UserService
from src.db.models.models import UserType

class AuthService:
    def __init__(self, user_service: UserService, jwt_handler, password_hasher):
        self.logger = logging.getLogger("Auth Service")
        self.jwt_handler = jwt_handler
        self.password_hasher = password_hasher
        self.user_service = user_service

    def register_user(self, name: str, email: str, password: str, role: UserType = UserType.STUDENT):
        try:
            hashed_pw = self.password_hasher.get_password_hash(password)
            user = self.user_service.create_user(name, email, hashed_pw, role)

            return {"id": user.id, "email": user.email, "role": user.type}

        except (ConflictError, ServiceError):
            raise
        except Exception as e:
            self.logger.error(f"Register user failed: {e}")
            raise ServiceError("Could not register user") from e

    def login_user(self, email: str, password: str):
        try:
            user = self.user_service.get_user_by_email(email)
            if not self.password_hasher.verify_password(password, user.password):
                raise AuthError("Invalid credentials")

            token = self.jwt_handler.create_access_token(
                {"user_id": user.id, "role": user.type}
            )
            return {"access_token": token, "token_type": "bearer"}

        except NotFoundError:
            raise AuthError("Invalid credentials")
        except AuthError:
            raise
        except Exception as e:
            self.logger.error(f"Login user failed: {e}")
            raise ServiceError("Could not log in user") from e

    def verify_token(self, token: str):
        try:
            payload = self.jwt_handler.verify_token(token)
            if payload is None:
                raise AuthError("Invalid or expired token")

            user = self.user_service.get_user_by_id(payload["user_id"])
            return user

        except NotFoundError:
            raise AuthError("User not found")
        except AuthError:
            raise
        except Exception as e:
            self.logger.error(f"Token verification failed: {e}")
            raise ServiceError("Could not verify token") from e
