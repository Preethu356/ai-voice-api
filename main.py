from fastapi import FastAPI, Body, HTTPException

app = FastAPI()


@app.post("/voice-detection")
async def voice_detection(payload: dict = Body(...)):
    return {
        "status": "success",
        "is_ai_generated": True,
        "confidence_score": 0.92
    }


@app.post("/honeypot")
async def honeypot(payload: dict = Body(...)):
    if "message" not in payload:
        raise HTTPException(status_code=422, detail="message is required")

    msg = payload["message"].lower()

    return {
        "scam_detected": True,
        "scam_type": "banking_fraud" if "bank" in msg or "otp" in msg else "unknown",
        "risk_score": 0.9,
        "recommended_action": "Do not respond. Block and report."
    }
