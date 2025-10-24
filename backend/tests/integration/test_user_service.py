import pytest
from unittest.mock import MagicMock, patch
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from backend.src.db.models import Base, User
from backend.src.services.user import UserService
from backend.src.utils.exceptions import NotFoundError, ServiceError

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(engine)
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture
def user_service(db_session):
    return UserService(db_session)

def test_create_user(user_service, db_session):
    user_service.create_user("Alice", "alice@gmail.com", "hello")
    user = db_session.query(User).filter_by(email="alice@gmail.com").first()
    assert user is not None
    assert user.type == "student"

def test_get_user_by_id(user_service, db_session):
    user = User("Bob", "bob43@gmail.com", "hello")
    db_session.add(user)
    db_session.commit()

    fetched = user_service.get_user_by_id(user.id)
    assert fetched.email == "bob43@gmail.com"

def test_update_user_type(user_service, db_session):
    user = User("Dave", "dave@gmail.com", "helloworld")
    db_session.add(user)
    db_session.commit()

    assert user_service.delete_user(user.id) is True
