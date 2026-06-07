"""Edge-TTS engine implementation."""

from __future__ import annotations

import uuid
from pathlib import Path

from app.config import OUTPUT_DIR
from app.core.tts_engine import TTSEngine
from app.models.tts_request import TTSRequest, TTSResult, VoiceInfo


class EdgeTTSEngine(TTSEngine):
    """Microsoft Edge TTS engine using edge-tts library."""

    _voices_cache: list[VoiceInfo] | None = None

    def name(self) -> str:
        return "Edge TTS"

    def engine_id(self) -> str:
        return "edge-tts"

    def is_available(self) -> bool:
        try:
            import edge_tts  # noqa: F401

            return True
        except ImportError:
            return False

    async def list_voices(self, language: str | None = None) -> list[VoiceInfo]:
        import edge_tts

        if EdgeTTSEngine._voices_cache is None:
            raw_voices = await edge_tts.list_voices()
            EdgeTTSEngine._voices_cache = [
                VoiceInfo(
                    id=v["ShortName"],
                    name=v["FriendlyName"],
                    language=v["Locale"],
                    gender=v.get("Gender", ""),
                    engine="edge-tts",
                )
                for v in raw_voices
            ]

        voices = EdgeTTSEngine._voices_cache
        if language:
            lang_lower = language.lower()
            voices = [v for v in voices if v.language.lower().startswith(lang_lower)]
        return voices

    async def synthesize(self, request: TTSRequest) -> TTSResult:
        import edge_tts

        # Build rate/pitch/volume strings
        rate_str = _format_rate(request.speed)
        pitch_str = _format_pitch(request.pitch)
        volume_str = _format_volume(request.volume)

        communicate = edge_tts.Communicate(
            text=request.text,
            voice=request.voice,
            rate=rate_str,
            pitch=pitch_str,
            volume=volume_str,
        )

        filename = f"edge_{uuid.uuid4().hex[:8]}.mp3"
        output_path = Path(request.output_path) if request.output_path else OUTPUT_DIR / filename
        await communicate.save(str(output_path))

        duration = _estimate_duration(output_path)

        return TTSResult(
            audio_path=str(output_path),
            duration_seconds=duration,
            sample_rate=24000,
            engine="edge-tts",
            text=request.text,
            voice=request.voice,
        )


def _format_rate(speed: float) -> str:
    """Convert speed multiplier to Edge-TTS rate string."""
    pct = int((speed - 1.0) * 100)
    return f"{pct:+d}%" if pct != 0 else "+0%"


def _format_pitch(pitch: float) -> str:
    """Convert pitch multiplier (0.5–2.0, default 1.0) to Edge-TTS pitch string."""
    hz = int((pitch - 1.0) * 100)
    return f"{hz:+d}Hz"


def _format_volume(volume: float) -> str:
    """Convert volume multiplier to Edge-TTS volume string."""
    pct = int((volume - 1.0) * 100)
    return f"{pct:+d}%" if pct != 0 else "+0%"


def _estimate_duration(path: Path) -> float:
    """Estimate audio duration from file."""
    try:
        from mutagen.mp3 import MP3

        audio = MP3(str(path))
        return audio.info.length if audio.info else 0.0
    except Exception:
        return 0.0
