from sqlalchemy.orm import Session
from fastapi import APIRouter
import logging
from uuid import UUID
from src.db.models import User, UserType
from src.utils.exceptions import ServiceError, NotFoundError

class UserService:
    def __init__(self, db_session: Session):
        self.logger = logging.getLogger("User Service")
        self.db = db_session

    def create_user(self, name: str, email: str, pwd: str, user_type: UserType=UserType.STUDENT):
        try:
            user = User(
                name=name,
                email=email,
                password=pwd,
                type=user_type
            )
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Failed to create user {name}: {e}")
            raise ServiceError("Could not create user") from e

    def get_user_by_id(self, user_id: UUID):
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
                self.logger.error(f"User with email {email} not found")
            return user
        except Exception as e:
            self.logger.error(f"Get user by email failed: {e}")
            raise ServiceError("Could not fetch user by email") from e

    def update_user_type(self, user_id: UUID, user_type:UserType):
        try:
            user = self.get_user_by_id(user_id)

            if user_type:
                user.type = user_type

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        except NotFoundError:
            raise
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Update user failed: {e}")
            raise ServiceError("Could not update userm type") from e

    def update_user_email(self, user_id: UUID, email: str):
        try:
            user = self.get_user_by_id(user_id)

            if email:
                user.email = email

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        except NotFoundError:
            raise
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Update user failed: {e}")
            raise ServiceError("Could not update user email") from e

    def update_user_password(self, user_id: UUID, new_password: str):
        try:
            user = self.db.query(User).filter(User.id == user_id).first()

            if not user:
                raise NotFoundError("User not found")

            user.password = new_password

            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
        except NotFoundError:
            raise
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Update user failed: {e}")
            raise ServiceError("Could not update user") from e


    def delete_user(self, user_id: UUID):
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

    def list_users(self, role: UserType = None, limit :int=25, offset=0):
        try:
            query = self.db.query(User)
            if role:
                query = query.filter(User.type == role)

            users = query.limit(limit).offset(offset).all()
            return users
        except Exception as e:
            self.logger.error(f"List users failed: {e}")
            raise ServiceError("Could not list users") from e