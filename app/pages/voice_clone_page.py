"""Voice clone page — OmniVoice zero-shot voice cloning interface."""

from __future__ import annotations

import uuid
from pathlib import Path

from nicegui import run, ui

from app.config import OUTPUT_DIR
from app.core.audio_utils import preprocess_text, validate_text_length
from app.i18n.translations import t
from app.models.history import HistoryRecord
from app.models.tts_request import TTSRequest
from app.storage import db


def voice_clone_page(engines: dict) -> None:
    """Render the voice clone page."""

    state = {"ref_audio_path": None, "generating": False}

    # Check OmniVoice engine availability on load
    omnivoice_eng = engines.get("omnivoice")
    if omnivoice_eng is None or not omnivoice_eng.is_available():
        ui.markdown(f"⚠️ **{t('omnivoice_unavailable')}**").classes(
            "bg-yellow-900/30 text-yellow-200 p-4 rounded-lg mb-4"
        )

    async def handle_upload(e):
        if e.content is None:
            return
        upload_dir = OUTPUT_DIR / "uploads"
        upload_dir.mkdir(parents=True, exist_ok=True)
        dest = upload_dir / e.name
        dest.write_bytes(e.content.read())
        state["ref_audio_path"] = str(dest)
        ui.notify(f"✅ {t('upload_success')}: {e.name}", type="positive")

    async def clone_generate():
        if state["generating"]:
            return
        ref = state.get("ref_audio_path")
        if not ref:
            ui.notify(t("upload_ref_first"), type="warning")
            return
        raw_text = clone_text.value or ""
        ok, msg = validate_text_length(raw_text)
        if not ok:
            ui.notify(msg, type="warning")
            return

        state["generating"] = True
        clone_btn.disable()
        progress.visible = True

        try:
            processed = preprocess_text(raw_text)
            file_id = uuid.uuid4().hex[:12]
            out_path = str(OUTPUT_DIR / f"clone_{file_id}.wav")

            eng = engines.get("omnivoice")
            if eng is None or not eng.is_available():
                ui.notify(t("omnivoice_unavailable"), type="negative")
                return

            request = TTSRequest(
                text=processed,
                voice="clone",
                language="zh-TW",
                engine="omnivoice",
                speed=1.0,
                pitch=1.0,
                volume=1.0,
                output_format="wav",
                output_path=out_path,
                ref_audio=ref,
            )

            result = await eng.synthesize(request)

            audio_player.set_source(f"/output/{Path(result.audio_path).name}")
            audio_player.visible = True

            record = HistoryRecord(
                text=processed,
                engine="omnivoice",
                voice="clone",
                language="zh-TW",
                speed=1.0,
                pitch=1.0,
                volume=1.0,
                output_format="wav",
                audio_path=result.audio_path,
                duration_seconds=result.duration_seconds,
            )
            await db.add_history_record(record)

            ui.notify(
                f"✅ {t('clone_success')} ({result.duration_seconds:.1f}s)",
                type="positive",
            )

        except Exception as exc:
            ui.notify(f"❌ {t('generate_error')}: {exc}", type="negative")
        finally:
            state["generating"] = False
            clone_btn.enable()
            progress.visible = False

    # ── Layout ──
    ui.label(t("clone_title")).classes("text-2xl font-bold mb-4")
    ui.label(t("clone_description")).classes("text-gray-400 mb-4")

    with ui.card().classes("w-full p-4"):
        ui.label(f"🎤 {t('upload_ref_audio')}").classes("font-semibold mb-2")
        ui.upload(
            label=t("upload_label"),
            on_upload=handle_upload,
            auto_upload=True,
        ).classes("w-full").props('accept="audio/*"')

        ui.separator().classes("my-4")

        clone_text = (
            ui.textarea(
                label=t("clone_target_text"),
                placeholder=t("clone_placeholder"),
            )
            .classes("w-full")
            .props("rows=5")
        )

        with ui.row().classes("mt-4 gap-4"):
            clone_btn = ui.button(
                f"🎙️ {t('clone_btn')}",
                on_click=clone_generate,
            ).classes("bg-purple-600 text-white px-6 py-2")

        progress = ui.linear_progress().classes("mt-2")
        progress.visible = False

        audio_player = ui.audio("").classes("w-full mt-4")
        audio_player.visible = False
