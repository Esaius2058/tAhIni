from sqlalchemy import Column, String, Enum, Text, TIMESTAMP, ForeignKey, Float, func, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship, sessionmaker
from pathlib import Path
from dotenv import load_dotenv
import sys
import enum
import uuid

BASE_DIR = Path(__file__).resolve().parents[3]
print("BASE_DIR", BASE_DIR)
load_dotenv(BASE_DIR / ".env")

sys.path.append(str(BASE_DIR))

from src.db.base import Base, engine

class Exam(Base):
    __tablename__ = "exam"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    duration = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    questions = relationship("Question", back_populates="exam")
    submissions = relationship("Submission", back_populates="exam")

class QuestionType(enum.Enum):
    MCQ = "mcq"
    MULTI_RESPONSE = "multi_response"
    TRUE_FALSE = "true_false"
    SHORT_ANSWER = "short_answer"
    ESSAY = "essay"
    CODE = "code"
    NUMERICAL = "numerical"

class Question(Base):
    __tablename__ = "question"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(Enum(QuestionType, name="question_type_enum"), nullable=False, default=QuestionType.SHORT_ANSWER)
    text = Column(String)
    difficulty = Column(String)
    tags = Column(JSONB)
    embedding = Column(Vector(1536))
    exam_id = Column(UUID(as_uuid=True), ForeignKey("exam.id"))

    exam = relationship("Exam", back_populates="questions")
    answers = relationship("Answer", back_populates="question")

class Answer(Base):
    __tablename__ = "answer"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text = Column(String)
    options = Column(JSONB)
    correct_option = Column(String)
    rubric = Column(JSONB)

    question_id = Column(UUID(as_uuid=True), ForeignKey("question.id"))
    question = relationship("Question", back_populates="answers")

class Submission(Base):
    __tablename__ = "submission"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submitted_at = Column(TIMESTAMP, server_default=func.now())
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    exam_id = Column(UUID(as_uuid=True), ForeignKey("exam.id"))

    user = relationship("User", back_populates="submissions")
    exam = relationship("Exam", back_populates="submissions")
    answers = relationship("SubmissionAnswer", back_populates="submission", cascade="all, delete-orphan")

class SubmissionAnswer(Base):
    __table_name__ = "submission_answer"
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submission.id"))
    question_id = Column(UUID(as_uuid=True), ForeignKey("question.id"))
    answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    __table_args__ = (
        PrimaryKeyConstraint("submission_id", "question_id")
    )

    submission = relationship("Submission", back_populates="answers")
    question = relationship("Question")

class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    type = Column(String)

    submissions = relationship("Submission", back_populates="user")

class GradeLog(Base):
    __tablename__ = "gradelog"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    score = Column(Float, nullable=False)
    grader = Column(UUID(as_uuid=True), nullable=False)
    details = Column(JSONB)          #rubric breakdown, AI confidence scores, etc.
    graded_at = Column(TIMESTAMP, server_default=func.now())
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submission.id"))

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submission.id"))
    comments = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())
    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))

class Uploads(Base):
    __tablename__ = "uploads"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    filename = Column(String, nullable=False)
    storage_url = Column(String)
    status = Column(Enum("pending", "processed", "failed", name="upload_status"), default="pending")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class ExamContent(Base):
    __tablename__ = "exam_content"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4())
    upload_id = Column(UUID(as_uuid=True), ForeignKey("uploads.id"))
    text = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.commit()
