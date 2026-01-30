from typing import Optional
from sqlmodel import Field, SQLModel

class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    imdb_id: str = Field(index=True, unique=True)
    title: str
    poster_path: Optional[str] = None
    release_year: Optional[str] = None
    status: str = Field(default="to-watch") # "to-watch" or "watched"
    rating: Optional[str] = None
    personal_note: Optional[str] = None
    color: Optional[str] = Field(default="slate")
    actors: Optional[str] = None
    description: Optional[str] = None
    is_favorite: bool = Field(default=False)

class MovieCreate(SQLModel):
    imdb_id: str
    title: str
    poster_path: Optional[str] = None
    release_year: Optional[str] = None
    status: str = "to-watch"
    color: str = "slate"
    actors: Optional[str] = None
    description: Optional[str] = None
    is_favorite: bool = False

class MovieUpdate(SQLModel):
    status: Optional[str] = None
    color: Optional[str] = None
    personal_note: Optional[str] = None
    rating: Optional[str] = None
    is_favorite: Optional[bool] = None
