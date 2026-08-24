from fastapi import FastAPI
app = FastAPI()
@app.get("/health")
def health(): return {"status": "ok", "service": "customer-api"}
@app.get("/customers/{customer_id}")
def get_customer(customer_id: str):
    return {"customer_id": customer_id, "name": f"Customer {customer_id}", "status": "ACTIVE"}
