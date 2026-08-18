from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
    

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "Bearer"




class MealRequest(BaseModel):
    craving: str
    cuisine_type: str
    dietary_preference: str
    cooking_time: str

class MealSuggestions(BaseModel):
    id: int
    suggestions: list

    model_config = ConfigDict(from_attributes=True)

class RecipeRequest(BaseModel):
    meal_name: str
    suggestion_id: int

class RecipeResponse(BaseModel):
    id: int
    meal_name : str
    cuisine_type: str
    dietary_preference: str
    cooking_time: str
    ingredients: str
    steps: str
    tips:str | None = None
    rating: float | None = None
    is_favourite: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class RecipeUpdate(BaseModel):
    rating: Optional[float] = Field(None, ge=1, le=5)
    is_favourite: Optional[bool] = None



class PaginatedRecipeResponse(BaseModel):
    total: int
    page: int
    limit: int
    results: list[RecipeResponse]

