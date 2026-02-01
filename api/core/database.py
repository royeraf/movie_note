from sqlmodel import create_engine, Session, SQLModel
from api.core.config import get_settings

settings = get_settings()

# Create engine - works with both SQLite (local) and PostgreSQL (production)
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=False
)

def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get database session."""
    with Session(engine) as session:
        yield session
