from sqlmodel import create_engine, Session, SQLModel
from api.core.config import get_settings

settings = get_settings()

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
