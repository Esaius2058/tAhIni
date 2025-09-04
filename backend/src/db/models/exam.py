from sqlalchemy import Column, String, Text, TIMESTAMP, ForeignKey, Float, func
from sqlalchemy.dialects.postgresql import UUID, JSONB, ARRAY
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship, sessionmaker
from src.db.base import Base, engine
import uuid

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

class Question(Base):
    __tablename__ = "question"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String, nullable=False)
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

class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(String)

    submissions = relationship("Submission", back_populates="user")

class GradeLog(Base):
    __tablename__ = "gradelog"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    score = Column(Float, nullable=False)
    grader = Column(String, nullable=False)
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

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.commit()
