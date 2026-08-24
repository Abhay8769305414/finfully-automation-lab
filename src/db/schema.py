import sqlite3

def init_db(conn: sqlite3.Connection):
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS invoice_ledger (
                invoice_id TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'PENDING',
                claimed_by TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS execution_jobs (
                execution_id TEXT PRIMARY KEY,
                file_path TEXT NOT NULL,
                source TEXT DEFAULT 'manual',
                status TEXT NOT NULL DEFAULT 'queued',
                result_summary TEXT,
                report_path TEXT,
                error_message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS human_review_queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT NOT NULL,
                customer_name TEXT,
                raw_note TEXT NOT NULL,
                flag_reason TEXT,
                status TEXT NOT NULL DEFAULT 'pending',
                reviewed_by TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ai_classification_idempotency (
                idempotency_key TEXT PRIMARY KEY,
                customer_id TEXT NOT NULL,
                raw_note TEXT NOT NULL,
                classification_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
