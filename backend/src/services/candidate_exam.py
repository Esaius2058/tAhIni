from datetime import datetime
from src.db.models import CandidateExamSession, ExamStatus, Answer
from src.utils.exceptions import NotFoundError, ServiceError

class CandidateExamService:
    def __init__(self, db, logger):
        self.db = db
        self.logger = logger

    def _get_active_session(self, session_id):
        session = (
            self.db.query(CandidateExamSession)
            .filter(CandidateExamSession.id == session_id)
            .one_or_none()
        )

        if not session:
            raise NotFoundError("Exam session not found")

        if session.status != ExamStatus.IN_PROGRESS:
            raise ServiceError("Exam session is not active")

        if datetime.now(datetime.UTC) > session.ends_at:
            session.status = ExamStatus.TIMED_OUT
            self.db.commit()
            raise ServiceError("Exam session has expired")

        return session

    def upsert_submission_answer(self, submission_id: UUID, question_id: UUID, answer_text: str):
        record = (
            self.db.query(SubmissionAnswer)
            .filter_by(
                submission_id=submission_id,
                question_id=question_id,
            )
            .first()
        )

        if record:
            record.answer = answer_text
        else:
            record = SubmissionAnswer(
                submission_id=submission_id,
                question_id=question_id,
                answer=answer_text,
            )
            self.db.add(record)

        self.db.commit()
        return record

    def enter_exam(self, exam_code: str) -> Exam:
        exam = (
            self.db.query(Exam)
            .filter(Exam.exam_code == exam_code)
            .one_or_none()
        )

        if not exam:
            raise ServiceError("Invalid exam code")

        return exam

    def start_exam(
            self,
            exam_id: UUID,
            candidate_name: str,
            candidate_ref: str | None = None,
    ):
        exam = self.db.query(Exam).filter(Exam.id == exam_id).one_or_none()
        if not exam:
            raise ServiceError("Exam not found")

        if candidate_ref:
            existing = (
                self.db.query(CandidateExamSession)
                .filter(
                    CandidateExamSession.exam_id == exam_id,
                    CandidateExamSession.candidate_ref == candidate_ref,
                )
                .first()
            )
            if existing:
                raise ServiceError("Candidate has already started this exam")

        now = datetime.now(datetime.UTC)
        ends_at = now + timedelta(minutes=exam.duration_minutes)

        session = CandidateExamSession(
            exam_id=exam.id,
            candidate_name=candidate_name,
            candidate_ref=candidate_ref,
            started_at=now,
            ends_at=ends_at,
            status=ExamStatus.IN_PROGRESS,
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        token = create_candidate_jwt(
            session_id=session.id,
            expires_at=ends_at,
        )

        return {
            "session_id": session.id,
            "ends_at": ends_at,
            "token": token,
        }

    def get_questions(self, session_id: UUID) -> list[dict]:
        session = self._get_active_session(session_id)

        questions = (
            self.db.query(Question)
            .filter(Question.exam_id == session.exam_id)
            .all()
        )

        return [
            {
                "id": q.id,
                "type": q.type,
                "prompt": q.prompt,
                "options": q.options,   # MCQ only
                "required": q.required,
            }
            for q in questions
        ]

    def autosave(self, session_id: UUID, answers: list[AnswerInput]):
        session = self._get_active_session(session_id)

        for answer in answers:
            self.upsert_submission_answer(
                db=self.db,
                session_id=session.id,
                question_id=answer.question_id,
                payload=answer.payload,
            )

        self.db.commit()

    def submit_exam(self, session_id: UUID):
        session = self._get_active_session(session_id)

        if datetime.now(datetime.UTC) > session.ends_at:
            session.status = ExamStatus.EXPIRED
        else:
            session.status =ExamStatus.SUBMITTED

        session.submitted_at = datetime.now(datetime.UTC)
        self.db.commit()

