import logging
from sqlalchemy.orm import Session
from src.db.models import Exam, Question, ExamSession, ExamStatus
from src.utils.exceptions import NotFoundError, ServiceError

class ExamService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.logger = logging.getLogger("Exam Service")

    def create_exam(self, subject: str, title: str, course_id: str, semester_id: str, duration: str = "2h"):
        try:
            exam = Exam(
                subject=subject,
                title=title,
                course_id=course_id,
                semester_id=semester_id,
                duration=duration
            )
            self.db.add(exam)
            self.db.commit()
            self.db.refresh(exam)
            return {
                "title": exam.title,
                "subject": exam.subject,
                "duration": exam.duration
            }
        except Exception as e:
            self.logger.error(
                f"Failed to fetch exam with id: {exam_id} : {e}"
            )
            self.db.rollback()
            raise ServiceError(f"Failed to create exam: {e}")

    def get_exam_by_id(self, exam_id: str):
        try:
            exam = self.db.query(Exam).filter_by(id=exam_id).first()
            if not exam:
                raise NotFoundError(f"Exam {exam_id} not found")
            return exam
        except Exception as e:
            self.logger.error(
                f"Failed to fetch exam with id: {exam_id} : {e}"
            )
            raise ServiceError(f"Failed to fetch exam with id: {exam_id} : {e}")

    def get_exams_by_course(self, course_id: str, semester_id: str):
        try:
            exams = self.db.query(Exam).filter(Exam.course_id == course_id, Exam.semester_id == semester_id).all()
            if not exams:
                raise NotFoundError(f"Exams for course {course_id} in semester {semester_id} not found")
            return exams
        except Exception as e:
            self.logger.error(
                f"Failed to fetch exams for course: {course_id} : {e}"
            )
            raise ServiceError(f"Failed to fetch exam for course: {course_id} : {e}")

    def add_question_to_exam(self, question_id, exam_id):
        try:
            question = self.db.query(Question).filter(Question.id == question_id).first()
            if not question:
                raise NotFoundError(f"Question {question_id} not found")

            question.exam_id = exam_id
            self.db.add(question)
            self.db.commit()
            self.db.refresh(question)
            return question
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to add question {question_id} to exam: {e}")
            self.db.rollback()
            raise ServiceError(f"Failed to add question {question_id} to exam: {e}")

    def delete_question_from_exam(self, question_id, exam_id):
        try:
            question = (
                self.db.query(Question)
                .filter(Question.id == question_id, Question.exam_id == exam_id)
                .first()
            )
            if not question:
                raise NotFoundError(f"Question {question_id} not found")

            question.exam_id = None
            self.db.add(question)
            self.db.commit()
            self.db.refresh(question)
            return True
        except Exception as e:
            self.logger.error(f"Failed to add question to exam: {e}")
            self.db.rollback()
            raise ServiceError(f"Failed to add question to exam: {e}")


    def list_exams(self, subject: str | None = None, title: str | None = None, limit: int = 50, offset: int = 0):
        try:
            query = self.db.query(Exam)
            if subject:
                query = query.filter(Exam.subject == subject)
            if title:
                query = query.filter(Exam.title.ilike(f"%{title}%"))

            exams = query.limit(limit).offset(offset).all()
            return exams
        except Exception as e:
            self.logger.error(f"Failed to list exams: {e}")
            raise ServiceError(f"Failed to list exams: {e}")

    def list_exam_questions(self, exam_id: str):
        try:
            exam = self.db.query(Exam).filter(Exam.id == exam_id).first()
            if not exam:
                return None
            return exam.questions
        except Exception as e:
            self.logger.error(
                f"Failed to list questions from exam id: {exam_id} : {e}"
            )
            raise ServiceError(f"Failed to fetch exams : {e}")

    def update_exam(self, exam_id: str, subject: str | None=None, title: str | None=None):
        try:
            updated_exam = self.db.query(Exam).filter(Exam.id == exam_id).first()

            if subject:
                updated_exam.subject = subject

            if title:
                updated_exam.title = title

            self.db.add(updated_exam)
            self.db.commit()
            self.db.refresh(updated_exam)
            return updated_exam
        except Exception as e:
            self.logger.error(
                f"Failed to fetch exam with id: {exam_id} : {e}"
            )
            raise ServiceError(f"Failed to update exam details: {e}")

    def delete_exam(self, exam_id :str):
        try:
            exam = self.db.query(Exam).filter(Exam.id == exam_id).first()

            if exam:
                self.db.delete(exam)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.logger.error(
                f"Failed to fetch exam with id: {exam_id} : {e}"
            )
            raise ServiceError(f"Failed to update exam details: {e}")

    def start_exam(self, user_id: str, exam_id: str):
        try:
            exam = self.db.query(Exam).filter(Exam.id == exam_id).first()
            if not exam:
                raise NotFoundError("Exam not found")

            existing_session = (
                self.db.query(ExamSession)
                .filter(ExamSession.exam_id == exam_id, ExamSession.student_id == user_id)
                .first()
            )

            if existing_session and existing_session.status == ExamStatus.IN_PROGRESS:
                return existing_session

            new_session = StudentExam(
                exam_id=exam_id,
                student_id=user_id,
                start_time=datetime.utcnow(),
                end_time=datetime.utcnow() + parse_duration(exam.duration),
                status=ExamStatus.IN_PROGRESS
            )

            self.db.add(new_session)
            self.db.commit()
            self.db.refresh(new_session)

            questions = self.db.query(Question).filter(Question.exam_id == exam_id).all()

            return {
                "session_id": new_session.id,
                "exam_title": exam.title,
                "duration": exam.duration,
                "questions": questions
            }
        except Exception as e:
            self.logger.error(f"Failed to start exam {exam_id} for user {user_id}: {e}")
            raise ServiceError("Could not start exam")
