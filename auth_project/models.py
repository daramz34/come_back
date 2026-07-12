from auth_project.database import Base
from sqlalchemy import Column, String, Integer, Float

class Auth(Base):
    __tablename__ = "Auth"
    id = Column(Integer, primary_key=True, index=True)
    username= Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)