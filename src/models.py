from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    username = Column(String(150), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="author", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")


class Post(Base):
    __tablename__ = "posts"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(INTEGER, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    post_id = Column(INTEGER, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    author_id = Column(INTEGER, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")


class Like(Base):
    __tablename__ = "likes"
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    post_id = Column(INTEGER, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(INTEGER, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="likes")

    __table_args__ = (UniqueConstraint("post_id", "user_id", name="uix_post_user"),)
