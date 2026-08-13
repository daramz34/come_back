from fastapi import APIRouter
from Blogging_api.api.v1.endpoints import auth, Blog


api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(Blog.router)