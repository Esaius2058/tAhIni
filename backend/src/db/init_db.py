from src.db.base import engine
from base import Base

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
