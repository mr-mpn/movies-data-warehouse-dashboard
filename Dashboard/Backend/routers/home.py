from fastapi import APIRouter, Query
import sys
sys.path.append(".")
from Module.db_connector import get_session
from Module.orm_models import Movie
from Dashboard.Backend.DTO.models import PaginatedHomeResponse
from sqlalchemy import func
import math

router = APIRouter()

@router.get('/home')
async def get_Home(page: int = Query(default=1, ge=1), page_size: int = Query(default=10, ge=1)) -> PaginatedHomeResponse:
    session = get_session()
    try:
        offset = (page - 1) * page_size

        total = session.query(func.count(Movie.id)).scalar()
        total_pages = math.ceil(total / page_size)

        movies = session.query(Movie.id, Movie.title, Movie.vote_average, Movie.vote_count)\
            .order_by(Movie.vote_average.desc())\
            .offset(offset).limit(page_size).all()

        return {
            "movies": [
                {"id": m.id, "title": m.title, "vote_average": m.vote_average, "vote_count": m.vote_count}
                for m in movies
            ],
            "total_pages": total_pages,
            "page": page
        }
    finally:
        session.close()
