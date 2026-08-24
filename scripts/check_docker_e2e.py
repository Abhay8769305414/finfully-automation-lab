import httpx

api_url = "http://localhost:8000"
payload = {"file_path": "data/sales.csv", "execution_id": "EXEC-DOCKER-E2E-001", "source": "e2e_check"}

print("Dispatching POST /process...")
res = httpx.post(f"{api_url}/process", json=payload, timeout=5.0)
print(f"POST /process status: {res.status_code}")
print(f"Response body: {res.json()}")

print("\nFetching GET /status/EXEC-DOCKER-E2E-001...")
status_res = httpx.get(f"{api_url}/status/EXEC-DOCKER-E2E-001", timeout=5.0)
print(f"GET /status status: {status_res.status_code}")
print(f"Response body: {status_res.json()}")

print("\nFetching GET /reports/EXEC-DOCKER-E2E-001...")
report_res = httpx.get(f"{api_url}/reports/EXEC-DOCKER-E2E-001", timeout=5.0)
print(f"GET /reports status: {report_res.status_code}")
print(f"Report summary: {report_res.json().get('summary') if report_res.status_code == 200 else report_res.text}")
