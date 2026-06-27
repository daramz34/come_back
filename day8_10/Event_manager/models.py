from sqlalchemy import Column, String, Integer, Numeric, DateTime
from datetime import datetime
from Event_manager.database import Base


class Event(Base):
    __tablename__ = "EVENT"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    organizer = Column(String, nullable=False)
    capacity = Column(Integer, nullable=False)
    ticket_price = Column(Numeric(7,2), default=0.00)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)