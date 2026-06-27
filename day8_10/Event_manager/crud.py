from sqlalchemy.orm import Session
from day8_10.Event_manager.schemas import EventCreate, EventResponse, EventUpdate
from day8_10.Event_manager.models import Event


def create_event(db: Session, event: EventCreate):
    db_event = Event(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    
    return db_event


def sorted_event_response(db:Session, skip: int=0, limit: int=10, sort: str="id"):
    db_query = db.query(Event)
    if sort == "organizer":
        db_query = db_query.order_by(Event.organizer)
    elif sort == "capacity":
        db_query = db_query.order_by(Event.capacity)
    elif sort == "ticket_price":
        db_query = db_query.order_by(Event.ticket_price)
    else:
        db_query = db_query.order_by(Event.id)
    return db_query.offset(skip).limit(limit).all()
    

def get_all_event(db:Session):
    return db.query(Event).all()


def update_event(db:Session, event_id:int,event: EventUpdate):
    db_event = db.query(Event).filter( Event.id == event_id).first()
    if not db_event:
        return None
    
    update_data = event.model_dump(exclude_none=True)

    for key,value in update_data.items():
        setattr(db_event, key, value)
    
    db.commit()
    db.refresh(db_event)
    return db_event



def delete_event(db:Session, event_id:int):
    db_event = db.query(Event).filter(Event.id ==event_id).first()
    if not db_event:
        return False
    db.delete(db_event)
    db.commit()
    return{
        "MSG":"EVENT was deleted successfully"
    }