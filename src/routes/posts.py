from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ..controllers import get_current_user, get_db
from ..models import Post, User, Like, Comment
from ..schemas import PostCreate, PostOut, PostUpdate

router = APIRouter(prefix="/api/posts")


@router.post("", response_model=PostOut, status_code=201)
async def create_post(p: PostCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    post = Post(title=p.title, content=p.content, author_id=current_user.id)
    db.add(post)
    await db.commit()
    await db.refresh(post)
    # counts
    like_q = await db.execute(select(func.count()).select_from(Like).where(Like.post_id == post.id))
    like_count = like_q.scalar() or 0
    comment_q = await db.execute(select(func.count()).select_from(Comment).where(Comment.post_id == post.id))
    comment_count = comment_q.scalar() or 0
    # author username
    author_q = await db.execute(select(User.username).where(User.id == post.author_id))
    author_username = author_q.scalar_one()
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
        "author_username": author_username,
        "created_at": post.created_at.isoformat(),
        "like_count": like_count,
        "comment_count": comment_count,
    }


@router.get("", response_model=List[PostOut])
async def read_posts(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Post).order_by(Post.created_at.desc()))
    posts = q.scalars().all()
    results = []
    for post in posts:
        like_q = await db.execute(select(func.count()).select_from(Like).where(Like.post_id == post.id))
        like_count = like_q.scalar() or 0
        comment_q = await db.execute(select(func.count()).select_from(Comment).where(Comment.post_id == post.id))
        comment_count = comment_q.scalar() or 0
        author_q = await db.execute(select(User.username).where(User.id == post.author_id))
        author_username = author_q.scalar_one()
        results.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": post.author_id,
            "author_username": author_username,
            "created_at": post.created_at.isoformat(),
            "like_count": like_count,
            "comment_count": comment_count,
        })
    return results


@router.get("/{post_id}", response_model=PostOut)
async def read_post(post_id: int, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Post).where(Post.id == post_id))
    post = q.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    like_q = await db.execute(select(func.count()).select_from(Like).where(Like.post_id == post.id))
    like_count = like_q.scalar() or 0
    comment_q = await db.execute(select(func.count()).select_from(Comment).where(Comment.post_id == post.id))
    comment_count = comment_q.scalar() or 0
    author_q = await db.execute(select(User.username).where(User.id == post.author_id))
    author_username = author_q.scalar_one()
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
        "author_username": author_username,
        "created_at": post.created_at.isoformat(),
        "like_count": like_count,
        "comment_count": comment_count,
    }


@router.put("/{post_id}", response_model=PostOut)
async def update_post(post_id: int, p: PostUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Post).where(Post.id == post_id))
    post = q.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    if p.title is not None:
        post.title = p.title
    if p.content is not None:
        post.content = p.content
    await db.commit()
    await db.refresh(post)
    like_q = await db.execute(select(func.count()).select_from(Like).where(Like.post_id == post.id))
    like_count = like_q.scalar() or 0
    comment_q = await db.execute(select(func.count()).select_from(Comment).where(Comment.post_id == post.id))
    comment_count = comment_q.scalar() or 0
    author_q = await db.execute(select(User.username).where(User.id == post.author_id))
    author_username = author_q.scalar_one()
    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
        "author_username": author_username,
        "created_at": post.created_at.isoformat(),
        "like_count": like_count,
        "comment_count": comment_count,
    }


@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Post).where(Post.id == post_id))
    post = q.scalars().first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    await db.delete(post)
    await db.commit()
    return
