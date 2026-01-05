from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class CallRequest(BaseModel):
    phone_number: str
    text: str

@app.get("/")
def home():
    return {"status": "AI Call Blocker backend"}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/classify")
def classify_call(data: CallRequest):
    text = data.text.lower()

    spam_keywords = [
        "final notice",
        "extended warranty",
        "act now",
        "urgent",
        "limited time",
        "press 1",
        "verify your account"
    ]

    if any(word in text for word in spam_keywords):
        classification = "likely_spam"
        reason = "Common spam indicators detected"
    else:
        classification = "likely_safe"
        reason = "No spam indicators detected"

    return {
        "phone_number": data.phone_number,
        "classification": classification,
        "reason": reason
    }
