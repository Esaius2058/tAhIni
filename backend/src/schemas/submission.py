from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from uuid import UUID

class CreateSubmissionRequest(BaseModel):
    user_id: UUID = Field(..., example="user-123")
    exam_id: UUID = Field(..., example="exam-456")

class AddAnswerRequest(BaseModel):
    submission_id: UUID = Field(..., example="sub-789")
    question_id: UUID = Field(..., example="ques-123")
    answer_text: str = Field(..., example="The answer to question 1")

class AnswerItem(BaseModel):
    question_id: UUID
    question: Optional[str] = None
    answer_text: str

class SubmissionResponse(BaseModel):
    submission_id: UUID
    exam_id: UUID
    user_id: UUID
    user_name: Optional[str] = None
    submitted_at: Optional[datetime] = None
    answers: Optional[List[AnswerItem]] = None

    class Config:
        orm_mode = True

class BasicSubmissionResponse(BaseModel):
    submission_id: UUID
    exam_id: UUID
    user_id: UUID
    submitted_at: Optional[datetime]

    class Config:
        orm_mode = True

class DetailedSubmissionResponse(BaseModel):
    submission_id: UUID
    exam_id: UUID
    user_id: UUID
    user_name: Optional[str]
    score: Optional[float]
    answers: List[AnswerItem]

    class Config:
        orm_mode = True
