from fastapi import APIRouter, HTTPException, Query, status, Depends
from Campus_clinic_api.crud import (
    get_all_appointments, get_appointments_by_id,
    update_appointment_by_id,delete_appointment_by_id,
    create_appointment,create_user,authenticate_user, get_all_doctors
)
from Campus_clinic_api.schemas import (
    UserResponse,TokenResponse,PaginatedResponse, DoctorResponse,MeResponse,
    AppointmentResponse, UserCreate, AppointmentCreate, AppointmentUpdate
    )
from Campus_clinic_api.database import get_db, Base, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from Campus_clinic_api.models import User
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from datetime import datetime, timedelta
import jwt
import os




router = APIRouter(prefix="/Campus_clinic", tags=["clinic"])

load_dotenv()

SECRET_KEY= os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXP_MINS= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Campus_clinic/login")

def create_access_token(data:dict) -> str:
    to_encode= data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXP_MINS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY,algorithm=ALGORITHM)

def verify_access_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    user = db.query(User).filter(User.id == int(payload.get("sub"))).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


@router.post("/login", response_model=TokenResponse, description="Logins in user")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token":token,
        "token_type":"bearer"
    }


@router.post("/register", response_model=UserResponse, description="Register a student or doctor")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    return new_user



@router.post("/appointments", response_model=AppointmentResponse, status_code=status.HTTP_200_OK, description="Book an appointment")
def create_an_appointment(appointment: AppointmentCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return create_appointment(db, appointment, current_user)


@router.get("/appointments", response_model=PaginatedResponse, status_code=status.HTTP_200_OK,description="Get all appointment")
def get_all_appointment_paginated(
    page: int = Query(1, ge=1),
    limit: int=Query(10, ge=1, le=50),
    status: str = Query(None),
    db: Session= Depends(get_db), 
    current_user: dict = Depends(get_current_user)):
    db_appointment = get_all_appointments(db, page, limit, status, current_user)
    return db_appointment

@router.get("/appointments/{id}", response_model=AppointmentResponse,status_code=status.HTTP_200_OK, description="Get single appointment")
def get_single_appointment(id: int, db: Session = Depends(get_db),current_user: dict= Depends(get_current_user)):
    db_appointment = get_appointments_by_id(db, id)
    if not db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    return db_appointment

@router.put("/appointment/{id}", response_model=AppointmentResponse,status_code=status.HTTP_200_OK, description="Update appointment")
def update_appointment(id: int, update: AppointmentUpdate, db: Session = Depends(get_db), current_user: dict= Depends(get_current_user)):
    db_appointment = update_appointment_by_id(db, id, update)
    if not db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Appointment not found"
        )
    return db_appointment


@router.delete("/appointment/{id}", status_code=status.HTTP_200_OK,description="Delete/Cancel appointment")
def delete_appointment(id: int, db:Session= Depends(get_db), current_user: dict= Depends(get_current_user)):
    db_appointment = delete_appointment_by_id(db, id)
    if not db_appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Appointment not found"
        )
    return db_appointment

@router.get("/doctors", response_model=list[DoctorResponse], description="Get all doctors")
def get_doctor(db: Session= Depends(get_db), current_user: dict= Depends(get_current_user)):
    db_doc = get_all_doctors(db)
    return db_doc


@router.get("/me", response_model=MeResponse, description="Returns the currently logged in user")
def get_me(current_user: User = Depends(get_current_user)):
    return current_user