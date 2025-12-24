import logging
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status, Query
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.schemas.storage import (
    UploadResponse,
    FileItem,
    DeleteResponse,
    PublicURLResponse,
    UpdateStatusRequest,
)
from src.services.supabase_client import supabase_client
from src.services.storage import StorageService

class StorageRouter:
    def __init__(self):
        self.router = APIRouter(prefix="/api/v1/storage", tags=["Storage"])
        self.logger = logging.getLogger("Storage Router")

        self.router.add_api_route(
            "/upload",
            self.upload_file,
            methods=["POST"],
            response_model=UploadResponse,
            status_code=status.HTTP_201_CREATED,
        )
        self.router.add_api_route(
            "/download/{file_name}",
            self.download_file,
            methods=["GET"],
            response_model=dict,
        )
        self.router.add_api_route(
            "/delete/{file_name}",
            self.delete_file,
            methods=["DELETE"],
            response_model=DeleteResponse,
        )
        self.router.add_api_route(
            "/list",
            self.list_files,
            methods=["GET"],
            response_model=list[FileItem],
        )
        self.router.add_api_route(
            "/public-url/{file_name}",
            self.get_public_url,
            methods=["GET"],
            response_model=PublicURLResponse,
        )
        self.router.add_api_route(
            "/status/{upload_id}",
            self.update_status,
            methods=["PATCH"],
            response_model=dict,
        )

    async def upload_file(
        self,
        file: UploadFile = File(...),
        user_id: str = Form(...),
        db: Session = Depends(get_db)
    ):
        service = StorageService(supabase_client, "uploads", db)
        try:
            file_bytes = await file.read()
            upload = service.upload_file(file_bytes, file.filename, user_id)

            if not upload:
                self.logger.error("StorageService.upload_file returned None")
                raise HTTPException(status_code=500, detail="File upload failed")

            return UploadResponse(
                id=upload.id,
                filename=upload.filename,
                storage_url=upload.storage_url,
                user_id=upload.user_id,
                status=upload.status,
            )
        except HTTPException:
            raise
        except Exception as e:
            self.logger.exception(f"Upload failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def download_file(self, file_name: str, db: Session = Depends(get_db)):
        service = StorageService(supabase_client, "uploads", db)
        dest = f"/tmp/{file_name}"
        try:
            path = service.download_file(file_name, dest)
            if not path:
                raise HTTPException(status_code=404, detail="File not found")
            return {"saved_to": path}
        except HTTPException:
            raise
        except Exception as e:
            self.logger.exception(f"Download failed for '{file_name}': {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def delete_file(self, file_name: str, db: Session = Depends(get_db)):
        service = StorageService(supabase_client, "uploads", db)
        try:
            result = service.delete_file(file_name)
            if not result:
                raise HTTPException(status_code=404, detail="File not found")
            return DeleteResponse(message="File deleted successfully")
        except HTTPException:
            raise
        except Exception as e:
            self.logger.exception(f"Delete failed for '{file_name}': {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def list_files(
        self,
        user_id: str | None = Query(None),
        db: Session = Depends(get_db)
    ):
        service = StorageService(supabase_client, "uploads", db)
        try:
            files = service.list_files(user_id)
            if files is None:
                self.logger.error("StorageService.list_files returned None")
                raise HTTPException(status_code=500, detail="Could not fetch files")

            return [
                FileItem(
                    id=f.id,
                    filename=f.filename,
                    storage_url=f.storage_url,
                    user_id=f.user_id,
                    status=f.status,
                    created_at=f.created_at,
                )
                for f in files
            ]
        except HTTPException:
            raise
        except Exception as e:
            self.logger.exception(f"List files failed: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    def get_public_url(self, file_name: str, db: Session = Depends(get_db)):
        service = StorageService(supabase_client, "uploads", db)
        try:
            url = service.get_public_url(file_name)
            return PublicURLResponse(url=url)
        except Exception as e:
            self.logger.exception(f"Get public URL failed for '{file_name}': {e}")
            raise HTTPException(status_code=500, detail="Could not generate public URL")

    def update_status(
        self,
        upload_id: str,
        payload: UpdateStatusRequest,
        db: Session = Depends(get_db)
    ):
        service = StorageService(supabase_client, "uploads", db)
        try:
            success = service.update_upload_status(upload_id, payload.status)
            if not success:
                raise HTTPException(status_code=404, detail="Upload not found")
            return {"message": "Status updated"}
        except HTTPException:
            raise
        except Exception as e:
            self.logger.exception(f"Update status failed for '{upload_id}': {e}")
            raise HTTPException(status_code=500, detail="Internal server error")
