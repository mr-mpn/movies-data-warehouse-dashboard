from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logger = logging.getLogger(__name__)

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