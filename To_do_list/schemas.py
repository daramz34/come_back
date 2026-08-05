from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from To_do_list.enums import TodoStatus, Priority

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    

    class Config:
        from_attributes = True


class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TodoStatus
    priority: Priority
    due_date: datetime
    

class TodoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TodoStatus
    priority: Priority
    due_date: datetime
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


