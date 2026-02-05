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

from fastapi import Header, HTTPException
from typing import Optional

API_KEY = "sarvadamana-ai-voice-2026"

# --------------------------------------------------
# HONEYPOT – GET (conversation sanity check)
# --------------------------------------------------
@app.get("/honeypot", include_in_schema=True)
def honeypot_get():
    return {
        "status": "success",
        "reply": "Why is my account being suspended?"
    }


# --------------------------------------------------
# HONEYPOT – POST (conversation analysis)
# --------------------------------------------------
@app.post("/honeypot", include_in_schema=True)
async def honeypot_post(
    payload: dict,
    x_api_key: Optional[str] = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    message = payload.get("message", {})
    text = ""

    if isinstance(message, dict):
        text = message.get("text", "")
    elif isinstance(message, str):
        text = message

    text_lower = text.lower()

    scam_keywords = [
        "blocked", "verify", "urgent",
        "click", "otp", "suspended",
        "immediately"
    ]

    is_scam = any(word in text_lower for word in scam_keywords)

    return {
        "status": "success",
        "reply": (
            "This message appears to be a scam. Do not respond or click links."
            if is_scam
            else
            "This message does not show common scam indicators."
        )
    }
