import os
from backend.config import settings
from datetime import datetime, timedelta
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

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=self.expire_minutes)
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return token

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
