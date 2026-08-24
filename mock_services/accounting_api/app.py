from fastapi import FastAPI
app = FastAPI()
@app.get("/health")
def health(): return {"status": "ok", "service": "accounting-api"}
@app.post("/post")
def post_accounting(data: dict):
    return {"status": "POSTED", "reference": "ACC-REF-9999"}
