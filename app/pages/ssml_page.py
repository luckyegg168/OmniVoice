"""SSML editor page — advanced Speech Synthesis Markup Language editing."""

from __future__ import annotations

import uuid
from pathlib import Path

from nicegui import run, ui

from app.config import OUTPUT_DIR
from app.i18n.translations import t
from app.models.history import HistoryRecord
from app.models.tts_request import TTSRequest
from app.storage import db

SSML_TEMPLATES = {
    "basic": (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"'
        ' xml:lang="zh-TW">\n'
        "  <voice name=\"zh-TW-HsiaoChenNeural\">\n"
        "    你好，歡迎使用語音合成。\n"
        "  </voice>\n"
        "</speak>"
    ),
    "pause": (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"'
        ' xml:lang="zh-TW">\n'
        "  第一段文字。\n"
        '  <break time="500ms"/>\n'
        "  第二段文字。\n"
        "</speak>"
    ),
    "emphasis": (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"'
        ' xml:lang="zh-TW">\n'
        '  這是<emphasis level="strong">重點</emphasis>內容。\n'
        "</speak>"
    ),
    "prosody": (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"'
        ' xml:lang="zh-TW">\n'
        '  <prosody rate="slow" pitch="high">\n'
        "    慢速高音的語音。\n"
        "  </prosody>\n"
        "</speak>"
    ),
}


def ssml_page(engines: dict) -> None:
    """Render the SSML editor page."""

    state = {"generating": False}

    def insert_template(name: str):
        template = SSML_TEMPLATES.get(name, "")
        if template:
            ssml_editor.value = template

    async def synthesize_ssml():
        if state["generating"]:
            return
        ssml_text = ssml_editor.value or ""
        if not ssml_text.strip():
            ui.notify(t("ssml_empty"), type="warning")
            return

        state["generating"] = True
        ssml_btn.disable()
        progress.visible = True

        try:
            eng = engines.get("edge-tts")
            if eng is None:
                ui.notify(t("engine_unavailable"), type="negative")
                return

            file_id = uuid.uuid4().hex[:12]
            out_path = str(OUTPUT_DIR / f"ssml_{file_id}.mp3")

            request = TTSRequest(
                text=ssml_text,
                voice="zh-TW-HsiaoChenNeural",
                language="zh-TW",
                engine="edge-tts",
                speed=1.0,
                pitch=1.0,
                volume=1.0,
                output_format="mp3",
                output_path=out_path,
                ssml=True,
            )

            result = await eng.synthesize(request)

            audio_player.set_source(f"/output/{Path(result.audio_path).name}")
            audio_player.visible = True

            record = HistoryRecord(
                text=ssml_text[:200],
                engine="edge-tts",
                voice="ssml",
                language="zh-TW",
                speed=1.0,
                pitch=1.0,
                volume=1.0,
                output_format="mp3",
                audio_path=result.audio_path,
                duration_seconds=result.duration_seconds,
            )
            await db.add_history_record(record)

            ui.notify(f"✅ {t('generate_success')}", type="positive")

        except Exception as exc:
            ui.notify(f"❌ {t('generate_error')}: {exc}", type="negative")
        finally:
            state["generating"] = False
            ssml_btn.enable()
            progress.visible = False

    # ── Layout ──
    ui.label(t("ssml_title")).classes("text-2xl font-bold mb-4")
    ui.label(t("ssml_description")).classes("text-gray-400 mb-4")

    with ui.row().classes("gap-2 mb-4"):
        ui.label(f"📝 {t('ssml_templates')}:").classes("self-center")
        for name in SSML_TEMPLATES:
            ui.button(
                name.capitalize(),
                on_click=lambda _, n=name: insert_template(n),
            ).props("flat dense")

    ssml_editor = ui.textarea(
        label=t("ssml_editor_label"),
        value=SSML_TEMPLATES["basic"],
    ).classes("w-full font-mono").props("rows=12")

    with ui.row().classes("mt-4"):
        ssml_btn = ui.button(
            f"🎙️ {t('ssml_generate')}",
            on_click=synthesize_ssml,
        ).classes("bg-blue-600 text-white px-6 py-2")

    progress = ui.linear_progress().classes("mt-2")
    progress.visible = False

    audio_player = ui.audio("").classes("w-full mt-4")
    audio_player.visible = False
