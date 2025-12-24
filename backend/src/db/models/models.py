from sqlalchemy import Column, Integer, Boolean, String, Enum, Text, TIMESTAMP, ForeignKey, Float, func, PrimaryKeyConstraint
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector
from sqlalchemy.orm import relationship, sessionmaker
from pathlib import Path
from dotenv import load_dotenv
import sys, os, enum, uuid
from datetime import datetime, timedelta

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from src.db.base import Base

class ProgramLevel(str, enum.Enum):
    CERTIFICATE = "certificate"
    DIPLOMA = "diploma"
    UNDERGRADUATE = "undergraduate"
    POSTGRADUATE = "postgraduate"
    MASTERS = "masters"
    DOCTORATE = "doctorate"

class Program(Base):
    __tablename__ = "program"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    code = Column(String, nullable=False)
    level = Column(
        Enum(ProgramLevel, name="program_level_enum"),
        default=ProgramLevel.UNDERGRADUATE
    )
    degree_title = Column(String, nullable=False)   # BSc, MSc
    degree_name = Column(String, nullable=False)    # Bachelor of Science
    department = Column(String, nullable=False)
    duration_years = Column(Float, default=4.0)

    courses = relationship("Course", back_populates="program")
    curricula = relationship("Curriculum", back_populates="program")


class Curriculum(Base):
    __tablename__ = "curriculum"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    program_id = Column(UUID(as_uuid=True), ForeignKey("program.id"), nullable=False)
    name = Column(String, nullable=False)  # e.g. "BSc CS 2024 Curriculum"
    version = Column(String, nullable=False)  # "2024", "2025"
    start_year = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True)

    program = relationship("Program", back_populates="curricula")
    academic_years = relationship("AcademicYear", back_populates="curriculum")

class AcademicYear(Base):
    __tablename__ = "academic_year"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    curriculum_id = Column(UUID(as_uuid=True), ForeignKey("curriculum.id"), nullable=False)
    year_number = Column(Integer, nullable=False)  # 1, 2, 3, 4
    name = Column(String, nullable=False)  # "Year 1"

    curriculum = relationship("Curriculum", back_populates="academic_years")
    semesters = relationship("Semester", back_populates="academic_year")


class Semester(Base):
    __tablename__ = "semester"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    academic_year_id = Column(
        UUID(as_uuid=True),
        ForeignKey("academic_year.id"),
        nullable=False
    )
    name = Column(String, nullable=False)  # "Semester 1"
    start_date = Column(TIMESTAMP, nullable=False)
    end_date = Column(TIMESTAMP, nullable=False)

    academic_year = relationship("AcademicYear", back_populates="semesters")
    courses = relationship("Course", back_populates="semester")
    exams = relationship("Exam", back_populates="semester")

class Course(Base):
    __tablename__ = "course"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, nullable=False)   # CS101
    name = Column(String, nullable=False)
    program_id = Column(UUID(as_uuid=True), ForeignKey("program.id"), nullable=False)
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semester.id"), nullable=False)

    program = relationship("Program", back_populates="courses")
    semester = relationship("Semester", back_populates="courses")
    exams = relationship("Exam", back_populates="course")

class Exam(Base):
    __tablename__ = "exam"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_code = Column(String, unique=True, index=True, nullable=False)

    author_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    course_id = Column(UUID(as_uuid=True), ForeignKey("course.id"))
    semester_id = Column(UUID(as_uuid=True), ForeignKey("semester.id"))

    title = Column(String, nullable=False)
    duration = Column(Integer)
    pass_mark = Column(Float, default=40.0)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    author = relationship("User", back_populates="exams_authored")
    course = relationship("Course", back_populates="exams")
    semester = relationship("Semester", back_populates="exams")
    questions = relationship("Question", back_populates="exam")
    submissions = relationship("Submission", back_populates="exam")
    exam_sessions = relationship("ExamSession", back_populates="exam")

