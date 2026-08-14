from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    bio: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    bio: Optional[str] = None
    created_at: datetime

    class config:
        from_attributes = True


class PostCreate(BaseModel):
    title: str = Field(..., max_length=100)
    content: str
    
    

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    is_published: bool
    like_count: int = 0
    created_at: datetime
    updated_at: datetime
    author: UserResponse   # FULL author details not just ID

    class config: 
        from_attributes= True

class PaginatedPostResponse(BaseModel):
    total: int
    page: int
    limit: int
    results: list[PostResponse]
class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    content: Optional[str] = None
    is_published: Optional[bool] = None
    


class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    author: UserResponse

    class config:
        from_attributes = True

class LikeResponse(BaseModel):
    post_id: int
    like_count: int

    class config: 
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
