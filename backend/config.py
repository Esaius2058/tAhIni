from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    AIVEN_DATABASE_URL: str
    DATABASE_URL: str
    DATABASE_POOLER_URL: str
    USER: str
    HOST: str
    PORT: str
    DB_NAME: str
    SUPABASE_URL: str
    SUPABASE_KEY: str
    HUGGING_FACE_TOKEN: str
    COHERE_KEY: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DB_VENDOR: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env")

settings = Settings()