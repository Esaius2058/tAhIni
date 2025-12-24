from pydantic import BaseModel, Field
from uuid import UUID
from typing import List, Optional
from datetime import datetime

# ---------- Requests ----------

class EnterExamRequest(BaseModel):
    exam_code: str = Field(..., min_length=4, max_length=20)


class StartExamRequest(BaseModel):
    exam_id: UUID
    candidate_name: str = Field(..., min_length=2, max_length=100)


class AnswerInput(BaseModel):
    question_id: UUID
    payload: dict  # flexible: MCQ | text | file refs


class AutosaveRequest(BaseModel):
    answers: List[AnswerInput]


# ---------- Responses ----------

class StartExamResponse(BaseModel):
    session_id: UUID
    ends_at: datetime
    token: str


class QuestionRead(BaseModel):
    id: UUID
    type: str
    prompt: str
    options: Optional[list] = None
    required: bool

class CandidateExamToken(BaseModel):
    exam_session_id: UUID
    submission_id: UUID
    exam_id: UUID
    exp: datetime

class CandidateExamSessionRead(BaseModel):
    id: UUID
    exam_id: UUID

    candidate_name: str
    candidate_ref: str | None = None

    started_at: datetime
    ends_at: datetime
    submitted_at: datetime | None = None

    status: ExamStatus

    model_config = ConfigDict(from_attributes=True)