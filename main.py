from fastapi import FastAPI
from pydantic import BaseModel, Field
from pydantic import ConfigDict

app = FastAPI()


class VoiceRequest(BaseModel):
    language: str = "en"

    audio_format: str = Field(
        ...,
        validation_alias="audioFormat"
    )

    audio_base64: str = Field(
        ...,
        validation_alias="audioBase64"
    )

    model_config = ConfigDict(
        populate_by_name=True
    )


@app.post("/voice-detection")
async def voice_detection(payload: VoiceRequest):
    return {
        "is_ai_generated": True,
        "confidence_score": 0.92,
        "language": payload.language,
        "audio_format": payload.audio_format,
        "status": "success"
    }
