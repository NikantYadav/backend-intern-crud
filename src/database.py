from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import MetaData, text
from dotenv import load_dotenv
import os
from typing import AsyncGenerator

# Load environment variables from .env file
load_dotenv()

# Print environment variables for debugging
print(f"Loading environment variables...")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
print(f"MYSQL_CHARSET: {os.getenv('MYSQL_CHARSET')}")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./database.db")
MYSQL_CHARSET = os.getenv("MYSQL_CHARSET", "utf8mb4")

# Define naming convention for constraints to ensure consistent constraint naming
# This helps with MySQL foreign key constraint management
metadata = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})

# async engine and session with explicit MySQL configuration
# aiomysql doesn't need connect_args for charset as it's better specified in the URL
engine = create_async_engine(
    DATABASE_URL, 
    echo=True,
    pool_pre_ping=True,
    pool_recycle=300,
    # Important: setting pool_timeout to avoid hanging connections
    pool_timeout=30,
    # Add MySQL-specific connect args if using MySQL
    connect_args={
        "init_command": "SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci"
    } if "mysql" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base(metadata=metadata)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
