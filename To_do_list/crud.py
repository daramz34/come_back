from sqlalchemy.orm import Session
from To_do_list.model import User, Todo
from To_do_list.enums import TodoStatus, Priority
from To_do_list.schemas import UserCreate, TodoCreate, TodoUpdate
from To_do_list.core.security import verify_password, hashed_password

def get_user_by_username(db:Session, username: str):
    return db.query(User).filter(User.username==username).first()

def authenticate_user(db: Session, username: str, password: str):
    db_user = get_user_by_username(db, username)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def create_user(db:Session, user: UserCreate):
    db_user = User(**user.model_dump(exclude={"password"}),      # in detail the user sends exactly what is in usercreate in the schemas(username, email, password) 
                   hashed_password = hashed_password(user.password))  # in the process i remove the password becuz it plain then put in hashed password function which returns a hashed password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_todo(db: Session, todo:TodoCreate, current_user: User):
    db_todo = Todo(**todo.model_dump(),
                   user_id=current_user.id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def get_paginated_todo(db: Session,current_user: User, page:int=1, limit: int=10, status:TodoStatus = None, priority: Priority = None):
    
    offset = (page -1) * limit
    query = db.query(Todo).filter(Todo.user_id==current_user.id)
    if status:
        query = query.filter(Todo.status == status)
    if priority:
        query = query.filter(Todo.priority == priority)
    total = query.count()
    todo = query.offset(offset).limit(limit).all()
    return {
        "total" : total,
        "page": page,
        "limit":limit,
        "results": todo
    }
def get_todo_by_id(db: Session, id: int, current_user: User):
    db_todo = db.query(Todo).filter(Todo.id == id, Todo.user_id==current_user.id).first()
    return db_todo


def update_todo_by_id(db: Session, id: int, update: TodoUpdate, current_user: User):
    db_todo = db.query(Todo).filter(Todo.id == id,
                                    Todo.user_id== current_user.id).first()
    if not db_todo:
        return None

    db_update = update.model_dump(exclude_none=True)
    for key, value in db_update.items():
        setattr(db_todo, key, value)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo_status(db: Session, id: int, status: TodoStatus,current_user: User):
    db_todo = db.query(Todo).filter(Todo.id == id, Todo.user_id==current_user.id).first()
    if not db_todo:
        return None

    db_todo.status = status
    db.commit()
    db.refresh(db_todo)
    return db_todo

def delete_todo_by_id(db:Session, id: int, current_user: User):
    db_todo = db.query(Todo).filter(Todo.id== id, Todo.user_id==current_user.id).first()
    if not db_todo:
        return None
    db.delete(db_todo)
    db.commit()
    return{
        "msg": "Todo deleted successfully"
    }