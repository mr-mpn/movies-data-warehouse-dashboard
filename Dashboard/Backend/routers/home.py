from fastapi import APIRouter
import sys
sys.path.append(".")
from Module.db_connector import connect_db
from Dashboard.Backend.DTO.models import HomeResponse, PaginatedHomeResponse
import pandas as pd
from typing import List
import math

router = APIRouter()

@router.get('/home')
async def get_Home(page: int = 1, page_size: int = 10):
    conn = connect_db()
    offset = (page - 1) * page_size

    count_df = pd.read_sql("SELECT COUNT(*) as total FROM rating_movie_silver", conn)
    total = int(count_df["total"][0])
    total_pages = math.ceil(total / page_size)

    df = pd.read_sql(f'''SELECT id, title, vote_average, vote_count
                    FROM movies
                    ORDER BY vote_average DESC LIMIT {page_size} OFFSET {offset}''', conn)

    return {
        "movies": df.to_dict(orient="records"),
        "total_pages": total_pages,
        "page": page
    }
