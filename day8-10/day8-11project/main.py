from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
from NOTEBOOK_project.database import Base, engine, get_db
import NOTEBOOK_project.models as models
from NOTEBOOK_project.schemas import StudentCreate, StudentResponse
import NOTEBOOK_project.crud as crud


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return{"Message": "Welcome"}



@app.get("/health")
def status():
    return{"STATUS": "UP & ACTIVE"}


@app.post("/students",response_model=StudentResponse)
def add_students(student: StudentCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_responses(db, student)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database save failed: {str(e)}")



@app.get("/students", response_model=list[StudentResponse])
def read_student(db: Session = Depends(get_db)):
    return crud.get_responses(db)



@app.delete("/students")
def delete_student(stud_id: int, db:Session = Depends(get_db)):
    success = crud.delete_responses_by_id(db, id=stud_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail=f"STUDENT ID {stud_id} does not exist"
        )
    return None
