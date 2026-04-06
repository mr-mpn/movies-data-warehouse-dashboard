'''
This ETL is used to:
    - Extract the data from the _raw tables (E)
    - Transform data (T)
    - Load the updated values into the _bronze tables (L)

The data transformation 
'''

import sys
sys.path.append(".")
from Module.db_connector import connect_db
from Module.get_raw import extract_raw
from Module.write_db import write_to_db
import pandas as pd
import logging
import ast
from sqlalchemy import types

movies_bronze_schema = {
    "budget": types.BIGINT,
    "homepage": types.TEXT,
    "id": types.INTEGER,
    "imdb_id": types.VARCHAR(20),
    "original_language": types.VARCHAR(10),
    "original_title": types.TEXT,
    "overview": types.TEXT,
    "popularity": types.FLOAT,
    "release_date": types.TEXT,
    "revenue": types.BIGINT,
    "runtime": types.FLOAT,
    "status": types.VARCHAR(50),
    "title": types.TEXT,
    "vote_average": types.FLOAT,
    "vote_count": types.INTEGER,
    "collection_name": types.TEXT,
    "genres_names": types.TEXT,
    "production_companies_names": types.TEXT,
    "production_countries_names": types.TEXT,
    "spoken_languages_names": types.TEXT,
}

ratings_bronze_schema = {
    "userId": types.INTEGER,
    "movieId": types.INTEGER,
    "rating": types.FLOAT,
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)



def extract_json_name(value):
    try:
        return ast.literal_eval(value)["name"]
    except:
        return None

def extract_json_names(value):
    try:
        return [item["name"] for item in ast.literal_eval(value)]
    except:
        return []

def transform_ratings(df):
    logger.info(f"Step2- Applying transformation on ratings_raw")

    logger.info(f"Step2.1- Removing nulls df :  ratings_raw")
    #Remove nulls from id , popularity , titel 
    df = df.dropna(subset=["userId","movieId","rating"])

    
    #Drop timestamp
    logger.info(f"Step2.1- Drop timestamp df :  ratings_raw")
    df = df.drop(columns = ["timestamp"])
    logger.info(f"Step2- Transformation completed")
    return df 


def transform_movies(df):
    logger.info(f"Step2- Applying transformation on movies_raw")

    logger.info(f"Step2.1- Removing nulls df :  movies_raw")
    #Remove nulls from id , popularity , titel 
    df = df.dropna(subset=["id", "popularity", "title" , "vote_count" , "vote_average"])
    
    logger.info(f"Step2.2- Removing duplications df :  movies_raw")
    #Remove duplication from id
    df = df.drop_duplicates(subset=["id" , "title"])

    logger.info(f"Step2.3- Dropping columns: adult, tagline, video")
    df = df.drop(columns=["adult", "tagline", "video" , "poster_path"])

    logger.info(f"Step2.4- Extracting JSON fields - collection_name")
    # belongs_to_collection -> collection_name
    df["collection_name"] = df["belongs_to_collection"].apply(extract_json_name)
    df = df.drop(columns=["belongs_to_collection"])

    # genres -> genres_names
    logger.info(f"Step2.4- Extracting JSON fields - genres_names")
    df["genres_names"] = df["genres"].apply(extract_json_names)
    df = df.drop(columns=["genres"])

    # production_companies -> production_companies_names
    logger.info(f"Step2.4- Extracting JSON fields - production_companies_names")
    df["production_companies_names"] = df["production_companies"].apply(extract_json_names)
    df = df.drop(columns=["production_companies"])

    # production_countries -> production_countries_names
    logger.info(f"Step2.4- Extracting JSON fields - production_countries_names")
    df["production_countries_names"] = df["production_countries"].apply(extract_json_names)
    df = df.drop(columns=["production_countries"])

    # spoken_languages -> spoken_languages_names
    logger.info(f"Step2.4- Extracting JSON fields - spoken_languages_names")
    df["spoken_languages_names"] = df["spoken_languages"].apply(extract_json_names)
    df = df.drop(columns=["spoken_languages"])

    # Convert lists to comma-separated strings
    logger.info(f"Step2.5- Creating a comma seperated list for each column")
    df["production_companies_names"] = df["production_companies_names"].apply(lambda x: ", ".join(x))
    df["production_countries_names"] = df["production_countries_names"].apply(lambda x: ", ".join(x))
    df["spoken_languages_names"] = df["spoken_languages_names"].apply(lambda x: ", ".join(x))
    df["genres_names"] = df["genres_names"].apply(lambda x: ", ".join(x))

    logger.info(f"Step2- Transformation completed")
    return df


if __name__ == "__main__":
    #Step0: Connect to DB 
    conn = connect_db();

    #step1: Extract the data from the db (E)
    ratings_raw = extract_raw ("ratings_raw" , conn)
    movies_raw  = extract_raw ("movies_raw", conn)

    #Step2: Transform the data (T)
    ratings_filtered = transform_ratings(ratings_raw)
    movies_filtered = transform_movies(movies_raw)

    #Step3: Load the transformed data into _bronze tables (L)
    
    write_to_db(ratings_filtered,"ratings_bronze" , conn , dtype = ratings_bronze_schema )
    write_to_db(movies_filtered,"movies_bronze" , conn , dtype = movies_bronze_schema )