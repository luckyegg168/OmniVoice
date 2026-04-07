"""Audio utility functions."""

from __future__ import annotations

import re


def estimate_speech_duration(text: str, speed: float = 1.0, language: str = "zh-TW") -> float:
    """Estimate speech duration in seconds based on text and language.

    CJK languages: ~4 chars/sec at normal speed.
    Latin languages: ~150 words/min at normal speed.
    """
    if not text.strip():
        return 0.0

    cjk_count = len(re.findall(r"[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]", text))
    latin_words = len(re.findall(r"[a-zA-Z]+", text))

    if cjk_count > latin_words:
        chars_per_sec = 4.0
        duration = cjk_count / chars_per_sec
    else:
        words_per_sec = 2.5
        duration = latin_words / words_per_sec

    duration = max(duration, 1.0)
    return duration / speed


def count_text_stats(text: str) -> dict[str, int]:
    """Count text statistics: chars, words, lines."""
    return {
        "chars": len(text),
        "words": len(text.split()),
        "lines": text.count("\n") + 1 if text else 0,
    }


def preprocess_text(text: str) -> str:
    """Preprocess text: normalize whitespace, expand simple number patterns."""
    text = re.sub(r"\s+", " ", text).strip()
    return text


NON_VERBAL_SYMBOLS = [
    "[laughter]",
    "[sigh]",
    "[confirmation-en]",
    "[question-en]",
    "[question-ah]",
    "[question-oh]",
    "[question-ei]",
    "[question-yi]",
    "[surprise-ah]",
    "[surprise-oh]",
    "[surprise-wa]",
    "[surprise-yo]",
    "[dissatisfaction-hnn]",
]


def validate_text_length(text: str, max_length: int = 10000) -> bool:
    """Validate text is within allowed length."""
    return 0 < len(text) <= max_length
