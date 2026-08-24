import pytest
from src.validator import validate_transformed_records

def test_validate_transformed_records():
    recs = [{"quantity": 5, "unit_price": 10.0}, {"quantity": 0, "unit_price": 5.0}]
    val = validate_transformed_records(recs)
    assert len(val) == 1
