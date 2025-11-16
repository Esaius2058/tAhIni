import logging
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.db.database import get_db
from src.services.submission import SubmissionService
from src.schemas.submission import (
    CreateSubmissionRequest,
    AddAnswerRequest,
    SubmissionResponse,
    BasicSubmissionResponse,
    DetailedSubmissionResponse,
)

class SubmissionRouter:
    def __init__(self):
        self.logger = logging.getLogger("Submission Router")
        self.router = APIRouter(prefix="/api/v1/submission", tags=["Submission"])

        self.router.add_api_route(
            "/create",
            self.create_submission,
            methods=["POST"],
            response_model=SubmissionResponse,
            status_code=status.HTTP_201_CREATED,
        )
        self.router.add_api_route(
            "/answer",
            self.add_answer,
            methods=["POST"],
            response_model=dict,
            status_code=status.HTTP_200_OK,
        )
        self.router.add_api_route(
            "/{submission_id}",
            self.get_submission,
            methods=["GET"],
            response_model=SubmissionResponse,
        )
        self.router.add_api_route(
            "/exam/{exam_id}/basic",
            self.list_exam_submissions_basic,
            methods=["GET"],
            response_model=list[BasicSubmissionResponse],
        )
        self.router.add_api_route(
            "/exam/{exam_id}/detailed",
            self.list_exam_submissions_detailed,
            methods=["GET"],
            response_model=list[DetailedSubmissionResponse],
        )

    def create_submission(self, payload: CreateSubmissionRequest, db: Session = Depends(get_db)):
        service = SubmissionService(db)
        try:
            submission = service.create_submission(payload.user_id, payload.exam_id)
            return {
                "message": "Submission created successfully",
                "submission": submission,
            }
        except Exception as e:
            self.logger.error(f"Failed to create submission: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def add_answer(self, payload: AddAnswerRequest, db: Session = Depends(get_db)):
        service = SubmissionService(db)
        try:
            result = service.add_answer(
                payload.submission_id, payload.question_id, payload.answer_text
            )
            if result:
                return {"message": "Answer added successfully"}
        except Exception as e:
            self.logger.error(f"Failed to add answer: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_submission(self, submission_id: str, db: Session = Depends(get_db)):
        service = SubmissionService(db)
        try:
            submission = service.get_submission_by_id(submission_id)
            return submission
        except Exception as e:
            self.logger.error(f"Failed to fetch submission {submission_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def list_exam_submissions_basic(
            self, exam_id: str, limit: int = Query(25, ge=1), offset: int = Query(0, ge=0),
            db: Session = Depends(get_db)
    ):
        service = SubmissionService(db)
        try:
            return service.list_exam_submissions_basic(exam_id, limit, offset)
        except Exception as e:
            self.logger.error(f"Failed to fetch basic submissions: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def list_exam_submissions_detailed(
            self, exam_id: str, limit: int = Query(25, ge=1), offset: int = Query(0, ge=0),
            db: Session = Depends(get_db)
    ):
        service = SubmissionService(db)
        try:
            return service.list_exam_submissions_detailed(exam_id, limit, offset)
        except Exception as e:
            self.logger.error(f"Failed to fetch detailed submissions: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")


