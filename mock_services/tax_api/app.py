from fastapi import FastAPI
app = FastAPI()
@app.get("/health")
def health(): return {"status": "ok", "service": "tax-api"}
@app.get("/tax/{country}")
def get_tax(country: str):
    return {"country": country, "tax_rate": 0.10}
