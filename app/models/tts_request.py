"""TTS request and result models."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TTSRequest(BaseModel):
    """Immutable TTS synthesis request."""

    text: str = Field(..., min_length=1, max_length=10000)
    voice: str = Field(default="zh-TW-HsiaoChenNeural")
    language: str = Field(default="zh-TW")
    engine: str = Field(default="edge-tts")
    speed: float = Field(default=1.0, ge=0.25, le=4.0)
    pitch: float = Field(default=0.0, ge=-50.0, le=50.0)
    volume: float = Field(default=1.0, ge=0.0, le=2.0)
    output_format: str = Field(default="mp3")
    output_path: str = Field(default="")
    ref_audio: str = Field(default="")
    ssml: bool = Field(default=False)

    model_config = {"frozen": True}


class TTSResult(BaseModel):
    """Immutable TTS synthesis result."""

    audio_path: str
    duration_seconds: float = 0.0
    sample_rate: int = 24000
    engine: str = ""
    text: str = ""
    voice: str = ""

    model_config = {"frozen": True}


class VoiceInfo(BaseModel):
    """Voice metadata."""

    id: str
    name: str
    language: str
    gender: str = ""
    engine: str = ""

    model_config = {"frozen": True}
