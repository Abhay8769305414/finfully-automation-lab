import os
import sqlite3
from typing import Optional

def get_connection(db_path: str = "state/ledger.db") -> sqlite3.Connection:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
