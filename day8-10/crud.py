from sqlalchemy.orm import Session
import models
import schemas

# READ ALL ITEMS
def get_all_items(db: Session):
    return db.query(models.Item).all()

# CREATE NEW ITEM
def create_item(db: Session, item_in: schemas.ItemCreateDTO):
    new_item = models.Item(
        name=item_in.name,
        description=item_in.description,
        price=item_in.price
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item