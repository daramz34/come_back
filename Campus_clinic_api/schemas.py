from pydantic import BaseModel, Field, EmailStr
from typing import Literal, Optional
from datetime import datetime

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


class MeResponse(BaseModel):
    username: str
    role: Literal["Student", "Doctor"]
    class Config:
        from_attributes = True
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AppointmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    appointment_date: datetime
    doctor_id : int
    
class AppointmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    appointment_date: Optional[datetime] = None
    status: Optional[Literal["pending", "confirmed", "cancelled"]] = None

class DoctorResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True
class AppointmentResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    appointment_date: datetime
    status: Literal["pending", "confirmed", "cancelled"]
    created_at: datetime
    student: UserResponse
    doctor: UserResponse

    class Config:
        from_attributes = True


class PaginatedResponse(BaseModel):
    total: int
    page: int
    limit : int
    results: list[AppointmentResponse]

    class Config:
        from_attributes = True


class AppointmentStatusUpdate(BaseModel):
    status: Literal["pending", "confirmed", "cancelled"]

