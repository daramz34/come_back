from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes=True
    
class BookCreate(BaseModel):
    title: str
    author: str
    genre: Optional[str] = None

class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    genre: Optional[str] = None
    created_at: datetime

    class Config:
        from_atrributes=True

class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str
    

class ReviewResponse(BaseModel):
    id: int
    rating: int = Field(..., ge=1, le=5)
    comment: str
    created_at: datetime
    user: Optional[UserResponse]
    book: Optional[BookResponse]

    class Config:
        from_attributes=True



class LoginRequest(BaseModel):
    username: str
    password: str



class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
