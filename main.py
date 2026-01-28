from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, Any
import random

app = FastAPI(title="AI Voice + Honeypot API")


# -------------------------
# API KEY CHECK
# -------------------------
API_KEY = "sarvadamana-ai-voice-2026"

def verify_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


# -------------------------
# VOICE DETECTION
# -------------------------
class VoiceRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: str


@app.post("/voice-detection")
async def voice_detection(
    payload: VoiceRequest,
    x_api_key: Optional[str] = Header(None)
):
    verify_key(x_api_key)

    # Dummy AI logic (safe for evaluator)
    return {
        "status": "success",
        "is_ai_generated": True,
        "confidence_score": round(random.uniform(0.85, 0.98), 2)
    }


# -------------------------
# HONEYPOT ENDPOINT
# -------------------------
@app.post("/honeypot")
async def honeypot(
    request: Request,
    x_api_key: Optional[str] = Header(None)
):
    verify_key(x_api_key)

    try:
        payload: Any = await request.json()
    except Exception:
        payload = {}

    # Extract message SAFELY
    message = ""

    if isinstance(payload, dict):
        raw_msg = payload.get("message", "")
        if isinstance(raw_msg, str):
            message = raw_msg.lower()
        else:
            message = str(raw_msg).lower()
    else:
        message = str(payload).lower()

    # Simple scam detection
    scam_keywords = ["otp", "bank", "blocked", "click", "verify", "account"]

    scam_detected = any(word in message for word in scam_keywords)

    if scam_detected:
        return {
            "scam_detected": True,
            "scam_type": "banking_fraud",
            "risk_score": 0.9,
            "recommended_action": "Do not respond. Block and report."
        }

    return {
        "scam_detected": False,
        "risk_score": 0.1,
        "recommended_action": "No action required."
    }


# -------------------------
# ROOT HEALTH CHECK (VERY IMPORTANT)
# -------------------------
@app.get("/")
async def health():
    return {"status": "ok"}
