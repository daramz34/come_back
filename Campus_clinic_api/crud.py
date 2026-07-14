from Campus_clinic_api.schemas import AppointmentCreate,AppointmentResponse,AppointmentUpdate,UserCreate,UserResponse,TokenResponse
from sqlalchemy.orm import Session
from Campus_clinic_api.models import User, Appointment
from passlib.context import CryptContext
from typing import Literal


pwd_Context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_Context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_Context.verify(plain_password, hashed_password)
def get_user_by_username(db: Session, username: str):
    db_user = db.query(User).filter(User.username == username).first()
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    db_user = get_user_by_username(db, username)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_user(db: Session, user: UserCreate):
    db_user = User(**user.model_dump(exclude={"password"}),
                   hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def create_appointment(db:Session, appointment: AppointmentCreate):
    db_appointment = Appointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment



def get_all_appointments(db: Session, page: int=1, limit: int=10, status: Literal["pending", "confirmed", "cancelled"]= None):
    offset = (page - 1) *limit
    query = db.query(Appointment)
    
    if status:
        query = query.filter(Appointment.status == status)

    total = query.count()
    appointments = (query.offset(offset).limit(limit).all())
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "results": appointments

    }



def get_appointments_by_id(db: Session, id: int):
    db_user = db.query(Appointment).filter(Appointment.id == id).first()
    return db_user

def update_appointment_by_id(db: Session, id:int, update=AppointmentUpdate):
    db_appointment = db.query(Appointment).filter(Appointment.id == id).first()

    if not db_appointment:
        return None
    
    db_update = update.model_dump()
    for key, value in db_update.items():
        setattr(db_appointment, key, value)
    db.commit()
    db.refresh(db_update)
   
    return db_update



def delete_appointment_by_id(db:Session, id: int):
    db_appointment = db.query(Appointment).filter(Appointment.id == id).first()
    if not db_appointment:
        return None
    
    db.delete(db_appointment)
    db.commit()
    return{
        "Msg": "deletd successfully"
    }