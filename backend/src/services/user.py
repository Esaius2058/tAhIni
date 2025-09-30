from sqlalchemy.orm import Session
from fastapi import APIRouter
import logging
from backend.src.db.models import User
from backend.src.services.questions import ServiceError, NotFoundError, ValidationError

class UserService:
    def __init__(self, db_session: Session):
        self.logger = logging.getLogger("User Service")
        self.router = APIRouter()
        self.db = db_session

    def create_user(self, name: str, email: str, user_type :str = "student"):
        try:
            user = User(
                name=name,
                email=email,
                type=user_type
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Failed to create user {name}: {e}")
            raise ServiceError("Could not create user") from e

    def get_user_by_id(self, user_id: str):
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            if not user:
                raise NotFoundError(f"User {user_id} not found")
            return user
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Get user by ID failed: {e}")
            raise ServiceError("Could not fetch user by id") from e

    def get_user_by_email(self, email: str):
        try:
            user = self.db.query(User).filter(User.email == email).first()
            if not user:
                raise NotFoundError(f"User with email {email} not found")
            return user
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Get user by email failed: {e}")
            raise ServiceError("Could not fetch user by email") from e

    def update_user_type(self, user_id: str, user_type = None, email = None):
        try:
            user = self.get_user_by_id(user_id)

            if user_type:
                user.type = user_type

            if email:
                user.email = email
        except NotFoundError as nf:
            raise
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Update user failed: {e}")
            raise ServiceError("Could not update user") from e

    def delete_user(self, user_id: str):
        try:
            user = self.get_user_by_id(user_id)

            if user:
                self.db.delete(user)
                self.db.commit()
                return True
            return False
        except NotFoundError:
            raise
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Delete user failed: {e}")
            raise ServiceError("Could not delete user") from e

    def list_users(self, role: str = None, limit :int=25, offset=0):
        try:
            query = self.db.query(User)
            if role:
                query = query.filter(User.type == role)

            users = query.limit(limit).offset(offset).all()
            return users
        except Exception as e:
            self.logger.error(f"List users failed: {e}")
            raise ServiceError("Could not list users") from e