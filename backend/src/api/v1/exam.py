import logging
from typing import List
from sqlalchemy.orm import Session
from src.db.database import get_db
from uuid import UUID
from src.schemas.question import QuestionRead
from src.schemas.candidate_exam import CandidateExamSessionRead
from src.schemas.exam import ExamCreate, ExamBase, ExamStatsRead, ExamUpdate, ExamRead, ExamResultsRead
from src.services.exam import ExamService
from src.services.analytics import AnalyticsService
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

class ExamRouter:
    def __init__(self):
        self.logger = logging.getLogger("Exam Router")
        self.router = APIRouter(prefix="/api/v1/exam", tags=["Exam"])

        self.router.add_api_route(
            "/new",
            self.create_exam,
            methods=["POST"],
            response_model=ExamRead,
            status_code=status.HTTP_201_CREATED
        )
        self.router.add_api_route(
            "/{id}",
            self.get_exam_by_id,
            methods=["GET"],
            response_model=ExamRead,
            status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/questions/{id}",
            self.get_questions_in_exam,
            methods=["GET"],
            response_model=List[QuestionRead],
            status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/instructor/{instructor_id}",
            self.get_exams_by_author,
            response_model=List[ExamRead],
            methods=["GET"],
            status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/course/{course_id}/{semester_id}",
            self.get_exams_by_course,
            response_model=List[ExamBase],
            methods=["GET"],
            status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/{exam_id}/questions/{question_id}",
            self.get_questions_in_exam,
            methods=["GET"],
            response_model=QuestionRead,
            status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/{exam_id}/questions/{question_id}",
            self.delete_question_from_exam,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT
        )
        self.router.add_api_route(
            "/{exam_id}",
            self.update_exam,
            methods=["PATCH"],
            response_model=ExamUpdate,
            status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/{exam_id}",
            self.delete_exam,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT
        )
        self.router.add_api_route(
            "/{exam_id}/questions/{question_id}",
            self.add_question_to_exam,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED
        )
        self.router.add_api_route(
            "/{exam_id}/questions/{question_id}",
            self.delete_question_from_exam,
            methods=["DELETE"],
            status_code=status.HTTP_204_NO_CONTENT
        )
        self.router.add_api_route(
            "/{exam_id}/stats",
            self.get_exam_statistics,
            methods=["GET"],
            response_model=ExamStatsRead,
            status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "{exam_id}/results/{user_id}",
            self.get_exam_results,
            methods=["GET"],
            response_model=ExamResultsRead,
            status_code=status.HTTP_200_OK
        )

    def start_exam(self, exam_id: UUID, student_id: UUID, db: Session = Depends(get_db)):
        try:
            service = ExamSessionService(db)
            session = service.start_exam(exam_id, student_id)
            return session
        except NotFoundError as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
        except Exception as e:
            self.logger.error(f"Unexpected error while starting exam {exam_id}: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    def create_exam(self, exam_data: ExamCreate, db: Session=Depends(get_db)):
        try:
            service = ExamService(db)
            exam = service.create_exam(**exam_data.dict())
            return exam
        except Exception as e:
            self.logger.error(f"Failed to create exam: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    def get_exam_by_id(self, id: UUID, db: Session=Depends(get_db)):
        try:
            service = ExamService(db)
            exam = service.get_exam_by_id(id)
            if not exam:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Exam not found"
                )
            return exam
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to fetch exam {exam_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def get_exams_by_author(self, instructor_id: UUID, db: Session=Depends(get_db)):
        try:
            service = ExamService(db)
            exams = service.get_exams_by_author(instructor_id)
            if not exams:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Exams not found"
                )
            return exams
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to fetch exams by {instructor_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def get_exams_by_course(self, course_id: UUID, semester_id: UUID, db: Session=Depends(get_db)):
        try:
            service = ExamService(db)
            exams = service.get_exams_by_course(course_id, semester_id)

            if exams is None:
                self.logger.warning(f"No exams found for course {course_id} in semester {semester_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Exams for course not found"
                )
            return exams
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error fetching exams for course {exam_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def update_exam(self, exam_id: UUID, exam_data: ExamUpdate, db: Session=Depends(get_db)):
        try:
            service = ExamService(db)
            updated_exam = service.update_exam(
                exam_id=exam_id,
                subject=exam_data.subject,
                title=exam_data.title
            )

            if not updated_exam:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Exam with id {exam_id} not found"
                )

            return updated_exam

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to update exam {exam_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def delete_exam(self, exam_id: UUID, db: Session=Depends(get_db)):
        try:
            service = ExamService(db)
            deleted = service.delete_exam(exam_id)

            if not deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Exam with id {exam_id} not found"
                )

            return None  # 204 No Content...no response body

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to delete exam {exam_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def get_questions_in_exam(
            self,
            session: CandidateExamSessionRead = Depends(get_current_candidate_session),
            db: Session = Depends(get_db),
    ):
        try:
            service = ExamService(db)

            questions = service.list_exam_questions(
                exam_id=session.exam_id
            )

            if questions is None:
                self.logger.warning(
                    f"Exam {session.exam_id} not found or has no questions"
                )
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Exam not found"
                )

            if not questions:
                return []

            return [
                {
                    "id": q.id,
                    "type": q.type,
                    "prompt": q.prompt,
                    "options": q.options,
                    "required": q.required,
                }
                for q in questions
            ]

        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(
                f"Unexpected error fetching questions for exam {session.exam_id}: {e}"
            )
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def add_question_to_exam(self, exam_id: UUID, question_id: UUID, db: Session=Depends(get_db)):
        try:
            service = ExamService(db)
            question = service.add_question_to_exam(question_id, exam_id)
            return question
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to add question {question_id} to exam {exam_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def delete_question_from_exam(self, exam_id: UUID, question_id: UUID, db: Session=Depends(get_db)):
        try:
            service = ExamService(db)
            result = service.delete_question_from_exam(question_id, exam_id)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Question not found in exam"
                )

            return {"detail": "Question removed from exam"}
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to remove question {question_id} from exam {exam_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def get_exam_statistics(self, exam_id: UUID, db: Session=Depends(get_db)):
        try:
            service = AnalyticsService(db)
            stats = service.exam_statistics(exam_id)
            return stats
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to get statistics for exam {exam_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )

    def get_exam_results(self, exam_id: UUID, student_id: UUID, db: Session=Depends(get_db)):
        try:
            service = AnalyticsService(db)
            results = service.student_score_in_exam(student_id, exam_id)
            return results
        except HTTPException:
            raise
        except Exception as e:
            self.logger.error(f"Failed to remove question {question_id} from exam {exam_id}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error"
            )
