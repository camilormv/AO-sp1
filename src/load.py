# load.py
from typing import Dict

from pandas import DataFrame
from sqlalchemy.engine.base import Engine

def load(data_frames: Dict[str, DataFrame], database: Engine):
    """Load the dataframes into the sqlite database.

    Args:
        data_frames (Dict[str, DataFrame]): A dictionary with keys as the table names
        and values as the dataframes.
        database (Engine): SQLAlchemy Engine connected to your SQLite database.
    """
    for table_name, df in data_frames.items():
        df.to_sql(table_name, con=database, if_exists='replace', index=False)