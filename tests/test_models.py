"""Tests for Pydantic data models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from app.models.history import HistoryRecord
from app.models.tts_request import TTSRequest, TTSResult, VoiceInfo


class TestTTSRequest:
    def test_create_with_defaults(self):
        req = TTSRequest(text="hello world")
        assert req.text == "hello world"
        assert req.engine == "edge-tts"
        assert req.speed == 1.0
        assert req.output_format == "mp3"

    def test_create_with_custom(self):
        req = TTSRequest(
            text="test",
            voice="en-US-AriaNeural",
            language="en",
            engine="edge-tts",
            speed=1.5,
            pitch=10.0,
            volume=0.8,
            output_format="wav",
        )
        assert req.voice == "en-US-AriaNeural"
        assert req.speed == 1.5

    def test_immutable(self):
        req = TTSRequest(text="hello")
        with pytest.raises(ValidationError):
            req.text = "changed"  # type: ignore[misc]

    def test_empty_text_rejected(self):
        with pytest.raises(ValidationError):
            TTSRequest(text="")

    def test_speed_bounds(self):
        with pytest.raises(ValidationError):
            TTSRequest(text="test", speed=10.0)

    def test_ref_audio_field(self):
        req = TTSRequest(text="test", ref_audio="/path/to/audio.wav")
        assert req.ref_audio == "/path/to/audio.wav"

    def test_ssml_field(self):
        req = TTSRequest(text="<speak>test</speak>", ssml=True)
        assert req.ssml is True

    def test_output_path_field(self):
        req = TTSRequest(text="test", output_path="/tmp/output.mp3")
        assert req.output_path == "/tmp/output.mp3"


class TestTTSResult:
    def test_create(self):
        result = TTSResult(
            audio_path="/path/to/file.mp3",
            duration_seconds=5.5,
            engine="edge-tts",
        )
        assert result.audio_path == "/path/to/file.mp3"
        assert result.duration_seconds == 5.5

    def test_defaults(self):
        result = TTSResult(audio_path="/path/test.mp3")
        assert result.duration_seconds == 0.0
        assert result.sample_rate == 24000

    def test_immutable(self):
        result = TTSResult(audio_path="/path/test.mp3")
        with pytest.raises(ValidationError):
            result.audio_path = "changed"  # type: ignore[misc]


class TestVoiceInfo:
    def test_create(self):
        voice = VoiceInfo(
            id="zh-TW-HsiaoChenNeural",
            name="Hsiao Chen",
            language="zh-TW",
            gender="Female",
            engine="edge-tts",
        )
        assert voice.id == "zh-TW-HsiaoChenNeural"
        assert voice.gender == "Female"

    def test_immutable(self):
        voice = VoiceInfo(id="test", name="Test", language="en")
        with pytest.raises(ValidationError):
            voice.name = "changed"  # type: ignore[misc]


class TestHistoryRecord:
    def test_create_with_defaults(self):
        record = HistoryRecord(
            text="hello",
            engine="edge-tts",
            voice="zh-TW-HsiaoChenNeural",
            language="zh-TW",
        )
        assert record.text == "hello"
        assert record.id  # auto-generated
        assert record.timestamp  # auto-generated
        assert record.is_favorite is False

    def test_auto_generated_id(self):
        r1 = HistoryRecord(text="a", engine="e", voice="v", language="zh")
        r2 = HistoryRecord(text="b", engine="e", voice="v", language="zh")
        assert r1.id != r2.id

    def test_immutable(self):
        record = HistoryRecord(text="hi", engine="e", voice="v", language="zh")
        with pytest.raises(ValidationError):
            record.text = "changed"  # type: ignore[misc]
