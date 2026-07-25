from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from Campus_clinic_api.database import Base
from datetime import datetime
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, nullable=False, unique=True)
    email    = Column(String, index=True, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)

    student_appointments= relationship("Appointment", back_populates="student", foreign_keys="Appointment.student_id")
    doctor_appointments = relationship("Appointment", back_populates="doctor", foreign_keys="Appointment.doctor_id")


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String)
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String, default="pending")
    
    student_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default= datetime.utcnow)


    student = relationship("User", back_populates="student_appointments", foreign_keys=[student_id])
    doctor = relationship("User", back_populates="doctor_appointments", foreign_keys=[doctor_id])
