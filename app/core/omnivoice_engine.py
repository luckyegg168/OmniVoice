"""OmniVoice engine implementation (optional — requires omnivoice + torch)."""

from __future__ import annotations

import uuid

from app.config import OUTPUT_DIR
from app.core.tts_engine import TTSEngine
from app.models.tts_request import TTSRequest, TTSResult, VoiceInfo


class OmniVoiceEngine(TTSEngine):
    """k2-fsa/OmniVoice — 600+ language zero-shot TTS."""

    _model = None

    def name(self) -> str:
        return "OmniVoice"

    def engine_id(self) -> str:
        return "omnivoice"

    def is_available(self) -> bool:
        try:
            import omnivoice  # noqa: F401
            import torch  # noqa: F401

            return True
        except ImportError:
            return False

    def _load_model(self):
        if OmniVoiceEngine._model is None:
            import torch
            from omnivoice import OmniVoice

            device = "cuda:0" if torch.cuda.is_available() else "cpu"
            dtype = torch.float16 if torch.cuda.is_available() else torch.float32
            OmniVoiceEngine._model = OmniVoice.from_pretrained(
                "k2-fsa/OmniVoice",
                device_map=device,
                dtype=dtype,
            )

    async def list_voices(self, language: str | None = None) -> list[VoiceInfo]:
        return [
            VoiceInfo(
                id="omnivoice-auto",
                name="OmniVoice Auto",
                language=language or "multilingual",
                gender="",
                engine="omnivoice",
            ),
            VoiceInfo(
                id="omnivoice-design",
                name="OmniVoice Voice Design",
                language=language or "multilingual",
                gender="",
                engine="omnivoice",
            ),
        ]

    async def synthesize(self, request: TTSRequest) -> TTSResult:
        from nicegui import run

        result = await run.io_bound(self._synthesize_sync, request)
        return result

    def _synthesize_sync(self, request: TTSRequest) -> TTSResult:
        import torchaudio

        self._load_model()
        model = OmniVoiceEngine._model

        kwargs: dict = {"text": request.text, "speed": request.speed}

        audio = model.generate(**kwargs)

        from pathlib import Path as _Path

        filename = f"omni_{uuid.uuid4().hex[:8]}.wav"
        output_path = _Path(request.output_path) if request.output_path else OUTPUT_DIR / filename
        torchaudio.save(str(output_path), audio[0], 24000)

        duration = audio[0].shape[-1] / 24000.0

        return TTSResult(
            audio_path=str(output_path),
            duration_seconds=duration,
            sample_rate=24000,
            engine="omnivoice",
            text=request.text,
            voice=request.voice,
        )
