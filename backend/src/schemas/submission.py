from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class CreateSubmissionRequest(BaseModel):
    user_id: str = Field(..., example="user-123")
    exam_id: str = Field(..., example="exam-456")

class AddAnswerRequest(BaseModel):
    submission_id: str = Field(..., example="sub-789")
    question_id: str = Field(..., example="ques-123")
    answer_text: str = Field(..., example="The answer to question 1")

class AnswerItem(BaseModel):
    question_id: str
    question: Optional[str] = None
    answer_text: str

class SubmissionResponse(BaseModel):
    submission_id: str
    exam_id: str
    user_id: str
    user_name: Optional[str] = None
    submitted_at: Optional[datetime] = None
    answers: Optional[List[AnswerItem]] = None

    class Config:
        orm_mode = True

class BasicSubmissionResponse(BaseModel):
    submission_id: str
    exam_id: str
    user_id: str
    submitted_at: Optional[datetime]

    class Config:
        orm_mode = True

class DetailedSubmissionResponse(BaseModel):
    submission_id: str
    exam_id: str
    user_id: str
    user_name: Optional[str]
    score: Optional[float]
    answers: List[AnswerItem]

    class Config:
        orm_mode = True
