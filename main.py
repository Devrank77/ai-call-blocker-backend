from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AI Call Guardian")

class CallRequest(BaseModel):
    phone_number: str
    transcript: str | None = None

@app.get("/")
def home():
    return {"status": "AI Call Guardian backend running"}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/classify")
def classify_call(call: CallRequest):
    spam_keywords = [
        "warranty",
        "insurance",
        "car accident",
        "credit card",
        "press one",
        "limited time"
    ]

    text = (call.transcript or "").lower()

    for word in spam_keywords:
        if word in text:
            return {
                "phone_number": call.phone_number,
                "classification": "spam",
                "reason": f"Detected keyword: {word}"
            }

    return {
        "phone_number": call.phone_number,
        "classification": "likely_safe",
        "reason": "No spam indicators detected"
    }
