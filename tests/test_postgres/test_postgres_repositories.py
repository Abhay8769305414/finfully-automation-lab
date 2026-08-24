"""
test_postgres_repositories.py
------------------------------
PostgreSQL Real Integration Test Suite.
"""

import threading
import pytest
import psycopg
from psycopg.rows import dict_row
from datetime import datetime, timezone, timedelta

from src.config import Config
from src.db.postgres_schema import init_postgres_db
from src.repositories.postgres.ledger_repo import PostgresLedgerRepository
from src.repositories.postgres.execution_repo import PostgresExecutionRepository
from src.repositories.postgres.review_repo import PostgresReviewRepository
from src.repositories.postgres.ai_idempotency_repo import PostgresAIIdempotencyRepository


def is_postgres_available() -> bool:
    import os
    dsn = os.getenv(
        "DATABASE_URL",
        f"postgresql://{os.getenv('PGUSER', 'postgres')}:{os.getenv('PGPASSWORD', 'postgres')}@{os.getenv('PGHOST', 'localhost')}:{os.getenv('PGPORT', '5432')}/{os.getenv('PGDATABASE', 'finfully')}"
    )
    try:
        with psycopg.connect(dsn, connect_timeout=1) as conn:
            return True
    except Exception:
        return False


@pytest.fixture
def pg_conn():
    import os
    dsn = os.getenv(
        "DATABASE_URL",
        f"postgresql://{os.getenv('PGUSER', 'postgres')}:{os.getenv('PGPASSWORD', 'postgres')}@{os.getenv('PGHOST', 'localhost')}:{os.getenv('PGPORT', '5432')}/{os.getenv('PGDATABASE', 'finfully')}"
    )
    conn = psycopg.connect(dsn, row_factory=dict_row, autocommit=True)
    with conn.cursor() as cur:
        cur.execute("TRUNCATE invoice_ledger, execution_jobs, human_review_queue, ai_classification_idempotency RESTART IDENTITY CASCADE;")
    yield conn
    conn.close()


class TestPostgresRepositories:

    def test_postgres_invoice_lifecycle(self, pg_conn):
        repo = PostgresLedgerRepository(pg_conn)
        res = repo.create_invoice("INV-PG-001", "CUST-PG-1", 100.0)
        assert res["status"] == "PENDING"
        claimed = repo.claim_invoice("INV-PG-001", "EXEC-PG-01")
        assert claimed is True

    def test_postgres_stale_processing_recovery(self, pg_conn):
        repo = PostgresLedgerRepository(pg_conn)
        repo.create_invoice("INV-PG-STALE", "CUST-1", 200.0)
        repo.claim_invoice("INV-PG-STALE", "OLD-EXEC")
        with pg_conn.cursor() as cur:
            old_time = datetime.now(timezone.utc) - timedelta(minutes=15)
            cur.execute("UPDATE invoice_ledger SET updated_at = %s WHERE invoice_id = %s", (old_time, "INV-PG-STALE"))
        recovered = repo.recover_stale_processing(timeout_minutes=10)
        assert recovered == 1

    def test_postgres_unique_constraints(self, pg_conn):
        repo = PostgresLedgerRepository(pg_conn)
        repo.create_invoice("INV-PG-DUP", "CUST-1", 50.0)
        with pytest.raises(Exception):
            repo.create_invoice("INV-PG-DUP", "CUST-1", 50.0)

    def test_postgres_transaction_rollback(self, pg_conn):
        repo = PostgresLedgerRepository(pg_conn)
        try:
            with pg_conn.transaction():
                repo.create_invoice("INV-PG-TX1", "CUST-1", 10.0)
                raise RuntimeError("Simulated DB failure")
        except RuntimeError:
            pass
        found = repo.get_by_id("INV-PG-TX1")
        assert found is None

    def test_postgres_execution_jobs_lifecycle(self, pg_conn):
        repo = PostgresExecutionRepository(pg_conn)
        created = repo.create_job("EXEC-PG-100", file_path="data/sales.csv", source="pytest")
        assert created["status"] == "queued"
        upd = repo.update_job_status("EXEC-PG-100", "running")
        assert upd["status"] == "running"
        comp = repo.update_job_status("EXEC-PG-100", "completed", result_summary={"invoices": 4})
        assert comp["status"] == "completed"

    def test_postgres_human_review_state_machine(self, pg_conn):
        repo = PostgresReviewRepository(pg_conn)
        created = repo.create_review_item("CUST-1", "Initech LLC", "Bad note", {"reason": "risk"})
        item_id = created["id"]
        assert created["status"] == "pending"
        approved = repo.approve_item(item_id, reviewed_by="admin")
        assert approved["status"] == "approved"

    def test_postgres_ai_idempotency_jsonb(self, pg_conn):
        repo = PostgresAIIdempotencyRepository(pg_conn)
        payload = {"intent": "urgent", "confidence": 0.95}
        key = repo.generate_key("CUST-1", "Urgent note")
        repo.save(key, "CUST-1", "Urgent note", payload)
        found = repo.get(key)
        assert found is not None
        assert found["intent"] == "urgent"

    def test_postgres_atomic_concurrent_invoice_claim(self, pg_conn):
        repo = PostgresLedgerRepository(pg_conn)
        repo.create_invoice("INV-CONCURRENT-001", "CUST-1", 100.0)

        results = []
        def worker(thread_id):
            import os
            dsn = os.getenv(
                "DATABASE_URL",
                f"postgresql://{os.getenv('PGUSER', 'postgres')}:{os.getenv('PGPASSWORD', 'postgres')}@{os.getenv('PGHOST', 'localhost')}:{os.getenv('PGPORT', '5432')}/{os.getenv('PGDATABASE', 'finfully')}"
            )
            c = psycopg.connect(dsn, row_factory=dict_row, autocommit=True)
            r = PostgresLedgerRepository(c)
            claimed = r.claim_invoice("INV-CONCURRENT-001", f"EXEC-THREAD-{thread_id}")
            results.append(claimed)
            c.close()

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert results.count(True) == 1
        assert results.count(False) == 4
