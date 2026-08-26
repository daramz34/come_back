from contextlib import asynccontextmanager
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from fastapi import FastAPI


# 1. Define your Job function
def test_reminder_job():
    print(
        f"[{datetime.now().strftime('%H:%M:%S')}] Job Executed: Sending reminder emails..."
    )


# 2. Instantiate the BackgroundScheduler
scheduler = BackgroundScheduler()


def start_scheduler():
    # Runs every 2 minutes
    scheduler.add_job(
        test_reminder_job,
        trigger=IntervalTrigger(minutes=2),
        id="medication_reminder_job",
        replace_existing=True,
    )
    scheduler.start()
    print("Scheduler started! Next run in 2 minutes...")


# 3. Connect the scheduler startup & shutdown to FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()  # Starts when server launches
    yield
    scheduler.shutdown()  # Cleans up when server stops


# 4. Pass lifespan to FastAPI app instance

app = FastAPI(lifespan=lifespan)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("scheduler_test:app", host="0.0.0.0", port=8000, reload=True)