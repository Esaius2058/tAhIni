import logging
from backend.src.utils.embeddings import generate_embedding
from backend.src.db.models import Question
from sqlalchemy.orm import Session

class QuestionService:
    def __init__(self, db_session: Session):
        self.logger = logging.getLogger("Question Service")
        self.db = db_session

    def store_question(self, text: str, tags: list[str], bulk: bool = False):
        try:
            embedding = generate_embedding(text)
            question = Question(
                text=text,
                tags=tags,
                embedding=embedding,
            )
            if not bulk:
                self.db.add(question)
                self.db.commit()
            return question
        except Exception as e:
            self.logger.error(f"Error storing question in database: {e}")
            self.db.rollback()
            return None

    def semantic_search(self, query: str, top_n: int = 5):
        try:
            query_embedding = generate_embedding(query)

            sql = text("""
            SELECT id, text, tags
            FROM questions
            ORDER BY embedding <-> :embedding
            LIMIT :limit;
            """)

            result = self.db.execute(
                sql,
                {"embedding": query_embedding, "limit": top_n}
            ).fetchall()
            return result
        except Exception as e:
            self.logger.error(f"Error trying fetch similar questions: {e}")
            return None

    def keyword_search(self, query:str, difficulty: str | None, tags: list[str] | None):
        try:
            sql = text("""
                SELECT id, text, tags,
                    ts_rank_cd(
                        to_tsvector('english', text), 
                        plainto_tsquery(:query)
                    ) AS rank
                FROM questions
                where to_tsvector('english', text) @@ plainto_tsquery(:query)
            """)

            if difficulty:
                sql += " AND difficulty = :difficulty"

            if tags:
                sql += " AND tags @> ARRAY[:tags]"

            sql += " ORDER BY rank DESC"

            params = {"query": query}
            if difficulty:
                params["difficulty"] = difficulty
            if tags:
                params["tags"] = tags

            text_results = self.db.execute(
                sql,
                params
            ).fetchall()
            return text_results
        except Exception as e:
            self.logger.warning(
                f"Keyword search failed for query='{query}' "
                f"difficulty='{difficulty}' tags='{tags}': {e}"
            )
            return None

    def get_question_by_id(self, question_id):
        try:
            question = self.db.query(Question).filter_by(id=question_id).first()
            return question
        except Exception as e:
            self.logger.error(f"Error trying fetch question by id: {e}")
            return None

    def get_questions_by_tags(self, tags):
        try:
            questions = self.db.query(Question).filter(Question.contains(tags)).all()
            return questions
        except Exception as e:
            self.logger.error(f"Error trying to fetch questions by tags: {e}")
            return None

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
            self.logger.error(f"Error trying list questions: {e}")
            return None

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
        except Exception as e:
            self.logger.error(f"Error updating question: {e}")
            self.db.rollback()
            return False

    def delete_question(self, question_id):
        try:
            question = self.db.query(Question).filter(Question.id == question_id).first()
            if question:
                self.db.delete(question)
                self.db.commit()
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error deleting question: {e}")
            self.db.rollback()
            return False

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
            self.logger.error(f"Error storing questions in bulk: {e}")
            self.db.rollback()
            return None

    #def get_random_question(self):