from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from To_do_list.crud import authenticate_user, create_user
from To_do_list.schemas import UserCreate, UserResponse, Token
from To_do_list.database import get_db
from To_do_list.core.dependencies import oauth_scheme
from To_do_list.model import User
from To_do_list.core.security import create_access_token, verify_access_token


router  = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse, description="Register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    return new_user

@router.post("/login", response_model=Token, description="User login")
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
                            )

    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token" : token,
        "token_type": "bearer"
    }

def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    user = db.query(User).filter(User.id == int(payload.get("sub"))).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
