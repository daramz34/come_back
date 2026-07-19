from fastapi import FastAPI, Request
from Campus_clinic_api.database import Base, engine
from Campus_clinic_api.route import clinic
from fastapi.templating import Jinja2Templates


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Campus Clinic API",
              summary="A Backend system for a unviersity health clinic where students can register, book appointments, and doctors can manage their schedules",
              version="1.0.1")


app.include_router(clinic.router)

templates = Jinja2Templates(directory="Campus_clinic_api/templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", 
                                      {"request":request})



@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", 
                                      {"request":request})

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/dashboard")
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})