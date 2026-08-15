from sqlalchemy import Column, String, DateTime, ForeignKey,Integer, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from To_do_list.database import Base
from To_do_list.enums import TodoStatus, Priority



class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, nullable=False)
    email = Column(String, nullable=False, index=True, unique=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    todo = relationship("Todo", back_populates="owner")

    # def get_info(self):
    #     return {
    #         "username": self.username,
    #     }
    # @classmethod
    # def get_table_name(cls):
    #     return cls.__tablename__


class Todo(Base):
    __tablename__ = "todo"
    id =Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=False)
    status = Column(Enum(TodoStatus), default=TodoStatus.PENDING, nullable=False)
    priority = Column(Enum(Priority), default=Priority.MEDIUM, nullable=False)
    due_date= Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="todo")



# print(User.get_table_name())
# user = User(username="Daramz", email="hshsh", hashed_password="9993")
# print(user.get_info())