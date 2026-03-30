import logging
import pandas as pd

logger = logging.getLogger(__name__)

def write_to_db(df,table_name, conn):
    try:
        logger.info(f"Step3 - Starting to write to db  , table name = {table_name}")
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        logger.info(f"Data has been inserted to {table_name}")
    except Exception as e:
        logger.warning(f"Error writing to DB raw , table name = {table_name} : {e}")
