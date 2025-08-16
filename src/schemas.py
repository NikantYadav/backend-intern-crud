from pydantic import BaseModel
from typing import Optional, List


class UserCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]


class PostOut(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    author_username: str
    created_at: str
    like_count: int
    comment_count: int

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    content: str


class CommentOut(BaseModel):
    id: int
    post_id: int
    author_id: int
    author_username: str
    content: str
    created_at: str

    class Config:
        orm_mode = True


class DeleteResponse(BaseModel):
    message: str
    deleted_id: int
