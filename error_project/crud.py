from error_project.database import SessionLocal
from error_project.models import Item, User  
from error_project.schemas import ItemCreate, UserCreate
from sqlalchemy.orm import Session
from error_project.security import hash_password

# --- USER CRUD OPERATIONS ---
def create_user(db: Session, user_in: UserCreate):
    secured_password = hash_password(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=secured_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# --- ITEM CRUD OPERATIONS ---
def create_item(db: Session, item_in: ItemCreate, owner_id: int):
    db_item = Item(
        name=item_in.name,
        description=item_in.description,
        price=item_in.price,
        user_id=owner_id  
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item(db: Session):
    return db.query(Item).all()

def delete_item(db: Session, id: int) -> bool:
    db_item = db.query(Item).filter(Item.id == id).first()
    if not db_item:
        return False
    db.delete(db_item)
    db.commit()
    return True    

def get_paginated_items(db: Session, skip: int = 0, limit: int = 5, min_price: float = None, max_price: float = None):
    query = db.query(Item)
    if min_price is not None:
        query = query.filter(Item.price >= min_price)
    if max_price is not None:
        query = query.filter(Item.price <= max_price)
    
    total_count = query.count()
    data = query.offset(skip).limit(limit).all()
    return data, total_count