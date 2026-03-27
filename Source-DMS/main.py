import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

'''
This Script would act as the DMS (Database Management System).
The goal is to:
-Download the data from the other source 
-read csv files 
-store them inside the Postgres DB (This would be the exact mirror of the data.)

Source dataset = https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?resource=download
'''

def read_dataset(file_name):
    logger.info(f"Reading dataset : {file_name}")
    try:
        df = pd.read_csv(f"./Source-DMS/dataset/{file_name}.csv" , low_memory = False)
        logger.info(f"Dataframe has been loaded")
        return df
    except Exception as e:
        logger.warning(f"Error loading the file: {e}")


def connect_db():
    logger.info("Connecting to db : raw")
    try:
        user = os.getenv("POSTGRES_USER")
        password = os.getenv("POSTGRES_PASSWORD")
        db = os.getenv("POSTGRES_DB")
        engine = create_engine(f"postgresql://{user}:{password}@localhost:5432/{db}")
        logger.info("Connected to DB ...")
        return engine
    except Exception as e:
        logger.warning(f"Error Connecting to DB : {e}")

def write_to_db(df,table_name, conn):
    try:
        logger.info(f"Starting to write to db  , table name = {table_name}")
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        logger.info(f"Data has been inserted to {table_name}")
    except Exception as e:
        logger.warning(f"Error writing to DB raw , table name = {table_name} : {e}")


if __name__ == "__main__":

    #Step 1 : Read the dataset
    ratings = read_dataset("ratings_small")
    movies = read_dataset("movies_metadata")

    #Step2: Connect to the DB 
    conn  = connect_db()

    # Step 3: Write to the DB
    write_to_db(ratings , 'ratings_raw' , conn)
    write_to_db(movies , 'movies_raw' , conn)

