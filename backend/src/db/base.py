from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))
from config import settings

Base = declarative_base()
engine = create_engine(settings.DATABASE_URL, echo=True)
