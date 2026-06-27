from fastapi import FastAPI, Depends,status, HTTPException, Request
from Event_manager.database import get_db, Base,engine
from fastapi.responses import JSONResponse
from Event_manager.schemas import EventCreate, EventResponse,EventUpdate
from Event_manager.crud import create_event,delete_event,get_all_event,sorted_event_response,update_event
from sqlalchemy.orm import Session
from fastapi.exceptions import RequestValidationError
app = FastAPI(
    title="CAMPUS EVENT MANAGER",
    description="A FastAPI application that allows students clubs to list events, view available schedules, and delete canceled events",
    version="1.10.2",

)

Base.metadata.create_all(bind=engine)
@app.exception_handler(HTTPException)
async def custom_http_handler(request: Request, exc:HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error":
            {
                "message": exc.detail,
                "status": exc.status_code
            }
        }
    )


@app.get("/",summary="WELCOME PAGE")
def home():
    return{"msg": "welcome"}



@app.post("/event", response_model=EventResponse, status_code=status.HTTP_201_CREATED,
          summary="Create an Event")
def create_event_routes(event: EventCreate, db: Session = Depends(get_db)):
    return create_event(db=db, event=event)


@app.get("/sorted_event", response_model=list[EventResponse], status_code=status.HTTP_200_OK,
         summary="Set an order")
def get_sorted_routes(skip: int=0, limit: int=10,sort: str="id", db: Session=Depends(get_db)):
    return sorted_event_response(db=db, skip=skip, limit=limit, sort=sort)

@app.get("/event", response_model=list[EventResponse], status_code=status.HTTP_200_OK, 
         summary="Get all event")
def get_event(db:Session = Depends(get_db)):
    return get_all_event(db)

@app.put("/event/{event_id}", response_model=EventResponse, status_code=status.HTTP_200_OK, summary="Update an event")
def update_event_routes(event_id:int, event: EventUpdate, db: Session = Depends(get_db)):
    update_events = update_event(db=db, event=event, event_id=event_id)
    if not update_events:
        raise HTTPException(
          
                status_code=404,
                detail="Event not found"
            
        )
    return update_events


@app.delete("/event/{event_id}",  status_code=status.HTTP_204_NO_CONTENT,
            summary="Permantely delete a event")
def delete_event_route(event_id:int, db:Session = Depends(get_db)):
    delete = delete_event(db=db, event_id=event_id)
    if not delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="item not found")
    return delete