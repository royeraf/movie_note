from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from api.core.database import get_session
from api.models.movie import Movie, MovieCreate, MovieUpdate

router = APIRouter()

@router.get("/", response_model=List[Movie])
def get_movies(session: Session = Depends(get_session)):
    movies = session.exec(select(Movie)).all()
    return movies

@router.post("/", response_model=Movie)
def add_movie(movie: MovieCreate, session: Session = Depends(get_session)):
    # Check if already exists
    statement = select(Movie).where(Movie.imdb_id == movie.imdb_id)
    existing = session.exec(statement).first()
    if existing:
        return existing
    
    db_movie = Movie.from_orm(movie)
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie

@router.patch("/{imdb_id}")
def update_movie(
    imdb_id: str, 
    status: Optional[str] = None,
    color: Optional[str] = None,
    session: Session = Depends(get_session)
):
    statement = select(Movie).where(Movie.imdb_id == imdb_id)
    db_movie = session.exec(statement).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    if status is not None:
        db_movie.status = status
    if color is not None:
        db_movie.color = color
        
    session.add(db_movie)
    session.commit()
    session.refresh(db_movie)
    return db_movie

@router.delete("/{imdb_id}")
def delete_movie(imdb_id: str, session: Session = Depends(get_session)):
    statement = select(Movie).where(Movie.imdb_id == imdb_id)
    db_movie = session.exec(statement).first()
    if not db_movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    session.delete(db_movie)
    session.commit()
    return {"message": "Movie deleted"}
