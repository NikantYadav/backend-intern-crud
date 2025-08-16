from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database import engine, Base
from src.routes import posts, auth, like, comments
from src.models import User, Post, Comment, Like  # Import models explicitly
from sqlalchemy import text
from dotenv import load_dotenv
import os

load_dotenv()

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       
    allow_credentials=True,
    allow_methods=["*"],       
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        try:
            await conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            
            await conn.execute(text("DROP TABLE IF EXISTS likes"))
            await conn.execute(text("DROP TABLE IF EXISTS comments"))
            await conn.execute(text("DROP TABLE IF EXISTS posts"))
            await conn.execute(text("DROP TABLE IF EXISTS users"))
            
            await conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
            
            await conn.execute(text('''
                CREATE TABLE users (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(150) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL,
                    INDEX (username)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            '''))
            
            await conn.execute(text('''
                CREATE TABLE posts (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    author_id INT NOT NULL,
                    created_at DATETIME,
                    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            '''))
            
            await conn.execute(text('''
                CREATE TABLE comments (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    post_id INT NOT NULL,
                    author_id INT NOT NULL,
                    content TEXT NOT NULL,
                    created_at DATETIME,
                    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
                    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            '''))
            
            await conn.execute(text('''
                CREATE TABLE likes (
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    post_id INT NOT NULL,
                    user_id INT NOT NULL,
                    created_at DATETIME,
                    UNIQUE KEY uix_post_user (post_id, user_id),
                    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            '''))
            
            print("Tables created successfully using raw SQL")
        except Exception as e:
            print(f"Error creating tables with raw SQL: {e}")
            try:
                await conn.run_sync(Base.metadata.create_all)
                print("Tables created successfully using SQLAlchemy")
            except Exception as e2:
                print(f"Error creating tables with SQLAlchemy: {e2}")

app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(like.router)
app.include_router(comments.router)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)