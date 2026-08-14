from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from Blogging_api.api.v1.router import api_router
from Blogging_api.database import Base, engine
from To_do_list.core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI( title=settings.APP_NAME,
    version= settings.VERSION,
    description="A production ready Blog API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

app.add_middleware(BaseHTTPMiddleware, dispatch=security_headers_middleware)

app.include_router(api_router, prefix="/api/v1")