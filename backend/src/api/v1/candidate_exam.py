import logging
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.services.candidate_exam import CandidateExamService
from src.utils.exceptions import NotFoundError, ServiceError
from src.schemas.candidate_exam import (
    EnterExamRequest,
    StartExamRequest,
    StartExamResponse,
    QuestionRead,
    AutosaveRequest,
)

class CandidateExamRouter:
    def __init__(self):
        self.logger = logging.getLogger("Candidate Exam Router")
        self.router = APIRouter(
            prefix="/api/v1/candidate",
            tags=["Candidate Exam"]
        )

        self.router.add_api_route(
            "/exams/enter",
            self.enter_exam,
            methods=["POST"],
            status_code=status.HTTP_200_OK,
        )

        self.router.add_api_route(
            "/exams/start",
            self.start_exam,
            methods=["POST"],
            response_model=StartExamResponse,
            status_code=status.HTTP_201_CREATED,
        )

        self.router.add_api_route(
            "/exam-sessions/{session_id}/questions",
            self.get_questions,
            methods=["GET"],
            response_model=List[QuestionRead],
            status_code=status.HTTP_200_OK,
        )

        self.router.add_api_route(
            "/exam-sessions/{session_id}/autosave",
            self.autosave,
            methods=["POST"],
            status_code=status.HTTP_204_NO_CONTENT,
        )

        self.router.add_api_route(
            "/exam-sessions/{session_id}/submit",
            self.submit_exam,
            methods=["POST"],
            status_code=status.HTTP_204_NO_CONTENT,
        )

    def enter_exam(
        self,
        payload: EnterExamRequest,
        db: Session = Depends(get_db),
    ):
        try:
            service = CandidateExamService(db, self.logger)
            exam = service.enter_exam(payload.exam_code)

            return {
                "exam_id": exam.id,
                "title": exam.title,
                "duration_minutes": exam.duration_minutes,
            }

        except ServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

    def start_exam(
        self,
        payload: StartExamRequest,
        db: Session = Depends(get_db),
    ):
        try:
            service = CandidateExamService(db, self.logger)
            return service.start_exam(
                exam_id=payload.exam_id,
                candidate_name=payload.candidate_name,
            )

        except ServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )

    def get_questions(
        self,
        session_id: UUID,
        db: Session = Depends(get_db),
    ):
        try:
            service = CandidateExamService(db, self.logger)
            return service.get_questions(session_id)

        except NotFoundError as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e),
            )
        except ServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e),
            )

    def autosave(
        self,
        question_id: UUID,
        answer: str,
        session: ExamSession = Depends(get_active_session),
        db: Session = Depends(get_db),
    ):
        try:
            service = CandidateExamService(db)
            service.upsert_submission_answer(
                submission_id=session.submission_id,
                question_id=question_id,
                answer_text=answer,
            )
            return {"status": "saved"}

        except ServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e),
            )

    def submit_exam(
        self,
        session_id: UUID,
        db: Session = Depends(get_db),
    ):
        try:
            service = CandidateExamService(db, self.logger)
            service.submit_exam(session_id)
            return None  # 204

        except ServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(e),
            )


