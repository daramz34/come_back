from fastapi import FastAPI, Depends, status, HTTPException
from sqlalchemy.orm import Session
import NOTEBOOK_project.database as database
import NOTEBOOK_project.models as models
import NOTEBOOK_project.schemas as schemas
import NOTEBOOK_project.crud as crud

app = FastAPI()

# Force the database tables to create themselves on startup
models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def home():
    return {"status": "Online", "challenge": "Day 9 - POST and CRUD Architecture"}


# DAY 8 GET ROUTE (Filtered by ItemResponseDTO)
@app.get("/items", response_model=list[schemas.ItemResponseDTO], status_code=status.HTTP_200_OK)
def read_items(db: Session = Depends(database.get_db)):
    return crud.get_all_items(db)


# DAY 9 POST ROUTE (Accepts ItemCreateDTO, Returns ItemResponseDTO)
@app.post("/items", response_model=schemas.ItemResponseDTO, status_code=status.HTTP_201_CREATED)
def add_item(item_in: schemas.ItemCreateDTO, db: Session = Depends(database.get_db)):
    try:
        return crud.create_item(db, item_in)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database save failed: {str(e)}")