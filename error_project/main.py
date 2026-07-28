from fastapi import FastAPI, Depends, status, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
import jwt
from error_project.security import SECRET_KEY, ALGORITHM
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from error_project.database import Base, engine, get_db
import error_project.crud as crud
from error_project.security import verify_password, hash_password, create_access_token
import error_project.schemas as schemas
import time

app = FastAPI()
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "*"
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],)
security_scheme = HTTPBearer()
Base.metadata.create_all(bind=engine)

# setting up cache
CACHE = {}
CACHE_TTL = 60

# Keep your exception handlers exactly as they are!
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

# --- AUTHENTICATION ROUTES ---

# Signup route to register brand-new accounts
@app.post("/signup/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def signup(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = crud.get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user_in=user_in)

# Login route that returns the secure access token
@app.post("/login/", response_model=schemas.Token)
def login(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=user_in.email)
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    # We store both the email and the primary key user_id inside the JWT payload
    token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {
        "access_token": token,
        "token_type": "bearer"
    }

# Dependency helper to check the incoming token credentials
def get_current_user(token: HTTPAuthorizationCredentials = Depends(security_scheme)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials/Token invalid or expired"
        )



# -- Create Category

@app.post("/categories/", response_model=schemas.CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category_in: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db=db, category_in=category_in)


# --- INVENTORY ITEMS ROUTES ---

# Create items (requires a valid JWT token now!)
@app.post("/items/", response_model=schemas.ItemResponse, status_code=status.HTTP_201_CREATED)
def api_create_items(
    item_in: schemas.ItemCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    owner_id = current_user.get("user_id")
    return crud.create_item(db=db, item_in=item_in, owner_id=owner_id)

@app.get("/items/", response_model=list[schemas.ItemResponse])
def api_get_items(db: Session = Depends(get_db)):
    current_time = time.time()
    if "items_list" in CACHE:
        cached_data, timestamp = CACHE["items_list"]
        if current_time - timestamp < CACHE_TTL:
            print("🟢 [CACHE HIT]: Returning items from memory")
            
            return cached_data
    print("🔴 [CACHE MISS]: Fetching items from database")
    
    items = crud.get_item(db)
    item_responses = [schemas.ItemResponse.model_validate(item) for item in items]
    CACHE["items_list"] = (item_responses, current_time)
    return item_responses


@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def get_single_items(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(crud.Item).filter(crud.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.get("/items/paginated/", response_model=schemas.PaginationItemResponse)
def read_items(
    page: int = Query(1, ge=1), 
    limit: int = Query(5, ge=1, le=100),
    min_price: float = Query(None),
    max_price: float = Query(None),
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit
    items, total_count = crud.get_paginated_items(
        db, skip=skip, limit=limit, min_price=min_price, max_price=max_price
    )
    return {
        "total": total_count,
        "page": page,
        "limit": limit,
        "results": items
    }

# Protected Delete endpoint checking item ownership
@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item_route(
    item_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user) # Must be logged in to delete
):
    # 1. Look up the item to verify its ownership state
    db_item = db.query(crud.Item).filter(crud.Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
        
    # 2. Check if logged-in user matches the item owner_id
    logged_in_user_id = current_user.get("user_id")
    if db_item.user_id != logged_in_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: You do not own this item. Access denied."
        )
    
    crud.delete_item(db, item_id)
    return None
