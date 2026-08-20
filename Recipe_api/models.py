from sqlalchemy import Column, String, Boolean, Float, DateTime, ForeignKey, Text, Integer
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from Recipe_api.database import Base


def utcnow():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    recipes = relationship("Recipe", back_populates="user", cascade="all, delete")
    suggestions = relationship("MealSuggestion", back_populates="user", cascade="all, delete")
        


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    suggestion_id = Column(Integer, ForeignKey("meal_suggestions.id"), nullable=False)
    meal_name = Column(String, nullable=False)
    cuisine_type = Column(String, nullable=False)
    dietary_preference = Column(String, nullable=False)
    cooking_time = Column(String, nullable=False)
    ingredients = Column(Text, nullable=False)
    steps = Column(Text, nullable=False)
    tips = Column(Text, nullable=True)
    rating = Column(Float, nullable=True)
    is_favourite = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    user = relationship("User", back_populates="recipes")
    suggestions = relationship("MealSuggestion", back_populates="recipes")
    
    


class MealSuggestion(Base):
    __tablename__ = "meal_suggestions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    suggestions = Column(Text, nullable=False)
    cuisine_type = Column(String, nullable=False)
    dietary_preference = Column(String, nullable=False)
    cooking_time = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    user = relationship("User", back_populates="suggestions")
    recipes = relationship("Recipe", back_populates="suggestions")

        