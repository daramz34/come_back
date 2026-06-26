from sqlalchemy.orm import Session
import NOTEBOOK_project.models as models
import NOTEBOOK_project.schemas as schemas

def get_responses(db:Session):
    return db.query(models.Student).all()


def create_responses(db:Session, student: schemas.StudentCreate):
    db_item = models.Student(**student.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item



def delete_responses_by_id(db:Session, id:int) -> bool:
    db_item = db.query(models.Student).filter(models.Student.id== id).first()
    if not db_item:
        return False
    
    db.delete(db_item)
    db.commit()
    return True

