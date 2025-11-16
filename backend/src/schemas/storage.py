from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UploadResponse(BaseModel):
    id: str
    filename: str
    storage_url: str
    user_id: str
    status: Optional[str] = "uploaded"

    class Config:
        orm_mode = True


class FileItem(BaseModel):
    id: str
    filename: str
    storage_url: str
    user_id: str
    status: Optional[str]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


class DeleteResponse(BaseModel):
    message: str = Field(example="File deleted successfully")


class PublicURLResponse(BaseModel):
    url: str


class UpdateStatusRequest(BaseModel):
    status: str = Field(..., example="processed")
