import pandas as pd
from surprise import Reader, Dataset
from app_configuration import AppConfig
from sqlalchemy import create_engine

class DataAccessError(Exception):
    """Custom exception for data access errors."""

class DataAccess:

    app_config = AppConfig()

    engine = create_engine(
        app_config.postgres_url,
        echo=False,  # If set to True, SQL statements and other details are logged (useful for debugging)
        pool_size=app_config.engine_pool_size,  # The number of connections to keep in the pool
        pool_timeout=app_config.engine_pool_timeout_in_s,  # Number of seconds to wait before giving up on returning a connection from the pool
        pool_recycle=app_config.engine_pool_recycle_in_s  # Number of seconds a connection can persist before being recycled
        # Add other parameters as needed
    )

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.app_configuration = AppConfig()
        self.postgres_url = self.app_configuration.postgres_url
        self.pg_schema = self.app_configuration.postgres_schema
        self.pg_table = self.app_configuration.postgres_table


    def load_data_from_csv(self, user_col, item_col, rating_col, rating_scale=(1, 5)):
        try:
            df = pd.read_csv(self.csv_path)
            reader = Reader(rating_scale=rating_scale)
            data = Dataset.load_from_df(df[[user_col, item_col, rating_col]], reader)
            return data
        except Exception as e:
            raise DataAccessError(f"Error loading data: {e}")

    def get_csv_data_frame(self):
        try:
            return pd.read_csv(self.csv_path)
        except Exception as e:
            raise DataAccessError(f"Error getting data frame: {e}")

    def get_postgres_data_frame(self, user_col, item_col, rating_col):
        try:
            #\" -> no sql inj possible
            query = f"SELECT \"{user_col}\", \"{item_col}\", \"{rating_col}\" FROM \"{self.pg_schema}\".\"{self.pg_table}\""


            return pd.read_sql_query(query, DataAccess.engine)
        except Exception as e:
            raise DataAccessError(f"Error getting data frame from PostgreSQL: {e}")

    def load_data_from_db(self, user_col, item_col, rating_col, rating_scale=(1, 5)):
        try:
            # \" -> no sql inj possible
            query = f"SELECT \"{user_col}\", \"{item_col}\", \"{rating_col}\" FROM \"{self.pg_schema}\".\"{self.pg_table}\""

            df = pd.read_sql(query, DataAccess.engine)
            reader = Reader(rating_scale=rating_scale)
            data = Dataset.load_from_df(df[[user_col, item_col, rating_col]], reader)
            return data
        except Exception as e:
            raise DataAccessError(f"Error loading data from PostgreSQL: {e}")


