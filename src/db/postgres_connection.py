import os
import psycopg
from psycopg.rows import dict_row
from src.config import Config

def get_postgres_connection():
    dsn = Config.get_postgres_dsn()
    return psycopg.connect(dsn, row_factory=dict_row, autocommit=True)