class ExamStatus(enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SUBMITTED = "submitted"
    EXPIRED = "expired"

class ExamSession(Base):
    __tablename__ = "exam_session"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    exam_id = Column(UUID(as_uuid=True), ForeignKey("exam.id"), nullable=False)

    start_time = Column(TIMESTAMP, server_default=func.now())
    end_time = Column(TIMESTAMP)
    submitted_at = Column(TIMESTAMP)

    score = Column(String)
    current_question_index = Column(String)
    status = Column(Enum(ExamStatus, name="exam_status_enum"), default=ExamStatus.NOT_STARTED)

    student = relationship("User", back_populates="exam_sessions")
    exam = relationship("Exam", back_populates="exam_sessions")
    candidate_sessions = relationship(
        "CandidateExamSession",
        back_populates="exam",
        cascade="all, delete-orphan"
    )


class CandidateExamSession(Base):
    __tablename__ = "candidate_exam_session"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exam_id = Column(UUID(as_uuid=True), ForeignKey("exam.id"), nullable=False)

    candidate_name = Column(String, nullable=False)
    candidate_ref = Column(String, nullable=True)

    started_at = Column(TIMESTAMP, nullable=False)
    ends_at = Column(TIMESTAMP, nullable=False)
    submitted_at = Column(TIMESTAMP)

    status = Column(Enum(ExamStatus), nullable=False)

    exam = relationship("Exam", back_populates="candidate_sessions")


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
    tags = Column(MutableList.as_mutable(JSONB), default=list)
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
    exam_id = Column(
        UUID(as_uuid=True),
        ForeignKey("exam.id"),
        nullable=False
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("user.id"),
        nullable=True
    )
    exam_session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("exam_session.id"),
        nullable=True
    )
    candidate_session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("candidate_exam_session.id"),
        nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            """
            (exam_session_id IS NOT NULL AND candidate_session_id IS NULL)
            OR
            (exam_session_id IS NULL AND candidate_session_id IS NOT NULL)
            """,
            name="submission_exactly_one_session"
        ),
    )

    # relationships
    exam = relationship("Exam", back_populates="submissions")
    user = relationship("User", back_populates="submissions")
    exam_session = relationship("ExamSession")
    candidate_session = relationship("CandidateExamSession")
    answers = relationship(
        "SubmissionAnswer",
        back_populates="submission",
        cascade="all, delete-orphan"
    )
    grade_log = relationship(
        "GradeLog",
        back_populates="submission",
        uselist=False,
        cascade="all, delete-orphan"
    )

class SubmissionAnswer(Base):
    __tablename__ = "submission_answer"
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submission.id"))
    question_id = Column(UUID(as_uuid=True), ForeignKey("question.id", ondelete="CASCADE"))
    answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    __table_args__ = (
        PrimaryKeyConstraint("submission_id", "question_id"),
    )

    submission = relationship("Submission", back_populates="answers")
    question = relationship("Question")

class UserType(enum.Enum):
    STUDENT = "student"
    INSTRUCTOR = "instructor"
    ADMIN = "admin"

class User(Base):
    __tablename__ = "user"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    type = Column(Enum(UserType, name="user_type_enum"), default=UserType.STUDENT)
    created_at = Column(TIMESTAMP, server_default=func.now())

    submissions = relationship("Submission", back_populates="user")
    uploads = relationship(
        "Uploads",
        backref="user",
        cascade="all, delete-orphan",
        passive_deletes=True
    )
    exams_authored = relationship("Exam", back_populates="author")
    exam_sessions = relationship("ExamSession", back_populates="student")

class GradeLog(Base):
    __tablename__ = "gradelog"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    score = Column(Float, nullable=False)
    grader = Column(UUID(as_uuid=True), nullable=False)
    details = Column(JSONB)          #rubric breakdown, AI confidence scores, etc.
    graded_at = Column(TIMESTAMP, server_default=func.now())
    submission_id = Column(UUID(as_uuid=True), ForeignKey("submission.id"))

    submission = relationship("Submission", back_populates="grade_log")

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
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"))
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
