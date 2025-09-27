from sqlalchemy.orm import Session
from backend.src.db.models import Exam

class ExamService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.logger = logging.getLogger("Exam Service")

    def create_exam(self, subject: str, title: str, duration: str = "2h"):
        try:
            exam = Exam(
                subject=subject,
                title=title,
                duration=duration
            )
            self.db.add(exam)
            self.db.commit()
            self.db.refresh(exam)
            return f"Successfully created exam titled: {exam.title}, id:{exam.id}"
        except Exception as e:
            self.logger.error(
                f"Failed to fetch exam with id: {exam_id} : {e}"
            )
            raise ValueError(f"Failed to create exam: {e}")

    def get_exam_by_id(self, exam_id: str):
        try:
            exam = self.db.query(Exam).filter_by(id=exam_id).first()
            return exam
        except Exception as e:
            self.logger.error(
                f"Failed to fetch exam with id: {exam_id} : {e}"
            )
            raise ValueError(f"Failed to fetch exam with id: {exam_id} : {e}")

    def list_exams(self, filters: dict | None, limit: int = 50, offset: int = 0):
        try:
            exams = self.db.query(Exam)
            if filters.subject:
                exams = exams.filter(Exam.subject == filters.subject)
            if filters.title:
                exams = exams.filter(Exam.title.ilike(title))

            query.limit(limit).offset(offset).all()
            return exams
        except Exception as e:
            self.logger.error(
                f"Failed to fetch exam with id: {exam_id} : {e}"
            )
            raise ValueError(f"Failed to fetch exams : {e}")

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
            raise ValueError(f"Failed to fetch exams : {e}")

    def update_exam(self, exam_id: str, subject: str | None, title: str | None):
        try:
            updated_exam = self.db.query(Exam).filter(Exam.id == exam_id)

            if subject:
                updated_exam.subject = subject

            if title:
                updated_exam.title = title

            self.db.add(exam)
            self.db.commit()
            self.db.refresh(exam)
            return True
        except Exception as e:
            self.logger.error(
                f"Failed to fetch exam with id: {exam_id} : {e}"
            )
            raise ValueError(f"Failed to update exam details: {e}")

    def delete_exam(self, exam_id :str):
        try:
            exam = self.db.query(Exam).filter(Exam.id == exam_id)

            if exam:
                self.db.delete(exam)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.logger.error(
                f"Failed to fetch exam with id: {exam_id} : {e}"
            )
            raise ValueError(f"Failed to update exam details: {e}")
