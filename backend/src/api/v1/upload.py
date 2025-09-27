import logging
from fastapi import APIRouter, UploadFile
from sqlalchemy.orm import Session
from backend.src.db.models import Uploads, User
from supabase import create_client, Client
from backend.src.services.storage import StorageService

class UploadRouter:
    def __init__(self, storage_service: StorageService):
        self.storage = storage_service
        self.router = APIRouter()
        self.logger = logging.getLogger("Upload Router")
        self.router.add_api_route(
            "/upload", self.upload_file, methods=["POST"]
        )

    async def upload_file(self, file: UploadFile):
        upload = self.storage.upload_file(file.file, file.filename)

        try:
            self.storage.update_upload_status(upload.id, "processed")
            return upload
        except Exception as e:
            logger.error(f"Error uploading file '{file.filename}': {e}")
            self.storage.update_upload_status(upload.id, "failed")
            return None