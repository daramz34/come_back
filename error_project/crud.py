from auth_project.database import SessionLocal
from models import Item
from auth_project.schemas import ItemCreate, ItemResponse
from sqlalchemy.orm import Session
from security import hash_password

def create_item(db: Session, item_in: ItemCreate):
    secured_password = hash_password(item_in.password)
    db_item = Item(**item_in.model_dump(exclude={"password"}), hashed_password=secured_password)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item


def get_item(db:Session):
    return db.query(Item).all()


def delete_item(db:Session, id:int )-> bool:
    db_item = db.query(Item).filter(Item.id ==id).first()
    if not db_item:
        return False

    db.delete(db_item)
    db.commit()
    return True    


def get_paginated_items(db:Session, skip: int=0, limit: int=5, min_price:float = None,max_price: float = None):
    query = db.query(Item)
    
    if min_price is not None:
        query = query.filter(Item.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Item.price <= max_price)
    
    total_count = query.count()

    data = query.offset(skip).limit(limit).all()

    return data, total_count

def get_user_by_email(db:Session,email:str):
    return db.query(Item).filter(Item.email==email).first()