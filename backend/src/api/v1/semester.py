import logging
from typing import List
from uuid import UUID
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from src.db.database import get_db
from src.schemas.semester import SemesterCreate, SemesterUpdate, SemesterRead, SemesterBase
from src.services.semester import SemesterService

class SemesterRouter:
    def __init__(self):
        self.logger = logging.getLogger("Semester Router")
        self.router = APIRouter(prefix="/api/v1/semester", tags=["Semester"])

        self.router.add_api_route(
            "/new",
            self.create_semester,
            methods=["POST"],
            response_model=SemesterRead,
            status_code=status.HTTP_201_CREATED
        )
        self.router.add_api_route(
            "/{semester_id}",
            self.get_semester_by_id,
            methods=["GET"],
            response_model=SemesterRead,
            status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/all",
            self.list_semesters,
            methods=["GET"],
            response_model=List[SemesterBase],
            status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/{semester_id}",
            self.update_semester,
            methods=["PATCH"],
            response_model=SemesterRead,
            status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/{semester_id}",
            self.delete_semester,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT
        )


    def create_semester(self, semester_data: SemesterCreate, db: Session = Depends(get_db)):
        try:
            service = SemesterService(db)
            semester = service.create_semester(**semester_data.dict())
            return semester

        except Exception as e:
            self.logger.error(f"Failed to create semester: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def get_semester_by_id(self, semester_id: UUID, db: Session = Depends(get_db)):
        try:
            service = SemesterService(db)
            semester = service.get_semester_by_id(semester_id)

            if not semester:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Semester not found"
                )
            return semester
        except HTTPException:
            raise

        except Exception as e:
            self.logger.error(f"Failed to fetch semester {semester_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def list_semesters(self, db: Session = Depends(get_db)):
        try:
            service = SemesterService(db)
            semesters = service.list_semesters()

            if semesters is None:
                return []
            return semesters
        except Exception as e:
            self.logger.error(f"Failed to list semesters: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def update_semester(self, semester_id: UUID, semester_data: SemesterUpdate, db: Session = Depends(get_db)):
        try:
            service = SemesterService(db)
            updated_semester = service.update_semester(
                semester_id=semester_id,
                **semester_data.dict(exclude_unset=True)
            )
            if not updated_semester:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Semester with id {semester_id} not found"
                )
            return updated_semester

        except HTTPException:
            raise

        except Exception as e:
            self.logger.error(f"Failed to update semester {semester_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def delete_semester(self, semester_id: UUID, db: Session = Depends(get_db)):
        try:
            service = SemesterService(db)
            deleted = service.delete_semester(semester_id)

            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Semester with id {semester_id} not found"
                )
            return None  # 204 No Content
        except HTTPException:
            raise

        except Exception as e:
            self.logger.error(f"Failed to delete semester {semester_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
