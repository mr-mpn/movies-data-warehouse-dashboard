'''
This ETL reads data from the bronze layer , creates a complex table which contains information
on both the ratings and the movies.

'''

import sys
sys.path.append(".")
from Module.db_connector import connect_db
from Module.get_raw import extract_raw
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)




if __name__ == "__main__":

    #Step0 : Connect to DB 
    conn = connect_db();

    #Step1: Read from Bronze 
    ratings_bronze = extract_raw("ratings_bronze",conn)
    movies_bronze = extract_raw("movies_bronze" , conn)

    #Step2: Transform
    ratings_movies_transformed = transform(ratings_bronze,movies_bronze)

    