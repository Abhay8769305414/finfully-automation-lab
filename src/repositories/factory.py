import os
from src.config import Config

class RepositoryFactory:
    @staticmethod
    def get_backend_type() -> str:
        return Config.DATABASE_BACKEND.lower()


def get_ledger_repository(conn=None):
    b = RepositoryFactory.get_backend_type()
    if b == "postgres":
        from src.repositories.postgres.ledger_repo import PostgresLedgerRepository
        return PostgresLedgerRepository(conn)
    else:
        from src.repositories.sqlite.ledger_repo import SQLiteLedgerRepository
        return SQLiteLedgerRepository(conn)


def get_execution_repository(conn=None):
    b = RepositoryFactory.get_backend_type()
    if b == "postgres":
        from src.repositories.postgres.execution_repo import PostgresExecutionRepository
        return PostgresExecutionRepository(conn)
    else:
        from src.repositories.sqlite.execution_repo import SQLiteExecutionRepository
        return SQLiteExecutionRepository(conn)


def get_review_repository(conn=None):
    b = RepositoryFactory.get_backend_type()
    if b == "postgres":
        from src.repositories.postgres.review_repo import PostgresReviewRepository
        return PostgresReviewRepository(conn)
    else:
        from src.repositories.sqlite.review_repo import SQLiteReviewRepository
        return SQLiteReviewRepository(conn)


def get_ai_idempotency_repository(conn=None):
    b = RepositoryFactory.get_backend_type()
    if b == "postgres":
        from src.repositories.postgres.ai_idempotency_repo import PostgresAIIdempotencyRepository
        return PostgresAIIdempotencyRepository(conn)
    else:
        from src.repositories.sqlite.ai_idempotency_repo import SQLiteAIIdempotencyRepository
        return SQLiteAIIdempotencyRepository(conn)
