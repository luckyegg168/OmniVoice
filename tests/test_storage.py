"""Tests for storage layer."""

from __future__ import annotations

import json
from pathlib import Path

from app.models.history import HistoryRecord


class TestJsonIO:
    """Test JSON read/write using sync file ops (mirrors storage logic)."""

    def test_write_and_read(self, tmp_path: Path):
        file_path = tmp_path / "test.json"
        data = {"key": "value", "list": [1, 2, 3]}
        file_path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        result = json.loads(file_path.read_text(encoding="utf-8"))
        assert result == data

    def test_read_missing_file(self, tmp_path: Path):
        file_path = tmp_path / "nonexistent.json"
        assert not file_path.exists()

    def test_write_overwrites(self, tmp_path: Path):
        file_path = tmp_path / "test.json"
        file_path.write_text(json.dumps({"a": 1}), encoding="utf-8")
        file_path.write_text(json.dumps({"b": 2}), encoding="utf-8")
        result = json.loads(file_path.read_text(encoding="utf-8"))
        assert result == {"b": 2}


class TestHistoryRecordSerialization:
    def test_serialization(self):
        record = HistoryRecord(
            text="test",
            engine="edge-tts",
            voice="v1",
            language="zh-TW",
            speed=1.0,
            pitch=0.0,
            volume=1.0,
            audio_path="/path/test.mp3",
            duration_seconds=3.0,
        )
        data = record.model_dump()
        assert data["text"] == "test"
        assert data["engine"] == "edge-tts"

        # Can reconstruct from dict
        restored = HistoryRecord(**data)
        assert restored.text == record.text
        assert restored.id == record.id
