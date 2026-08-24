from typing import List, Dict, Any

def validate_transformed_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    valid = []
    for r in records:
        if r["quantity"] > 0 and r["unit_price"] >= 0:
            valid.append(r)
    return valid
