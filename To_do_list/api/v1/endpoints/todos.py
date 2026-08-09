from fastapi import APIRouter, HTTPException, Query, status, Depends
from To_do_list.crud import (get_todo_by_id, 
                             get_paginated_todo, create_todo, delete_todo_by_id, update_todo_by_id, update_todo_status)
from sqlalchemy.orm import Session
from To_do_list.schemas import TodoResponse, TodoCreate, TodoUpdate
from To_do_list.model import User
from datetime import datetime
from To_do_list.database import get_db
from To_do_list.core.dependencies import get_current_user
from To_do_list.enums import TodoStatus, Priority
router = APIRouter(prefix="/todos", tags=["Todo"])

@router.post("/todo", response_model=TodoResponse, status_code=status.HTTP_201_CREATED, description="Create a Task/To_do")
def createtodo(todo: TodoCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_todo(db, todo, current_user)


@router.get("/get_todo", response_model=TodoResponse, status_code=status.HTTP_200_OK, description="Get Todo")
def get_all_paginated_todo(db: Session= Depends(get_db), current_user: User = Depends(get_current_user), 
                           page: int = Query(1, ge=1), limit: int=Query(10, ge=1, le=50),
                           status: TodoStatus = Query(None), priority: Priority = Query(None)):
    db_todo = get_paginated_todo(db, current_user, page, limit, status, priority)
    return db_todo


@router.get("/get_todo_by_id/{todo_id}", response_model=TodoResponse, status_code= status.HTTP_200_OK, description="Get Todo by id")
def get_to_do_by_id(db: Session= Depends(get_db), todo_id = int, current_user: User = Depends(get_current_user)):
    return get_todo_by_id(db, todo_id, current_user)


@router.put("/update_todo/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK, description="Update todo")
def update_todo(todo_id: int,update: TodoUpdate, db: Session = Depends(get_db),   current_user: User = Depends(get_current_user)):
    return update_todo_by_id(db, todo_id, update, current_user)

@router.patch("/update_todo_status/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK, description="Update todo status")
def update_status(todo_id: int, status: TodoStatus, db: Session=Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_todo_status(db, todo_id, status, db)


@router.delete("/delete_todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete Todo")
def delete_todo(todo_id: int, db: Session= Depends(get_db), current_user: User = Depends(get_current_user)):
    return delete_todo_by_id(db, todo_id, current_user)



