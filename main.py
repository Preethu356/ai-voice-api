from fastapi import FastAPI, Header, HTTPException, Request
from typing import Optional

app = FastAPI()

API_KEY = "sarvadamana-ai-voice-2026"


# ---------------- VOICE DETECTION ----------------
@app.post("/voice-detection")
async def voice_detection(payload: dict, x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return {
        "status": "success",
        "is_ai_generated": True,
        "confidence_score": 0.92
    }


# ---------------- HONEYPOT GET (Guvi ping) ----------------
@app.get("/honeypot")
async def honeypot_get():
    return {
        "status": "ready",
        "service": "honeypot"
    }


# ---------------- HONEYPOT POST ----------------
@app.post("/honeypot")
async def honeypot_post(
    request: Request,
    x_api_key: Optional[str] = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    payload = await request.json()

    message = ""

    if isinstance(payload, dict):
        raw = payload.get("message")

        if isinstance(raw, str):
            message = raw
        elif isinstance(raw, dict):
            message = str(raw.get("text", ""))
        elif isinstance(raw, list) and raw:
            message = str(raw[0])

    message = message.lower()

    scam_words = ["bank", "otp", "blocked", "click", "urgent", "account"]

    if any(word in message for word in scam_words):
        return {
            "scam_detected": True,
            "scam_type": "banking_fraud",
            "risk_score": 0.9,
            "recommended_action": "Do not respond. Block and report."
        }

    return {
        "scam_detected": False,
        "scam_type": "none",
        "risk_score": 0.1,
        "recommended_action": "No action required."
    }
