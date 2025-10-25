import json
import logging
from sqlalchemy import text
from src.utils.embeddings import generate_embedding
from src.db.models import Question, QuestionType
from sqlalchemy.orm import Session
from src.utils.exceptions import ServiceError, NotFoundError

class QuestionService:
    def __init__(self, db_session: Session):
        self.logger = logging.getLogger("Question Service")
        self.db = db_session

    def store_question(self, text: str, tags: list[str], type: QuestionType, bulk: bool = False):
        try:
            embedding = generate_embedding(text)
            question = Question(
                text=text,
                tags=tags,
                embedding=embedding,
                type=type,
            )
            if not bulk:
                self.db.add(question)
                self.db.commit()
            return question
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Failed to store question: {e}")
            raise ServiceError("Could not store question")

    def semantic_search(self, query: str, top_n: int = 5):
        try:
            query_embedding = generate_embedding(query)

            sql = text("""
                SELECT 
                    id, 
                    text, 
                    tags,
                    embedding <-> (:embedding)::vector AS similarity
                FROM question
                ORDER BY embedding <-> (:embedding)::vector
                LIMIT :limit;
            """)

            results = self.db.execute(
                sql,
                {"embedding": query_embedding, "limit": top_n}
            ).fetchall()
            print("Semantic results:", results)
            return results
        except Exception as e:
            self.logger.error(f"Semantic search failed: {e}")
            raise ServiceError("Could not perform semantic search")

    def keyword_search(self, query:str, difficulty: str | None=None, tags: list[str] | None=None):
        try:
            sql_query = """
                SELECT id, text, tags,
                    ts_rank_cd(
                        to_tsvector('english', text), 
                        plainto_tsquery(:query)
                    ) AS rank
                FROM question
                where to_tsvector('english', text) @@ plainto_tsquery(:query)
            """

            if difficulty:
                sql_query += " AND difficulty = :difficulty"

            if tags:
                sql_query += " AND tags @> :tags::jsonb"

            sql_query += " ORDER BY rank DESC"
            sql = text(sql_query)

            params = {"query": query}
            if difficulty:
                params["difficulty"] = difficulty
            if tags:
                params["tags"] = json.dumps(tags)

            text_results = self.db.execute(sql, params).fetchall()
            print("Keyword results:", text_results)
            return text_results
        except Exception as e:
            self.logger.error(f"Keyword search failed: {e}")
            raise ServiceError("Could not perform keyword search")

    def hybrid_search(self, query: str, difficulty: str | None=None, tags: list[str] | None=None, top_n: int = 5):
        try:
            text_results = self.keyword_search(query, difficulty, tags)
            semantic_results = self.semantic_search(query, top_n)

            text_scores = [row.rank for row in text_results]
            semantic_scores = [row.similarity for row in semantic_results]

            normalized_text = self.normalize_scores(text_scores)
            normalized_semantic = self.normalize_scores(semantic_scores)

            merged = [
                {"id": tr.id, "text": tr.text, "tags": tr.tags,
                 "score": self.merge_scores(ts,ss, weights={"text": 0.6, "semantic": 0.4})}
                for tr, ts, ss in zip(text_results, normalized_text, normalized_semantic)
            ]

            ranked = self.sort_by_score(merged)
            return ranked
        except Exception as e:
            self.logger.error(f"Hybrid search failed: {e}")
            raise ServiceError("Could not perform hybrid search")

    def merge_scores(self, text_score, semantic_score, weights=None):
        if weights is None:
            weights = {"text": 0.5, "semantic": 0.5}
        return (
            text_score * weights["text"]
            + semantic_score * weights["semantic"]
        )

    def normalize_scores(self, raw_scores: list[float]) -> list[float]:
        if not raw_scores:
            return []

        min_score = min(raw_scores)
        max_score = max(raw_scores)

        if max_score == min_score:
            return [0.0 for _ in raw_scores]

        return [(s - min_score) / (max_score - min_score) for s in raw_scores]

    def sort_by_score(self, results: list[dict]) -> list[dict]:
        return sorted(results, key=lambda r: r["score"], reverse=True)

    def get_question_by_id(self, question_id):
        try:
            question = self.db.query(Question).filter_by(id=question_id).first()
            if not question:
                raise NotFoundError(f"Question {question_id} not found")
            return question
        except NotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Get question by ID failed: {e}")
            raise ServiceError("Could not fetch question by id")

    def get_questions_by_tags(self, tags):
        try:
            questions = self.db.query(Question).filter(Question.tags.contains(tags)).all()
            return questions
        except Exception as e:
            self.logger.error(f"Get questions by tags failed: {e}")
            raise ServiceError("Could not fetch questions by tags")

    def list_questions(self, tags=None, text=None, difficulty=None, limit=20, offset=0):
        try:
            query = self.db.query(Question)
            if tags:
                query = query.filter(Question.tags.contains(tags))

            if text:
                query = query.filter(Question.text.ilike(f"%{text}"))

            if difficulty:
                query = query.filter(Question.difficulty == difficulty)

            questions = query.limit(limit).offset(offset).all()
            return questions
        except Exception as e:
            self.logger.error(f"List questions failed: {e}")
            raise ServiceError("Could not list questions")

    def update_question(self, question_id: str, new_difficulty = None, tags = None, question_type = None):
        try:
            question = self.db.query(Question).filter_by(id=question_id).first()

            if new_difficulty:
                question.difficulty = new_difficulty

            if tags:
                question.tags.extend(tags)

            if question_type:
                question.type = question_type

            self.db.add(question)
            self.db.commit()
            self.db.refresh(question)
            return True
        except NotFoundError as nf:
            self.logger.warning(str(nf))
            return {"error": str(nf)}, 404
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Update question failed: {e}")
            raise ServiceError("Could not update question")

    def delete_question(self, question_id):
        try:
            question = self.db.query(Question).filter(Question.id == question_id).first()
            if question:
                self.db.delete(question)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Delete question failed: {e}")
            raise ServiceError("Could not delete question")

    def bulk_store_questions(self, questions: list[dict | Question]):
        try:
            count = 0
            stored = []
            for question in questions:
                text = question.get("text") if isinstance(question, dict) else question.text
                tags = question.get("tags") if isinstance(question, dict) else question.tags
                question = self.store_question(text, tags, bulk=True)
                stored.append(question)
                count += 1
            self.db.add_all(stored)
            self.db.commit()
            return {"message": f"Successfully stored {count} questions!!", "questions": stored}
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Bulk store failed: {e}")
            raise ServiceError("Could not bulk store questions")

    #def get_random_question(self):