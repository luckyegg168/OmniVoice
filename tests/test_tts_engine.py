"""Tests for TTS engine interface and EdgeTTS engine."""

from __future__ import annotations

from app.core.edge_tts_engine import EdgeTTSEngine, _format_pitch, _format_rate, _format_volume
from app.core.gtts_engine import GTTSEngine
from app.core.omnivoice_engine import OmniVoiceEngine


class TestEdgeTTSEngine:
    def test_name(self):
        eng = EdgeTTSEngine()
        assert eng.name() == "Edge TTS"

    def test_engine_id(self):
        eng = EdgeTTSEngine()
        assert eng.engine_id() == "edge-tts"

    def test_is_available(self):
        eng = EdgeTTSEngine()
        # Should be True if edge-tts is installed, otherwise False
        result = eng.is_available()
        assert isinstance(result, bool)


class TestGTTSEngine:
    def test_name(self):
        eng = GTTSEngine()
        assert eng.name() == "Google TTS"

    def test_engine_id(self):
        eng = GTTSEngine()
        assert eng.engine_id() == "gtts"

    def test_is_available(self):
        eng = GTTSEngine()
        result = eng.is_available()
        assert isinstance(result, bool)


class TestOmniVoiceEngine:
    def test_name(self):
        eng = OmniVoiceEngine()
        assert eng.name() == "OmniVoice"

    def test_engine_id(self):
        eng = OmniVoiceEngine()
        assert eng.engine_id() == "omnivoice"

    def test_is_available(self):
        eng = OmniVoiceEngine()
        result = eng.is_available()
        assert isinstance(result, bool)


class TestFormatHelpers:
    def test_format_rate_normal(self):
        assert _format_rate(1.0) == "+0%"

    def test_format_rate_fast(self):
        result = _format_rate(1.5)
        assert result == "+50%"

    def test_format_rate_slow(self):
        result = _format_rate(0.5)
        assert result == "-50%"

    def test_format_pitch_zero(self):
        assert _format_pitch(0.0) == "+0Hz"

    def test_format_pitch_positive(self):
        assert _format_pitch(10.0) == "+10Hz"

    def test_format_pitch_negative(self):
        assert _format_pitch(-5.0) == "-5Hz"

    def test_format_volume_normal(self):
        assert _format_volume(1.0) == "+0%"

    def test_format_volume_loud(self):
        assert _format_volume(1.5) == "+50%"

    def test_format_volume_quiet(self):
        assert _format_volume(0.5) == "-50%"
