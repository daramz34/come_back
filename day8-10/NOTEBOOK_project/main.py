from fastapi import FastAPI, Depends, status, HTTPException, Request
from NOTEBOOK_project.database import get_db, Base, engine
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from NOTEBOOK_project.crud import delete_notes, create_note, update_notes, get_notes
from NOTEBOOK_project.schemas import NoteCreate, NoteResponse, NoteUpdate


app = FastAPI()
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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "error":{
                "message": "You sent bad data.... Check your fields",
                "status": 400
            }

        }
        
    )


@app.post("/notes/", response_model=NoteResponse, status_code=status.HTTP_201_CREATED)
def create_notes_route(note: NoteCreate, db: Session = Depends(get_db)):
    return create_note(db=db, note=note)


@app.get("/notes/", response_model=list[NoteResponse])
def get_notes_route(db: Session = Depends(get_db)):
    note = get_notes(db)
    return note

@app.put("/notes/{note_id}", response_model=NoteResponse)
def update_notes_routes(note_id:int, note: NoteUpdate, db:Session= Depends(get_db)):
    update_note= update_notes(db=db, note_id=note_id, note=note)
    if not update_note:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )
    return update_note


@app.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note_route(note_id:int, db:Session = Depends(get_db)):
    results = delete_notes(db, note_id)
   
    if not results:
        raise HTTPException(status_code=404, detail="item not found")
    
    return results