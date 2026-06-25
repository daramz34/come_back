from pydantic import BaseModel
from datetime import datetime


class ItemCreate(BaseModel):
    name: str
    description: str
    price: float


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    description: str
    created_at: datetime
    

    class Config:
        from_attributes = True




