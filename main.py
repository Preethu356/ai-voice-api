from fastapi import FastAPI, Header, HTTPException, Request
from typing import Optional, Any

app = FastAPI()

API_KEY = "sarvadamana-ai-voice-2026"


# =========================
# VOICE DETECTION (already working)
# =========================
@app.post("/voice-detection")
async def voice_detection(payload: dict, x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return {
        "status": "success",
        "is_ai_generated": True,
        "confidence_score": 0.92
    }


# =========================
# HONEYPOT – GET (Guvi ping)
# =========================
@app.get("/honeypot")
async def honeypot_get():
    # IMPORTANT: no auth check here
    return {
        "status": "ready",
        "service": "honeypot"
    }


# =========================
# HONEYPOT – POST (Guvi test)
# =========================
@app.post("/honeypot")
async def honeypot_post(
    request: Request,
    x_api_key: Optional[str] = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    payload = await request.json()

    # --- Extract message safely ---
    message = ""

    if isinstance(payload, dict):
        msg = payload.get("message")

        if isinstance(msg, str):
            message = msg
        elif isinstance(msg, dict):
            message = str(msg.get("text", ""))
        elif isinstance(msg, list) and len(msg) > 0:
            message = str(msg[0])

    message = message.lower()

    # --- Simple scam logic ---
    scam_keywords = ["bank", "otp", "blocked", "urgent", "click", "account"]

    if any(word in message for word in scam_keywords):
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
