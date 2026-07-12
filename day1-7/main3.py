from fastapi import FastAPI, status, Depends
from sqlalchemy.orm import Session
from auth_project.database import SessionLocal, Item


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return{
        "MSG" : "Welcome"
    }


@app.get("/items", status_code=status.HTTP_200_OK)
def read_all_items(db:Session = Depends(get_db)):
    all_items = db.query(Item).all()


    return{
        "status": "success",
        "count": len(all_items),
        "data": all_items
    }