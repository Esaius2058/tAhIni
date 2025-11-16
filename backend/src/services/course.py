from sqlalchemy.orm import Session
from backend.src.db.models import Course, Exam, User
from backend.src.services.program import ProgramService
from backend.src.utils.exceptions import ServiceError, NotFoundError
import logging
import uuid

class CourseService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.logger = logging.getLogger("Course Service")
        self.program_service = ProgramService(db_session)

    def create_course(self, course_id: str, name: str, description: str, instructor_id: str):
        try:
            course = Course(
                id=course_id,
                name=name,
                description=description,
                instructor_id=instructor_id
            )
            self.db.add(course)
            self.db.commit()
            self.db.refresh(course)
            return course
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Create course failed: {e}")
            raise ServiceError("Could not create course") from e

    def get_course(self, course_id: str):
        try:
            course = self.db.query(Course).filter(Course.id == course_id).first()
            if not course:
                raise NotFoundError("Course not found")
            return course
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Get course failed: {e}")
            raise ServiceError("Could not fetch course") from e

    def update_course(self, course_id: str, data: dict):
        try:
            course = self.get_course(course_id)
            for key, value in data.items():
                if hasattr(course, key):
                    setattr(course, key, value)
            self.db.commit()
            self.db.refresh(course)
            return course
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Update course failed: {e}")
            raise ServiceError("Could not update course") from e

    def delete_course(self, course_id: str):
        try:
            course = self.get_course(course_id)
            self.db.delete(course)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Delete course failed: {e}")
            raise ServiceError("Could not delete course") from e

    def list_courses(self, limit: int = 25, offset: int = 0):
        try:
            courses = self.db.query(Course).limit(limit).offset(offset).all()

            return [{
                "course_id": course.id,
                "name": course.name,
                "program": self.program_service.get_program(course.program_id).name,
            } for course in courses
            ]
        except Exception as e:
            self.logger.error(f"List courses failed: {e}")
            raise ServiceError("Could not list courses") from e

    def assign_exam(self, course_id: str, exam_id: str):
        try:
            course = self.get_course(course_id)
            exam = self.db.query(Exam).filter(Exam.id == exam_id).first()
            if not exam:
                raise NotFoundError("Exam not found")
            exam.course_id = course.id
            self.db.commit()
            self.db.refresh(exam)
            return exam
        except NotFoundError:
            raise
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Assign exam failed: {e}")
            raise ServiceError("Could not assign exam to course") from e
