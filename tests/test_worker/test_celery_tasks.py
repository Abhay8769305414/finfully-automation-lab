import pytest
from src.worker.tasks import process_invoice_batch_task

def test_process_invoice_batch_task(monkeypatch):
    monkeypatch.setenv("CELERY_TASK_ALWAYS_EAGER", "true")
    res = process_invoice_batch_task("data/sales.csv", "TEST-CELERY-001")
    assert res["processed_count"] > 0
