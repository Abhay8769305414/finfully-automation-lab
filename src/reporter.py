from typing import List, Dict, Any

def generate_summary(processed_invoices: List[Dict[str, Any]], execution_id: str) -> Dict[str, Any]:
    total_val = sum(r["total_amount"] for r in processed_invoices)
    return {
        "execution_id": execution_id,
        "processed_count": len(processed_invoices),
        "total_value": round(total_val, 2),
        "summary": {"invoices_processed": len(processed_invoices), "total_amount": round(total_val, 2)}
    }
