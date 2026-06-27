from fastapi import FastAPI, status, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from DTO_db import SessionLocal, Item, engine, Base


#DTO data transfer objects
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



class ItemResponseDTO(BaseModel):
    id: int
    name: str
    price: float


    class config:
        from_attributes = True



@app.get("/items/secure", response_model=list[ItemResponseDTO], status_code=status.HTTP_200_OK)
def read_all_items_secured(db: Session = Depends(get_db)):
    all_items = db.query(Item).all()


    return all_items