from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from database import Base


class Item(Base):
    __tablename__= "item"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, default=0.00)
    description = Column(String)
    hashed_password = Column(String, nullable=False)
    email= Column(String, nullable= False)
    created_at = Column(DateTime, default=datetime.utcnow)


