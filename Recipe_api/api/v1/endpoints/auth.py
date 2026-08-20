from Recipe_api.models import User
from Recipe_api.database import get_db
from Recipe_api.schemas import UserCreate, UserResponse, TokenResponse
from Recipe_api.crud import create_user, authenticate_user, get_user_by_username, get_user_by_email
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from Recipe_api.core.security import create_access_token
from fastapi.security import OAuth2PasswordRequestForm



router  = APIRouter(prefix="/auth", tags=["AUTH"])


@router.post("/register", response_model=UserResponse, description="REGISTER")
def register(user:UserCreate, db:Session=Depends(get_db)):
    existing_user = get_user_by_username(db, user.username)
    existing_email = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username Already Taken"
        )

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    return create_user(db, user)



@router.post("/login", response_model=TokenResponse, description="User Login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session=Depends(get_db)):
    user = authenticate_user(db, request.username, request.password)
    if not user: 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token" : token,
        "token_type":"bearer"
    }