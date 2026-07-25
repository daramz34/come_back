from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass
class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True

class ItemCreate(BaseModel):
    name: str
    description: str
    price: float
    category_id: Optional[int] = None

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    description: str
    user_id: int
    created_at: datetime
    category_id: Optional[int] = None

    category: Optional[CategoryResponse] =None

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