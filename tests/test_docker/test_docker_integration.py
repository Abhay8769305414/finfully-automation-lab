"""
test_docker_integration.py
---------------------------
Container Integration Tests for Stage 6 Docker Compose environment.

Verifies:
- API /health & /ready endpoints
- Mock Microservices health
- Job submission & Celery background task processing
- Invoice idempotency in containerized mode
"""

import time
import uuid
import httpx
import pytest

API_BASE_URL = "http://localhost:8000"


def is_docker_running() -> bool:
    try:
        res = httpx.get(f"{API_BASE_URL}/health", timeout=2.0)
        return res.status_code == 200
    except Exception:
        return False


# Skip tests if Docker Compose environment is not actively running on localhost:8000
pytestmark = pytest.mark.skipif(
    not is_docker_running(),
    reason="Docker Compose environment is not running on http://localhost:8000",
)


class TestDockerIntegration:
    def test_docker_api_health(self):
        res = httpx.get(f"{API_BASE_URL}/health", timeout=5.0)
        assert res.status_code == 200
        assert res.json()["status"] == "ok"

    def test_docker_api_readiness(self):
        res = httpx.get(f"{API_BASE_URL}/ready", timeout=5.0)
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "ready"
        assert data["database"] == "postgresql"

    def test_docker_e2e_invoice_processing(self):
        exec_id = f"EXEC-DOCKER-TEST-{uuid.uuid4().hex[:6]}"
        payload = {
            "file_path": "data/sales.csv",
            "execution_id": exec_id,
            "source": "docker_pytest",
        }

        res = httpx.post(f"{API_BASE_URL}/process", json=payload, timeout=5.0)
        assert res.status_code == 202
        assert res.json()["execution_id"] == exec_id

        # Poll status for up to 15s
        completed = False
        for _ in range(15):
            time.sleep(1)
            s_res = httpx.get(f"{API_BASE_URL}/status/{exec_id}", timeout=5.0)
            if s_res.status_code == 200 and s_res.json()["status"] == "completed":
                completed = True
                break
        assert completed, f"Job {exec_id} failed to reach 'completed' state within 15s"

        # Verify report availability
        rep_res = httpx.get(f"{API_BASE_URL}/reports/{exec_id}", timeout=5.0)
        assert rep_res.status_code == 200
        assert rep_res.json()["execution_id"] == exec_id

    def test_docker_job_idempotency(self):
        exec_id = f"EXEC-DOCKER-IDEM-{uuid.uuid4().hex[:6]}"
        payload = {"file_path": "data/sales.csv", "execution_id": exec_id}

        res1 = httpx.post(f"{API_BASE_URL}/process", json=payload, timeout=5.0)
        assert res1.status_code == 202

        res2 = httpx.post(f"{API_BASE_URL}/process", json=payload, timeout=5.0)
        assert res2.status_code in (200, 202)
        assert res2.json()["execution_id"] == exec_id
