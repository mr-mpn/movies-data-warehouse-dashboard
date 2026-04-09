from fastapi import APIRouter,HTTPException
import pandas as pd
import sys
sys.path.append(".")
from Module.db_connector import connect_db
from Dashboard.Backend.DTO.models import MovieResponse

router = APIRouter()

@router.get('/movie')
async def get_movie(movie_id : int)->MovieResponse:
    if not movie_id:
        raise HTTPException(status_code=400, detail="The id  is required")
    conn = connect_db()    
    df = pd.read_sql(f'''
                     SELECT id,title ,imdb_id, overview, release_date, spoken_languages_names FROM movies WHERE id={movie_id}
                     ''' , conn )
    results = df.to_dict(orient="records")
    if not results:
        raise HTTPException(status_code=404, detail="Movie not found")
    return results[0]
