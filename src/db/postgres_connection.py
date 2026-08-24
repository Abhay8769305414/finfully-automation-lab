"""
postgres_connection.py
----------------------
PostgreSQL Connection Pooling & Management using psycopg3 (psycopg_pool).
"""

import logging
from contextlib import contextmanager
from typing import Generator, Optional

import psycopg
from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

from src.config import Config
from src.api.metrics import DB_CONNECTION_ERRORS_TOTAL, DB_TRANSACTION_ROLLBACKS_TOTAL

logger = logging.getLogger(__name__)

_POSTGRES_POOL: Optional[ConnectionPool] = None


def get_postgres_pool() -> ConnectionPool:
    """
    Lazy singleton initializer for psycopg ConnectionPool.
    """
    global _POSTGRES_POOL
    if _POSTGRES_POOL is None or _POSTGRES_POOL.closed:
        dsn = Config.get_database_url()
        min_c = Config.POSTGRES_MIN_CONN
        max_c = Config.POSTGRES_MAX_CONN

        safe_dsn = dsn.split("@")[-1] if "@" in dsn else "localhost"
        logger.info("Initializing PostgreSQL Connection Pool (min=%d, max=%d, host=%s)", min_c, max_c, safe_dsn)

        try:
            _POSTGRES_POOL = ConnectionPool(
                conninfo=dsn,
                min_size=min_c,
                max_size=max_c,
                kwargs={"row_factory": dict_row, "connect_timeout": 2},
                check=ConnectionPool.check_connection,
                open=True,
                timeout=2.0,
            )
        except Exception as exc:
            DB_CONNECTION_ERRORS_TOTAL.inc()
            logger.error("Failed to connect to PostgreSQL: %s", exc)
            raise exc

    return _POSTGRES_POOL


@contextmanager
def get_postgres_connection() -> Generator[psycopg.Connection, None, None]:
    """
    Context manager for borrowing a PostgreSQL connection from the pool.
    """
    pool = get_postgres_pool()
    conn = None
    try:
        conn = pool.getconn(timeout=2.0)
    except Exception as pool_exc:
        logger.warning("Pool checkout failed, re-initializing pool: %s", pool_exc)
        close_postgres_pool()
        pool = get_postgres_pool()
        conn = pool.getconn(timeout=2.0)

    try:
        yield conn
        conn.commit()
    except Exception as exc:
        try:
            conn.rollback()
        except Exception:
            pass
        DB_TRANSACTION_ROLLBACKS_TOTAL.inc()
        logger.warning("PostgreSQL transaction rolled back due to error: %s", exc)
        raise exc
    finally:
        if conn is not None:
            try:
                if getattr(conn, "closed", False):
                    pool.putconn(conn, close=True)
                else:
                    pool.putconn(conn)
            except Exception:
                pass


def close_postgres_pool() -> None:
    """Close the global PostgreSQL connection pool."""
    global _POSTGRES_POOL
    if _POSTGRES_POOL is not None:
        try:
            if not _POSTGRES_POOL.closed:
                _POSTGRES_POOL.close(timeout=0.5)
        except Exception:
            pass
        _POSTGRES_POOL = None
        logger.info("PostgreSQL connection pool closed.")
