from fastapi import APIRouter
import sys
sys.path.append(".")
from Module.db_connector import connect_db
from Dashboard.Backend.DTO.models import HomeResponse
import pandas as pd
from typing import List

router = APIRouter()

@router.get('/home')
async def get_Home(page: int = 1, page_size: int = 10) -> List[HomeResponse]:
    conn = connect_db()
    offset = (page - 1) * page_size
    df = pd.read_sql(f'''SELECT title, vote_average, vote_count
                    FROM rating_movie_silver
                    ORDER BY vote_average DESC LIMIT {page_size} OFFSET {offset}''', conn)
    return df.to_dict(orient="records")
