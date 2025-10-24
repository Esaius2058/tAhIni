import pytest, os, sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from src.db.base import Base
from src.db.models import *
from config import settings

@pytest.fixture(scope="function")
def test_db_session():
    # Dynamically choose DB
    TEST_DATABASE_URL = os.getenv(
        "TEST_DATABASE_URL",
        "sqlite:///:memory:"  # default to SQLite for speed
    )

    engine = create_engine(TEST_DATABASE_URL)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(engine)
