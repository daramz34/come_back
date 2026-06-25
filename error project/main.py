from fastapi import FastAPI, Depends, status, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from crud import create_item, get_item, delete_item
from schemas import ItemCreate, ItemResponse
app = FastAPI()
Base.metadata.create_all(bind=engine)
# -------------------------------------------------------------------------
# 🛠️ DAY 12: GLOBAL EXCEPTION HANDLERS (The Error Standardization Layer)
# -------------------------------------------------------------------------

# 1. Catch Standard HTTPExceptions (like our manual 404s)
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.detail,
                "status": exc.status_code
            }
        }
    )

# 2. Catch Inbound Validation Errors (Pydantic / Bad Data Validation)
# This overrides the default FastAPI 422 error and returns a clean 400 Bad Request instead!
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract the exact fields causing the failure and format into a clean string
    errors = exc.errors()
    error_messages = []
    for err in errors:
        loc = " -> ".join(str(x) for x in err["loc"] if x != "body")
        error_messages.append(f"[{loc}]: {err['msg']}")
        
    readable_message = " | ".join(error_messages) if error_messages else "Invalid input data provided."

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "message": f"Validation Error: {readable_message}",
                "status": 400
            }
        }
    )

# 3. Catch ALL other unexpected Python crashes (Database down, AttributeErrors, etc.)
@app.exception_handler(Exception)
async def global_generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "message": f"An unexpected system error occurred: {str(exc)}",
                "status": 500
            }
        }
    )

# --- KEEP THE REST OF YOUR ROUTES BELOW ---





@app.post("/items/", response_model=ItemResponse)
def api_create_items(item: ItemCreate, db: Session = Depends(get_db)):
    return create_item(db, item)

@app.get("/items/", response_model=list[ItemResponse])
def api_get_items(db: Session = Depends(get_db)):
    items = get_item(db)
    return items

@app.delete("/items/{item_id}",
            status_code=status.HTTP_204_NO_CONTENT)
def delete_item_route(item_id: int, db: Session = Depends(get_db)):
    result = delete_item(db, item_id)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return None
