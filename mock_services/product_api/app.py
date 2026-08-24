from fastapi import FastAPI
app = FastAPI()
@app.get("/health")
def health(): return {"status": "ok", "service": "product-api"}
@app.get("/products/{product_id}")
def get_product(product_id: str):
    return {"product_id": product_id, "sku": f"SKU-{product_id}", "in_stock": True}
