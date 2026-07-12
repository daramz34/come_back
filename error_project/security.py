from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
SECRET_KEY = "SUPER_secret_ITEM_key"
ALGORITHM = "HS256"
ACCESS_TOEKN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict)-> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOEKN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)