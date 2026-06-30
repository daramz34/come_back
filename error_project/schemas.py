from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List

class ItemCreate(BaseModel):
    name: str
    description: str
    price: float
    email: EmailStr
    password: str


class ItemResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    price: float
    description: str
    created_at: datetime
    

    class Config:
        from_attributes = True


class PaginationItemResponse(BaseModel):
    total: int
    page: int
    limit: int
    results: list[ItemResponse]


    

