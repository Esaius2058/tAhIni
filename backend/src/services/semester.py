import logging
from sqlalchemy.orm import Session
from src.db.models import Semester
from uuid import UUID
from src.utils.exceptions import NotFoundError, ServiceError

class SemesterService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.logger = logging.getLogger("Semester Service")

    def create_semester(self, name: str, start_date, end_date):
        try:
            semester = Semester(
                name=name,
                start_date=start_date,
                end_date=end_date
            )

            self.db.add(semester)
            self.db.commit()
            self.db.refresh(semester)

            return {
                "id": semester.id,
                "name": semester.name,
                "start_date": semester.start_date,
                "end_date": semester.end_date
            }

        except Exception as e:
            self.logger.error(f"Failed to create semester: {e}")
            self.db.rollback()
            raise ServiceError(f"Failed to create semester: {e}")

    def get_semester_by_id(self, semester_id: UUID):
        try:
            semester = self.db.query(Semester).filter_by(id=semester_id).first()
            if not semester:
                raise NotFoundError(f"Semester {semester_id} not found")
            return semester

        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to fetch semester with id {semester_id}: {e}")
            raise ServiceError(f"Failed to fetch semester {semester_id}")

    def list_semesters(self, name: str | None = None, limit: int = 50, offset: int = 0):
        try:
            query = self.db.query(Semester)

            if name:
                query = query.filter(Semester.name.ilike(f"%{name}%"))

            semesters = query.limit(limit).offset(offset).all()
            return semesters

        except Exception as e:
            self.logger.error(f"Failed to list semesters: {e}")
            raise ServiceError(f"Failed to list semesters: {e}")

    def update_semester(self, semester_id: str, name: str | None = None,
                        start_date=None, end_date=None):
        try:
            semester = self.db.query(Semester).filter_by(id=semester_id).first()
            if not semester:
                raise NotFoundError(f"Semester {semester_id} not found")

            if name:
                semester.name = name
            if start_date:
                semester.start_date = start_date
            if end_date:
                semester.end_date = end_date

            self.db.add(semester)
            self.db.commit()
            self.db.refresh(semester)
            return semester

        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to update semester {semester_id}: {e}")
            self.db.rollback()
            raise ServiceError(f"Failed to update semester {semester_id}: {e}")

    def delete_semester(self, semester_id: UUID):
        try:
            semester = self.db.query(Semester).filter_by(id=semester_id).first()
            if not semester:
                raise NotFoundError(f"Semester {semester_id} not found")

            self.db.delete(semester)
            self.db.commit()
            return True

        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to delete semester {semester_id}: {e}")
            self.db.rollback()
            raise ServiceError(f"Failed to delete semester {semester_id}: {e}")

    def get_semester_exams(self, semester_id: UUID):
        try:
            semester = self.db.query(Semester).filter_by(id=semester_id).first()
            if not semester:
                raise NotFoundError(f"Semester {semester_id} not found")

            return semester.exams

        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to fetch exams for semester {semester_id}: {e}")
            raise ServiceError(f"Failed to fetch exams for semester {semester_id}: {e}")
