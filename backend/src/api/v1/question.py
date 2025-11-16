import logging
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.db.database import get_db
from src.services.question import QuestionService
from src.schemas.question import (
    QuestionCreate, QuestionRead, QuestionUpdate, TagRequest,
    BulkQuestionCreate, BulkQuestionResponse, QuestionSearchRequest
)

class QuestionRouter:
    def __init__(self):
        self.logger = logging.getLogger("Question Router")
        self.router = APIRouter(prefix="/api/v1/question", tags=["Question"])

        self.router.add_api_route(
            "/",
            self.create_question,
            methods=["POST"],
            response_model=QuestionRead,
            status_code=status.HTTP_201_CREATED
        )
        self.router.add_api_route(
            "/bulk/",
            self.bulk_store_questions,
            methods=["POST"],
            response_model=BulkQuestionResponse,
            status_code=status.HTTP_201_CREATED
        )
        self.router.add_api_route(
            "/search/",
            self.hybrid_search,
            methods=["POST"],
            response_model=List[QuestionRead],
            status_code=status.HTTP_200_OK
        )
        self.router.add_api_route(
            "/{question_id}/",
            self.get_question_by_id,
            methods=["GET"],
            response_model=QuestionRead
        )
        self.router.add_api_route(
            "/{question_id}/",
            self.update_question,
            methods=["PATCH"],
            response_model=QuestionRead
        )
        self.router.add_api_route(
            "/{question_id}/",
            self.delete_question,
            methods=["DELETE"],
            response_model=dict
        )
        self.router.add_api_route(
            "/all/",
            self.list_questions,
            methods=["GET"],
            response_model=List[QuestionRead]
        )
        self.router.add_api_route(
            "/tags/",
            self.get_questions_by_tags,
            methods=["POST"],
            response_model=List[QuestionRead]
        )

    def create_question(self, payload: QuestionCreate, db: Session = Depends(get_db)):
        service = QuestionService(db)
        try:
            question = service.store_question(payload.text, payload.tags, payload.type)
            return question
        except Exception as e:
            self.logger.error(f"Failed to create question: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def bulk_store_questions(self, payload: BulkQuestionCreate, db: Session = Depends(get_db)):
        service = QuestionService(db)
        try:
            return service.bulk_store_questions([q.dict() for q in payload.questions])
        except Exception as e:
            self.logger.error(f"Bulk store failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def hybrid_search(self, payload: QuestionSearchRequest, db: Session = Depends(get_db)):
        service = QuestionService(db)
        try:
            results = service.hybrid_search(
                query=payload.query,
                difficulty=payload.difficulty,
                tags=payload.tags,
                top_n=payload.top_n
            )
            return results
        except Exception as e:
            self.logger.error(f"Hybrid search failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_question_by_id(self, question_id: str, db: Session = Depends(get_db)):
        service = QuestionService(db)
        try:
            question = service.get_question_by_id(question_id)
            return question
        except Exception as e:
            self.logger.error(f"Failed to fetch question {question_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def update_question(self, question_id: str, payload: QuestionUpdate, db: Session = Depends(get_db)):
        service = QuestionService(db)
        try:
            updated = service.update_question(
                question_id,
                new_difficulty=payload.difficulty,
                tags=payload.tags,
                question_type=payload.type
            )
            if not updated:
                raise HTTPException(status_code=404, detail="Question not found")
            return service.get_question_by_id(question_id)
        except Exception as e:
            self.logger.error(f"Failed to update question {question_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def delete_question(self, question_id: str, db: Session = Depends(get_db)):
        service = QuestionService(db)
        try:
            success = service.delete_question(question_id)
            if not success:
                raise HTTPException(status_code=404, detail="Question not found")
            return {"message": "Question deleted successfully"}
        except Exception as e:
            self.logger.error(f"Failed to delete question {question_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def list_questions(self, db: Session = Depends(get_db)):
        service = QuestionService(db)
        try:
            return service.list_questions(limit=50)
        except Exception as e:
            self.logger.error(f"Failed to list questions: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_questions_by_tags(self, payload: TagRequest, db: Session = Depends(get_db)):
        service = QuestionService(db)
        try:
            return service.get_questions_by_tags(payload.tags)
        except Exception as e:
            self.logger.error(f"Failed to get questions by tags: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
