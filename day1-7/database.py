from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_URL = "sqlite:///./local_campus.db"

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)  #(10, 2) means Allow a max of 10 digits in total and exactly 2 of those digits must sit behind the decimal point
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    print("Syncing models with the db")
    init_db()
    print("Successful")