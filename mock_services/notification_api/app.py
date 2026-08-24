from fastapi import FastAPI
app = FastAPI()
@app.get("/health")
def health(): return {"status": "ok", "service": "notification-api"}
@app.post("/notify")
def notify(data: dict):
    return {"status": "SENT", "recipient": data.get("recipient", "admin")}
