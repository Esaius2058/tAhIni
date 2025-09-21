import supabase
import logging
from backend.src.db.models import Uploads
from backend.src.services.supabase_client import supabase_client

class StorageService:
    def __init__(self, client: supabase.Client, bucket, db_session):
        self.client = client
        self.bucket = bucket
        self.db = db_session
        self.logger = logging.getLogger("Storage Service")

    def upload_file(self, file_obj, file_name: str, user_id):
        try:
            self.client.storage.from_(self.bucket).upload(file_name, file_obj)
            public_url = self.get_public_url(file_name)

            new_upload = Uploads(
                filename=file_name,
                storage_url=public_url,
                user_id=user_id
            )
            self.db.add(new_upload)
            self.commit()
            self.refresh(new_upload)

            return new_upload
        except Exception as e:
            self.logger.error(f"Error uploading file: {e}")
            self.db.rollback()
            return None

    def download_file(self, file_name: str, file_dest: str):
        try:
            res = supabase.storage.from_(bucket_name).download(file_name)
            with open(file_dest, "wb") as f:
                f.write(res)
            return file_dest
        except Exception as e:
            self.logger.error(f"Error downloading file: {e}")
            return None

    def delete_file(self, file_name: str):
        try:
            supabase.storage.from_(bucket_name).remove([file_name])

            upload = self.db.query(Uploads).filter_by(filename=file_name).first()
            if upload:
                self.db.delete(upload)
                self.db.commit()
            return f"{file_name} deleted successfully"
        except Exception as e:
            self.logger.error(f"Error deleting file: {e}")
            self.db.rollback()
            return None

    def get_public_url(self, file_name: str):
        try:
            return supabase.storage.from_(bucket_name).get_public_url([file_name])
        except Exception as e:
            self.logger.error(f"Error getting public url for '{file_name}': {e}")
            return None

    def list_files(self, user_id=None):
        try:
            query = self.db.query(Uploads)
            if user_id:
                query = query.filter_by(user_id=user_id)
            return query.all()
        except Exception as e:
            self.logger.error(f"Error listing uploaded files: {e}")
            self.db.rollback()
            return None

    def update_upload_status(self, upload_id, status) -> bool:
        try:
            upload = self.db.query(Uploads).filter_by(id=upload_id).first()
            if not upload:
                return False

            upload.status = status
            self.db.commit()
            self.db.refresh(upload)
            return True
        except Exception as e:
            self.logger.error(f"Error updating upload status: {e}")
            self.db.rollback()
            return False