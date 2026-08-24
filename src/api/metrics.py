from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status_code'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Latency', ['method', 'endpoint'])
DB_CONNECTION_ERRORS_TOTAL = Counter('db_connection_errors_total', 'Total DB Connection Errors')
DB_TRANSACTION_ROLLBACKS_TOTAL = Counter('db_transaction_rollbacks_total', 'Total DB Transaction Rollbacks')
