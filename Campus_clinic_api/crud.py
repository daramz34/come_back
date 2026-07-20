from Campus_clinic_api.schemas import AppointmentCreate,AppointmentResponse,AppointmentUpdate,UserCreate,UserResponse,TokenResponse, DoctorResponse
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



def create_appointment(db: Session, appointment: AppointmentCreate, current_user: User):
    db_appointment = Appointment(
        **appointment.model_dump(),
        student_id=current_user.id
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def get_all_appointments(db: Session, page: int=1, limit: int=10, status: Literal["pending", "confirmed", "cancelled"]= None, current_user: User =None):
   
    query = db.query(Appointment)
    if current_user.role == "Doctor":
        query = query.filter(Appointment.doctor_id==current_user.id)
    elif current_user.role == "Student":
        query = query.filter(Appointment.student_id == current_user.id)
    if status:
        query = query.filter(Appointment.status == status)

    offset = (page - 1) *limit
    total = query.count()
    appointments = (query.offset(offset).limit(limit).all())
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "results": appointments

    }

def get_all_doctors(db: Session):
    db_doc = db.query(User).filter(User.role == "Doctor").all()
    if not db_doc:
        return None
    return db_doc

def get_current_logged_in_user(user):
    return user

def get_appointments_by_id(db: Session, id: int):
    db_user = db.query(Appointment).filter(Appointment.id == id).first()
    return db_user

def update_appointment_by_id(db: Session, id:int, update:AppointmentUpdate):
    db_appointment = db.query(Appointment).filter(Appointment.id == id).first()

    if not db_appointment:
        return None
    
    db_update = update.model_dump(exclude_none=True)
    for key, value in db_update.items():
        setattr(db_appointment, key, value)
    db.commit()
    db.refresh(db_appointment)
   
    return db_appointment



def delete_appointment_by_id(db:Session, id: int):
    db_appointment = db.query(Appointment).filter(Appointment.id == id).first()
    if not db_appointment:
        return None
    
    db.delete(db_appointment)
    db.commit()
    return{
        "Msg": "Deleted successfully"
    }