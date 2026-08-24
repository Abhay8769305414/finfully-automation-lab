import os
from src.config import Config
from src.db.connection import get_connection
from src.db.schema import init_db
from src.db.postgres_connection import get_postgres_connection
from src.db.postgres_schema import init_postgres_db

from src.repositories.sqlite.ledger_repo import SQLiteLedgerRepository
from src.repositories.sqlite.execution_repo import SQLiteExecutionRepository
from src.repositories.sqlite.review_repo import SQLiteReviewRepository
from src.repositories.sqlite.ai_idempotency_repo import SQLiteAIIdempotencyRepository

from src.repositories.postgres.ledger_repo import PostgresLedgerRepository
from src.repositories.postgres.execution_repo import PostgresExecutionRepository
from src.repositories.postgres.review_repo import PostgresReviewRepository
from src.repositories.postgres.ai_idempotency_repo import PostgresAIIdempotencyRepository

def get_backend_type() -> str:
    return os.getenv("DATABASE_BACKEND", Config.DATABASE_BACKEND).lower()

def get_ledger_repository():
    if get_backend_type() == "postgres":
        conn = get_postgres_connection()
        init_postgres_db(conn)
        return PostgresLedgerRepository(conn)
    conn = get_connection()
    init_db(conn)
    return SQLiteLedgerRepository(conn)

def get_execution_repository():
    if get_backend_type() == "postgres":
        conn = get_postgres_connection()
        init_postgres_db(conn)
        return PostgresExecutionRepository(conn)
    conn = get_connection()
    init_db(conn)
    return SQLiteExecutionRepository(conn)

def get_review_repository():
    if get_backend_type() == "postgres":
        conn = get_postgres_connection()
        init_postgres_db(conn)
        return PostgresReviewRepository(conn)
    conn = get_connection()
    init_db(conn)
    return SQLiteReviewRepository(conn)

def get_ai_idempotency_repository():
    if get_backend_type() == "postgres":
        conn = get_postgres_connection()
        init_postgres_db(conn)
        return PostgresAIIdempotencyRepository(conn)
    conn = get_connection()
    init_db(conn)
    return SQLiteAIIdempotencyRepository(conn)
