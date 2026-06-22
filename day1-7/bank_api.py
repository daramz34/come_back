from fastapi import FastAPI, Depends, status
from banking_db import Transaction, seed_transactions,SessionLocal, init_db
from sqlalchemy.orm import Session


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return{"msg": "welcome"}


@app.get("/transactions", status_code=status.HTTP_200_OK)
def read_all_transactions(db:Session = Depends(get_db)):
    all_transactions = db.query(Transaction).all()

    return{
        "Status": "success",
        "data": all_transactions
    }



if __name__ == "__main__":
    init_db()
    get_db()