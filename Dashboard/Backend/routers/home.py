from fastapi import APIRouter
import sys
sys.path.append(".")
from Module.db_connector import connect_db
from Dashboard.Backend.DTO.models import HomeResponse
import pandas as pd
from typing import List


router = APIRouter()

@router.get('/home')
async def get_Home() -> List[HomeResponse]:
    conn = connect_db();
    df = pd.read_sql('''SELECT title , vote_average ,vote_count
                    FROM rating_movie_silver 
                    ORDER BY vote_average DESC LIMIT 10''' , conn)
    return df.to_dict(orient="records")
 