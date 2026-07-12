from models import NOTES
from auth_project.database import SessionLocal
from auth_project.schemas import NoteResponse, NoteCreate, NoteUpdate
from sqlalchemy.orm import Session
from datetime import datetime




def create_note(db: Session, note: NoteCreate):
    db_notes = NOTES(**note.model_dump())
    db.add(db_notes)
    db.commit()
    db.refresh(db_notes)
    return db_notes

def get_notes(db: Session):
    return db.query(NOTES).all()

def get_notes_by_pagination(db:Session, skip: int = 0, limit: int = 8):
    query = db.query(NOTES)
    
    return query.offset(skip).limit(limit).all()


def update_notes(db: Session, note_id: int, note: NoteUpdate):
    db_notes = db.query(NOTES).filter(
        NOTES.id == note_id
    ).first()
    if not db_notes:
        return None
    update_data = note.model_dump()

    for key, value in update_data.items():
        setattr(db_notes, key, value)
    
    db.commit()
    db.refresh(db_notes)
    
    return db_notes


def delete_notes(db:Session, id:int):
    db_notes = db.query(NOTES).filter(NOTES.id==id).first()
    if not db_notes:
        return False
    db.delete(db_notes)
    db.commit()
    return{
        "msg": "Note deleted successfully"
    }
