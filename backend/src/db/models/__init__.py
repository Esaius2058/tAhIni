import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from src.db.models.models import (User, Exam, Feedback, Program, Course, ExamContent, SubmissionAnswer, Submission,
                                  Semester, Question, QuestionType, Answer, GradeLog, UserType, Uploads)
from sqlalchemy import Text, JSON
from sqlalchemy.dialects.postgresql import JSONB as PGJSONB
from pgvector.sqlalchemy import Vector as PGVector

if os.getenv("DB_VENDOR") == "sqlite":
    Vector = JSON
    JSONB = JSON
else:
    Vector = PGVector
    JSONB = PGJSONB
