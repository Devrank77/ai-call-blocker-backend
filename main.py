from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI()

# ---- Request schema (what the API expects) ----
class CallRequest(BaseModel):
    phone_number: str
    text: str

# ---- Spam rules ----
SPAM_KEYWORDS = [
    "extended warranty",
    "press 1",
    "act now",
    "final notice",
    "limited time",
    "free offer",
    "congratulations",
    "urgent",
    "win money"
]

# ---- Core logic ----
def classify_text(text: str):
    text_lower = text.lower()
    hits = [kw for kw in SPAM_KEYWORDS if kw in text_lower]

    if len(hits) >= 2:
        return "spam", hits
    elif len(hits) == 1:
        return "likely_spam", hits
    else:
        return "likely_safe", []

# ---- Routes ----
@app.get("/")
def home():
    return {"status": "AI Call Blocker backend running"}

@app.post("/classify")
def classify_call(data: CallRequest):
    classification, hits = classify_text(data.text)

    return {
        "phone_number": data.phone_number,
        "classification": classification,
        "matched_keywords": hits,
        "confidence": round(min(len(hits) * 0.4 + 0.2, 0.95), 2)
    }

@app.get("/health")
def health():
    return {"ok": True}
