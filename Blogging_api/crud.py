from sqlalchemy.orm import Session
from Blogging_api.models import User
from Blogging_api.schemas import UserCreate
from Blogging_api.core.security import hashed_password, verify_password




def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user:UserCreate):
    db_user = User(**user.model_dump(exclude={"password"}),
                   hashed_password = hashed_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username:str, password: str):
    db_user = get_user_by_username(db, username)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


