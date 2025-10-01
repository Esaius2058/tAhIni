import logging
from sqlalchemy.orm import Session
from backend.src.db.models import GradeLog
from backend.src.services.questions import ServiceError, NotFoundError

class GradeLogService:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def create_grade_log(self, user_id: str, exam_id: str, grade: float):
        try:
            grade_log = GradeLog(user_id=user_id, exam_id=exam_id, grade=grade)
            self.db.add(grade_log)
            self.db.commit()
            self.db.refresh(grade_log)
            return grade_log
        except Exception as e:
            self.logger.error(f"Create grade log failed: {e}")
            raise ServiceError("Could not create grade log") from e

    def get_grade_log(self, grade_log_id: str):
        try:
            grade_log = self.db.query(GradeLog).filter(GradeLog.id == grade_log_id).first()
            if not grade_log:
                raise NotFoundError("GradeLog not found")
            return grade_log
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Get grade log failed: {e}")
            raise ServiceError("Could not fetch grade log") from e

    def update_grade_log(self, grade_log_id: str, **kwargs):
        try:
            grade_log = self.get_grade_log(grade_log_id)
            for key, value in kwargs.items():
                setattr(grade_log, key, value)
            self.db.commit()
            self.db.refresh(grade_log)
            return grade_log
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Update grade log failed: {e}")
            raise ServiceError("Could not update grade log") from e

    def list_grades(self, limit: int = 25, offset: int = 0):
        try:
            grades = self.db.query(GradeLog).limit(limit).offset(offset).all()

            return [{
                "grade_id": grade.id,
                "score": grade.score,
                "grader": grade.grader,
                "details": grade.details,
                "graded_at": grade.graded_at
            } for grade in grades
            ]
        except Exception as e:
            self.logger.error(f"List grade logs failed: {e}")
            raise ServiceError("Could not list grade logs") from e

    def delete_grade_log(self, grade_log_id: str):
        try:
            grade_log = self.get_grade_log(grade_log_id)
            self.db.delete(grade_log)
            self.db.commit()
            return True
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Delete grade log failed: {e}")
            raise ServiceError("Could not delete grade log") from e
