from fastapi import APIRouter
from Recipe_api.api.v1.endpoints import auth, recipes

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(recipes.router)
