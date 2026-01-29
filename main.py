from fastapi import FastAPI, Header, HTTPException, Request
from typing import Optional

app = FastAPI()

API_KEY = "sarvadamana-ai-voice-2026"


# ---------------- VOICE DETECTION ----------------
@app.post("/voice-detection")
async def voice_detection(
    payload: dict,
    x_api_key: Optional[str] = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    is_ai_generated = True
    confidence = 0.92
    language = payload.get("language", "English")

    allowed_languages = {"english", "hindi", "tamil", "telugu", "malayalam"}
    if language.lower() not in allowed_languages:
        language = "English"

    return {
        "status": "success",
        "language": language.capitalize(),
        "classification": "AI_GENERATED" if is_ai_generated else "HUMAN",
        "confidenceScore": confidence,
        "explanation": _voice_explanation(is_ai_generated),

        # backward compatibility
        "is_ai_generated": is_ai_generated,
        "confidence_score": confidence
    }


API_KEY = "sarvadamana-ai-voice-2026"


def _extract_message(payload: dict) -> str:
    raw = payload.get("message", "")

    if isinstance(raw, str):
        return raw.lower()

    if isinstance(raw, dict):
        return str(raw.get("text", "")).lower()

    if isinstance(raw, list) and raw:
        return str(raw[0]).lower()

    return ""


def _evaluate_risk(message: str) -> tuple[bool, float, str]:
    score = 0.2
    scam_type = "none"

    if any(w in message for w in ("bank", "account", "otp", "blocked")):
        score += 0.4
        scam_type = "banking_fraud"

    if any(w in message for w in ("upi", "pay", "transfer")):
        score += 0.2
        scam_type = "payment_scam"

    if any(w in message for w in ("urgent", "verify", "immediately")):
        score += 0.1

    if any(w in message for w in ("http", "www", "click")):
        score += 0.1

    score = min(round(score, 2), 0.95)
    return score > 0.5, score, scam_type


# -----------------------------
# GET Honeypot (GUVI ping)
# -----------------------------
@app.get("/honeypot")
async def honeypot_get():
    return {
        "status": "ready",
        "service": "honeypot"
    }


# -----------------------------
# POST Honeypot (Intelligence)
# -----------------------------
@app.post("/honeypot")
async def honeypot_post(
    request: Request,
    x_api_key: Optional[str] = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    try:
        payload = await request.json()
    except Exception:
        payload = {}

    message = _extract_message(payload)
    scam_detected, risk_score, scam_type = _evaluate_risk(message)

    return {
        "scam_detected": scam_detected,
        "scam_type": scam_type,
        "risk_score": risk_score,
        "recommended_action": (
            "Do not respond. Block the sender and report the incident."
            if scam_detected
            else
            "No immediate threat detected. Remain cautious."
        )
    }

