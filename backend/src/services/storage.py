import supabase
import logging
from backend.src.services.supabase_client import supabase_client

logger = logging.getLogger("Storage Service")
bucket_name = "uploads"

def upload_file(file_path: str, file_name: str):
    try:
        with open(file_path, "rb") as f:
            res = supabase.storage.from_(bucket_name).upload(file_name, f)
        return res
    except Exception as e:
        logger.info(f"Error uploading file: {e}")
        return None

def download_file(file_name: str, file_dest: str):
    try:
        res = supabase.storage.from_(bucket_name).download(file_name)
        with open(file_dest, "wb") as f:
            f.write(res)
        return file_dest
    except Exception as e:
        logger.info(f"Error downloading file: {e}")
        return None

def delete_file(file_name: str):
    try:
        return supabase.storage.from_(bucket_name).remove([file_name])
    except Exception as e:
        logger.info(f"Error downloading file: {e}")
        return None

def get_public_url(file_name: str):
    try:
        return supabase.storage.from_(bucket_name).get_public_url([file_name])
    except Exception as e:
        logger.info(f"Error downloading file: {e}")
        return None
