import socket

hosts = [
    ("postgres", 5432),
    ("redis", 6379),
    ("customer-api", 8001),
    ("product-api", 8002),
    ("tax-api", 8003),
    ("accounting-api", 8004),
    ("notification-api", 8005),
]

for host, port in hosts:
    ip = socket.gethostbyname(host)
    print(f"[PASS] Resolved {host}:{port} -> {ip}")
