from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from uuid import UUID
from config import settings
from fastapi import Depends, HTTPException, status
from src.db.database import get_db
from src.db.models import CandidateExamSession, ExamStatus
from src.utils.jwt import decode_jwt
from src.schemas.candidate_exam import CandidateExamToken

security = HTTPBearer()


def get_active_session(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> ExamSession:
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        data = CandidateExamToken(**payload)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid session token")

    session = (
        db.query(ExamSession)
        .filter(ExamSession.id == data.exam_session_id)
        .first()
    )

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status in {ExamStatus.SUBMITTED, ExamStatus.EXPIRED}:
        raise HTTPException(
            status_code=403,
            detail="Exam session is no longer active",
        )

    return session

def get_current_candidate_session(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> CandidateExamSession:
    try:
        token = credentials.credentials
        payload = decode_jwt(token)

        if payload.get("sub") != "candidate":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token scope"
            )

        session_id = payload.get("session_id")
        if not session_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session ID missing from token"
            )

        session = (
            db.query(CandidateExamSession)
            .filter(CandidateExamSession.id == UUID(session_id))
            .one_or_none()
        )

        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Exam session not found"
            )

        if session.status != ExamStatus.IN_PROGRESS:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Exam session is not active"
            )

        if datetime.now(timezone.utc) > session.ends_at:
            session.status = ExamStatus.TIMED_OUT
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Exam session has expired"
            )

        return session

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

