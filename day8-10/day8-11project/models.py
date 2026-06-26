from sqlalchemy import String, Column, Float, Integer, Numeric, Boolean, DateTime
from datetime import datetime
from NOTEBOOK_project.database import Base


class Student(Base):
    __tablename__ = "STUDENT"
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    matric_number = Column(String(15), unique=True, nullable=False)
    gpa = Column(Numeric(1,2), nullable=False)
    is_active = Column(Boolean, default=True)
    enrolled_at = Column(DateTime, default=datetime.utcnow)


