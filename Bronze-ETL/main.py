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


def extract_raw(table_name , conn):
    logger.info(f"Extracting data from table : {table_name}")
    try:
        df = pd.read_sql(f"SELECT * FROM {table_name}" , conn)    
        logger.info(f"Extracted {len(df)} rows from {table_name}")
        return df
    except Exception as e :
        logger.warning(f"Error extracting data from DB : {e}")    

if __name__ == "__main__":
    #Step1: Connect to DB 
    conn = connect_db();

    #step2: Extract the data from the db (E)
    ratings_raw = extract_raw ("ratings_raw" , conn)
    movies_raw  = extract_raw ("movies_raw", conn)

    #Step3: Transform the data (T)


    #Step4: Load the transformed data into _bronze tables (L)