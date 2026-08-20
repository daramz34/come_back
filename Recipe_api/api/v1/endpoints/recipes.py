from fastapi import APIRouter, HTTPException, status, Depends
from Recipe_api.database import get_db
from Recipe_api.core.dependencies import get_current_user
from Recipe_api.schemas import (
    PaginatedRecipeResponse, RecipeUpdate,RecipeRequest,RecipeResponse,
    MealSuggestionCreate, MealSuggestions, MealRequest
)
from Recipe_api.crud import(
    create_recipe, get_suggestions_by_id,  create_suggestion,update_recipe,get_recipe_by_id,
    get_all_recipe, get_favourite_recipes, delete_recipe
)
from sqlalchemy.orm import Session
from Recipe_api.models import User
from Recipe_api.services.gemini import suggest_meals, generate_recipe
import json

router = APIRouter(prefix="/recipes", tags=["RECIPES"])

@router.post("/suggest", response_model=MealSuggestions, status_code=status.HTTP_200_OK, description="Suggest meal")
async def suggest_meals_endpoint(request: MealRequest, db:Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    meals = await suggest_meals(
        request.craving,
        request.cuisine_type,
        request.dietary_preference,
        request.cooking_time
    )

    suggestion_data = MealSuggestionCreate(
        suggestions=meals,
        cuisine_type=request.cuisine_type,
        dietary_preference=request.dietary_preference,
        cooking_time=request.cooking_time
    )

    db_suggestion = create_suggestion(db, suggestion_data, current_user)

    db_suggestion.suggestions = json.loads(db_suggestion.suggestions)
    return db_suggestion


@router.post("/generate", response_model=RecipeResponse, status_code=status.HTTP_201_CREATED, description="Generate recipe")
async def generate_recipe_endpoint(request: RecipeRequest, db: Session = Depends(get_db), current_user:User = Depends(get_current_user)):
    suggestion = get_suggestions_by_id(db, request.suggestion_id, current_user)

    if not suggestion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Suggestion not found")

    suggestions_list = json.loads(suggestion.suggestions)

    if request.meal_name not in suggestions_list:
        raise HTTPException(
            status_code=400,
            detail="Meal not in your suggestions — pick from the suggested meals"
        )
    recipe_data = await generate_recipe(
        request.meal_name,
        suggestion.cuisine_type,
        suggestion.dietary_preference,
        suggestion.cooking_time
    )
    recipe = create_recipe(db, recipe_data, request.suggestion_id, current_user, suggestion.cuisine_type, suggestion.dietary_preference, suggestion.cooking_time)

    return recipe




@router.get("/history", response_model=PaginatedRecipeResponse, status_code=status.HTTP_200_OK, description="User history")
def get_history(db: Session = Depends(get_db), page: int= 1, limit: int= 10, current_user: User = Depends(get_current_user)):
    history = get_all_recipe(db, current_user, page, limit)
    
    return history



@router.get("/favourites", response_model=list[RecipeResponse], status_code=status.HTTP_200_OK, description="User fav")
def favourites(db: Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    fav = get_favourite_recipes(db, current_user)
    
    return fav



@router.get("/{recipe_id}", response_model=RecipeResponse, status_code=status.HTTP_200_OK, description="Get a selected recipe")
def single_recipe(recipe_id: int, db:Session = Depends(get_db), current_user: User=Depends(get_current_user)):
    single = get_recipe_by_id(db, recipe_id, current_user)
    if not single:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    return single


@router.patch("/{recipe_id}", response_model=RecipeResponse, status_code=status.HTTP_200_OK, description="Update recipe")
def update_endpoint(recipe_id: int, update: RecipeUpdate, db:Session = Depends(get_db), current_user: User= Depends(get_current_user)):
    update = update_recipe(db, recipe_id, update, current_user)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Recipe not found"
        )
    return update


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a recipe")
def delete_endpoint(recipe_id: int, db:Session= Depends(get_db), current_user: User= Depends(get_current_user)):
    delete = delete_recipe(db, recipe_id, current_user)
    if not delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe not found"
        )
    return 