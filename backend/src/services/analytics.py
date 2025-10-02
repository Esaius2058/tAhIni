import logging
from sqlalchemy.orm import Session
from backend.src.db.models import Submission
from backend.src.services import exam, course, user, submission
from backend.src.utils.exceptions import NotFoundError, ServiceError

class AnalyticsService:
    def __init__(self, db_session: Session):
        self.logger = logging.getLogger("Analytics Service")
        self.db = db_session
        self.exam_service = exam.ExamService(db_session)
        self.course_service = course.CourseService(db_session)
        self.user_service = user.UserService(db_session)
        self.submission_service = submission.SubmissionService(db_session)

    def total_student_score(self, user_id: str, exam_id: str):
        try:
            submission_obj = (
                self.db.query(Submission)
                .filter(Submission.user_id == user_id, Submission.exam_id == exam_id)
                .first()
            )
            if not submission_obj or not submission_obj.grade_log:
                return 0

            return float(submission_obj.grade_log.score)
        except Exception as e:
            self.logger.error(f"Failed to get total score for student {user_id}: {e}")
            raise ServiceError("Failed to get total score for student") from e

    def exam_pass_rate(self, exam_id: str):
        try:
            exam_obj = self.exam_service.get_exam_by_id(exam_id)
            if not exam_obj:
                raise NotFoundError("Exam not found")

            submissions = (
                self.db.query(Submission)
                .options(joinedload(Submission.grade_log))
                .filter(Submission.exam_id == exam_id)
                .all()
            )

            total = len(submissions)
            if total == 0:
                return 0.0

            passed = sum(1 for sub in submissions if sub.grade_log and sub.grade_log.score >= exa_obj.pass_mark)
            return (passed / total) * 100
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to compute pass rate for exam {exam_id}: {e}")
            raise ServiceError("Could not compute pass rate") from e

    def exam_statistics(self, exam_id: str):
        try:
            exam_obj = self.exam_service.get_exam_by_id(exam_id)
            if not exam_obj:
                raise NotFoundError("Exam not found")

            submissions = self.submission_service.list_exam_submissions(exam_id)
            if not submissions:
                return {"average score": 0, "pass rate": 0}

            # Pull scores directly from the relationship
            scores = [sub.score for sub in submissions if sub.score]

            if not scores:
                return {"average score": 0, "pass rate": 0}

            average = sum(scores) / len(scores)
            pass_rate = self.exam_pass_rate(exam_id)

            return {
                "average score": average,
                "pass rate": pass_rate
            }
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to compute exam statistics for exam {exam_id}: {e}")
            raise ServiceError("Could not compute exam statistics") from e
