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
