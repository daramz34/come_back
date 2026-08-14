from sqlalchemy import Column, String, ForeignKey, Integer, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from Blogging_api.database import Base


def utcnow(): # becuz of the datetime update
    return datetime.now(timezone.utc)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, index=True, unique=True)
    email = Column(String, nullable=False, index=True, unique=True)
    hashed_password = Column(String, nullable=False)
    bio = Column(String)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    #relationships
    posts = relationship("Post", back_populates="author", cascade="all, delete")
    comments = relationship("Comment", back_populates="author", cascade="all, delete")
    likes = relationship("Like", back_populates="user", cascade="all, delete")


class Post(Base):
    __tablename__= "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, index=True)
    content = Column(Text, nullable=False)
    is_published = Column(Boolean, default=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    #relationships
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")
    likes = relationship("Like", back_populates="post", cascade="all, delete")

    @property
    def like_count(self):
        return len(self.likes)


class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    #relationships
    author = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

class Like(Base):
    __tablename__ ="like"
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    #relationships
    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")

