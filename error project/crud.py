from database import SessionLocal
from models import Item
from schemas import ItemCreate, ItemResponse
from sqlalchemy.orm import Session


def create_item(db: Session, item_in: ItemCreate):
    db_item = Item(**item_in.model_dump())
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