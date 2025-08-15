from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..controllers import get_current_user, get_db
from ..models import Post, Like, User

router = APIRouter(prefix="/api/posts")


@router.post("/{post_id}/like", status_code=201)
async def like_post(post_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Post).where(Post.id == post_id))
    post = q.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    existing_q = await db.execute(select(Like).where(Like.post_id == post_id, Like.user_id == current_user.id))
    existing = existing_q.scalars().first()
    if existing:
        raise HTTPException(status_code=400, detail="You have already liked this post")
    like = Like(post_id=post_id, user_id=current_user.id)
    db.add(like)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Unable to like post")
    return {"detail": "Post liked"}
