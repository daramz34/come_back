from fastapi import FastAPI, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse

app = FastAPI()

limiter = Limiter(key_func=get_remote_address) # tracks each user

app.state.limiter = limiter # storing the limit in app state


@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "detail": "Too many Requests"
        }
    )


#Rate limiter api
@app.get("/data")
@limiter.limit("5/minutes")
def get_data(request: Request):
    return{
        "msg":"success"
    }