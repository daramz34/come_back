from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from Blogging_api.api.v1.router import api_router
from Blogging_api.database import Base, engine
from Blogging_api.core.config import settings
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

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



templates = Jinja2Templates(directory="Blogging_api/frontend/templates")
app.mount("/frontend/static", StaticFiles(directory="Blogging_api/frontend/static"))


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", 
                                      {"request": request})