from pydantic import BaseModel, Field, EmailStr
from typing import Literal


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Literal["Student", "Doctor"]


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: Literal["Student", "Doctor"]

    class Config:
        from_attributes = True



# remains the remainig schemas