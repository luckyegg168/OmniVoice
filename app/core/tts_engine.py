"""Abstract TTS engine interface."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.models.tts_request import TTSRequest, TTSResult, VoiceInfo


class TTSEngine(ABC):
    """Abstract base for all TTS engines."""

    @abstractmethod
    async def synthesize(self, request: TTSRequest) -> TTSResult:
        """Synthesize text to speech audio."""

    @abstractmethod
    async def list_voices(self, language: str | None = None) -> list[VoiceInfo]:
        """List available voices, optionally filtered by language."""

    @abstractmethod
    def name(self) -> str:
        """Engine display name."""

    @abstractmethod
    def engine_id(self) -> str:
        """Engine identifier string."""

    def is_available(self) -> bool:
        """Check if engine is available (dependencies installed)."""
        return True
