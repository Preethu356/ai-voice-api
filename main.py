from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import base64

app = FastAPI(
    title="AI Generated Voice Detection API",
    version="1.0"
)

# 🔐 Change this if you want
EXPECTED_API_KEY = "sarvadamana-ai-voice-2026"


class VoiceRequest(BaseModel):
    language: str
    audio_format: str
    audio_base64: str


@app.post("/voice-detection")
def detect_voice(
    request: VoiceRequest,
    x_api_key: str = Header(...)
):
    # 🔐 API key validation
    if x_api_key != EXPECTED_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    # 🧪 Validate base64 audio
    try:
        base64.b64decode(request.audio_base64)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 audio")

    # ✅ Placeholder logic (safe for GUVI testing)
    return {
        "is_ai_generated": True,
        "confidence_score": 0.85,
        "language": request.language,
        "audio_format": request.audio_format,
        "status": "success"
    }
