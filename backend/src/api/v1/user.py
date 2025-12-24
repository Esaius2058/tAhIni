import logging
from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.services.user import UserService
from src.db.models.models import UserType
from src.schemas.user import UserRead, UpdateEmailRequest, UpdateUserTypeRequest

class UserRouter:
    def __init__(self):
        self.logger = logging.getLogger("User Router")
        self.router = APIRouter(prefix="/api/v1/user", tags=["User"])

        self.router.add_api_route(
            "/by-id/{user_id}/",
            self.get_user_by_id,
            response_model=UserRead,
            methods=["GET"],
            status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/by-email/{email}/",
            self.get_user_by_email,
            response_model=UserRead,
            methods=["GET"],
            status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/{user_id}/email/",
            self.update_user_email,
            methods=["PATCH"],
            response_model=UpdateEmailRequest,
            status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/{user_id}/type",
            self.update_user_type,
            methods=["PATCH"],
            response_model=UpdateUserTypeRequest,
            status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/all/",
            self.get_all_users,
            response_model=List[UserRead],
            methods=["GET"]
        )
        self.router.add_api_route(
            "/student/all/",
            self.get_all_students,
            response_model=List[UserRead],
            methods=["GET"]
        )
        self.router.add_api_route(
            "/instructor/all/",
            self.get_all_instructors,
            response_model=List[UserRead],
            methods=["GET"]
        )
        self.router.add_api_route(
            "/admin/all/",
            self.get_all_admins,
            response_model=List[UserRead],
            methods=["GET"]
        )

    def get_user_by_id(self, user_id: UUID, db: Session=Depends(get_db)):
        service = UserService(db)
        try:
            user = service.get_user_by_id(user_id)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return user
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to fetch user {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def get_user_by_email(self, email: str, db: Session=Depends(get_db)):
        service = UserService(db)
        try:
            user = service.get_user_by_email(email)
            if not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
            return user
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to fetch user with email {email}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def update_user_type(self, user_id: UUID, payload: UpdateUserTypeRequest,db: Session=Depends(get_db)):
        service = UserService(db)
        try:
            updated_user = service.update_user_type(user_id, payload.type)
            return updated_user
        except Exception as e:
            self.logger.error(f"Failed to update user type for user {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def update_user_email(self, user_id: UUID, payload: UpdateEmailRequest,db: Session=Depends(get_db)):
        service = UserService(db)
        try:
            updated_user = service.update_user_email(user_id, payload.email)
            return updated_user
        except Exception as e:
            self.logger.error(f"Failed to update email for user {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def get_all_users(self, db: Session=Depends(get_db)):
        service = UserService(db)
        try:
            users = service.list_users(limit=50)
            if not users:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Users not found")
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to update user type for user {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def get_all_students(self):
        service = UserService(db)
        try:
            students = service.list_users(role=UserType.STUDENT, limit=50)
            if not students:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Students not found")
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to update user type for user {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def get_all_instructors(self, db: Session=Depends(get_db)):
        service = UserService(db)
        try:
            students = service.list_users(role=UserType.INSTRUCTOR, limit=50)
            if not students:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Instructors not found")
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to update user type for user {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def get_all_admins(self,db: Session=Depends(get_db)):
        service = UserService(db)
        try:
            students = service.list_users(role=UserType.ADMIN, limit=50)
            if not students:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admins not found")
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to update user type for user {user_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
