from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"status": "AI Call Blocker backend is live"}

@app.get("/health")
def health():
    return {"ok": True}
