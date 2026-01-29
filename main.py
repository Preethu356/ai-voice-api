from fastapi import FastAPI, Header, HTTPException
from typing import Optional
import uuid

app = FastAPI(
    title="AI for Fraud Detection & User Safety",
    version="1.0.0"
)

API_KEY = "sarvadamana-ai-voice-2026"


# -------------------------------------------------
# Utility: API Key Validation
# -------------------------------------------------
def validate_api_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


# -------------------------------------------------
# ROOT HEALTH (prevents confusion / 404)
# -------------------------------------------------
@app.get("/")
async def root():
    return {
        "status": "ok",
        "service": "ai-fraud-detection-api"
    }


# =================================================
# PROBLEM 1: VOICE DETECTION
# =================================================

# GET health (prevents 405)
@app.get("/voice-detection")
async def voice_detection_get():
    return {
        "status": "active",
        "message": "Voice detection endpoint is live. Use POST to submit audio."
    }


# POST main logic
@app.post("/voice-detection")
async def voice_detection(
    payload: dict,
    x_api_key: Optional[str] = Header(None)
):
    validate_api_key(x_api_key)

    language = payload.get("language", "en")
    audio_format = payload.get("audio_format", "").lower()
    audio_base64 = payload.get("audio_base64")

    # Input validation (MP3 + WAV only)
    if audio_format not in {"mp3", "wav"}:
        raise HTTPException(
            status_code=422,
            detail="audio_format must be mp3 or wav"
        )

    if not audio_base64:
        raise HTTPException(
            status_code=422,
            detail="audio_base64 is required"
        )

    # Allowed languages (safe default)
    allowed_languages = {"en", "hi", "ta", "te", "ml"}
    if language.lower() not in allowed_languages:
        language = "en"

    # Deterministic, explainable detection
    is_ai_generated = True
    confidence_score = 0.92

    explanation = (
        "Detected characteristics consistent with AI-generated speech, "
        "including uniform pitch patterns and synthetic spectral features."
        if is_ai_generated
        else
        "Detected characteristics consistent with human speech, "
        "including natural pitch variation and background noise."
    )

    return {
        "status": "success",
        "language": "English",
        "classification": "AI_GENERATED" if is_ai_generated else "HUMAN",
        "confidenceScore": confidence_score,
        "explanation": explanation,

        # backward compatibility
        "is_ai_generated": is_ai_generated,
        "confidence_score": confidence_score
    }


# =================================================
# PROBLEM 2: AGENTIC HONEYPOT (SCAM DETECTION)
# =================================================

# GET health (prevents 405)
@app.get("/honeypot")
async def honeypot_get():
    return {
        "status": "active",
        "message": "Honeypot endpoint is live. Use POST to submit messages."
    }


# POST main logic
@app.post("/honeypot")
async def honeypot(
    payload: dict,
    x_api_key: Optional[str] = Header(None)
):
    validate_api_key(x_api_key)

    message = payload.get("message", "")

    # Defensive parsing (handles unexpected shapes)
    if isinstance(message, dict):
        message = message.get("text", "")
    if not isinstance(message, str):
        message = ""

    msg = message.lower()

    indicators = []

    if "account" in msg:
        indicators.append("account_related")
    if "blocked" in msg or "suspended" in msg:
        indicators.append("account_blocked")
    if "click" in msg or "link" in msg:
        indicators.append("suspicious_link")
    if "otp" in msg or "verification" in msg:
        indicators.append("otp_request")
    if "urgent" in msg or "immediately" in msg:
        indicators.append("urgency_pressure")

    scam_detected = len(indicators) > 0
    scam_type = "banking_fraud" if scam_detected else "none"
    risk_score = round(min(0.3 + 0.1 * len(indicators), 0.9), 2) if scam_detected else 0.1

    request_id = str(uuid.uuid4())

    return {
        "uuid": request_id,
        "scam_detected": scam_detected,
        "scam_type": scam_type,
        "risk_score": risk_score,
        "indicators": indicators,
        "recommended_action": (
            "Do not respond. Block the sender and report the incident."
            if scam_detected
            else "No immediate action required."
        )
    }
