import logging
from sqlalchemy.orm import Session
from backend.src.db.base import get_db
from backend.src.services.exam import ExamService
from fastapi import APIRouter

class ExamRouter:
    def __init__(self):
        self.logger = logging.getLogger("Exam Router")
        self.db = get_db()
        self.router = APIRouter()
        self.router.add_api_route("/exam/{id}", self.get_exam_by_id)
        self.exam_service = ExamService(self.db)

    def get_exam_by_id(self, exam_id: str):
        try:
            exam = self.exam_service.get_exam_by_id(exam_id)
            if not exam:
                return {"error": "Exam not found"}, 404
            return exam, 200
        except Exception as e:
            self.logger.error(f"Failed to fetch exam {exam_id}: {e}")
            return {"error": "Internal server error"}, 500

    def get_questions_in_exam(self, exam_id: str):
        try:
            questions = self.exam_service.list_exam_questions(exam_id)

            if questions is None:
                self.logger.warning(f"Exam {exam_id} not found or has no questions")
                return {"error": "Exam not found"}, 404

            return [question.to_dict() for question in questions]
        except Exception as e:
            self.logger.error(f"Unexpected error fetching questions for exam {exam_id}: {e}")
            return {"error": "Internal server error"}, 500
