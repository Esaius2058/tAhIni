import logging
from sqlalchemy.orm import Session, joinedload
from backend.src.services.user import UserService
from backend.src.utils.exceptions import ServiceError, NotFoundError
from backend.src.db.models import Submission, SubmissionAnswer

class SubmissionService:
    def __init__(self, db_session: Session):
        self.logger = logging.getLogger("Submission Service")
        self.db = db_session
        self.user_service = UserService(db_session)
        self.question_service = QuestionService(db_session)

    def create_submission(self, user_id: str, exam_id: str):
        try:
            submission = Submission(
                user_id=user_id,
                exam_id=exam_id
            )
            self.db.add(submission)
            self.db.commit()
            self.db.refresh(submission)
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Failed to create submission: {e}")
            raise ServiceError("Could not create submission") from e

    def add_answer(self,  submission_id: str, question_id: str, answer_text: str):
        try:
            """Save an answer to a question within a submission."""
            submission = self.db.query(Submission).get(submission_id)
            if not submission:
                raise NotFoundError("Submission not found")

            existing = (
                self.db.query(SubmissionAnswer)
                .filter_by(submission_id=submission_id, question_id=question_id)
                .first()
            )
            if existing:
                existing.answer = answer_text
            else:
                answer = SubmissionAnswer(
                    submission_id=submission_id,
                    question_id=question_id,
                    answer=answer_text
                )
                self.db.add(answer)

            self.db.commit()
            return True
        except NotFoundError:
            raise
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Failed to create submission: {e}")
            raise ServiceError("Could not create submission") from e

    def get_submission_by_id(self, submission_id: str):
        """Retrieve submission with answers."""
        try:
            submission = self.db.query(Submission).filter(Submission.id == submission_id).first()

            if not submission:
                raise NotFoundError("Submission not found")

            answers = (
                self.db.query(SubmissionAnswer)
                .filter(SubmissionAnswer.submission_id == submission_id)
                .all()
            )

            return {
                "submission_id": submission.id,
                "exam_id": submission.exam_id,
                "user_id": submission.user_id,
                "user_name": self.user_service.get_user_by_id(submission.user_id).name,
                "submitted_at": submission.submitted_at,
                "answers": [
                    {
                        "question_id": answer.question_id,
                        "answer_text": answer.answer
                    }
                    for answer in answers
                ]
            }
        except NotFoundError:
            raise
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Failed to get submission: {e}")
            raise ServiceError("Could not fetch submission") from e

    def _base_submission_query(self, exam_id: str, detailed: bool = False):
        query = self.db.query(Submission).filter(Submission.exam_id == exam_id)

        if detailed:
            query = query.options(
                joinedload(Submission.user),
                joinedload(Submission.answers).joinedload(SubmissionAnswer.question),
                joinedload(Submission.grade_log),
            )
        return query

    def list_exam_submissions_basic(self, exam_id: str, limit: int = 25, offset: int = 0):
        try:
            submissions = (
                self._base_submission_query(exam_id, detailed=False)
                .limit(limit)
                .offset(offset)
                .all()
            )

            return [
                {
                    "submission_id": sub.id,
                    "exam_id": sub.exam_id,
                    "user_id": sub.user_id,
                    "submitted_at": sub.submitted_at,
                }
                for sub in submissions
            ]
        except Exception as e:
            self.logger.error(f"Failed to fetch basic submissions for exam {exam_id}: {e}")
            raise ServiceError("Could not fetch basic submissions") from e

    def list_exam_submissions_detailed(self, exam_id: str, limit: int = 25, offset: int = 0):
        try:
            submissions = (
                self._base_submission_query(exam_id, detailed=True)
                .limit(limit)
                .offset(offset)
                .all()
            )

            return [
                {
                    "submission_id": sub.id,
                    "exam_id": sub.exam_id,
                    "user_id": sub.user_id,
                    "user_name": sub.user.name if sub.user else None,
                    "score": sub.grade_log.score if sub.grade_log else None,
                    "answers": [
                        {
                            "question_id": answer.question_id,
                            "question": answer.question.text,
                            "answer_text": answer.answer_text,
                        }
                        for answer in sub.answers
                    ],
                }
                for sub in submissions
            ]
        except Exception as e:
            self.logger.error(f"Failed to fetch detailed submissions for exam {exam_id}: {e}")
            raise ServiceError("Could not fetch detailed submissions") from e
