import pytest
from src.db.models.models import UserType
from src.utils.exceptions import AuthError, ConflictError, ServiceError, NotFoundError
from src.services.auth import AuthService
from src.services.user import UserService
from tests.conftest import test_db_session

class DummyHasher:
    def __init__(self):
        self.hashed_passwords = {}

    def get_password_hash(self, password: str):
        hashed = f"hashed_{password}"
        self.hashed_passwords[password] = hashed
        return hashed

    def verify_password(self, plain_password: str, hashed_password: str):
        return hashed_password == self.hashed_passwords.get(plain_password)


class DummyJWTHandler:
    def __init__(self):
        self.tokens = {}

    def create_access_token(self, payload: dict):
        token = f"token_{payload['user_id']}"
        self.tokens[token] = payload
        return token

    def verify_token(self, token: str):
        return self.tokens.get(token)


@pytest.fixture
def user_service(test_db_session):
    return UserService(test_db_session)


@pytest.fixture
def auth_service(user_service):
    jwt_handler = DummyJWTHandler()
    password_hasher = DummyHasher()
    return AuthService(
        user_service=user_service,
        jwt_handler=jwt_handler,
        password_hasher=password_hasher
    )

@pytest.fixture
def sample_user(user_service, auth_service):
    name = "John Doe"
    email = "john@example.com"
    password = "password123"
    hashed_pw = auth_service.password_hasher.get_password_hash(password)
    user = user_service.create_user(name, email, hashed_pw, user_type=UserType.STUDENT)
    yield user
    user_service.delete_user(user.id)


def test_register_user(auth_service, user_service):
    name = "Alice"
    email = "alice@example.com"
    password = "securepass"

    result = auth_service.register_user(name, email, password)
    user = user_service.get_user_by_email(email)

    assert result["id"] == user.id
    assert result["email"] == user.email
    assert UserType.STUDENT == result["role"]


def test_register_user_conflict(auth_service, sample_user):
    with pytest.raises((ConflictError, ServiceError)):
        auth_service.register_user(
            name="John Clone",
            email=sample_user.email,
            password="duplicate"
        )


def test_login_user_success(auth_service, sample_user):
    result = auth_service.login_user(email=sample_user.email, password="password123")
    assert "access_token" in result
    assert result["token_type"] == "bearer"


def test_login_user_invalid_password(auth_service, sample_user):
    with pytest.raises((AuthError, NotFoundError)):
        auth_service.login_user(email=sample_user.email, password="wrongpassword")


def test_login_user_not_found(auth_service):
    with pytest.raises(ServiceError):
        auth_service.login_user(email="missing@example.com", password="irrelevant")


def test_verify_token_success(auth_service, sample_user):
    token_data = auth_service.login_user(email=sample_user.email, password="password123")
    token = token_data["access_token"]
    user = auth_service.verify_token(token)

    assert user.id == sample_user.id
    assert user.email == sample_user.email


def test_verify_token_invalid(auth_service):
    with pytest.raises(AuthError):
        auth_service.verify_token("invalid_token")


def test_verify_token_user_not_found(auth_service, user_service):
    token = auth_service.jwt_handler.create_access_token({"user_id": "cd867592-12e3-4b28-9b5f-959613416ebd", "user_type": UserType.STUDENT})
    with pytest.raises(ServiceError):
        auth_service.verify_token(token)
