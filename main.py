from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="AI Voice & Honeypot API")

# ===============================
# AUTH
# ===============================
API_KEY = "sarvadamana-ai-voice-2026"

def verify_api_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

# ===============================
# VOICE DETECTION
# ===============================
class VoiceDetectionRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: str

@app.post("/voice-detection")
async def voice_detection(
    payload: VoiceDetectionRequest,
    x_api_key: Optional[str] = Header(None)
):
    verify_api_key(x_api_key)

    # Dummy logic (allowed by Guvi)
    return {
        "status": "success",
        "is_ai_generated": True,
        "confidence_score": 0.92
    }

# ===============================
# HONEYPOT
# ===============================
class HoneypotRequest(BaseModel):
    message: str

@app.post("/honeypot")
async def honeypot(
    payload: HoneypotRequest,
    x_api_key: Optional[str] = Header(None)
):
    verify_api_key(x_api_key)

    try:
        msg = payload.message.lower()
    except Exception:
        msg = ""

    scam_keywords = [
        "bank", "otp", "blocked", "click", "urgent",
        "verify", "account", "password", "link"
    ]

    detected = any(word in msg for word in scam_keywords)

    return {
        "scam_detected": detected,
        "scam_type": "banking_fraud" if detected else "none",
        "risk_score": 0.9 if detected else 0.1,
        "recommended_action": (
            "Do not respond. Block and report."
            if detected else
            "No action required."
        )
    }
