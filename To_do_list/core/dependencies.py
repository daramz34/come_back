from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from To_do_list.database import get_db
from To_do_list.core.security import verify_access_token
from To_do_list.model import User
oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")



def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    payload = verify_access_token(token)
    user = db.query(User).filter(User.id == int(payload.get("sub"))).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "User not found"
        )
    return user