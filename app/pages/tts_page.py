"""Main TTS page — the primary text-to-speech interface."""

from __future__ import annotations

import uuid
from pathlib import Path

from nicegui import run, ui

from app.config import OUTPUT_DIR
from app.core.audio_utils import (
    count_text_stats,
    estimate_speech_duration,
    preprocess_text,
    validate_text_length,
)
from app.i18n.translations import t
from app.models.history import HistoryRecord
from app.models.tts_request import TTSRequest, TTSResult, VoiceInfo
from app.storage import db


async def _do_synthesize(engine, request: TTSRequest) -> TTSResult:
    """Run synthesis in a thread-safe manner."""
    return await engine.synthesize(request)


def tts_page(engines: dict) -> None:
    """Render the main TTS page content inside the current page context."""

    # ── State ──
    state = {
        "current_engine_id": "edge-tts",
        "voices": [],
        "generating": False,
        "last_result": None,
    }

    # ── Helpers ──
    async def load_voices(engine_id: str) -> list[VoiceInfo]:
        eng = engines.get(engine_id)
        if eng is None:
            return []
        try:
            return await eng.list_voices()
        except Exception:
            return []

    async def refresh_voices():
        voices = await load_voices(state["current_engine_id"])
        state["voices"] = voices
        options = {v.id: f"{v.name} ({v.language})" for v in voices}
        voice_select.options = options
        if voices:
            voice_select.value = voices[0].id
        voice_select.update()

    def update_stats():
        txt = text_area.value or ""
        s = count_text_stats(txt)
        est = estimate_speech_duration(txt, speed_slider.value, "zh-TW")
        stats_label.text = (
            f"📝 {t('char_count')}: {s['chars']}  "
            f"📖 {t('word_count')}: {s['words']}  "
            f"⏱️ {t('est_duration')}: {est:.1f}s"
        )

    async def generate():
        if state["generating"]:
            return
        raw_text = text_area.value or ""
        ok, msg = validate_text_length(raw_text)
        if not ok:
            ui.notify(msg, type="warning")
            return

        state["generating"] = True
        gen_btn.disable()
        progress.visible = True

        try:
            processed = preprocess_text(raw_text)
            file_id = uuid.uuid4().hex[:12]
            ext = "wav" if state["current_engine_id"] == "omnivoice" else "mp3"
            out_path = str(OUTPUT_DIR / f"{file_id}.{ext}")

            request = TTSRequest(
                text=processed,
                voice=voice_select.value or "",
                language="zh-TW",
                engine=state["current_engine_id"],
                speed=speed_slider.value,
                pitch=pitch_slider.value,
                volume=volume_slider.value,
                output_format=ext,
                output_path=out_path,
            )

            eng = engines.get(state["current_engine_id"])
            if eng is None:
                ui.notify(t("engine_unavailable"), type="negative")
                return

            result: TTSResult = await _do_synthesize(eng, request)

            state["last_result"] = result
            audio_player.set_source(f"/output/{Path(result.audio_path).name}")
            audio_player.visible = True
            download_btn.visible = True

            # Save to history
            record = HistoryRecord(
                text=processed,
                engine=state["current_engine_id"],
                voice=voice_select.value or "",
                language="zh-TW",
                speed=speed_slider.value,
                pitch=pitch_slider.value,
                volume=volume_slider.value,
                output_format=ext,
                audio_path=result.audio_path,
                duration_seconds=result.duration_seconds,
            )
            await run.io_bound(db.add_history_record, record)

            ui.notify(
                f"✅ {t('generate_success')} ({result.duration_seconds:.1f}s)",
                type="positive",
            )

        except Exception as exc:
            ui.notify(f"❌ {t('generate_error')}: {exc}", type="negative")
        finally:
            state["generating"] = False
            gen_btn.enable()
            progress.visible = False

    def on_download():
        result = state.get("last_result")
        if result and Path(result.audio_path).exists():
            ui.download(result.audio_path)

    # ── Layout ──
    ui.label(t("tts_title")).classes("text-2xl font-bold mb-4")

    with ui.row().classes("w-full gap-4 items-end"):
        ui.select(
            options={eid: eng.name() for eid, eng in engines.items()},
            value=state["current_engine_id"],
            label=t("engine_label"),
            on_change=lambda e: _on_engine_change(e.value),
        ).classes("w-48")

        voice_select = ui.select(
            options={},
            label=t("voice_label"),
        ).classes("w-64")

    text_area = ui.textarea(
        label=t("input_text"),
        placeholder=t("input_placeholder"),
        on_change=lambda _: update_stats(),
    ).classes("w-full mt-4").props("rows=8")

    stats_label = ui.label("").classes("text-sm text-gray-400 mt-1")

    with ui.row().classes("w-full gap-6 mt-4"):
        with ui.column().classes("flex-1"):
            ui.label(f"🔊 {t('speed_label')}")
            speed_slider = ui.slider(min=0.5, max=2.0, step=0.1, value=1.0).classes("w-full")
        with ui.column().classes("flex-1"):
            ui.label(f"🎵 {t('pitch_label')}")
            pitch_slider = ui.slider(min=0.5, max=2.0, step=0.1, value=1.0).classes("w-full")
        with ui.column().classes("flex-1"):
            ui.label(f"📢 {t('volume_label')}")
            volume_slider = ui.slider(min=0.1, max=1.0, step=0.1, value=1.0).classes("w-full")

    with ui.row().classes("mt-4 gap-4"):
        gen_btn = ui.button(
            f"🎙️ {t('generate_btn')}",
            on_click=generate,
        ).classes("bg-blue-600 text-white px-6 py-2")

        download_btn = ui.button(
            f"💾 {t('download_btn')}",
            on_click=on_download,
        ).classes("bg-green-600 text-white px-4 py-2")
        download_btn.visible = False

    progress = ui.linear_progress().classes("mt-2")
    progress.visible = False

    audio_player = ui.audio("").classes("w-full mt-4")
    audio_player.visible = False

    # ── Engine change handler ──
    async def _on_engine_change(engine_id: str):
        state["current_engine_id"] = engine_id
        await refresh_voices()

    # ── Initial load ──
    async def _init():
        await refresh_voices()
        update_stats()

    ui.timer(0.1, _init, once=True)
