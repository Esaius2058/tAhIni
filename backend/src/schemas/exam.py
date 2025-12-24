from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID

class ExamBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    course_id: UUID
    semester_id: UUID
    duration: Optional[int] = Field(default=120)
    pass_mark: Optional[float] = Field(default=40.0)

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "title": "Database Systems Final",
                "course_id": "c984a50c-9204-0987-a05e-4a0012345cef",
                "semester_id": "vc4b7d23-01ar-4yt9-b9e8-7b10bdb68ce5",
                "duration": 180,
                "pass_mark": 40.0
            }
        }
    )

class ExamCreate(BaseModel):
    title: str
    course_id: UUID
    semester_id: UUID
    exam_type: str
    duration_minutes: int = 120

class ExamUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=200)
    duration: Optional[int] = None
    pass_mark: Optional[float] = None
    course_id: Optional[UUID] = None
    semester_id: Optional[UUID] = None
    exam_code: Optional[int]

class CourseSimple(BaseModel):
    name: str
    code: str
    model_config = ConfigDict(from_attributes=True)

class AuthorSimple(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

class ExamRead(BaseModel):
    id: UUID
    title: str
    exam_code: str
    duration_minutes: int
    course: CourseSimple
    author: AuthorSimple
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ExamStatsRead(BaseModel):
    exam_title: str
    average_score: float = Field(..., ge=0, le=100)
    pass_rate: float = Field(..., ge=0, le=100)

class ExamResultsRead(BaseModel):
    title: str
    grader: str
    score: float = Field(..., ge=0, le=100)