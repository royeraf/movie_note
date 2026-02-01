from sqlmodel import create_engine, Session, SQLModel
from api.core.config import get_settings
import os

settings = get_settings()

# Check if using Turso (production) or SQLite (local)
if settings.DATABASE_URL.startswith("libsql://"):
    # Turso configuration - requires sqlalchemy-libsql
    auth_token = os.getenv("TURSO_AUTH_TOKEN", "")
    
    # Convert libsql:// to sqlite+libsql:// for SQLAlchemy
    turso_url = settings.DATABASE_URL.replace("libsql://", "sqlite+libsql://")
    
    engine = create_engine(
        turso_url,
        connect_args={
            "check_same_thread": False,
            "sync_url": settings.DATABASE_URL,
            "auth_token": auth_token
        },
        echo=False
    )
else:
    # Local SQLite configuration
    engine = create_engine(
        settings.DATABASE_URL, 
        connect_args={"check_same_thread": False}
    )

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
