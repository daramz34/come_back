from book_review.schemas import BookCreate,UserCreate, ReviewCreate
from book_review.model import User, Book, Review
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password:str):
    return pwd_context.verify(plain_password, hashed_password)


def create_user(db: Session, user: UserCreate):
    db_user = User(**user.model_dump(exclude={"password"}), 
                   hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_book(db:Session, book: BookCreate):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
def get_all_books(db:Session):
    return db.query(Book).all()


def add_review_to_book(db: Session, book_id: int, current_user: User, reviews: ReviewCreate):
   db_book = db.query(Book).filter(Book.id == book_id).first()
   if not db_book:
       return None
   db_reviews = Review(**reviews.model_dump(),
                       book_id=book_id,
                       user_id=current_user.id)
   db.add(db_reviews)
   db.commit()
   db.refresh(db_reviews)
   return db_reviews


def get_all_review_for_book(db: Session,book_id:int):
    db_book = db.query(Book).filter(Book.id==book_id).first()
    if not db_book:
        return None
    return db_book.reviews

def delete_book(db:Session, book_id: int):
    db_book = db.query(Book).filter(Book.id==book_id).first()
    if not db_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    db.delete(db_book)
    db.commit()
    return{
        "msg": "Book deleted successfully"
    }


def get_user_by_username(db:Session, username: str):
    return db.query(User).filter(User.username==username).first()


def authenticate_user(db:Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
