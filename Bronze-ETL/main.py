import sys
sys.path.append(".")
from Module.db_connector import connect_db
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

'''
This ETL is used to:
    - Extract the data from the _raw tables (E)
    - Transform data (T)
    - Load the updated values into the _bronze tables (L)

The data transformation 
'''

def transform_movies(df):
    logger.info(f"Step2- Applying transformation on movies_raw")
    logger.info(f"Step2.1- Removing nulls df :  movies_raw")
    #Remove nulls from id , popularity , titel 
    df = df.dropna(subset=["id", "popularity", "title"])
    logger.info(f"Step2.2- Removing duplications df :  movies_raw")
    #Remove duplication from id
    df = df.drop_duplicates(subset=["id"])


def extract_raw(table_name , conn):
    logger.info(f"Step1 - Extracting data from table : {table_name}")
    try:
        df = pd.read_sql(f"SELECT * FROM {table_name}" , conn)    
        logger.info(f"Step1 - Extracted {len(df)} rows from {table_name}")
        return df
    except Exception as e :
        logger.warning(f"Step1 - Error extracting data from DB : {e}")    

if __name__ == "__main__":
    #Step0: Connect to DB 
    conn = connect_db();

    #step1: Extract the data from the db (E)
    ratings_raw = extract_raw ("ratings_raw" , conn)
    movies_raw  = extract_raw ("movies_raw", conn)

    #Step2: Transform the data (T)

    movies_filtered = transform_movies(movies_raw)

    #Step3: Load the transformed data into _bronze tables (L)