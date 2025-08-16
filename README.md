# FastAPI CRUD Backend

A RESTful API backend built with FastAPI and MySQL for managing posts, comments, likes, and user authentication.

## Features

- User authentication and authorization
- CRUD operations for posts
- Comment system
- Like/unlike functionality
- MySQL database with proper relationships
- CORS enabled for frontend integration

## Prerequisites

- Python 3.8+
- MySQL 8.0+
- pip (Python package manager)

## Setup Instructions

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv env
source env/bin/activate  
```

### 3. Install Dependencies
```bash
pip install -r src/requirements.txt
```

### 4. Database Setup

#### Create MySQL Database
```sql
CREATE DATABASE backend_intern_crud;
CREATE USER 'crud_user'@'localhost' IDENTIFIED BY 'securepassword';
GRANT ALL PRIVILEGES ON backend_intern_crud.* TO 'crud_user'@'localhost';
FLUSH PRIVILEGES;
```

#### Configure Environment Variables
The `.env` file is already configured with default settings:
```env
DATABASE_URL=mysql+aiomysql://crud_user:securepassword@localhost:3306/backend_intern_crud?charset=utf8mb4&use_unicode=1
HOST=0.0.0.0
PORT=8000
MYSQL_CHARSET=utf8mb4
ALGORITHM=HS256
SECRET_KEY=SLKDFLASM
```

### 5. Database Tables
Tables will be automatically created when the application starts. The startup process creates:
- `users` - User accounts
- `posts` - Blog posts/content
- `comments` - Post comments
- `likes` - Post likes

## Running the Application

### Development Mode
```bash
python src/main.py
```

### Production Mode with Uvicorn
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000
```

### With Auto-reload 
```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

The application will be available at `http://localhost:8000`

### Health Check
- `GET /health` - Application health status

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login

### Posts
- `GET /posts` - Get all posts
- `POST /posts` - Create new post
- `GET /posts/{id}` - Get specific post
- `PUT /posts/{id}` - Update post
- `DELETE /posts/{id}` - Delete post

### Comments
- `GET /posts/{post_id}/comments` - Get post comments
- `POST /posts/{post_id}/comments` - Add comment
- `DELETE /comments/{id}` - Delete comment

### Likes
- `POST /posts/{post_id}/like` - Like/unlike post
- `GET /posts/{post_id}/likes` - Get post likes

