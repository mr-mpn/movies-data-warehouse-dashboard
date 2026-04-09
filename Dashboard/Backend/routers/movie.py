from fastapi import APIRouter, HTTPException
import sys
sys.path.append(".")
from Module.db_connector import get_session
from Module.orm_models import Movie
from Dashboard.Backend.DTO.models import MovieResponse

router = APIRouter()

@router.get('/movie')
async def get_movie(movie_id: int) -> MovieResponse:
    session = get_session()
    try:
        movie_info = session.query(
            Movie.id, Movie.title, Movie.imdb_id, Movie.overview,
            Movie.release_date, Movie.spoken_languages_names
        ).filter(Movie.id == movie_id).first()

        if not movie_info:
            raise HTTPException(status_code=404, detail="Movie not found")

        return movie_info._asdict()
    finally:
        session.close()
