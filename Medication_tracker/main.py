from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from Medication_tracker.api.v1.router import api_router
from Medication_tracker.database import Base, engine
from Medication_tracker.service.scheduler import start_scheduler
from Medication_tracker.core.config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Track your medications, streaks, and get email reminders"
)

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

@app.on_event("startup")
def startup():
    start_scheduler()

@app.on_event("shutdown")
def shutdown():
    from Medication_tracker.service.scheduler import scheduler
    scheduler.shutdown()