from fastapi import APIRouter
from api.v1.endpoints import movies, search

api_router = APIRouter()

api_router.include_router(movies.router, prefix="/movies", tags=["movies"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
