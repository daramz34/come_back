from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class ItemCreate(BaseModel):
    name: str
    description: str
    price: float

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    description: str
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PaginationItemResponse(BaseModel):
    total: int
    page: int
    limit: int
    results: List[ItemResponse]

class Token(BaseModel):
    access_token: str
    token_type: str