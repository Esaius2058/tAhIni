import logging
import time
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from backend.src.db.models import Submission, GradeLog
from backend.src.services import exam, course, submission
from backend.src.utils.exceptions import NotFoundError, ServiceError

class AnalyticsService:
    def __init__(self, db_session: Session):
        self.logger = logging.getLogger("Analytics Service")
        self.db = db_session
        self.exam_service = exam.ExamService(db_session)
        self.course_service = course.CourseService(db_session)
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
                "exam title": exam_obj.title,
                "average score": average,
                "pass rate": pass_rate
            }
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to compute exam statistics for exam {exam_id}: {e}")
            raise ServiceError("Could not compute exam statistics") from e

    def course_performance_per_semester(self, course_id: str, start_date: datetime, end_date: datetime):
        try:
            if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
                raise TypeError("start_date and end_date must be datetime objects")

            exams = self.exam_service.get_exams_by_course(course_id)

            exam_ids = [e.id for e in exams]
            query = (
                self.db.query(Submission)
                .options(joinedload(Submission.grade_log))
                .filter(
                    Submission.exam_id.in_(exam_ids),
                    Submission.submitted_at >= start_date,
                    Submission.submitted_at <= end_date
                )
            )

            submissions = query.all()
            total_submissions = query.count()
            scores = [sub.grade_log.score for sub in submissions]
            total_score = sum(score for score in scores)
            exam_stats =[self.exam_statistics(exam_id) for exam_id in exam_ids]
            overall_average_score = total_score / total_submissions
            overall_pass_rate = sum(stat["pass rate"] for stat in exam_stats) / total_submissions

            return {
                "course id": course_id,
                "course name": self.course_service.get_course(course_id).name,
                "number of exams": len(exam_ids),
                "number of students": total_submissions,
                "average score": overall_average_score,
                "pass rate": overall_pass_rate,
                "exam breakdown": [
                    {
                        "exam": stat["exam title"],
                        "average score": stat["average score"],
                        "pass rate": stat["pass rate"]
                    }
                    for stat in exam_stats
                ]
            }
        except Exception as e:
            self.logger.error(f"Failed to compute course performance: {e}")
            raise ServiceError("Could not compute course performance") from e


def course_performance_per_semester_sql(self, course_id: str, start_date: datetime, end_date: datetime):
    try:
        exam_ids = [
            e.id for e in self.exam_service.get_exams_by_course(course_id)
        ]

        result = (
            self.db.query(
                func.count(Submission.id).label("num_submissions"),
                func.avg(GradeLog.score).label("average_score"),
                func.sum(
                    func.case(
                        (GradeLog.score >= 40, 1), else_=0
                    )
                ).label("pass_count"),
            )
            .join(GradeLog, Submission.id == GradeLog.submission_id)
            .filter(
                Submission.exam_id.in_(exam_ids),
                Submission.submitted_at >= start_date,
                Submission.submitted_at <= end_date,
            )
            .one()
        )

        return {
            "course id": course_id,
            "course name": self.course_service.get_course(course_id).name,
            "number of exams": len(exam_ids),
            "number of students": result.num_submissions,
            "average score": float(result.average_score or 0),
            "pass rate": (
                result.pass_count / result.num_submissions
                if result.num_submissions > 0 else 0
            ),
        }
    except Exception as e:
        self.logger.error(f"Failed to compute course performance: {e}")
        raise ServiceError("Could not compute course performance") from e
