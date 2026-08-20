from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles

from Recipe_api.api.v1.router import api_router
from Recipe_api.database import Base, engine
from Recipe_api.core.config import settings


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Recipe API with Gemini",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response


app.add_middleware(
    BaseHTTPMiddleware,
    dispatch=security_headers_middleware,
)

# Keep API routes before the frontend mount.
app.include_router(api_router, prefix="/api/v1")

frontend_path = Path(__file__).resolve().parent / "frontend"

# Serves index.html, auth.html, recipe.html, and collections.html.
app.mount(
    "/",
    StaticFiles(directory=frontend_path, html=True),
    name="frontend",
)