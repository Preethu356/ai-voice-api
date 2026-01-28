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



# ---------- GET Honeypot (Guvi requires this) ----------
@app.get("/honeypot")
def honeypot_get(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return {
        "status": "ready",
        "message": "Honeypot endpoint reachable"
    }


# ---------- POST Honeypot ----------
@app.post("/honeypot")
def honeypot_post(
    payload: HoneypotRequest,
    x_api_key: Optional[str] = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    msg = payload.message.lower()

    if any(word in msg for word in ["bank", "otp", "blocked", "urgent", "click", "account"]):
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
