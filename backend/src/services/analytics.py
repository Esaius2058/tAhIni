import logging
import time
from collections import defaultdict
from numpy.ma.extras import average
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload
from src.db.models import Submission, GradeLog, User, Exam
from src.services import exam, course, submission, semester
from src.utils.exceptions import NotFoundError, ServiceError

class AnalyticsService:
    def __init__(self, db_session: Session):
        self.logger = logging.getLogger("Analytics Service")
        self.db = db_session
        self.semester_service = semester.SemesterService(db_session)
        self.exam_service = exam.ExamService(db_session)
        self.course_service = course.CourseService(db_session)
        self.submission_service = submission.SubmissionService(db_session)

    def student_score_in_exam(self, student_id: str, exam_id: str):
        try:
            exam_obj = self.db.query(Exam).filter(Exam.id == exam_id).first()
            if not exam_obj:
                raise NotFoundError(f"Exam {exam_id} not found")

            submission_obj = (
                self.db.query(Submission)
                .filter(Submission.user_id == user_id, Submission.exam_id == exam_id)
                .first()
            )
            if not submission_obj or not submission_obj.grade_log:
                return 0

            return {
                "title": exam_obj.title,
                "subject": exam_obj.subject,
                "grader": submission_obj.grade_log.grader,
                "score": float(submission_obj.grade_log.score),
            }
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

            average_score = sum(scores) / len(scores)
            pass_rate = self.exam_pass_rate(exam_id)

            return {
                "exam title": exam_obj.title,
                "average score": average_score,
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

            semester = self.semester_service.get_semester_by_date(start_date, end_date)
            exams = self.exam_service.get_exams_by_course(course_id, semester.id)

            exam_ids = [e.id for e in exams]
            query = (
                self.db.query(Submission)
                .options(joinedload(Submission.grade_log))
                .filter(
                    Submission.exam_id.in_(exam_ids)
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
                "semester": semester.name,
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
            semester = self.semester_service.get_semester_by_date(start_date, end_date)
            exam_ids = [
                e.id for e in self.exam_service.get_exams_by_course(course_id, semester.id)
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
                "semester": semester.name,
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

    def grade_from_score(self, score):
        if score >= 70:
            return "A"
        elif score >= 60:
            return "B"
        elif score >= 50:
            return "C"
        elif score >= 40:
            return "D"
        else:
            return "F"

    def score_to_gpa(self, score):
        if score >= 90:
            return 4.0
        elif score >= 80:
            return 3.7
        elif score >= 70:
            return 3.0
        elif score >= 60:
            return 2.0
        elif score >= 50:
            return 1.0
        else:
            return 0.0

    def compute_improvement_rate(self, progress_data: dict):
        if len(progress_data) < 2:
            return 0
        first = progress_data[0]["average_score"]
        last = progress_data[-1]["average_score"]
        return ((last - first) / first) * 100 if first else 0

    def compute_gpa_trend(self, progress_data: dict):
        return [(s["semester_name"], s["average_score"]) for s in progress_data]

    def find_weakest_course(self, progress_data: dict):
        all_courses = [c for s in progress_data for c in s["courses"]]
        return min(all_courses, key=lambda c: c["average_score"])

    def compute_cumulative_gpa(self, progress_data):
        if not progress_data:
            return 0.0

        total_weighted_gpa = 0
        total_courses = 0

        for semester in progress_data:
            gpa = score_to_gpa(semester["average_score"])
            num_courses = semester.get("num_courses", 1)
            total_weighted_gpa += gpa * num_courses
            total_courses += num_courses

        cumulative_gpa = total_weighted_gpa / total_courses if total_courses > 0 else 0
        return round(cumulative_gpa, 2)

    def student_performance_per_semester(self, student_id: str, start_date: datetime, end_date: datetime):
        try:
            semester = self.semester_service.get_semester_by_date(start_date, end_date)
            query = (
                self.db.query(
                Exam.course_id,
                func.count(Submission.id).label("num_submissions"),
                func.avg(GradeLog.score).label("average_score")
                )
                .join(Submission.exam)
                .join(Submission.grade_log)
                .filter(
                    Submission.user_id == student_id,
                    Exam.semester_id == semester.id
                )
                .group_by(Exam.course_id)
            )

            results = query.all()
            overall_avg = sum(r.average_score for r in results) / len(results) if results else 0

            return {
                "student_id": student_id,
                "date_range": (start_date, end_date),
                "num_courses": len(results),
                "overall_average": overall_avg,
                "overall_grade": self.grade_from_score(overall_avg),
                "courses": [
                {
                    "course_id": r.course_id,
                    "course_name": self.course_service.get_course(r.course_id).name,
                    "average_score": r.average_score,
                    "grade": self.grade_from_score(r.average_score),
                }
                for r in results
                ],
            }
        except Exception as e:
            self.logger.error(f"Failed to compute student performance: {e}")
            raise ServiceError("Could not compute student performance") from e

    def student_performance_per_course(self, student_id: str, start_date: datetime, end_date: datetime):
        try:
            semester = self.semester_service.get_semester_by_date(start_date, end_date)

            exam_ids = [e.id for e in self.exam_service.get_exams_by_semester(semester.id)]

            submissions = (self.db.query(Submission)
            .join(GradeLog, Submission.id == GradeLog.submission_id)
            .join(Exam, Submission.exam_id == Exam.id)
            .filter(
                Submission.user_id == student_id,
                Submission.exam_id.in_(exam_ids)
            ).all())

            return [{
                "course_id": sub.exam.course_id,
                "course_name": sub.exam.course.name,
                "exam_id": sub.exam_id,
                "exam_title": sub.exam.title,
                "score": sub.grade_log.score,
                "grade": self.grade_from_score(sub.grade_log.score),
                "status": "passed" if sub.grade_log.score >= 40 else "failed",
                "submitted_at": sub.submitted_at
            } for sub in submissions]
        except Exception as e:
            self.logger.error(f"Failed to compute student performance for semester: {e}")
            raise ServiceError("Could not compute student performance") from e

    def student_progress(self, user_id: str):
        try:
            results = (
                query(Exam)
                .join(Semester)
                .options(
                    selectinload(Exam.semester),
                    selectinload(Exam.submissions).selectinload(Submission.grade_log),
                )
                .filter(Exam.user_id == user_id)
                .all()
            )

            if not results:
                raise NotFoundError(f"No semesters found for student {user_id}")

            semester_map = defaultdict(list)
            for exam in results:
                semester_map[exam.semester].append(exam)
            #semesters = sorted({result.semester for result in results}, key=lambda s: s.start_date)

            semesters = sorted(semester_map.keys(), key=lambda s: s.start_date)

            progress_data = []

            for semester in semesters:
                exams = semester_map[semester]
                exam_scores = []

                for exam in exams:
                    submission_scores = [
                        s.grade_log.score
                        for s in exam.submissions
                        if s.grade_log and s.grade_log.score is not None
                    ]

                    if submission_scores:
                        exam_avg = mean(submission_scores)
                        exam_scores.append(exam_avg)

                if not exam_scores:
                    continue  # skip semesters without any scores

                semester_avg = mean(exam_scores)
                grade = self.score_to_grade(semester_avg)
                num_courses = len(exams)

                """semester_performance = self.student_performance_per_semester(
                    user_id, semester.start_date, semester.end_date
                )"""

                progress_data.append({
                    "semester_name": semester.name,
                    "average_score": round(semester_avg, 2),
                    "grade": grade,
                    "num_courses": num_courses,
                    "courses": [
                        {
                            "course_name": exam.course.name,
                            "average_score": round(mean([
                                s.grade_log.score for s in exam.submissions
                                if s.grade_log and s.grade_log.score is not None
                            ]), 2),
                            "grade": self.score_to_grade(round(mean([
                                s.grade_log.score for s in exam.submissions
                                if s.grade_log and s.grade_log.score is not None
                            ]), 2))
                        }
                        for exam in exams if exam.submissions
                    ]
                })

            if not progress_data:
                raise NotFoundError(f"No valid exam data found for {user_id}")

            improvement_rate = compute_improvement_rate(progress_data)
            gpa_trend = compute_gpa_trend(progress_data)
            weakest_course = find_weakest_course(progress_data)

            return {
                "student_id": user_id,
                "total_semesters": len(progress_data),
                "average_gpa": self.compute_cumulative_gpa(progress_data),
                "gpa_trend": gpa_trend,
                "improvement_rate": improvement_rate,
                "weakest_course": weakest_course,
                "semester_breakdown": progress_data
            }

        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to compute student progress for {user_id}: {e}")
            raise ServiceError("Could not compute student progress") from e
