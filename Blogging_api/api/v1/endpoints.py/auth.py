from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from Blogging_api.core.security import create_access_token, verify_access_token, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from Blogging_api.core.dependencies import oauth_scheme
from Blogging_api.models import User
from Blogging_api.database import get_db
from Blogging_api.schemas import UserResponse, UserCreate, TokenResponse
from Blogging_api.crud import create_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["AUTH"])

@router.post("/register", response_model=UserResponse, description="Register User")
def register(user: UserCreate, db: Session=Depends(get_db)):
    return create_user(db, user)

@router.post("/login", response_model=TokenResponse, description="User Login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail= "Invalid username or passwird"
        )
    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token" : token,
        "token_type": "bearer"
    }


def get_current_user(token: str = Depends(oauth_scheme), db: Session= Depends(get_db)):
    payload = verify_access_token(token)
    user = db.qery(User).filter(User.id == int(payload.get("sub"))).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
