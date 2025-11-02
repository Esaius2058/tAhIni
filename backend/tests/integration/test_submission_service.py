import pytest
from src.services.submission import SubmissionService
from src.services.user import UserService
from src.services.questions import QuestionService
from src.utils.exceptions import ServiceError, NotFoundError
from src.db.models import Submission, SubmissionAnswer, QuestionType, Exam, UserType
from tests.conftest import test_db_session

@pytest.fixture
def user_service(test_db_session):
    return UserService(test_db_session)


@pytest.fixture
def question_service(test_db_session):
    return QuestionService(test_db_session)


@pytest.fixture
def submission_service(test_db_session):
    return SubmissionService(test_db_session)

@pytest.fixture
def sample_exam(test_db_session):
    exam = Exam(
        title="End of Semester",
        subject="Math"
    )
    test_db_session.add(exam)
    test_db_session.commit()
    yield exam
    test_db_session.delete(exam)
    test_db_session.commit()

@pytest.fixture
def sample_user(user_service, test_db_session):
    user = user_service.create_user(
        name="Jane Student",
        email="jane@student.com",
        pwd="hashed_pw",
        user_type=UserType.STUDENT,
    )
    test_db_session.add(user)
    test_db_session.commit()
    yield user
    user_service.delete_user(user.id)
    test_db_session.commit()

@pytest.fixture
def sample_question(question_service):
    question = question_service.store_question(
        text="Explain Newton’s First Law of Motion.",
        tags=["physics", "science"],
        question_type=QuestionType.ESSAY,
        bulk=True
    )
    question_service.db.add(question)
    question_service.db.commit()
    yield question
    question_service.db.delete(question)
    question_service.db.commit()


@pytest.fixture
def sample_submission(submission_service, sample_user, sample_exam):
    exam_id = sample_exam.id
    submission_service.create_submission(sample_user.id, exam_id)
    submission = (
        submission_service.db.query(Submission)
        .filter_by(user_id=sample_user.id, exam_id=exam_id)
        .first()
    )
    yield submission
    submission_service.db.delete(submission)
    submission_service.db.commit()


def test_create_submission(submission_service, sample_user, test_db_session, sample_exam):
    exam_id = sample_exam.id
    submission_service.create_submission(sample_user.id, exam_id)
    query = (
        test_db_session.query(Submission)
        .filter_by(user_id=sample_user.id, exam_id=exam_id)
        .first()
    )
    assert query is not None
    assert query.exam_id == exam_id
    assert query.user_id == sample_user.id


def test_add_answer_success(submission_service, sample_submission, sample_question, test_db_session):
    result = submission_service.add_answer(
        submission_id=sample_submission.id,
        question_id=sample_question.id,
        answer_text="It states that an object remains in uniform motion unless acted upon by force."
    )
    assert result is True
    saved = (
        test_db_session.query(SubmissionAnswer)
        .filter_by(submission_id=sample_submission.id, question_id=sample_question.id)
        .first()
    )
    assert saved is not None
    assert "object remains" in saved.answer


def test_add_answer_updates_existing(submission_service, sample_submission, sample_question):
    submission_service.add_answer(sample_submission.id, sample_question.id, "Initial answer")
    submission_service.add_answer(sample_submission.id, sample_question.id, "Updated answer")

    updated = (
        submission_service.db.query(SubmissionAnswer)
        .filter_by(submission_id=sample_submission.id, question_id=sample_question.id)
        .first()
    )
    assert updated.answer == "Updated answer"


def test_add_answer_nonexistent_submission(submission_service, sample_question):
    with pytest.raises(NotFoundError):
        submission_service.add_answer(
            submission_id="0488cf2b-adab-453a-88c6-d622db8656c2",
            question_id=sample_question.id,
            answer_text="Invalid submission case"
        )


def test_get_submission_by_id(submission_service, sample_submission, sample_question):
    submission_service.add_answer(sample_submission.id, sample_question.id, "Force and inertia")
    data = submission_service.get_submission_by_id(sample_submission.id)

    assert data["submission_id"] == sample_submission.id
    assert data["user_id"] == sample_submission.user_id
    assert "answers" in data
    assert len(data["answers"]) >= 1
    assert "Force" in data["answers"][0]["answer_text"]


def test_get_submission_not_found(submission_service):
    with pytest.raises(NotFoundError):
        submission_service.get_submission_by_id("0488cf2b-adab-453a-88c6-d622db8656c2")


def test_list_exam_submissions_basic(submission_service, sample_submission):
    results = submission_service.list_exam_submissions_basic(exam_id=sample_submission.exam_id)
    assert any(sub["submission_id"] == sample_submission.id for sub in results)
    assert "user_id" in results[0]
    assert "submitted_at" in results[0]


def test_list_exam_submissions_detailed(submission_service, sample_submission):
    results = submission_service.list_exam_submissions_detailed(exam_id=sample_submission.exam_id)
    assert isinstance(results, list)
    assert all("submission_id" in r for r in results)
    assert all("exam_id" in r for r in results)


def test_list_exam_submissions_basic_error(monkeypatch, submission_service):
    def faulty_query(*args, **kwargs):
        raise Exception("DB failed")

    monkeypatch.setattr(submission_service, "_base_submission_query", faulty_query)

    with pytest.raises(ServiceError):
        submission_service.list_exam_submissions_basic(exam_id="0488cf2b-adab-453a-88c6-d622db8656c2")


def test_list_exam_submissions_detailed_error(monkeypatch, submission_service):
    def faulty_query(*args, **kwargs):
        raise Exception("DB failed")

    monkeypatch.setattr(submission_service, "_base_submission_query", faulty_query)

    with pytest.raises(ServiceError):
        submission_service.list_exam_submissions_detailed(exam_id="0488cf2b-adab-453a-88c6-d622db8656c2")
