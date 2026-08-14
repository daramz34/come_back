from fastapi import APIRouter, HTTPException, Query, status, Depends
from Blogging_api.database import get_db
from Blogging_api.core.dependencies import get_current_user
from Blogging_api.schemas import (
    PaginatedPostResponse, CommentCreate,CommentResponse, 
    PostCreate,PostResponse, PostUpdate
)
from Blogging_api.crud import (
    create_comment,create_likes, get_post_comments,create_post, delete_post,
    get_all_posts,get_my_post, get_post_by_id, update_post_by_id,update_post_publish
)
from sqlalchemy.orm import Session
from Blogging_api.models import User




router = APIRouter(prefix="/blog", tags=["BLOG"])

@router.post("/posts", response_model=PostResponse, status_code=status.HTTP_201_CREATED, description="Create a post")
def createpost(post: PostCreate, db: Session= Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_post(db, post, current_user)


@router.get("/posts", response_model=PaginatedPostResponse, status_code=status.HTTP_200_OK, description="Get post")
def get_post(db:Session = Depends(get_db), page: int= 1, limit: int=10 ):
    return get_all_posts(db, page, limit)


@router.get("/posts/mine", response_model=PaginatedPostResponse, status_code=status.HTTP_200_OK, description="Get my personsal post")
def get_mine(db: Session = Depends(get_db), current_user: User = Depends(get_current_user), page: int = 1, limit: int = 10):
    return get_my_post(db, current_user, page, limit)

@router.get("/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK, description="Get post by id")
def get_postid(post_id: int, db: Session = Depends(get_db)):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= "Post not found")
    return post


@router.put("/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK, description="Update post")
def update_post(post_id: int, update: PostUpdate, db: Session= Depends(get_db), current_user: User= Depends(get_current_user)):
    update = update_post_by_id(db, post_id, update, current_user)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Unable to update"
        )
    return update

@router.patch("/posts/{post_id}", response_model=PostResponse, status_code=status.HTTP_200_OK, description="Update is_publish")
def update_publish(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    update = update_post_publish(db, post_id, current_user)
    if not update:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return update

@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, description="Delete a post")
def deletepost(post_id:int, db: Session= Depends(get_db), current_user: User = Depends(get_current_user)):
    delete= delete_post(db, post_id, current_user)
    if not delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=" Post not found"
        )
    return

@router.post("/comments/{post_id}", response_model=CommentResponse, status_code=status.HTTP_200_OK, description="Write a comment")
def createcomment(post_id: int, comment: CommentCreate, db: Session= Depends(get_db), current_user: User = Depends(get_current_user)):
    post = get_post_by_id(db, post_id) # what if post_id doesnt exist
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return create_comment(db, post_id, comment, current_user)

@router.get("/posts/{post_id}/comments", response_model=list[CommentResponse], status_code=status.HTTP_200_OK, description="Get comments on a post")
def get_comments(post_id: int, db: Session = Depends(get_db)):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return get_post_comments(db, post_id)

@router.post("/likes/{post_id}", status_code=status.HTTP_200_OK, description="drop a like")
def createlike(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = get_post_by_id(db, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    res = create_likes(db, post_id, current_user)
    if not res:
        raise HTTPException(status_code=400, detail="You already Liked this post")
    
    return res


