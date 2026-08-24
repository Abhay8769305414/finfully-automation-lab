import pytest
from src.transformer import transform_records

def test_transform_records():
    raw = [{"invoice_id": "INV-1", "customer_id": "C1", "customer_name": "Acme", "product_id": "P1", "product_name": "W1", "quantity": "2", "unit_price": "10.0", "invoice_date": "2026-01-01"}]
    res = transform_records(raw)
    assert len(res) == 1
    assert res[0]["total_amount"] == 20.0
