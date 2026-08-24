import pytest
from src.reader import read_sales_csv

def test_read_sales_csv():
    records = read_sales_csv("data/sales.csv")
    assert len(records) > 0
    assert "invoice_id" in records[0]
