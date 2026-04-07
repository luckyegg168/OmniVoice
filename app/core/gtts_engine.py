"""Google TTS (gTTS) engine implementation."""

from __future__ import annotations

import uuid
from pathlib import Path

from app.config import OUTPUT_DIR
from app.core.tts_engine import TTSEngine
from app.models.tts_request import TTSRequest, TTSResult, VoiceInfo

# gTTS supported languages (subset — gTTS auto-detects more)
_GTTS_LANGUAGES = {
    "zh-TW": "Chinese (Traditional)",
    "zh-CN": "Chinese (Simplified)",
    "en": "English",
    "ja": "Japanese",
    "ko": "Korean",
    "fr": "French",
    "de": "German",
    "es": "Spanish",
    "pt": "Portuguese",
    "ru": "Russian",
    "ar": "Arabic",
    "hi": "Hindi",
    "it": "Italian",
    "nl": "Dutch",
    "pl": "Polish",
    "th": "Thai",
    "vi": "Vietnamese",
    "id": "Indonesian",
    "tr": "Turkish",
    "sv": "Swedish",
}


class GTTSEngine(TTSEngine):
    """Google Text-to-Speech engine using gTTS library."""

    def name(self) -> str:
        return "Google TTS"

    def engine_id(self) -> str:
        return "gtts"

    def is_available(self) -> bool:
        try:
            from gtts import gTTS  # noqa: F401

            return True
        except ImportError:
            return False

    async def list_voices(self, language: str | None = None) -> list[VoiceInfo]:
        voices = [
            VoiceInfo(
                id=f"gtts-{lang_code}",
                name=f"Google - {lang_name}",
                language=lang_code,
                gender="",
                engine="gtts",
            )
            for lang_code, lang_name in _GTTS_LANGUAGES.items()
        ]
        if language:
            lang_lower = language.lower()
            voices = [v for v in voices if v.language.lower().startswith(lang_lower)]
        return voices

    async def synthesize(self, request: TTSRequest) -> TTSResult:
        from nicegui import run

        result = await run.io_bound(self._synthesize_sync, request)
        return result

    def _synthesize_sync(self, request: TTSRequest) -> TTSResult:
        from gtts import gTTS

        lang = request.language.split("-")[0] if "-" in request.language else request.language
        tld = "com.tw" if request.language.startswith("zh-TW") else "com"

        tts = gTTS(text=request.text, lang=lang, tld=tld, slow=(request.speed < 0.75))

        filename = f"gtts_{uuid.uuid4().hex[:8]}.mp3"
        output_path = Path(request.output_path) if request.output_path else OUTPUT_DIR / filename
        tts.save(str(output_path))

        duration = _estimate_duration(output_path)

        return TTSResult(
            audio_path=str(output_path),
            duration_seconds=duration,
            sample_rate=24000,
            engine="gtts",
            text=request.text,
            voice=request.voice,
        )


def _estimate_duration(path: Path) -> float:
    """Estimate audio duration from MP3 file."""
    try:
        from mutagen.mp3 import MP3

        audio = MP3(str(path))
        return audio.info.length if audio.info else 0.0
    except Exception:
        return 0.0
