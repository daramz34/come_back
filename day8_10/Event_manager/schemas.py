from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class EventCreate(BaseModel):
    title: str
    organizer: str
    capacity: int
    ticket_price: float

    

class EventResponse(BaseModel):
    id: int
    title: str
    organizer: str
    capacity: int
    ticket_price: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes= True


class EventUpdate(BaseModel):
    title: Optional[str] = None
    organizer: Optional[str] = None
    capacity: Optional[int] = None
    ticket_price: Optional[float] = None
    
