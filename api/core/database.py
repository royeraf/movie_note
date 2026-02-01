"""
Database configuration for SQLModel.
Supports both SQLite (local development) and Turso/libSQL (production).
"""
import os
from sqlmodel import create_engine, Session, SQLModel
from api.core.config import get_settings

settings = get_settings()


def _get_engine():
    """
    Create database engine based on DATABASE_URL type.
    
    Supports:
    - sqlite:///./movies.db for local development
    - libsql:// for Turso in production
    """
    database_url = settings.DATABASE_URL
    turso_token = os.getenv("TURSO_AUTH_TOKEN", "")
    
    # Check if using Turso (libsql)
    if database_url.startswith("libsql://"):
        if not turso_token:
            print("⚠️  TURSO_AUTH_TOKEN not set, falling back to local SQLite")
            return create_engine(
                "sqlite:///./movies.db",
                connect_args={"check_same_thread": False},
                echo=False
            )
        
        # Convert libsql:// to sqlite+libsql:// format for sqlalchemy-libsql driver
        # Remote database format: sqlite+libsql://hostname?secure=true
        host = database_url.replace("libsql://", "")
        turso_url = f"sqlite+libsql://{host}?secure=true"
        
        print(f"🔌 Using Turso database: {host}")
        
        # Auth token must be passed in connect_args, not in the URL
        return create_engine(
            turso_url,
            connect_args={
                "auth_token": turso_token,
            },
            echo=False
        )
    
    # Default: SQLite local
    if "sqlite" in database_url:
        return create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            echo=False
        )
    
    # Other databases (PostgreSQL, etc)
    return create_engine(database_url, echo=False)


engine = _get_engine()


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session."""
    with Session(engine) as session:
        yield session
