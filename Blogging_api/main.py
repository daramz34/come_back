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
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

app.add_middleware(BaseHTTPMiddleware, dispatch=security_headers_middleware)

app.include_router(api_router, prefix="/api/v1")



templates = Jinja2Templates(directory="Blogging_api/frontend/templates")
app.mount("/static", StaticFiles(directory="Blogging_api/frontend/static"), name="static")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", 
                                      {"request": request})



@app.get("/auth")
def auth_page(request: Request):
    return templates.TemplateResponse("auth.html", 
                                      {"request": request})


@app.get("/feed")
def feed_page(request: Request):
    return templates.TemplateResponse("feed.html", {"request": request})


@app.get("/feed")
def feed_page(request: Request):
    return templates.TemplateResponse("feed.html", {"request": request})


@app.get("/post/{post_id}")
def post_page(request: Request, post_id: int):
    return templates.TemplateResponse("post.html", {"request": request, "post_id": post_id})


@app.get("/create")
def create_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@app.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/edit/{post_id}")
def edit_page(request: Request, post_id: int):
    return templates.TemplateResponse("edit.html", {"request": request, "post_id": post_id})