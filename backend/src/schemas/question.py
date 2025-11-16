from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from src.db.models import QuestionType

class QuestionBase(BaseModel):
    text: str
    tags: List[str] = Field(default_factory=list)
    type: QuestionType
    difficulty: Optional[str] = None


class QuestionCreate(QuestionBase):
    pass

class QuestionRead(QuestionBase):
    id: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class QuestionSearchRequest(BaseModel):
    query: str
    top_n: Optional[int] = 5
    difficulty: Optional[str] = None
    tags: Optional[List[str]] = None


class QuestionUpdate(BaseModel):
    difficulty: Optional[str] = None
    tags: Optional[List[str]] = None
    type: Optional[QuestionType] = None


class BulkQuestionCreate(BaseModel):
    questions: List[QuestionCreate]


class BulkQuestionResponse(BaseModel):
    message: str
    questions: List[QuestionRead]

class TagRequest(BaseModel):
    tags: List[str]
