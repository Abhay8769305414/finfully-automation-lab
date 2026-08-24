from typing import List, Dict, Any

def transform_records(raw_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    transformed = []
    for r in raw_records:
        qty = int(r.get("quantity", 0))
        price = float(r.get("unit_price", 0.0))
        calc_total = round(qty * price, 2)
        transformed.append({
            "invoice_id": r["invoice_id"].strip(),
            "customer_id": r["customer_id"].strip(),
            "customer_name": r["customer_name"].strip(),
            "product_id": r["product_id"].strip(),
            "product_name": r["product_name"].strip(),
            "quantity": qty,
            "unit_price": price,
            "total_amount": calc_total,
            "invoice_date": r["invoice_date"].strip(),
            "status": r.get("status", "PENDING").strip(),
        })
    return transformed
