from fastapi import FastAPI, Depends, status, HTTPException
from book_review.crud import  create_user,create_book,get_all_books,get_all_review_for_book,add_review_to_book,delete_book, authenticate_user
from book_review.database import get_db, Base, engine
import jwt
import os
from book_review.model import User, Book, Review
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from book_review.schemas import BookCreate, BookResponse, ReviewCreate,ReviewResponse,LoginRequest,UserCreate,UserResponse,TokenResponse

app = FastAPI(
    title="Book Review",
    status="active",
    verison="5.44",

)
Base.metadata.create_all(bind=engine)

load_dotenv()

SECRET_KEY= os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXP_MINS= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data:dict)-> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXP_MINS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    

def get_current_user(token: str= Depends(oauth2_scheme), db: Session= Depends(get_db)):
    payload = verify_access_token(token)
    user = db.query(User).filter(User.id == int(payload.get("sub"))).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user


@app.post("/register", response_model=UserResponse)
def Register(user: UserCreate, db: Session =Depends(get_db)):
    new_user = create_user(db, user)
    return new_user

@app.post("/login", response_model=TokenResponse)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session= Depends(get_db)):
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid username or password"
        )
    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type":"bearer"
    }


@app.post("/books/", response_model=BookResponse)
def create_book_route(book: BookCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_book = create_book(db, book)
    return db_book


@app.get("/books/", response_model= list[BookResponse])
def get_all_books_route(db: Session=Depends(get_db), current_user:dict = Depends(get_current_user)):
    return get_all_books(db)


@app.post("/books/{book_id}/review", response_model= ReviewResponse)
def add_a_review_to_book_route(reviews: ReviewCreate, book_id: int, db: Session=Depends(get_db), current_user: dict=Depends(get_current_user)):
    db_review = add_review_to_book(db, book_id, current_user, reviews)
    if not db_review:  
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return db_review

@app.get("/books/{book_id}/reviews", response_model= list[ReviewResponse])
def get_all_reviews_for_book_route(book_id: int, db: Session=Depends(get_db), current_user:dict = Depends(get_current_user)):
    db_reviews= get_all_review_for_book(db, book_id)
    if not db_reviews:  
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return db_reviews


@app.delete("/books/{book_id}")
def delete_book_route(book_id: int, db: Session=Depends(get_db), current_user: dict=Depends(get_current_user)):
    db_delete_book = delete_book(db, book_id)
    if not db_delete_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return db_delete_book