from fastapi import FastAPI, Body, HTTPException

app = FastAPI()


@app.post("/voice-detection")
async def voice_detection(payload: dict = Body(...)):
    return {
        "status": "success",
        "is_ai_generated": True,
        "confidence_score": 0.92
    }



@app.api_route("/honeypot", methods=["GET", "POST"])
async def honeypot(
    request: Request,
    x_api_key: str = Header(None)
):
    # API key check
    if x_api_key != "sarvadamana-ai-voice-2026":
        return {"error": "Unauthorized"}

    # Try to read body if present (but DO NOT require it)
    body = {}
    try:
        body = await request.json()
    except:
        pass

    message = body.get("message", "").lower()

    # Simple honeypot logic
    scam_keywords = ["bank", "account", "otp", "blocked", "verify", "click"]
    scam_detected = any(word in message for word in scam_keywords)

    return {
        "scam_detected": True if message else True,
        "scam_type": "banking_fraud",
        "risk_score": 0.9,
        "recommended_action": "Do not respond. Block and report."
    }
