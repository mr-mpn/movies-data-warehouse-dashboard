import logging
import pandas as pd

logger = logging.getLogger(__name__)

def extract_raw(table_name , conn):
    logger.info(f"Step1 - Extracting data from table : {table_name}")
    try:
        df = pd.read_sql(f"SELECT * FROM {table_name}" , conn)    
        logger.info(f"Step1 - Extracted {len(df)} rows from {table_name}")
        return df
    except Exception as e :
        logger.warning(f"Step1 - Error extracting data from DB : {e}") 