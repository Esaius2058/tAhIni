import logging
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from src.db.database import get_db
from src.services.question import QuestionService
from src.schemas.search import SearchResponse, SearchRequest

class SearchRouter:
    def __init__(self, db_session: Session = Depends(get_db)):
        self.router = APIRouter()
        self.logger = logging.getLogger("Search Router")
        self.router.add_api_route(
            "/semantic-search",
            self.search_questions_semantically,
            response_model=list[SearchResponse],
            methods=["GET"]
        )
        self.router.add_api_route(
            "/keyword-search",
            self.search_questions_by_keyword,
            response_model=list[SearchResponse],
            methods=["GET"]
        )
        self.router.add_api_route(
            "/search",
            self.hybrid_search,
            response_model=list[SearchResponse],
            methods=["GET"]
        )
        self.db = db_session
        self.question_service = QuestionService(self.db)

    def search_questions_semantically(self, payload: SearchRequest):
        self.logger.info(f"Semantic search for: {payload.query}")
        return self.question_service.semantic_search(payload.query, payload.top_n)

    def search_questions_by_keyword(self, payload: SearchRequest):
        self.logger.info(f"Keyword search for: {payload.query}")
        return self.question_service.keyword_search(payload.query, payload.tags, payload.difficulty)

    def hybrid_search(self, payload: SearchRequest):
        self.logger.info(f"Hybrid search for: {payload.query}")
        return self.question_service.hybrid_search(payload.query, payload.difficulty, payload.tags, payload.top_n)
