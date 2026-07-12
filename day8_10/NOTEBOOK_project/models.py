from sqlalchemy import Column, String, Integer, Float, Text, DateTime
from auth_project.database import Base
from datetime import datetime


class NOTES(Base):
    __tablename__ = "Notes"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    content = Column(Text)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)