import pytest
from src.main import run_pipeline

def test_run_pipeline():
    rep = run_pipeline("data/sales.csv", "TEST-EXEC")
    assert rep["processed_count"] > 0
