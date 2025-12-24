import logging, supabase, io
from src.db.models import Uploads
from uuid import UUID
from src.utils.exceptions import ServiceError, NotFoundError

class StorageService:
    def __init__(self, client: supabase.Client, bucket, db_session):
        self.client = client
        self.bucket = bucket
        self.db = db_session
        self.logger = logging.getLogger("Storage Service")

    def upload_file(self, file_obj, file_name: str, user_id: UUID):
        try:
            bucket = self.client.storage.from_(self.bucket)
            bucket.upload(file_name, file_obj)

            public_url = bucket.get_public_url(file_name)
            upload = Uploads(filename=file_name, storage_url=public_url, user_id=user_id)

            self.db.add(upload)
            self.db.commit()
            return upload
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Failed to upload file '{file_name}': {e}")
            return None

    def download_file(self, file_name: str, destination_path: str):
        try:
            bucket = self.client.storage.from_(self.bucket)
            file_data = bucket.download(file_name)

            with open(destination_path, "wb") as f:
                f.write(file_data)

            return destination_path
        except FileNotFoundError:
            self.logger.warning(f"File not found: {file_name}")
            return None
        except Exception as e:
            self.logger.error(f"Failed to download '{file_name}': {e}")
            return None

    def delete_file(self, file_name: str):
        try:
            bucket = self.client.storage.from_(self.bucket)
            bucket.remove([file_name])

            upload = self.db.query(Uploads).filter_by(filename=file_name).first()
            if upload:
                self.db.delete(upload)
                self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Failed to delete file '{file_name}': {e}")
            return None

    def get_public_url(self, file_name: str):
        try:
            bucket = self.client.storage.from_(self.bucket)
            return bucket.get_public_url(file_name)
        except Exception as e:
            self.logger.error(f"Error getting public URL for '{file_name}': {e}")
            raise ServiceError("Could not generate public URL") from e

    def list_files(self, user_id: UUID = None):
        try:
            query = self.db.query(Uploads)
            if user_id:
                query = query.filter_by(user_id=user_id)
            return query.all()
        except Exception as e:
            self.logger.error(f"Failed to list files: {e}")
            return None

    def update_upload_status(self, upload_id: UUID, status: str):
        try:
            upload = self.db.query(Uploads).get(upload_id)
            if not upload:
                raise NotFoundError("Upload not found")

            upload.status = status
            self.db.commit()
            return True
        except NotFoundError:
            return False
        except Exception as e:
            self.db.rollback()
            self.logger.error(f"Failed to update status for upload '{upload_id}': {e}")
            return False