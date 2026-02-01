"""
Database configuration for SQLModel.
Supports both SQLite (local development) and Turso/libSQL (production).

Optimized for serverless environments with proper connection pooling.
"""
import os
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import NullPool, StaticPool
from api.core.config import get_settings

settings = get_settings()

# Cache the engine to avoid recreating it on every request
_engine = None


def _get_engine():
    """
    Create database engine based on DATABASE_URL type.
    Uses NullPool for serverless (no persistent connections that can timeout).
    """
    global _engine
    if _engine is not None:
        return _engine
    
    database_url = settings.DATABASE_URL
    turso_token = os.getenv("TURSO_AUTH_TOKEN", "")
    
    # Check if using Turso (libsql)
    if database_url.startswith("libsql://"):
        if not turso_token:
            print("⚠️  TURSO_AUTH_TOKEN not set, falling back to local SQLite")
            _engine = create_engine(
                "sqlite:///./movies.db",
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,  # Single connection for SQLite
                echo=False
            )
            return _engine
        
        # Convert libsql:// to sqlite+libsql:// format
        host = database_url.replace("libsql://", "")
        turso_url = f"sqlite+libsql://{host}?secure=true"
        
        print(f"🔌 Using Turso database: {host}")
        
        # NullPool = no connection pooling (best for serverless)
        # Each request gets a fresh connection, no stale connections
        _engine = create_engine(
            turso_url,
            connect_args={
                "auth_token": turso_token,
            },
            poolclass=NullPool,  # Best for serverless - no stale connections
            echo=False
        )
        return _engine
    
    # Default: SQLite local
    if "sqlite" in database_url:
        _engine = create_engine(
            database_url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,  # Single persistent connection for local dev
            echo=False
        )
        return _engine
    
    # Other databases (PostgreSQL, etc)
    _engine = create_engine(database_url, poolclass=NullPool, echo=False)
    return _engine


engine = _get_engine()


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Get database session. 
    Uses a context manager for proper cleanup.
    """
    with Session(engine) as session:
        yield session
