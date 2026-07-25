from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


DB_URL = f"sqlite:///{BASE_DIR}/items.db"



engine = create_engine(DB_URL, connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()