from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from dotenv import load_dotenv
import jwt
import os
from auth_project.database import get_db, Base,engine
from auth_project.schemas import LoginRequest, TokenResponse, UserCreate, UserResponse
from auth_project.crud import authenticate_user, create_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


load_dotenv()

app = FastAPI()

Base.metadata.create_all(bind=engine)




SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#im tired i have started copyng and pasting

def create_access_token(data:dict)-> str:
    to_encode = data.copy()
    expire = datetime.utcnow()+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token:str):
    try:
        payload = jwt.decode(token, SECRET_KEY,algorithms=[ALGORITHM])
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )


def get_current_user(token: str= Depends(oauth2_scheme)):
    return verify_access_token(token)


@app.post("/register/", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    return new_user


@app.post("/login", response_model=TokenResponse)
def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, request.username, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    token = create_access_token({"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
@app.get("/protected")
def protected_route(current_user: dict = Depends(get_current_user)):
    return {
        "message": "Welcome! You have access to this protected route 🎉",
        "user_id": current_user["sub"]
    }
