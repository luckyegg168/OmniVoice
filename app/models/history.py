"""History record model."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, Field


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_id() -> str:
    return uuid.uuid4().hex[:12]


class HistoryRecord(BaseModel):
    """Immutable history record."""

    id: str = Field(default_factory=_new_id)
    timestamp: str = Field(default_factory=_utc_now_iso)
    text: str = ""
    engine: str = ""
    voice: str = ""
    language: str = ""
    speed: float = 1.0
    pitch: float = 0.0
    volume: float = 1.0
    audio_path: str = ""
    duration_seconds: float = 0.0
    is_favorite: bool = False

    model_config = {"frozen": True}
