"""Application configuration."""

from __future__ import annotations

import os
from pathlib import Path

from pydantic import BaseModel, Field


class AppSettings(BaseModel):
    """Application settings with defaults."""

    locale: str = Field(default="zh-TW", description="UI locale")
    theme: str = Field(default="dark", description="dark or light")
    default_engine: str = Field(default="edge-tts", description="Default TTS engine")
    default_voice: str = Field(
        default="zh-TW-HsiaoChenNeural", description="Default voice ID"
    )
    output_dir: str = Field(default="./output", description="Output directory for audio files")
    max_history: int = Field(default=500, description="Max history records")
    max_text_length: int = Field(default=10000, description="Max input text length")
    max_upload_mb: int = Field(default=10, description="Max upload file size in MB")

    model_config = {"frozen": True}


# Singleton-like default settings
APP_VERSION = "1.0.0"
APP_NAME = "OmniVoice TTS"
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"
STORAGE_DIR = BASE_DIR / "storage"

# Ensure directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# Port config from env
APP_PORT = int(os.environ.get("OMNIVOICE_PORT", "8080"))
APP_HOST = os.environ.get("OMNIVOICE_HOST", "0.0.0.0")
