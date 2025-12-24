import uuid
import pytest, sys, os
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from src.db.database import engine
from src.db.base import Base
from src.db.models.models import Exam, Question, User, UserType, Submission, Feedback, GradeLog

# set up a fresh test database session
Session = sessionmaker(bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    sess = Session()
    yield sess
    sess.rollback()
    sess.close()

def test_insert_exam(session):
    exam = Exam(
        id=uuid.uuid4(),
        title="Math Final",
        subject="Mathematics",
        duration="2h"
    )
    session.add(exam)
    session.commit()

    result = session.query(Exam).filter_by(title="Math Final").first()
    assert result is not None
    assert result.subject == "Mathematics"

def test_insert_question_with_exam_fk(session):
    exam = Exam(
        id=uuid.uuid4(),
        title="CAT 1",
        subject="English",
        duration="2h"
    )
    session.add(exam)
    session.commit()

    question = Question(
        id=uuid.uuid4(),
        type="MCQ",
        text="What is Newton's 2nd law?",
        difficulty="medium",
        exam_id=exam.id
    )
    session.add(question)
    session.commit()

    result = session.query(Question).filter_by(exam_id=exam.id).first()
    assert result.text == "What is Newton's 2nd law?"

def test_fk_constraint_on_question_exam_id(session):
    exam = Exam(
        id=uuid.uuid4(),
        title="CAT 1",
        subject="English",
        duration="2h"
    )
    session.add(exam)
    session.commit()

    question = Question(
        id=uuid.uuid4(),
        type="MCQ",
        text="What is Newton's 2nd law?",
        difficulty="medium",
        exam_id=uuid.uuid4()
    )
    session.add(question)

    with pytest.raises(IntegrityError):
        session.commit()

def test_insert_submission_and_user(session):
    user = User(
        id=uuid.uuid4(),
        name="Flynn",
        email="flynn@americazzz.com",
        password="hello world"
    )
    session.add(user)
    session.commit()

    exam = Exam(
        id=uuid.uuid4(),
        title="CAT 1",
        subject="English",
        duration="2h"
    )
    session.add(exam)
    session.commit()

    submission = Submission(
        id=uuid.uuid4(),
        user_id=user.id,
        exam_id=exam.id
    )
    session.add(submission)
    session.commit()

    assert submission is not None
    assert submission.user_id == user.id
    assert submission.exam_id == exam.id

def test_invalid_submission_fk(session):
    submission = Submission(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        exam_id=uuid.uuid4()
    )

    session.add(submission)
    with pytest.raises(IntegrityError):
        session.commit()

def test_insert_feedback_and_gradelog(session):
    user = User(
        id=uuid.uuid4(),
        name="Flynn",
        email="flynn@americazzz.com",
        password="hello world",
    )
    session.add(user)
    session.commit()

    user2 = User(
        id=uuid.uuid4(),
        name="Lorraine",
        email="lorraine@gmail.com",
        password="hello world",
        type=UserType.INSTRUCTOR
    )
    session.add(user2)
    session.commit()

    exam = Exam(
        id=uuid.uuid4(),
        title="Semi Final",
        subject="History",
        duration="1h30m"
    )
    session.add(exam)
    session.commit()

    submission = Submission(
        id=uuid.uuid4(),
        user_id=user2.id,
        exam_id=exam.id
    )
    session.add(submission)
    session.commit()

    feedback = Feedback(
        id=uuid.uuid4(),
        submission_id=submission.id,
        comments="should focus more on details and specification of answers",
        author_id=user.id
    )
    session.add(feedback)
    session.commit()

    gradelog = GradeLog(
        id=uuid.uuid4(),
        score=56.00,
        grader=user.id,
        submission_id=submission.id
    )
    session.add(gradelog)
    session.commit()

    assert feedback.id is not None
    assert gradelog.grader == feedback.author_id
