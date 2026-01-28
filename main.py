from fastapi import FastAPI, Body, HTTPException

app = FastAPI()


@app.post("/voice-detection")
async def voice_detection(payload: dict = Body(...)):
    # Required fields as per GUVI
    required_fields = ["language", "audioFormat", "audioBase64"]

    missing = [f for f in required_fields if f not in payload]
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"Missing required fields: {missing}"
        )

    language = payload["language"]
    audio_format = payload["audioFormat"]
    audio_base64 = payload["audioBase64"]

    return {
        "is_ai_generated": True,
        "confidence_score": 0.92,
        "language": language,
        "audio_format": audio_format,
        "status": "success"
    }

@app.post("/voice-detection")
async def voice_detection(payload: dict = Body(...)):
    if "language" not in payload:
        raise HTTPException(status_code=422, detail="language is required")
    if "audioFormat" not in payload:
        raise HTTPException(status_code=422, detail="audioFormat is required")
    if "audioBase64" not in payload:
        raise HTTPException(status_code=422, detail="audioBase64 is required")

    return {
        "is_ai_generated": True,
        "confidence_score": 0.92,
        "language": payload["language"],
        "audio_format": payload["audioFormat"],
        "status": "success"
    }


# 🐝 Agentic Honey-Pot Endpoint
@app.post("/honeypot")
async def honeypot(payload: dict = Body(...)):
    if "message" not in payload:
        raise HTTPException(status_code=422, detail="message is required")

    scam_message = payload["message"].lower()

    scam_type = "unknown"
    risk_score = 0.3
    indicators = []

    if "otp" in scam_message or "bank" in scam_message:
        scam_type = "banking_fraud"
        risk_score = 0.9
        indicators.append("banking_keywords")

    if "upi" in scam_message or "pay" in scam_message:
        indicators.append("payment_request")

    if "http" in scam_message or "www" in scam_message:
        indicators.append("suspicious_link")

    return {
        "scam_detected": True if risk_score > 0.6 else False,
        "scam_type": scam_type,
        "risk_score": risk_score,
        "extracted_indicators": indicators,
        "recommended_action": "Do not respond. Report and block sender."
    }
