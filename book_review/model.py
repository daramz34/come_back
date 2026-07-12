from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Float,  Text
from datetime import datetime
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, index= True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)

    reviews = relationship("Review", back_populates="user",cascade="all, delete")


class Book(Base):
    __tablename__= "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable = False)
    author = Column(String, nullable=False)
    genre = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    reviews = relationship("Review", back_populates="book",cascade="all, delete")

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, nullable=False)
    comment = Column(Text)
    created_at = Column(DateTime, default= datetime.utcnow)


    # Foreign key
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    
    #relationship
    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")




