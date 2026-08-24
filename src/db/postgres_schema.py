def init_postgres_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS invoice_ledger (
                invoice_id VARCHAR(255) PRIMARY KEY,
                customer_id VARCHAR(255) NOT NULL,
                total_amount NUMERIC(12,2) NOT NULL,
                status VARCHAR(50) NOT NULL DEFAULT 'PENDING',
                claimed_by VARCHAR(255),
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS execution_jobs (
                execution_id VARCHAR(255) PRIMARY KEY,
                file_path TEXT NOT NULL,
                source VARCHAR(100) DEFAULT 'manual',
                status VARCHAR(50) NOT NULL DEFAULT 'queued',
                result_summary JSONB,
                report_path TEXT,
                error_message TEXT,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS human_review_queue (
                id SERIAL PRIMARY KEY,
                customer_id VARCHAR(255) NOT NULL,
                customer_name VARCHAR(255),
                raw_note TEXT NOT NULL,
                flag_reason JSONB,
                status VARCHAR(50) NOT NULL DEFAULT 'pending',
                reviewed_by VARCHAR(255),
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS ai_classification_idempotency (
                idempotency_key VARCHAR(255) PRIMARY KEY,
                customer_id VARCHAR(255) NOT NULL,
                raw_note TEXT NOT NULL,
                classification_json JSONB NOT NULL,
                created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
            );
        """)
