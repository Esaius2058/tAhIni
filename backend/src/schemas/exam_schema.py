from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class ExamBase(BaseModel):
    title: str
    subject: str
    course_id: str
    semester_id: str
    duration: str = "2h"

    class Config:
        orm_mode = True

class ExamCreate(ExamBase):
    pass

class ExamUpdate(BaseModel):
    subject: Optional[str] = None
    title: Optional[str] = None
    duration: Optional[str] = None

class ExamRead(ExamBase):
    id: str
    created_at: Optional[datetime] = None
