from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from To_do_list.database import Base, engine
from To_do_list.api.v1.router import api_router
from To_do_list.core.config import settings


Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version= settings.VERSION,
    description="A production ready Todo List API"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

app.add_middleware(SecurityHeadersMiddleware)




app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["Home"])
def home():
    return {"message": f"Welcome to {settings.APP_NAME}!",
            "version": settings.VERSION,
            "docs": "/docs"}