from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
import uuid

class ExamBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200, example="Data Structures Midterm")
    subject: str = Field(..., min_length=2, max_length=100, example="Computer Science")
    course_id: str = Field(..., example="CSC301")
    semester_id: str = Field(..., example="SEM1-2025")
    duration: str = Field(default="2h", example="2h")

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "title": "Database Systems Final",
                "subject": "Computer Science",
                "course_id": "CSC302",
                "semester_id": "SEM2-2025",
                "duration": "3h",
            }
        }

class ExamCreate(ExamBase):
    pass

class ExamUpdate(BaseModel):
    subject: Optional[str] = Field(None, min_length=2, max_length=100, example="Software Engineering")
    title: Optional[str] = Field(None, min_length=3, max_length=200, example="Updated Midterm Title")
    duration: Optional[str] = Field(None, example="1.5h")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Revised Algorithm Exam",
                "duration": "1.5h"
            }
        }

class ExamRead(ExamBase):
    id: str = Field(..., example="a1b2c3d4-1234-5678-9101-abcdefabcdef")
    created_at: Optional[datetime] = Field(None, example="2025-10-14T08:30:00Z")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "a1b2c3d4-1234-5678-9101-abcdefabcdef",
                "title": "Data Structures Midterm",
                "subject": "Computer Science",
                "course_id": "CSC301",
                "semester_id": "SEM1-2025",
                "duration": "2h",
                "created_at": "2025-10-14T08:30:00Z"
            }
        }

class ExamStatsRead(BaseModel):
    exam_title: str = Field(..., example="Database Systems Final")
    average_score: float = Field(..., ge=0, le=100, example=72.5)
    pass_rate: float = Field(..., ge=0, le=100, example=85.0)

    class Config:
        json_schema_extra = {
            "example": {
                "exam_title": "Database Systems Final",
                "average_score": 72.5,
                "pass_rate": 85.0
            }
        }

class ExamResultsRead(BaseModel):
    title: str = Field(..., example="Software Engineering Final")
    subject: str = Field(..., example="Software Engineering")
    grader: str = Field(..., example="Prof. Jane Doe")
    score: float = Field(..., ge=0, le=100, example=89.0)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Software Engineering Final",
                "subject": "Software Engineering",
                "grader": "Prof. Jane Doe",
                "score": 89.0
            }
        }
