import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

'''
This Script would act as the DMS (Database Management System).
The goal is to:
-Download the data from the other source 
-read csv files 
-store them inside the Postgres DB (This would be the exact mirror of the data.)

Source dataset = https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset?resource=download
'''

def read_dataset(file_name):
    return pd.read_csv(f"./Source-DMS/dataset/{file_name}.csv")

def connect_db():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db = os.getenv("POSTGRES_DB")
    engine = create_engine(f"postgresql://{user}:{password}@localhost:5432/{db}")
    return engine


if __name__ == "__main__":

    #Step 1 : Read the dataset
    ratings = read_dataset("ratings_small")
    movies = read_dataset("movies_metadata")

    #Step2: Connect to the DB 
    conn  = connect_db()

    # Step 3: Write to the DB
    ratings.to_sql("ratings_raw", conn, if_exists="replace", index=False)
    movies.to_sql("movies_raw", conn, if_exists="replace", index=False)


