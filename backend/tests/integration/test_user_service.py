import pytest, sys, os
from sqlalchemy.orm import sessionmaker
from ..conftest import test_db_session
from src.db.models import User, UserType
from src.services.user import UserService
from src.utils.exceptions import NotFoundError, ServiceError

@pytest.fixture
def user_service(test_db_session):
    return UserService(test_db_session)

def test_create_user(user_service, test_db_session):
    user_service.create_user(name="Alice", email="alice@gmail.com", pwd="hello")
    user = test_db_session.query(User).filter_by(email="alice@gmail.com").first()
    assert user is not None
    assert user.type == UserType.STUDENT

def test_get_user_by_id(user_service, test_db_session):
    user = User(name="Bob", email="bob43@gmail.com", password="hello")
    test_db_session.add(user)
    test_db_session.commit()

    fetched = user_service.get_user_by_id(user.id)
    assert fetched.email == "bob43@gmail.com"

def test_update_user_type(user_service, test_db_session):
    user = User(name="Dave", email="dave@gmail.com", password="helloworld")
    test_db_session.add(user)
    test_db_session.commit()

    assert user_service.delete_user(user.id) is True

def test_list_users(user_service, test_db_session):
    test_db_session.add_all([
        User(name="Eve", email="eve@example.com", password="123"),
        User(name="Frank", email="frank@example.com", password="456", type=UserType.INSTRUCTOR),
    ])
    test_db_session.commit()

    all_users = user_service.list_users()
    assert len(all_users) == 2

    filtered = user_service.list_users(role=UserType.INSTRUCTOR)
    assert len(filtered) == 1
    assert filtered[0].name == "Frank"