from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID

class SemesterBase(BaseModel):
    name: str = Field(..., example="Semester 1")
    start_date: datetime = Field(..., example="2025-01-15T08:00:00Z")
    end_date: datetime = Field(..., example="2025-05-15T17:00:00Z")

class SemesterCreate(SemesterBase):
    """Schema for creating a semester."""
    pass

class SemesterUpdate(BaseModel):
    name: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None

class SemesterRead(SemesterBase):
    id: UUID

    class Config:
        from_attributes = True
