from fastapi import FastAPI
from Campus_clinic_api.database import Base, engine
from Campus_clinic_api.route import clinic


Base.metadata.create_all(bind=engine)
app = FastAPI(title="Campus Clinic API",
              summary="A Backend system for a unviersity health clinic where students can register, book appointments, and doctors can manage their schedules",
              version="1.0.1")


app.include_router(clinic.router)



@app.get("/home")
def home():
    return {
        "msg": "Welcome"
    }
