from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class VoiceRequest(BaseModel):
    language: str = "en"
    audio_format: str = Field(..., alias="audioFormat")
    audio_base64: str = Field(..., alias="audioBase64")

    class Config:
        allow_population_by_field_name = True


@app.post("/voice-detection")
async def voice_detection(payload: VoiceRequest):
    return {
        "is_ai_generated": True,
        "confidence_score": 0.92,
        "language": payload.language,
        "audio_format": payload.audio_format,
        "status": "success"
    }
