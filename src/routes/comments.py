from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..controllers import get_current_user, get_db
from ..models import Post, Comment, User
from ..schemas import CommentCreate, CommentOut

router = APIRouter(prefix="/api/posts")


@router.post("/{post_id}/comment", response_model=CommentOut, status_code=201)
async def add_comment(post_id: int, c: CommentCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Post).where(Post.id == post_id))
    post = q.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = Comment(post_id=post_id, author_id=current_user.id, content=c.content)
    db.add(comment)
    await db.commit()
    await db.refresh(comment)
    author_q = await db.execute(select(User.username).where(User.id == comment.author_id))
    author_username = author_q.scalar_one()
    return {
        "id": comment.id,
        "post_id": comment.post_id,
        "author_id": comment.author_id,
        "author_username": author_username,
        "content": comment.content,
        "created_at": comment.created_at.isoformat(),
    }


@router.get("/{post_id}/comments", response_model=List[CommentOut])
async def get_comments(post_id: int, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Post).where(Post.id == post_id))
    post = q.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comments_q = await db.execute(select(Comment).where(Comment.post_id == post_id).order_by(Comment.created_at.asc()))
    comments = comments_q.scalars().all()
    results = []
    for comment in comments:
        author_q = await db.execute(select(User.username).where(User.id == comment.author_id))
        author_username = author_q.scalar_one()
        results.append({
            "id": comment.id,
            "post_id": comment.post_id,
            "author_id": comment.author_id,
            "author_username": author_username,
            "content": comment.content,
            "created_at": comment.created_at.isoformat(),
        })
    return results
