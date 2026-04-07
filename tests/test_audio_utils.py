"""Tests for audio utilities."""

from __future__ import annotations

from app.core.audio_utils import (
    count_text_stats,
    estimate_speech_duration,
    preprocess_text,
    validate_text_length,
)


class TestCountTextStats:
    def test_empty_string(self):
        result = count_text_stats("")
        assert result["chars"] == 0
        assert result["words"] == 0
        assert result["lines"] == 0

    def test_chinese_text(self):
        result = count_text_stats("你好世界")
        assert result["chars"] == 4
        assert result["words"] >= 1
        assert result["lines"] == 1

    def test_english_text(self):
        result = count_text_stats("hello world test")
        assert result["chars"] == 16
        assert result["words"] == 3
        assert result["lines"] == 1

    def test_multiline(self):
        result = count_text_stats("line one\nline two\nline three")
        assert result["lines"] == 3
        assert result["words"] == 6


class TestEstimateSpeechDuration:
    def test_returns_float(self):
        result = estimate_speech_duration("hello world", 1.0, "en")
        assert isinstance(result, float)

    def test_empty_text(self):
        result = estimate_speech_duration("", 1.0, "en")
        assert result == 0.0

    def test_speed_affects_duration(self):
        normal = estimate_speech_duration("hello world test text", 1.0, "en")
        fast = estimate_speech_duration("hello world test text", 2.0, "en")
        assert fast < normal

    def test_chinese_text(self):
        result = estimate_speech_duration("你好世界歡迎使用", 1.0, "zh-TW")
        assert result > 0


class TestPreprocessText:
    def test_strips_whitespace(self):
        result = preprocess_text("  hello  ")
        assert result == "hello"

    def test_normalizes_newlines(self):
        result = preprocess_text("line1\r\nline2")
        assert "\r" not in result

    def test_preserves_content(self):
        result = preprocess_text("你好世界")
        assert result == "你好世界"


class TestValidateTextLength:
    def test_valid_text(self):
        assert validate_text_length("hello") is True

    def test_empty_text(self):
        assert validate_text_length("") is False

    def test_whitespace_only(self):
        # whitespace has length > 0, so it passes length check
        assert validate_text_length("   ") is True

    def test_over_max(self):
        assert validate_text_length("a" * 10001) is False
