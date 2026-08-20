from sqlalchemy.orm import Session
from Recipe_api.models import User, MealSuggestion, Recipe
from Recipe_api.schemas import MealSuggestionCreate, UserCreate,RecipeUpdate
from Recipe_api.core.security import hashed_password, verify_password
import json


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email:str):
    return db.query(User).filter(User.email == email).first()


def create_user(db:Session, user: UserCreate):
    db_user = User(**user.model_dump(exclude={"password"}),
                   hashed_password = hashed_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db:Session, username: str, password: str):
    db_user = get_user_by_username(db, username)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user

def create_suggestion(db:Session, meal: MealSuggestionCreate,  current_user: User):
    db_suggestion = MealSuggestion(user_id=current_user.id,
                                    suggestions=json.dumps(meal.suggestions),  # store list as JSON string
                                    cuisine_type=meal.cuisine_type,
                                    dietary_preference=meal.dietary_preference,
                                    cooking_time=meal.cooking_time)
    db.add(db_suggestion)
    db.commit()
    db.refresh(db_suggestion)
    return db_suggestion

def get_suggestions_by_id(db:Session, meal_id: int, current_user: User):
    db_meal = db.query(MealSuggestion).filter(MealSuggestion.id == meal_id,
                                              MealSuggestion.user_id == current_user.id).first()
    if not db_meal:
        return None
    return db_meal


def create_recipe(db:Session, recipe_data: dict, suggestion_id: int, current_user: User, cuisine_type: str, dietary_preference: str, cooking_time: str):
    db_recipe = Recipe( 
        suggestion_id=suggestion_id,
        user_id=current_user.id,
        meal_name=recipe_data["meal_name"],
        ingredients=recipe_data["ingredients"],
        steps=recipe_data["steps"],
        tips=recipe_data.get("tips"),  
        cuisine_type=cuisine_type,
        dietary_preference=dietary_preference,
        cooking_time=cooking_time
        )
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe


def get_recipe_by_id(db:Session, recipe_id: int, current_user: User):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id,
                                        Recipe.user_id==current_user.id).first()
    if not db_recipe:
        return None
    return db_recipe

def get_all_recipe(db:Session,current_user: User, page:int =1, limit: int=10) -> dict:
    offset = (page -1) * limit
    query = db.query(Recipe).filter(Recipe.user_id==current_user.id)

    total = query.count()
    results = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "results": results
    }

def get_favourite_recipes(db: Session, current_user: User):
    db_recipe = db.query(Recipe).filter(Recipe.user_id == current_user.id,
                                        Recipe.is_favourite==True).all()
    
    return db_recipe


def update_recipe(db:Session, recipe_id: int, update: RecipeUpdate, current_user: User):
    db_recipe = db.query(Recipe).filter(Recipe.id== recipe_id,
                                        Recipe.user_id == current_user.id).first()
    if not db_recipe:
        return None

    db_update = update.model_dump(exclude_none=True)
    for key, value in db_update.items():
        setattr(db_recipe, key, value)
    db.commit()
    db.refresh(db_recipe)

    return db_recipe

def delete_recipe(db: Session, recipe_id: int, current_user: User):
    db_recipe = db.query(Recipe).filter(Recipe.id== recipe_id,
                                            Recipe.user_id == current_user.id).first()
    if not db_recipe:
        return None

    db.delete(db_recipe)
    db.commit()
    return {
        "msg": "Recipe deleted successfully"
    }
        