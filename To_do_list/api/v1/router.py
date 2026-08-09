from fastapi import APIRouter
from To_do_list.api.v1.endpoints import auth, todos


api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(todos.router)

