import logging
from sqlalchemy.orm import Session
from uuid import UUID
from src.db.models import Answer
from src.services.questions import ServiceError, NotFoundError

class AnswerService:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger(__name__)

    def create_answer(self, submission_id: UUID, question_id: UUID, content: str, is_correct: bool):
        try:
            answer = Answer(
                submission_id=submission_id,
                question_id=question_id,
                content=content,
                is_correct=is_correct
            )
            self.db.add(answer)
            self.db.commit()
            self.db.refresh(answer)
            return answer
        except Exception as e:
            self.logger.error(f"Create answer failed: {e}")
            raise ServiceError("Could not create answer") from e

    def get_answer(self, answer_id: UUID):
        try:
            answer = self.db.query(Answer).filter(Answer.id == answer_id).first()
            if not answer:
                raise NotFoundError("Answer not found")
            return answer
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Get answer failed: {e}")
            raise ServiceError("Could not fetch answer") from e

    def update_answer(self, answer_id: UUID, **kwargs):
        try:
            answer = self.get_answer(answer_id)
            for key, value in kwargs.items():
                setattr(answer, key, value)
            self.db.commit()
            self.db.refresh(answer)
            return answer
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Update answer failed: {e}")
            raise ServiceError("Could not update answer") from e

    def list_answers(self, limit: int = 25, offset: int = 0):
        try:
            answers = self.db.query(Answer).limit(limit).offset(offset).all()

            return [{
                "answer_id": answer.id,
                "text": answer.text,
                "options": answer.options,
                "correct_option": answer.correct_option
            } for answer in answers
            ]
        except Exception as e:
            self.logger.error(f"List answers failed: {e}")
            raise ServiceError("Could not list answers") from e

    def delete_answer(self, answer_id: UUID):
        try:
            answer = self.get_answer(answer_id)
            self.db.delete(answer)
            self.db.commit()
            return True
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Delete answer failed: {e}")
            raise ServiceError("Could not delete answer") from e
