from sqlalchemy.orm import Session
from Blogging_api.models import User, Post, Comment,Like
from Blogging_api.schemas import UserCreate, PostCreate, CommentCreate,PostUpdate
from Blogging_api.core.security import hashed_password, verify_password
from Blogging_api.core.cache import get_cache, set_cache, delete_cache



def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user:UserCreate):
    db_user = User(**user.model_dump(exclude={"password"}),
                   hashed_password = hashed_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username:str, password: str):
    db_user = get_user_by_username(db, username)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user




def create_post(db: Session, post: PostCreate, current_user: User):
    db_post = Post(**post.model_dump(),
                   author_id= current_user.id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_all_posts(db: Session, page: int = 1, limit: int = 10):
    cache_key = f"posts_total:page={page}:limit={limit}"

    cached_total = get_cache(cache_key)
    
    offset = (page - 1) * limit
    query = db.query(Post).filter(Post.is_published == True)

    
    total = cached_total if cached_total else query.count()
    
    if not cached_total:
        set_cache(cache_key, total, expire=60)

    posts = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "results": posts
    }


def get_post_by_id(db: Session, post_id: int):
    return db.query(Post).filter(Post.id == post_id).first()

def update_post_by_id(db: Session,post_id: int, update: PostUpdate, current_user:User):
    db_post = db.query(Post).filter(Post.id == post_id,
                                    Post.author_id == current_user.id).first()
    if not db_post:
        return None

    db_update = update.model_dump(exclude_none=True)
    for key, value in db_update.items():
        setattr(db_post, key,value)
    db.commit()
    db.refresh(db_post)

    delete_cache(f"post:{post_id}")
    delete_cache("all_posts:page=1:limit=10")
    return db_post


def update_post_publish(db: Session, post_id: int, current_user: User):
    db_post = db.query(Post).filter(Post.id == post_id,
                                    Post.author_id == current_user.id).first()

    if not db_post:
        return None
    db_post.is_published = True
    db.commit()
    db.refresh(db_post)

    delete_cache(f"post:{post_id}")
    delete_cache("all_posts:page=1:limit=10")
    return db_post


def delete_post(db: Session, post_id: int, current_user: User):
    db_post = db.query(Post).filter(Post.id == post_id,
                                    Post.author_id == current_user.id).first()
    if not db_post:
        return None

    db.delete(db_post)
    db.commit()

    delete_cache(f"post:{post_id}")
    delete_cache("all_posts:page=1:limit=10")
    return{
        "msg": "Post deleted successfully"
    }


def create_comment(db: Session, post_id: int, comment: CommentCreate, current_user: User):
    db_comment = Comment(**comment.model_dump(),
                         post_id = post_id,
                         author_id = current_user.id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def create_likes(db: Session, post_id: int, current_user:User):
    existing = db.query(Like).filter(Like.post_id==post_id,
                                     Like.user_id == current_user.id).first()
    if existing:
        return None
    db_like = Like(post_id =post_id,
                   user_id= current_user.id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def get_my_post(db: Session, current_user: User, page: int =1, limit: int = 10): # this is to enable to user to see their own posts
    offset = (page - 1) * limit
    query = db.query(Post).filter(Post.author_id == current_user.id)

    total = query.count()
    posts = query.offset(offset).limit(limit).all()

    return {
        "total":total,
        "page": page,
        "limit": limit,
        "results": posts
    }

def get_post_comments(db: Session, post_id: int):
    return db.query(Comment).filter(Comment.post_id == post_id).all()