import os
from uuid import UUID
from config import settings
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

class JWTHandler:
    def __init__(self, secret_key: str = settings.SECRET_KEY,
        algorithm: str = settings.ALGORITHM,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")
        self.session_ttl_minutes = 180

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes)
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return token

    def create_candidate_jwt(
            self,
            exam_session_id: UUID,
            submission_id: UUID,
            exam_id: UUID,
    ) -> str:
        payload = CandidateExamToken(
            exam_session_id=exam_session_id,
            submission_id=submission_id,
            exam_id=exam_id,
            exp=datetime.now(datetime.UTC) + timedelta(minutes=self.session_ttl_minutes),
        )

        return jwt.encode(payload.model_dump(), self.secret_key, self.algorithm)

    def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def get_current_user(self, token: str = Depends(OAuth2PasswordBearer(tokenUrl="/v1/auth/login"))):
        return self.verify_token(token)
